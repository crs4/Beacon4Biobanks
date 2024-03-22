"""
Filtering terms Endpoint.

Querying the filtering terms endpoint reveals information about existing ontology filters in this beacon.
These are stored in the DB inside the table named 'ontology_terms'.

"""
from aiohttp import web

from beacon import conf
from beacon.backends.fhir.filtering_terms import get_filtering_terms
from beacon.request import RequestParams


async def handler(request, qparams: RequestParams, entity_schema):
    _, _, docs = get_filtering_terms(entry_id=None, qparams=qparams)

    response = {
        'meta': conf.beacon.beacon_id,
        'apiVersion': conf.beacon.api_version,
        'filteringTerms': conf.beacon.ontology_terms,
    }
    return web.json_response(response)
