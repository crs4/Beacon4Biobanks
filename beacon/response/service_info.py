import logging

from aiohttp import web
from aiohttp.web_request import Request

from beacon.response.build_response import build_beacon_service_info_response

LOG = logging.getLogger(__name__)


async def handler(request: Request):
    LOG.info('Running a GET service info request')
    response_converted = build_beacon_service_info_response()
    return web.json_response(response_converted)
