import argparse
import logging
import os
import ssl
from pathlib import Path

from aiohttp import web
from aiohttp_middlewares import cors_middleware
from jwt import PyJWKClient

from beacon import load_logger, load_config

LOG = logging.getLogger(__name__)


async def initialize(app):
    # conf.update({'update_datetime': datetime.now().isoformat()})
    LOG.info("Initialization done.")


async def destroy(app):
    """Upon server close, close the DB connections."""
    LOG.info("Shutting down.")


def main(conf_file, path=None):
    load_config(conf_file)
    load_logger()

    from beacon import conf
    from beacon.request.routes import routes
    from beacon.response import middlewares

    ms = [web.normalize_path_middleware(), cors_middleware(origins=["http://localhost:3000"]),
          middlewares.error_middleware]

    if conf.service.auth_key is not None:
        ms.append(middlewares.token_auth_middleware())

    if conf.idp is not None:
        public_endpoints = [
            '^/api$', '^/api/info$', '^/api/service-info$',
            '^/api/filtering_terms$', '^/api/configuration$', '^/api/entry_types$',
            '^/api/map$'
        ]
        jwks_client = PyJWKClient(conf.idp.jwk_set_url, cache_keys=True)
        ms.append(
            middlewares.JWTMiddleware(jwks_client, whitelist=public_endpoints, algorithms=["RS256"],
                                      issuer=conf.idp.issuer, audience=conf.idp.audience))

    beacon = web.Application(
        middlewares=ms
    )

    beacon.on_startup.append(initialize)
    beacon.on_cleanup.append(destroy)
    # Configure the endpoints
    beacon.add_routes(routes)

    # Configure HTTPS (or not)
    ssl_context = None
    if getattr(conf, "beacon_tls_enabled", False):
        use_as_client = getattr(conf, "beacon_tls_client", False)
        sslcontext = ssl.create_default_context(
            ssl.Purpose.CLIENT_AUTH if use_as_client else ssl.Purpose.SERVER_AUTH
        )
        sslcontext.load_cert_chain(conf.beacon_cert, conf.beacon_key)  # should exist
        sslcontext.check_hostname = False
        # TODO: add the CA chain

    # Run beacon
    if path:
        if os.path.exists(path):
            os.unlink(path)
        # will create the UDS socket and bind to it
        web.run_app(beacon, path=path, shutdown_timeout=0, ssl_context=ssl_context)
    else:
        web.run_app(
            beacon,
            host=getattr(conf, "beacon_host", "0.0.0.0"),
            port=getattr(conf, "beacon_port", 5050),
            shutdown_timeout=0,
            ssl_context=ssl_context,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help="The configuration file for this beacon", type=str, required=True,
                        default='./config.molgenis.yml')
    parser.add_argument('--socket', '-s',
                        help="The socket file to use. If present the web app will run as a unix socket",
                        required=False)
    args = parser.parse_args()
    conf_file_path = Path(args.config).as_posix()

    if args.socket:
        main(path=args.socket, conf_file=conf_file_path)
    else:
        main(conf_file=args.config)
