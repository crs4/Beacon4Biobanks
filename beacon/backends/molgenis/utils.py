import logging

from beacon import conf
from beacon.backends.molgenis.client import perform_request

LOG = logging.getLogger(__name__)


def get_resources_results(rsql_query, start, num):
    return perform_request(conf.molgenis.url, conf.molgenis.user, conf.molgenis.password, 'eu_bbmri_eric_collections',
                           attributes='id,name,description,url,timestamp,biobank,diagnosis_available',
                           expand='biobank', q=rsql_query, start=start, batch_size=num, raw=True)


def collection_exists_in_default_molgenis(collection_id):
    res = perform_request(conf.molgenis.base_resource_check_url, None, None, 'eu_bbmri_eric_collections',
                          attributes='id', q=f"id=={collection_id}")
    return len(res) == 1


def get_url(base_url, collection_id):
    if base_url.endswith('/'):
        return f'{base_url}{collection_id}'
    else:
        return f'{base_url}/{collection_id}'


def get_collection_uri(collection_id):
    if conf.molgenis.alternative_base_resource_url is not None and not collection_exists_in_default_molgenis(collection_id):
        LOG.warning("Collection not found in the default molgenis %s" % conf.molgenis.base_resource_url)
        LOG.warning("Using alternative")
        return get_url(conf.molgenis.alternative_base_resource_url, collection_id)
    else:
        return get_url(conf.molgenis.base_resource_url, collection_id)


def validate_disease_filter(filter):
    if isinstance(filter, str):
        return True
    return not any(f.startswith('ordo:') for f in filter) or not any(f.startswith('Orphanet_') for f in filter)
