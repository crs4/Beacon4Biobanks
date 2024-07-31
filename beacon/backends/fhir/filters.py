import logging
import re
from typing import List, Union

from aiohttp.web_exceptions import HTTPBadRequest

from beacon.backends.fhir.cql.parameters import get_cql_parameter_factory
from beacon.backends.fhir.mappings import get_cql_condition_arguments_from_beacon_filter
from beacon.backends.fhir.mappings import get_unsupported_filters
from beacon.backends.fhir.utils import validate_disease_filter
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9.-_]*$'  # N.B. The dot (.) is allowed in the right part (code)


def _match_ids_to_ontologies(id_: Union[str, list]):
    if isinstance(id_, str):
        return re.match(CURIE_REGEX, id_)
    else:
        return all(re.match(CURIE_REGEX, i) for i in id_)


def apply_filters(filters: List[dict], scope='biosamples'):
    query_conditions = list()
    unsupported_filters = []
    for f in filters:
        if not validate_disease_filter(f['id']):
            raise HTTPBadRequest(
                text="Invalid query: different ontology specs combined in the same array for Disease filter parameter")
        if f['id'] in get_unsupported_filters() and f['id'] not in get_unsupported_filters():  # skip filter
            unsupported_filters.append(f['id'])
            continue
        if "value" in f:
            f = AlphanumericFilter(**f)
            LOG.debug("Alphanumeric filter: %s %s %s", f.id, f.operator, f.value)
            condition = apply_alphanumeric_filter(f, unsupported_filters, scope)
            if condition is not None:
                query_conditions.append(condition)
        elif "similarity" in f or "includeDescendantTerms" in f or _match_ids_to_ontologies(f["id"]):
            f = OntologyFilter(**f)
            LOG.debug("Ontology filter: %s", f.id)
            condition = apply_ontology_filter(f, unsupported_filters, scope)
            if condition is not None:
                query_conditions.append(condition)
        else:
            f = CustomFilter(**f)
            LOG.debug("Custom filter: %s", f.id)
            condition = apply_custom_filter(f, unsupported_filters, scope)
            if condition is not None:
                query_conditions.append(apply_custom_filter(f, unsupported_filters, scope))
    return query_conditions, unsupported_filters


def apply_ontology_filter(filter_: OntologyFilter, unsupported_filters: List, scope='biosamples'):
    if isinstance(filter_.id, str):
        ontology_terms = [filter_.id]
    else:
        ontology_terms = filter_.id
    parameter = None
    for ot in ontology_terms:
        try:
            curie_prefix, curie_reference = ot.split(':')
            # exception: in case of diagnosis code, the correspondent cql param class is assigned by hand
            if curie_prefix in ('icd10', 'ordo'):
                parameter_args = get_cql_condition_arguments_from_beacon_filter(curie_prefix, unsupported_filters)
                parameter_type, extension = parameter_args['cql_parameter_class'], parameter_args['extension']
                code_system, code = curie_prefix, curie_reference
            else:
                # for all the others ontology parameters, we might support different ontologies for the query
                parameter_args = get_cql_condition_arguments_from_beacon_filter(ot, unsupported_filters)
                parameter_type, code_system, code, extension = parameter_args['cql_parameter_class'], \
                    parameter_args['fhir_codesystem'], parameter_args['value'], parameter_args['extension']

            if parameter is None:
                parameter = create_parameter(parameter_type, scope)
            parameter.add_condition_parameters(code=code, code_system=code_system, extension=extension)
        except KeyError:
            logging.error(f'Filter with ontology term {ot} is not supported')
    return parameter


def apply_alphanumeric_filter(filter_: AlphanumericFilter, unsupported_filters: List,
                              scope='biosamples'):
    if type(filter_.value) in (str, int):
        values = [filter_.value]
    else:
        values = filter_.value

    try:
        parameter_args = get_cql_condition_arguments_from_beacon_filter(filter_.id, unsupported_filters)
        parameter_type = parameter_args['cql_parameter_class']
        parameter = create_parameter(parameter_type, scope)
        for v in values:
            try:
                parameter_value = parameter_args['values_mapper'](v)
            except KeyError:
                raise HTTPBadRequest(
                    text=f'Invalid query: value {v} not allowed for filter {filter_.id}')

            if isinstance(parameter_value, list):
                for pv in parameter_value:
                    parameter.add_condition_parameters(operator=filter_.operator, value=pv)
            else:
                parameter.add_condition_parameters(operator=filter_.operator, value=parameter_value)
        return parameter
    except KeyError:
        logging.error(f'Filter {values} is not supported')


def apply_custom_filter(filter_: CustomFilter, unsupported_filters: List, scope='biosamples'):
    if type(filter_.id) in (str, int):
        custom_terms = [filter_.id]
    else:
        custom_terms = filter_.id
    parameter = None
    for ct in custom_terms:
        if ct.startswith('Orphanet_'):
            filter_spec = 'Orphanet_'
        else:
            filter_spec = ct

        try:
            parameter_args = get_cql_condition_arguments_from_beacon_filter(filter_spec, unsupported_filters)
            parameter_type = parameter_args['cql_parameter_class']
            if parameter is None:
                parameter = create_parameter(parameter_type, scope)
            parameter.add_condition_parameters(code=ct, code_system=parameter_args.get('fhir_codesystem'))
        except KeyError:
            logging.error(f'Filter {ct} is not supported')
    return parameter


def create_parameter(parameter_type: str, scope='biosamples'):
    factory = get_cql_parameter_factory(parameter_type, scope)
    parameter = factory()
    return parameter
