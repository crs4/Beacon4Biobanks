import logging
import re
from typing import List, Union

from beacon.backends.fhir.cql.parameters import get_cql_parameter_factory
from beacon.backends.fhir.mappings import get_cql_condition_arguments_from_beacon_filter
from beacon.backends.fhir.mappings import get_unsupported_filters
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9.-_]*$'  # N.B. The dot (.) is allowed in the right part (code)


def _match_ids_to_ontologies(id_: Union[str, list]):
    if type(id_) == str:
        return re.match(CURIE_REGEX, id_)
    else:
        return all(re.match(CURIE_REGEX, i) for i in id_)


def apply_filters(filters: List[dict], scope='biosamples'):
    query_conditions = {}
    unsupported_filters = []
    for f in filters:
        if f['id'] in get_unsupported_filters():  # skip filter
            unsupported_filters.append(f['id'])
            continue
        if "value" in f:
            f = AlphanumericFilter(**f)
            LOG.debug("Alphanumeric filter: %s %s %s", f.id, f.operator, f.value)
            apply_alphanumeric_filter(query_conditions, f, scope)
        elif "similarity" in f or "includeDescendantTerms" in f or _match_ids_to_ontologies(f["id"]):
            f = OntologyFilter(**f)
            LOG.debug("Ontology filter: %s", f.id)
            apply_ontology_filter(query_conditions, f, scope)
        else:
            f = CustomFilter(**f)
            LOG.debug("Custom filter: %s", f.id)
            apply_custom_filter(query_conditions, f, scope)
    return query_conditions.values(), unsupported_filters


def apply_ontology_filter(parameters: dict, filter_: OntologyFilter, scope='biosamples'):
    if type(filter_.id) == str:
        ontology_terms = [filter_.id]
    else:
        ontology_terms = filter_.id
    for ot in ontology_terms:
        curie_prefix, curie_reference = ot.split(':')
        # exception: in case of diagnosis code, the correspondent cql param class is assigned by hand
        if curie_prefix in ('icd10', 'ordo'):
            parameter_args = get_cql_condition_arguments_from_beacon_filter(curie_prefix)
            parameter_type, extension = parameter_args['cql_parameter_class'], parameter_args['extension']
            code_system, code = curie_prefix, curie_reference
        else:
            # for all the others ontology parameters, we might support different ontologies for the query
            parameter_args = get_cql_condition_arguments_from_beacon_filter(ot)
            parameter_type, code_system, code, extension = parameter_args['cql_parameter_class'], \
                parameter_args['fhir_codesystem'], parameter_args['value'], parameter_args['extension']

        parameter = _get_or_create_parameter(parameters, parameter_type, scope)
        parameter.add_condition_parameters(code=code, code_system=code_system, extension=extension)


def apply_alphanumeric_filter(parameters: dict, filter_: AlphanumericFilter, scope='biosamples'):
    if type(filter_.value) in (str, int):
        values = [filter_.value]
    else:
        values = filter_.value

    parameter_args = get_cql_condition_arguments_from_beacon_filter(filter_.id)
    parameter_type = parameter_args['cql_parameter_class']
    parameter = _get_or_create_parameter(parameters, parameter_type, scope)
    for v in values:
        try:
            parameter_value = parameter_args['values_mapper'](v)
        except KeyError:
            parameter_value = ''

        if type(parameter_value) == list:
            for pv in parameter_value:
                parameter.add_condition_parameters(operator=filter_.operator, value=pv)
        else:
            parameter.add_condition_parameters(operator=filter_.operator, value=parameter_value)


def apply_custom_filter(parameters: dict, filter: CustomFilter, scope='biosamples'):
    parameter_args = get_cql_condition_arguments_from_beacon_filter(filter.id)
    parameter_type = parameter_args['cql_parameter_class']

    parameter = _get_or_create_parameter(parameters, parameter_type, scope)
    parameter.add_condition_parameters(code=parameter_args['id'], code_system=parameter_args['fhir_codesystem'])


def _get_or_create_parameter(parameters: dict, parameter_type: str, scope='biosamples'):
    factory = get_cql_parameter_factory(parameter_type, scope)
    try:
        parameter = parameters[parameter_type]
    except KeyError:
        parameter = factory()
        parameters[parameter_type] = parameter

    return parameter
