import pytest


@pytest.fixture(scope='session', autouse=True)
def query_single_orphacode_string_v3():
    return {
        'query': {
            "filters": [
                {"id": "Orphanet_457260"}
            ]
            , "requestedGranularity": "count"
        },
        'expected_biosamples_count': 46,
        'expected_individuals_count': 18,

    }


@pytest.fixture(scope='session', autouse=True)
def query_single_orphacode_string_v4():
    return {
        'query': {
            "filters": [
                {"id": "ordo:Orphanet_457260"}
            ]
            , "requestedGranularity": "count"
        },
        'expected_biosamples_count': 46,
        'expected_individuals_count': 18,
    }


@pytest.fixture(scope='session', autouse=True)
def query_single_orphacode_array_v3():
    return {
        'query': {
            "filters": [
                {"id": ["Orphanet_79241"]}
            ]
            , "requestedGranularity": "count"
        },
        'expected_biosamples_count': 2,
        'expected_individuals_count': 1
    }


@pytest.fixture(scope='session', autouse=True)
def query_single_orphacode_array_v4():
    return {
        'query': {
            "filters": [
                {"id": ["ordo:Orphanet_79241"]}
            ]
            , "requestedGranularity": "count"
        },
        'expected_biosamples_count': 2,
        'expected_individuals_count': 1
    }


@pytest.fixture(scope='session', autouse=True)
def query_multiple_orphacodes_array():
    return {
        'query': {
            "filters": [
                {"id": ["ordo:Orphanet_457260", "ordo:Orphanet_79241"]}
            ]
            , "requestedGranularity": "count"
        },
        'expected_biosamples_count': 48,
        'expected_individuals_count': 19
    }


@pytest.fixture(scope='session', autouse=True)
def query_multiple_orphacodes_and_filter():
    return {
        'query': {
            "filters": [
                {"id": ["ordo:Orphanet_803", "ordo:Orphanet_550"]},
                {"id": "ordo:Orphanet_791"}
            ]
            , "requestedGranularity": "count"
        },
        'expected_individuals_count': 0
    }


@pytest.fixture(scope='session', autouse=True)
def query_multiple_orphacodes_array_v3_v4_combined():
    return {
        'query': {
            "filters": [
                {"id": ["Orphanet_457260", "ordo:Orphanet_79241"]}
            ]
            , "requestedGranularity": "count"
        },
        'expected_error': "Invalid query: different ontology specs combined in the same array for Disease filter parameter"
    }


@pytest.fixture(scope='session', autouse=True)
def query_sex_single_value():
    return {
        "query": {
            "filters": [{
                "id": "ncit:C28421",
                "operator": "=",
                "value": "ncit:C16576"
            }]
        },
        'expected_biosamples_count': 388,
        'expected_individuals_count': 280
    }


@pytest.fixture(scope='session', autouse=True)
def query_sex_multiple_value():
    return {
        "query": {
            "filters": [{
                "id": "ncit:C28421",
                "operator": "=",
                "value": ["ncit:C16576", 'ncit:C20197']
            }]
        },
        'expected_biosamples_count': 747,
        'expected_individuals_count': 555
    }


@pytest.fixture(scope='session', autouse=True)
def query_sex_multiple_value_not_allowed():
    return {
        "query": {
            "filters": [{
                "id": "ncit:C28421",
                "operator": "=",
                "value": ["ncit:C16576", 'ncit:C179197']
            }]
        },
        'expected_error': "Invalid query: value ncit:C179197 not allowed for filter ncit:C28421"
    }


@pytest.fixture(scope='session', autouse=True)
def query_age_this_year():
    return {
        "query": {
            "filters": [
                {
                    "id": "ncit:C83164",
                    "operator": ">=",
                    "value": "20"
                },
                {
                    "id": "ncit:C83164",
                    "operator": "<=",
                    "value": "40"
                }
            ]
        },
        'expected_error': "No valid query params provided. At least one supported and valid parameter should be provided"
    }


@pytest.fixture(scope='session', autouse=True)
def query_unsupported_param():
    return {
        "query": {
            "meta": {
                "apiVersion": "2.0",
                "requestedGranularity": "count"
            },
            "query": {
                "filters": [{
                    "id": "sio:SIO_010056",
                    "operator": "=",
                    "value": "hp:0001251"
                }]
            }
        },
        'expected_error': "No valid query params provided. At least one supported and valid parameter should be provided"
    }


@pytest.fixture(scope='session', autouse=True)
def query_both_supported_and_unsupported():
    return {
        "query": {"filters": [{"id": ["ordo:Orphanet_100051", "ordo:Orphanet_99995"]},
                              {"id": "ncit:C28421", "operator": "=",
                               "value": ["ncit:C16576", "ncit:C20197", "ncit:C124294", "ncit:C17998"]},
                              {"id": "ncit:C124353", "operator": ">=", "value": "0"},
                              {"id": "ncit:C124353", "operator": "<=", "value": "100"}]},
        'expected_biosamples_count': 4,
        'expected_individuals_count': 4,
        'unsupported_filters': ['ncit:C124353']
    }


@pytest.fixture(scope='session', autouse=True)
def query_disease_code_and_sex():
    return {
        "query": {
            "filters": [
                {
                    "id": ["ordo:Orphanet_231512", "ordo:Orphanet_166"]}, {
                    "id": "ncit:C28421",
                    "operator": "=",
                    "value": ["ncit:C16576", "ncit:C20197"]
                }]
            , "requestedGranularity": "count"
        },
        'expected_biosamples_count': 219,
        'expected_individuals_count': 217
    }


@pytest.fixture(scope='session', autouse=True)
def query_sample_type_transcoded_to_single_code():
    return {
        "query": {
            "filters": [{
                "id": "ncit:C70713",
                "operator": "=",
                "value": ["obi:0000651"]
            }]
        },
        'expected_biosamples_count': 22,
        'expected_individuals_count': 22
    }


@pytest.fixture(scope='session', autouse=True)
def query_sample_type_transcoded_to_multiple_code():
    return {
        "query": {
            "filters": [{
                "id": "ncit:C70713",
                "operator": "=",
                "value": ["obi:0000655"]
            }]
        },
        'expected_biosamples_count': 1,
        'expected_individuals_count': 1
    }


@pytest.fixture(scope='session', autouse=True)
def query_empty_filter():
    return {
        "query": {
            "meta": {
                "apiVersion": "2.0",
                "requestedGranularity": "count"
            },
            "query": {
                "filters": []
            }
        },
        'expected_error': "No valid query params provided. At least one supported and valid parameter should be provided"
    }


@pytest.fixture(scope='session', autouse=True)
def query_age_of_diagnosis():
    return {
        "query": {
            "filters": [
                {
                    "id": "ncit:C156420",
                    "operator": ">=",
                    "value": '0'
                },
                {
                    "id": "ncit:C156420",
                    "operator": "<=",
                    "value": '95'
                }
            ]
        },
        'expected_biosamples_count': 2,
        'expected_individuals_count': 1
    }
