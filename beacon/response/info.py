"""
Info Endpoint.

Querying the info endpoint reveals information about this beacon and its existing datasets 
and their associated metadata.

* ``/`` Beacon-v1
* ``/info`` Beacon-v1
* ``/info?model=GA4GH-ServiceInfo-v0.1`` GA4GH
* ``/service-info`` GA4GH

"""

import logging

from aiohttp import web
from aiohttp.web_request import Request

from beacon.request import RequestParams
from beacon.response.build_response import build_beacon_info_response

LOG = logging.getLogger(__name__)


async def handler(request: Request):
    qparams = RequestParams().from_request(request)

    response_converted = build_beacon_info_response(qparams)
    return web.json_response(response_converted)
