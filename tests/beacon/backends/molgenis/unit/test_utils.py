import pytest

from beacon.backends.molgenis.utils import get_resources_results, get_collection_uri


class MockMolgenisSession:
    def __init__(self, *args):
        pass

    def get(self, *args, **kwargs):
        return expected_matching_biobanks

    def login(self, user, password):
        pass


@pytest.fixture
def expected_results():
    return [{
        '_href': '/api/v2/eu_bbmri_eric_collections/bbmri:eric-biobank-1:collection:collection_1',
        'biobank': {
            '_href': '/api/v2/eu_bbmri_eric_biobanks/bbmri:eric-biobank-1',
            'id': 'bbmri:eric-biobank-1',
            'name': 'Biobank 1 Milan Institute',
            'country': {
                'id': 'IT',
                'name': 'Italy'
            }
        },
        'description': 'Plasma and other samples collection',
        'id': 'bbmri:eric-biobank-1:collection:collection_1',
        'name': 'Collection_1 of Biobank_1'
    }, {
        '_href': '/api/v2/eu_bbmri_eric_collections/bbmri:eric-biobank-1:collection:collection_2',
        'biobank': {
            '_href': '/api/v2/eu_bbmri_eric_biobanks/bbmri:eric-biobank-1',
            'id': 'bbmri:eric-biobank-1',
            'name': 'Biobank 1 Milan Institute',
            'country': {
                'id': 'IT',
                'name': 'Italy'
            }
        },
        'description': 'DNA, tissue and paraffin embedded colleciton',
        'id': 'bbmri:eric-biobank-1:collection:collection_2',
        'name': 'Collection_2 of Biobank_1'
    }]


@pytest.fixture
def expected_matching_biobanks():
    return [{'id': 'b1'}, {'id': 'b2'}]


def test_get_resources_results(mocker, expected_results):
    rsql_query = 'diagnosis_available=in=(ORPHA:10, ORPHA:100)'
    session = mocker.patch('beacon.backends.molgenis.client.Session', autospec=True)
    session.return_value.get.return_value = expected_results
    assert expected_results == get_resources_results(rsql_query, 0, 100)


def test_get_collection_url(mocker):
    collection_id = 'collection_1'
    mocker.patch('beacon.backends.molgenis.utils.conf.molgenis.base_resource_url', new='http://molgenisurl/#/collection')
    assert 'http://molgenisurl/#/collection/collection_1' == get_collection_uri(collection_id)
