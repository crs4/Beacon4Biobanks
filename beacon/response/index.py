from aiohttp import web
from aiohttp.web_request import Request


async def handler(request: Request):
    location = request.app.router['info'].url_for()
    raise web.HTTPFound(location=location)
