import logging

from aiohttp import web
from molgenis.client import Session
from molgenis.errors import MolgenisRequestError
from requests.exceptions import ConnectionError

from beacon import conf

LOG = logging.getLogger(__name__)


def get_session():
    s = Session(conf.molgenis.url)
    if conf.molgenis.user is not None and conf.molgenis.password is not None:
        s.login(conf.molgenis.user, conf.molgenis.password)
    return s


def perform_request(entity, **kwargs):
    try:
        session = get_session()
        return session.get(entity, **kwargs)
    except (MolgenisRequestError, ConnectionError) as e:
        LOG.error("Error contacting molgenis")
        LOG.error(e)
        raise web.HTTPInternalServerError(reason="Connection to data source failed")
