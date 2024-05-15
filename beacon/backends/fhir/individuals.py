import logging
from typing import Optional

from beacon.backends.fhir.cql.builder import create_cql
from beacon.backends.fhir.filters import apply_filters
from beacon.backends.fhir.mappers.records import map_individuals
from beacon.backends.fhir.utils import get_individuals_results, get_filtering_terms_results
from beacon.exceptions import OperationNotSupported
from beacon.request.model import RequestParams, Granularity
from beacon.schemas import get_schema_from_query_params

LOG = logging.getLogger(__name__)


def get_individuals(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    filters = apply_filters(qparams.query.filters, 'individuals')
    query_arguments = filters[0]
    unsupported_filters = filters[1]
    cql_query = create_cql(query_arguments, 'individuals', entry_id)
    count, resources = get_individuals_results(cql_query, granularity)
    if granularity == Granularity.COUNT or count == 0:  # no need to perform the mapping in this case
        return get_schema_from_query_params("individual", qparams), count, [], unsupported_filters
    else:
        individuals = list(map(map_individuals, resources))
        return get_schema_from_query_params("individual", qparams), count, individuals, unsupported_filters


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    terms = get_filtering_terms_results('individuals')
    return get_schema_from_query_params("individual", qparams), len(terms), terms


def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()
