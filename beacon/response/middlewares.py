import jwt
import logging
import re
# import aiohttp_csrf
from aiohttp import web, hdrs
from aiohttp.web_response import json_response
from aiohttp_jwt.utils import invoke, check_request
from functools import partial
from typing import Tuple

from beacon import conf

LOG = logging.getLogger(__name__)

CSRF_FIELD_NAME = 'csrf_token'
SESSION_STORAGE = 'beacon_session'


def handle_error(request, exc):
    # exc is a web.HTTPException
    raise exc  # We don't handle it


async def build_error_response(ex):
    return json_response(status=ex.status_code, data={
        'errorCode': ex.status_code,
        'errorMessage': ex.text
    })


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:  # Just the 400's and 500's
        # if the request comes from /api/*, we output the json version
        print('Error on page %s: %s', request.path, ex)
        LOG.error('Error on page %s: %s', request.path, ex)
        return await build_error_response(ex)


# Add authorization token middleware
def token_auth_middleware(  # user_loader: Callable,
        request_property: str = 'user',
        expected_token=conf.service.auth_key,
        exclude_routes: Tuple = tuple(),
        exclude_methods: Tuple = tuple()):
    """
    Checks a auth token and adds a user from user_loader in request.
    """

    @web.middleware
    async def middleware(request, handler):
        if conf.service.auth_key is not None:
            try:
                token = request.headers['auth-key']
            except KeyError:
                raise web.HTTPUnauthorized(reason='Missing authorization header')
            except ValueError:
                raise web.HTTPForbidden(reason='Invalid authorization header')
            else:
                if expected_token != token:
                    raise web.HTTPForbidden(reason='Invalid token value')
        return await handler(request)

    return middleware


def JWTMiddleware(
        jwks_client,
        request_property='payload',
        credentials_required=True,
        whitelist=tuple(),
        token_getter=None,
        is_revoked=None,
        store_token=False,
        algorithms=None,
        auth_scheme='Bearer',
        audience=None,
        issuer=None
):
    """
    Reimplementation of aiohttp JWTMiddleware that uses JWKS to get the info from the issuer
    """
    if not jwks_client:
        raise RuntimeError(
            'JWKS URL must be provided',
        )

    if not isinstance(request_property, str):
        raise TypeError('request_property should be a str')

    global _request_property

    _request_property = request_property

    @web.middleware
    async def middleware(request, handler):
        if request.method == hdrs.METH_OPTIONS:
            return await handler(request)

        if check_request(request, whitelist):
            return await handler(request)

        token = None

        if callable(token_getter):
            token = await invoke(partial(token_getter, request))
        elif 'Authorization' in request.headers:
            try:
                scheme, token = request.headers.get(
                    'Authorization'
                ).strip().split(' ')
            except ValueError:
                raise web.HTTPForbidden(
                    reason='Invalid authorization header',
                )

            if not re.match(auth_scheme, scheme):
                if credentials_required:
                    raise web.HTTPForbidden(
                        reason='Invalid token scheme',
                    )
                return await handler(request)

        if not token and credentials_required:
            raise web.HTTPUnauthorized(
                reason='Missing authorization token',
            )

        if token is not None:
            try:
                signing_key = jwks_client.get_signing_key_from_jwt(token)
            except jwt.exceptions.PyJWKClientError:
                raise web.HTTPUnauthorized(reason="Invalid token")

            try:
                decoded = jwt.decode(
                    token,
                    key=signing_key.key,
                    algorithms=algorithms,
                    audience=audience,
                    issuer=issuer
                )
            except jwt.InvalidTokenError as exc:
                msg = f'Invalid authorization token, {exc}'
                raise web.HTTPUnauthorized(reason=msg)

            if callable(is_revoked):
                if await invoke(partial(
                        is_revoked,
                        request,
                        decoded,
                )):
                    raise web.HTTPForbidden(reason='Token is revoked')

            request[request_property] = decoded

            if store_token and isinstance(store_token, str):
                request[store_token] = token

        return await handler(request)

    return middleware
