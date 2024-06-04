import logging
import re
from typing import List, Union

from aiohttp.web_exceptions import HTTPBadRequest

from beacon.backends.molgenis.mappers.filters import get_filter_spec
from beacon.backends.molgenis.rsql.parameters import Parameter
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9.-_]*$'  # N.B. The dot (.) is allowed in the right part (code)


def _match_ids_to_ontologies(id_: Union[str, list]):
    if tid_ is str:
        return re.match(CURIE_REGEX, id_)
    else:
        return all(re.match(CURIE_REGEX, i) for i in id_)


def apply_filters(filters: List[dict], scope='catalogs'):
    rsql_params = []
    unsupported_filters = []
    for f in filters:
        LOG.debug('Processing filter %s', f['id'])
        if 'value' in f:
            f = AlphanumericFilter(**f)
            LOG.debug('Alphanumeric filter: %s %s %s', f.id, f.operator, f.value)
            param = apply_alphanumeric_filter(f)
            if param is not None:
                rsql_params.append(param)
            else:
                unsupported_filters.append(f.id)
        elif 'similarity' in f or 'includeDescendantTerms' in f or _match_ids_to_ontologies(f['id']):
            f = OntologyFilter(**f)
            LOG.debug("Ontology filter: %s", f.id)
            param, unsupported_terms = apply_ontology_filter(f)
            if param is not None:
                rsql_params.append(param)
            unsupported_filters.extend(unsupported_terms)
        else:
            f = CustomFilter(**f)
            LOG.debug("Custom filter: %s", f.id)
            param, unsupported_terms = apply_custom_filter(f)
            if param is not None:
                rsql_params.append(param)
            else:
                unsupported_filters.append(f.id)

    return rsql_params, unsupported_filters


def apply_ontology_filter(_filter: OntologyFilter):
    ontology_terms = [_filter.id] if type(_filter.id) == str else _filter.id
    unsupported_terms = []
    mapped_value = []
    attribute = None
    operator = None

    for i, ot in enumerate(ontology_terms):
        filter_spec = get_filter_spec(ot)
        if filter_spec == 'ejprd:Biobank':  # skip it but without marking it as unsupported
            continue
        if filter_spec is None:
            unsupported_terms.append(ot)
            continue
        elif filter_spec['attribute'] != attribute:
            # we accept a list of values regarding the same attribute.
            # It means that two values of different ontologies for the same type are ok (e.g., ordo and icd)
            if i == 0:
                attribute = filter_spec['attribute']
                operator = filter_spec['operator']
            else:
                raise HTTPBadRequest(text='Cannot perform an or request with parameters of different type')

        mapped_value.append(filter_spec['mapper'](ot))
    if len(mapped_value) == 0:
        return None, unsupported_terms
    else:
        return Parameter(attribute, operator, mapped_value), unsupported_terms


def apply_alphanumeric_filter(_filter: AlphanumericFilter):
    filter_spec = get_filter_spec(_filter.id)
    if filter_spec is None:
        return None

    if _filter.value is str:
        filter_value = [_filter.value]
    else:
        filter_value = _filter.value
    mapped_values = list(map(filter_spec['mapper'], filter_value))
    return Parameter(filter_spec['attribute'], filter_spec['operator'], mapped_values)


def apply_custom_filter(_filter: CustomFilter):
    custom_terms = [_filter.id] if _filter.id is str else _filter.id
    unsupported_terms = []
    mapped_value = []
    attribute = None
    operator = None

    for i, ct in enumerate(custom_terms):
        if ct.startswith('Orphanet_'):
            filter_spec = get_filter_spec('Orphanet_')
        else:
            filter_spec = None

        if filter_spec is None:
            unsupported_terms.append(ct)
            continue
        elif filter_spec['attribute'] != attribute:
            # we accept a list of values regarding the same attribute.
            # It means that two values of different ontologies for the same type are ok (e.g., ordo and icd)
            if i == 0:
                attribute = filter_spec['attribute']
                operator = filter_spec['operator']
            else:
                raise HTTPBadRequest(text='Cannot perform an or request with parameters of different type')

        mapped_value.append(filter_spec['mapper'](ct))
    if len(mapped_value) == 0:
        return None, unsupported_terms
    else:
        return Parameter(attribute, operator, mapped_value), unsupported_terms


def map_filter_values(_filter):
    return list(map(_filter['mapper'], _filter.id))
