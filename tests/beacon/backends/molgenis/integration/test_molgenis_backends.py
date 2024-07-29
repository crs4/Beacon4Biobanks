import pytest
import requests

from tests.beacon.backends.molgenis.integration.consts import COLLECTION_1_BIOBANK_1, COLLECTION_2_BIOBANK_1, \
    COLLECTION_2_BIOBANK_3, COLLECTION_1_BIOBANK_2, COLLECTION_2_BIOBANK_2, COLLECTION_3_BIOBANK_2, \
    COLLECTION_2_BIOBANK_4, COLLECTION_5_BIOBANK_4, COLLECTION_1_BIOBANK_3, COLLECTION_1_BIOBANK_4, \
    COLLECTION_3_BIOBANK_4, COLLECTION_4_BIOBANK_4, COLLECTION_3_BIOBANK_1, COLLECTION_4_BIOBANK_1, EJPRD_SCHEMA

pytest_plugins = 'pytest_asyncio'


@pytest.fixture
def disease_multiple_values_query():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": [
                        "ordo:Orphanet_10", "ordo:Orphanet_100"
                    ]
                }],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [
                        {
                            "id": [
                                "ordo:Orphanet_10",
                                "ordo:Orphanet_100"
                            ]
                        }
                    ],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [
                    EJPRD_SCHEMA
                ]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 4
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 4,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_1_BIOBANK_1,
                        COLLECTION_2_BIOBANK_1,
                        COLLECTION_2_BIOBANK_3,
                        COLLECTION_5_BIOBANK_4
                    ]
                }]
            }
        }
    }


@pytest.fixture
def disease_query_repeated_params():
    return {
        'request_body': {
            'query': {
                "filters": [{
                    "id": ["ordo:Orphanet_10", "ordo:Orphanet_100"]},
                    {"id": "ordo:Orphanet_100001"}
                ],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": [
                            "ordo:Orphanet_10",
                            "ordo:Orphanet_100"
                        ]
                    }, {
                        "id": "ordo:Orphanet_100001"
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 1
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 1,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_2_BIOBANK_1
                    ]}
                ]
            }
        }
    }


@pytest.fixture
def name_multiple_values_query():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "name",
                    "operator": "=",
                    "value": ["_2", "_5"]
                }],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "name",
                        "operator": "=",
                        "value": [
                            "_2",
                            "_5"
                        ]
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 7
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 7,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_2_BIOBANK_1,
                        COLLECTION_1_BIOBANK_2,
                        COLLECTION_2_BIOBANK_2,
                        COLLECTION_3_BIOBANK_2,
                        COLLECTION_2_BIOBANK_3,
                        COLLECTION_2_BIOBANK_4,
                        COLLECTION_5_BIOBANK_4
                    ]
                }]
            }
        }
    }


@pytest.fixture
def name_param_repeated():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "name",
                    "operator": "=",
                    "value": ["_2", "_5"]
                }, {
                    "id": "name",
                    "operator": "=",
                    "value": "_4"
                }],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "name",
                        "operator": "=",
                        "value": ["_2", "_5"]
                    }, {
                        "id": "name",
                        "operator": "=",
                        "value": "_4"
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 2
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 2,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_2_BIOBANK_4,
                        COLLECTION_5_BIOBANK_4
                    ]
                }]
            }
        }
    }


@pytest.fixture
def description_multiple_values_query():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "description",
                    "operator": "=",
                    "value": ["serum", "whole"]}
                ],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "description",
                        "operator": "=",
                        "value": [
                            "serum",
                            "whole"
                        ]
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 1
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 1,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_1_BIOBANK_2
                    ]
                }]
            }
        }
    }


@pytest.fixture
def description_param_repeated():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "description",
                    "operator": "=",
                    "value": ["DNA", "whole"]
                }, {
                    "id": "description",
                    "operator": "=",
                    "value": "tissue"
                }],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "description",
                        "operator": "=",
                        "value": [
                            "DNA",
                            "whole"
                        ]
                    }, {
                        "id": "description",
                        "operator": "=",
                        "value": "tissue"
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 2
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 2,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_2_BIOBANK_1,
                        COLLECTION_3_BIOBANK_1
                    ]
                }]
            }
        }
    }


@pytest.fixture
def organization_multiple_values_query():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "organization",
                    "operator": "=",
                    "value": ["Milan", "Rome"]}

                ],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "organization",
                        "operator": "=",
                        "value": [
                            "Milan",
                            "Rome"
                        ]
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 7
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 7,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_1_BIOBANK_1,
                        COLLECTION_2_BIOBANK_1,
                        COLLECTION_3_BIOBANK_1,
                        COLLECTION_4_BIOBANK_1,
                        COLLECTION_1_BIOBANK_2,
                        COLLECTION_2_BIOBANK_2,
                        COLLECTION_3_BIOBANK_2
                    ]
                }]
            }
        }
    }


@pytest.fixture
def organization_param_repeated():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "organization",
                    "operator": "=",
                    "value": ["Biobank", "Institute"]
                }, {
                    "id": "organization",
                    "operator": "=",
                    "value": ["Madrid"]
                }],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "organization",
                        "operator": "=",
                        "value": [
                            "Biobank",
                            "Institute"
                        ]
                    }, {
                        "id": "organization",
                        "operator": "=",
                        "value": [
                            "Madrid"
                        ]
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 2
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 2,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_1_BIOBANK_3,
                        COLLECTION_2_BIOBANK_3
                    ]}
                ]
            }
        }
    }


