import pytest

@pytest.fixture(scope='session', autouse=True)
def query_single_orphacode_string_v3():
    return {
        "query": {
            "filters": [
                {
                    "id": "Orphanet_558"}]
            , "requestedGranularity": "record"
        },
        'expected_count': 3,
        'expected_resources_ids': ["bbmri-eric:ID:EXT_44001:collection:MainCollection",
                                   "bbmri-eric:ID:IT_1382965524316631:collection:1444717339490516",
                                   "bbmri-eric:ID:IT_1385652938842205:collection:77630"]
    }

@pytest.fixture(scope='session', autouse=True)
def query_single_orphacode_string_v4():
    return {
        "query": {
            "filters": [
                {
                    "id": "ordo:Orphanet_15"}]
            , "requestedGranularity": "record"
        },
        'expected_count': 2,
        'expected_resources_ids': ["bbmri-eric:ID:IT_1382965524316631:collection:1444717339490516",
                                   "bbmri-eric:ID:EXT_44001:collection:MainCollection"]
    }


@pytest.fixture(scope='session', autouse=True)
def query_multiple_orphacode_array_v3():
    return {
        "query": {
            "filters": [
                {
                    "id": ["Orphanet_70", "Orphanet_555"]}]
            , "requestedGranularity": "record"
        },
        'expected_count': 7,
        'expected_resources_ids': ["bbmri-eric:ID:EXT_168416:collection:MainCollection",
                                   "bbmri-eric:ID:HU_SUB:collection:NEPSYBANK",
                                   "bbmri-eric:ID:HU_SUB:collection:NEPSYBANK_SMA",
                                   "bbmri-eric:ID:IT_1382965524316631:collection:1444717339490516",
                                   "bbmri-eric:ID:IT_1383047508168267:collection:1444717360015607",
                                   "bbmri-eric:ID:IT_1383230735994332:collection:1450446268862465",
                                   "bbmri-eric:ID:IT_1383929642991480:collection:1444717553513748"
                                   ]
    }


@pytest.fixture(scope='session', autouse=True)
def query_multiple_orphacode_array_v4():
    return {
        "query": {
            "filters": [
                {
                    "id": ["ordo:Orphanet_70", "ordo:Orphanet_555"]}]
            , "requestedGranularity": "record"
        },
        'expected_count': 7,
        'expected_resources_ids': ["bbmri-eric:ID:EXT_168416:collection:MainCollection",
                                   "bbmri-eric:ID:HU_SUB:collection:NEPSYBANK",
                                   "bbmri-eric:ID:HU_SUB:collection:NEPSYBANK_SMA",
                                   "bbmri-eric:ID:IT_1382965524316631:collection:1444717339490516",
                                   "bbmri-eric:ID:IT_1383047508168267:collection:1444717360015607",
                                   "bbmri-eric:ID:IT_1383230735994332:collection:1450446268862465",
                                   "bbmri-eric:ID:IT_1383929642991480:collection:1444717553513748"
                                   ]
    }

@pytest.fixture(scope='session', autouse=True)
def query_multiple_orphacode_and_filters():
    return {
        "query": {
            "filters": [
                {"id": ["ordo:Orphanet_15", "ordo:Orphanet_70"]},
                {"id": "ordo:Orphanet_555"}],
            "requestedGranularity": "record"
        },
        'expected_count': 1,
        'expected_resources_ids': ["bbmri-eric:ID:IT_1382965524316631:collection:1444717339490516"]
    }

@pytest.fixture(scope='session', autouse=True)
def query_country():
    return {
        "query": {
            "filters": [
                {"id": "dct:spatial", "operator": "=", "value": ["MT"]}],
            "requestedGranularity": "record"
        },
        'expected_count': 2,
        'expected_resources_ids': ["bbmri-eric:ID:EXT_DwarnaBio:collection:all_samples",
                                   "bbmri-eric:ID:MT_DwarnaBio:collection:studjuDwarna"
                                   ]
    }

@pytest.fixture(scope='session', autouse=True)
def query_by_resource_type_with_unsupported_filters():
    return {
        "query": {
            "filters": [
                {
                    "id": ["ejprd:Biobank"]},
                {
                    "id": ["ejprd:Guideline"]}
            ],
            "requestedGranularity": "record"
        },
        'expected_count': 3204,
        'expected_unsupported_filters': ["ejprd:Guideline"]
    }


@pytest.fixture(scope='session', autouse=True)
def query_unsupported_filters():
    return {
        "query": {
            "filters": [
                {
                    "id": ["ejprd:Guideline"]}
            ]
            , "requestedGranularity": "record"
        },
        'expected_error': "No valid query params provided. At least one supported and valid parameter should be provided"

    }


@pytest.fixture(scope='session', autouse=True)
def query_empty_filter():
    return {
        "query": {
            "filters": []
            , "requestedGranularity": "record"
        },
        'expected_error': "No valid query params provided. At least one supported and valid parameter should be provided"

    }

