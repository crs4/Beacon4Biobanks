import logging

LOG = logging.getLogger(__name__)


def create_rsql_query(rsql_params):
    """
    Creates RSQL query, according to the various query parameters
    """
    rsql = ' and '.join('({})'.format(p.get_rsql()) for p in rsql_params if p.get_rsql() != '')
    LOG.debug("Generated RSQL is %s", rsql)
    return rsql
