import logging
from typing import Optional

from beacon.backends.fhir.cql.builder import create_cql
from beacon.backends.fhir.filters import apply_filters
from beacon.backends.fhir.mappers.records import map_biosamples
from beacon.backends.fhir.utils import get_biosample_results, get_filtering_terms_results
from beacon.request import RequestParams
from beacon.request.model import Granularity
from beacon.schemas import get_schema_from_query_params

LOG = logging.getLogger(__name__)


def get_biosamples(entry_id: str, qparams, granularity=Granularity.COUNT):
    """
    Queries for biosamples in FHIR store
    """
    filters = apply_filters(qparams.query.filters, 'biosamples')
    query_arguments = filters[0]
    unsupported_filters = filters[1]
    cql_query = create_cql(query_arguments, 'biosamples', entry_id)
    count, resources = get_biosample_results(cql_query, granularity)
    if granularity == Granularity.COUNT or count == 0:
        return get_schema_from_query_params("biosample", qparams), count, [], unsupported_filters
    else:
        biosamples = list(map(map_biosamples, resources))
        return get_schema_from_query_params("biosample", qparams), count, biosamples, unsupported_filters


def get_biosample_with_id(entry_id: str, qparams, granularity=Granularity.COUNT):
    query_arguments = apply_filters(qparams.query.filters, 'biosamples')[0]
    cql_query = create_cql(query_arguments, 'biosamples')
    cql_query['id'] = entry_id
    resources = get_biosample_results(cql_query, qparams.query.requested_granularity)
    biosamples = list(map(map_biosamples, resources))
    return get_schema_from_query_params("biosample", qparams), len(biosamples), biosamples


def get_filtering_terms_of_biosample(entry_id: str, qparams, granularity=Granularity.COUNT):
    terms = get_filtering_terms_results('biosamples')
    return get_schema_from_query_params("biosample", qparams), len(terms), terms


def get_variants_of_biosample(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    pass


def get_analyses_of_biosample(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    pass


def get_runs_of_biosample(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    pass
