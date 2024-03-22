import logging

from beacon.backends.molgenis.filters import apply_filters
from beacon.backends.molgenis.mappers.records import map_resource
from beacon.backends.molgenis.rsql.builder import create_rsql_query
from beacon.backends.molgenis.utils import get_resources_results
from beacon.schemas import get_schema_from_query_params

LOG = logging.getLogger(__name__)


def get_resources(entry_id, qparams, granularity=None):
    """
    Queries for Catalogs (Collections) in the BBMRI Directory (Molgenis)
    """
    query_arguments, unsupported_filters = apply_filters(qparams.query.filters)
    rsql_query = create_rsql_query(query_arguments)
    schema = get_schema_from_query_params("resource", qparams)
    result = get_resources_results(rsql_query, qparams.query.pagination.skip, qparams.query.pagination.limit)
    resources = list(map(map_resource(schema["schema"]), result["items"]))

    return schema, result['total'], resources, unsupported_filters
