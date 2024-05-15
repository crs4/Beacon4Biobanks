import logging

from aiohttp import web
from aiohttp.web_request import Request

from beacon import conf
from beacon.backends.molgenis.mappers.filters import FILTER_SPEC
from beacon.request.model import RequestParams, Granularity
from beacon.response.build_response import (
    build_filtering_terms_response, build_beacon_boolean_response, build_beacon_count_response,
    build_beacon_collection_response,
)

LOG = logging.getLogger(__name__)


def filtering_terms_handler(fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        entry_id = request.match_info.get('id', None)

        # Get response
        entity_schema, count, records = fn(entry_id, qparams)
        filtering_terms_data = {
            'resources': FILTER_SPEC['resources'],
            'filteringTerms': (
                [r for r in records] if records else []
            )

        }
        response = build_filtering_terms_response(filtering_terms_data, count, qparams, lambda x, y: x, entity_schema)
        return web.json_response(response)

    return wrapper


def collection_handler(fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None
        # Get response
        entity_schema, count, records = fn(entry_id, qparams)
        response_converted = (
            [r for r in records] if records else []
        )
        response = build_beacon_collection_response(
            response_converted, count, qparams, lambda x, y: x, entity_schema
        )
        return web.json_response(response)
        # return await json_stream(request, response)

    return wrapper


def generic_handler(fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)

        if conf.service.max_beacon_granularity == Granularity.BOOLEAN:
            granularity = Granularity.BOOLEAN
        elif conf.service.max_beacon_granularity == Granularity.COUNT:
            if qparams.query.requested_granularity == Granularity.RECORD:
                granularity = Granularity.COUNT
            else:  # In case granularity is COUNT or BOOLEAN it returns the one required
                granularity = qparams.query.requested_granularity
        else:
            # force granularity to count
            granularity = Granularity.COUNT

        entry_id = request.headers.get('X-Resource-ID', None)
        entity_schema, count, records, unsupported_filters = fn(entry_id, qparams, granularity)
        LOG.debug(entity_schema)
        if granularity == Granularity.BOOLEAN:
            response = build_beacon_boolean_response(records, count, qparams, lambda x, y: x, entity_schema)
        elif granularity == Granularity.COUNT:
            response = build_beacon_count_response(records, count, qparams, lambda x, y: x, entity_schema,
                                                   unsupported_filters)
        else:
            response = build_beacon_count_response(records, count, qparams, lambda x, y: x, entity_schema,
                                                   unsupported_filters)
        return web.json_response(response)

    return wrapper