@pytest.fixture
def country_multiple_values_query():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "country",
                    "operator": "=",
                    "value": ["ES", "DE"]}
                ],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "country",
                        "operator": "=",
                        "value": [
                            "ES",
                            "DE"
                        ]
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 7
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 7,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_1_BIOBANK_3,
                        COLLECTION_2_BIOBANK_3,
                        COLLECTION_1_BIOBANK_4,
                        COLLECTION_2_BIOBANK_4,
                        COLLECTION_3_BIOBANK_4,
                        COLLECTION_4_BIOBANK_4,
                        COLLECTION_5_BIOBANK_4
                    ]
                }]
            }
        }
    }


@pytest.fixture
def id_multiple_values_query():
    return {
        'request_body': {
            "query": {
                "filters": [{
                    "id": "id",
                    "operator": "=",
                    "value": [
                        "bbmri:eric-biobank-1:collection:collection_1",
                        "bbmri:eric-biobank-1:collection:collection_2"
                    ]}
                ],
                "requestedGranularity": "record"
            }
        },
        'expected_response': {
            "meta": {
                "beaconId": "",
                "apiVersion": "v2.0.0",
                "returnedGranularity": "record",
                "receivedRequestSummary": {
                    "apiVersion": "v2.0.0",
                    "requestedSchemas": [],
                    "filters": [{
                        "id": "id",
                        "operator": "=",
                        "value": [
                            "bbmri:eric-biobank-1:collection:collection_1",
                            "bbmri:eric-biobank-1:collection:collection_2"
                        ]
                    }],
                    "requestParameters": {},
                    "includeResultsetResponses": "HIT",
                    "pagination": {
                        "skip": 0,
                        "limit": 100
                    },
                    "requestedGranularity": "record",
                    "testMode": False
                },
                'returnedSchemas': [EJPRD_SCHEMA]
            },
            "responseSummary": {
                "exists": True,
                "numTotalResults": 2
            },
            "beaconHandovers": [],
            "response": {
                "resultSets": [{
                    "id": "",
                    "exists": True,
                    "resultsCount": 2,
                    'resultsHandover': None,
                    'setType': '',
                    "results": [
                        COLLECTION_1_BIOBANK_1,
                        COLLECTION_2_BIOBANK_1
                    ]}
                ]
            }
        }
    }


@pytest.fixture
def unsupported_filter_query():
    return {
        'request_body': {
            "query": {
                "filters": [{"id": "HP:HP_0001251"}],
                "requestedGranularity": "record"
            }
        },
        'expected_response': None
    }


@pytest.mark.molgenis_up
def test_expected_catalog_response_disease_multiple_value(disease_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs', json=disease_multiple_values_query['request_body'])
    assert disease_multiple_values_query['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_disease_repeated(disease_query_repeated_params):
    response = requests.post('http://localhost:5050/api/catalogs', json=disease_query_repeated_params['request_body'])
    assert disease_query_repeated_params['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_name_multiple(name_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs', json=name_multiple_values_query['request_body'])
    assert name_multiple_values_query['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_name_repeated(name_param_repeated):
    response = requests.post('http://localhost:5050/api/catalogs', json=name_param_repeated['request_body'])
    assert name_param_repeated['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_description_multiple(description_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs',
                             json=description_multiple_values_query['request_body'])
    assert description_multiple_values_query['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_description_repeated(description_param_repeated):
    response = requests.post('http://localhost:5050/api/catalogs', json=description_param_repeated['request_body'])
    assert description_param_repeated['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_organization_multiple(organization_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs',
                             json=organization_multiple_values_query['request_body'])
    assert organization_multiple_values_query['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_expected_catalog_response_organization_repeated(organization_param_repeated):
    response = requests.post('http://localhost:5050/api/catalogs', json=organization_param_repeated['request_body'])
    assert organization_param_repeated['expected_response'] == response.json()


@pytest.mark.molgenis_up
# country has only or query, and query makes no sense
def test_expected_catalog_response_country_multiple(country_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs',
                             json=country_multiple_values_query['request_body'])
    assert country_multiple_values_query['expected_response'] == response.json()


@pytest.mark.molgenis_up
# id has only exact query
def test_expected_catalog_response_id_multiple(id_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs',
                             json=id_multiple_values_query['request_body'])
    assert id_multiple_values_query['expected_response'] == response.json()


@pytest.mark.molgenis_up
def test_unsupported_filter(unsupported_filter_query):
    response = requests.post('http://localhost:5050/api/catalogs',
                             json=unsupported_filter_query['request_body'])
    assert response.status_code == 200
    assert response.json()['info'] == {
        "warnings": {
            "unsupportedFilters": ["HP:HP_0001251"]
        }
    }


@pytest.mark.molgenis_down
def test_molgenis_connection_error(disease_multiple_values_query):
    response = requests.post('http://localhost:5050/api/catalogs',
                             json=disease_multiple_values_query['request_body'])
    assert response.status_code == 200
    assert response.json() == {
        'errorCode': 500,
        'errorMessage': 'Connection to data source failed'
    }
