import logging

from beacon import conf
from beacon.backends.molgenis.client import perform_request

LOG = logging.getLogger(__name__)


def get_resources_results(rsql_query, start, num):
    return perform_request('eu_bbmri_eric_collections',
                           attributes='id,name,description,url,timestamp,biobank,diagnosis_available',
                           expand='biobank', q=rsql_query, start=start, batch_size=num, raw=True)


def get_collection_uri(collection_id):
    if conf.molgenis.base_resource_url.endswith('/'):
        return f'{conf.molgenis.base_resource_url}{collection_id}'
    else:
        return f'{conf.molgenis.base_resource_url}/{collection_id}'
