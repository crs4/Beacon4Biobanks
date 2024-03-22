import pytest

from beacon.backends.molgenis.utils import get_resources_results


@pytest.fixture
def expected_resources_multiple_orphacode_or():
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
    }, {
        '_href': '/api/v2/eu_bbmri_eric_collections/bbmri:eric-biobank-3:collection:collection_2',
        'biobank': {
            '_href': '/api/v2/eu_bbmri_eric_biobanks/bbmri:eric-biobank-3',
            'id': 'bbmri:eric-biobank-3',
            'name': 'Biobank 3 Madrid Institute',
            'country': {
                'id': 'ES',
                'name': 'Spain'
            }
        },
        'description': 'plasma collection',
        'id': 'bbmri:eric-biobank-3:collection:collection_2',
        'name': 'Collection_2 of Biobank_3'
    }, {
        '_href': '/api/v2/eu_bbmri_eric_collections/bbmri:eric-biobank-4:collection:collection_5',
        'biobank': {
            '_href': '/api/v2/eu_bbmri_eric_biobanks/bbmri:eric-biobank-4',
            'id': 'bbmri:eric-biobank-4',
            'name': 'Biobank 4 Monaco Institute',
            'country': {
                'id': 'DE',
                'name': 'Germany'
            }
        },
        'description': 'cell lines and DNA collection',
        'id': 'bbmri:eric-biobank-4:collection:collection_5',
        'name': 'Collection_5 of Biobank_4'
    }]


@pytest.mark.molgenis_up
def test_get_resources_multiple_orphacodes_in_or(expected_resources_multiple_orphacode_or):
    rsql = 'diagnosis_available=in=(ORPHA:10, ORPHA:100)'
    resources = get_resources_results(rsql, 0, 100)
    for i, r in enumerate(resources['items']):
        assert r['id'] == expected_resources_multiple_orphacode_or[i]['id']
        assert r['name'] == expected_resources_multiple_orphacode_or[i]['name']
        assert r['description'] == expected_resources_multiple_orphacode_or[i]['description']
        assert r['biobank']['id'] == expected_resources_multiple_orphacode_or[i]['biobank']['id']
        assert r['biobank']['name'] == expected_resources_multiple_orphacode_or[i]['biobank']['name']
        assert r['biobank']['country']['id'] == expected_resources_multiple_orphacode_or[i]['biobank']['country']['id']
        assert r['biobank']['country']['name'] == expected_resources_multiple_orphacode_or[i]['biobank']['country']['name']


def get_testing_matching_biobanks_by_countries():
    pass


def get_collection_uri():
    pass
