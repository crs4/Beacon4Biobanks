import logging

from aiohttp import web
from molgenis.client import Session
from molgenis.errors import MolgenisRequestError
from requests.exceptions import ConnectionError

from beacon import conf

LOG = logging.getLogger(__name__)


def get_session(url, user, password):
    s = Session(url)
    if user is not None and password is not None:
        s.login(user, password)
    return s


def perform_request(molgenis_url, molgenis_user, molgenis_password, entity, **kwargs):
    try:
        session = get_session(molgenis_url, molgenis_user, molgenis_password)
        return session.get(entity, **kwargs)
    except (MolgenisRequestError, ConnectionError) as e:
        LOG.error("Error contacting molgenis")
        LOG.error(e)
        raise web.HTTPInternalServerError(reason="Connection to data source failed")
