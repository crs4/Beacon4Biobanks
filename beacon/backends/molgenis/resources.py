import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from molgenis.errors import MolgenisRequestError

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
    try:
        query_arguments, unsupported_filters = apply_filters(qparams.query.filters)
        if len(query_arguments) == 0:
            raise HTTPBadRequest(
                text="No valid query params provided. At least one supported and valid parameter should be provided")
        rsql_query = create_rsql_query(query_arguments)
        schema = get_schema_from_query_params("resource", qparams)

        result = get_resources_results(rsql_query, qparams.query.pagination.skip, qparams.query.pagination.limit)
        resources = list(map(map_resource(schema["schema"]), result["items"]))

        return schema, result['total'], resources, unsupported_filters
    except (MolgenisRequestError, ConnectionError) as e:
        LOG.error("Error contacting molgenis")
        LOG.error(e)
        raise web.HTTPInternalServerError(reason="Connection to data source failed")
