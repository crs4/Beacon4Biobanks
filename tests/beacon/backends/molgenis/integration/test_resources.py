import pytest

from beacon.backends.molgenis.resources import get_resources
from beacon.request.model import RequestMeta, RequestParams, RequestQuery, Granularity
from beacon.schemas import get_default_schema
from tests.integration.molgenis import COLLECTION_1_BIOBANK_1, COLLECTION_2_BIOBANK_1, \
    COLLECTION_2_BIOBANK_3, COLLECTION_5_BIOBANK_4, COLLECTION_3_BIOBANK_1, COLLECTION_1_BIOBANK_2, \
    COLLECTION_2_BIOBANK_4, COLLECTION_4_BIOBANK_4


@pytest.fixture
def request_meta():
    r_meta = RequestMeta()
    r_meta.requested_schemas = []
    r_meta.api_version = 'v2.0.0'
    return r_meta


@pytest.fixture
def request_qparams_diseases_filter_multiple_values(request_meta):
    r_params = RequestParams()
    r_params.meta = request_meta
    r_query = RequestQuery()
    filters = [{'id': ['ordo:Orphanet_10', 'ordo:Orphanet_100', 'ordo:Orphanet_100008']}]
    r_query.filters = filters
    r_query.requested_granularity = Granularity.RECORD
    r_params.query = r_query
    return {'request_params': r_params,
            'expected_result': [
                COLLECTION_1_BIOBANK_1,
                COLLECTION_2_BIOBANK_1,
                COLLECTION_3_BIOBANK_1,
                COLLECTION_2_BIOBANK_3,
                COLLECTION_5_BIOBANK_4]
            }


@pytest.fixture
def request_qparams_diseases_filter_repeated(request_meta):
    r_params = RequestParams()
    r_params.meta = request_meta
    r_query = RequestQuery()
    filters = [{'id': ['ordo:Orphanet_10', 'ordo:Orphanet_100']}, {'id': ['ordo:Orphanet_100001']}]
    r_query.filters = filters
    r_query.requested_granularity = Granularity.RECORD
    r_params.query = r_query
    return {
        'request_params': r_params,
        'expected_result': [COLLECTION_2_BIOBANK_1]
    }


@pytest.fixture
def request_qparams_alphanumeric_filter_multiple_values(request_meta):
    r_params = RequestParams()
    r_params.meta = request_meta
    r_query = RequestQuery()
    filters = [{'id': 'description', 'operator': '=', 'value': ['DNA', 'serum']}]
    r_query.filters = filters
    r_query.requested_granularity = Granularity.RECORD
    r_params.query = r_query
    return {'request_params': r_params,
            'expected_result': [
                COLLECTION_2_BIOBANK_1,
                COLLECTION_3_BIOBANK_1,
                COLLECTION_1_BIOBANK_2,
                COLLECTION_2_BIOBANK_4,
                COLLECTION_4_BIOBANK_4,
                COLLECTION_5_BIOBANK_4
            ]}


@pytest.fixture
def request_qparams_alphanumeric_filter_repeated(request_meta):
    r_params = RequestParams()
    r_params.meta = request_meta
    r_query = RequestQuery()
    filters = [{'id': 'description', 'operator': '=', 'value': ['DNA', 'serum']},
               {'id': 'description', 'operator': '=', 'value': 'paraffin'}]
    r_query.filters = filters
    r_query.requested_granularity = Granularity.RECORD
    r_params.query = r_query
    return {
        'request_params': r_params,
        'expected_result': [COLLECTION_2_BIOBANK_1, COLLECTION_3_BIOBANK_1]
    }


@pytest.mark.molgenis_up
def test_get_datasets_diseases_filter_multiple_values(request_qparams_diseases_filter_multiple_values):
    datasets = get_resources(None, request_qparams_diseases_filter_multiple_values['request_params'],
                             get_default_schema("resource"))
    assert datasets[2] == request_qparams_diseases_filter_multiple_values['expected_result']


@pytest.mark.molgenis_up
def test_get_datasets_diseases_filter_multiple_param_presence(request_qparams_diseases_filter_repeated):
    datasets = get_resources(None, request_qparams_diseases_filter_repeated['request_params'],
                             get_default_schema("resource"))
    assert datasets[2] == request_qparams_diseases_filter_repeated['expected_result']


@pytest.mark.molgenis_up
def test_get_datasets_alphanumeric_filter_multiple_values_contains_clause(
        request_qparams_alphanumeric_filter_multiple_values):
    datasets = get_resources(None, request_qparams_alphanumeric_filter_multiple_values['request_params'],
                             get_default_schema("resource"))
    assert datasets[2] == request_qparams_alphanumeric_filter_multiple_values['expected_result']


@pytest.mark.molgenis_up
def test_get_datasets_alphanumeric_filter_multiple_param_presence_contains_clause(
        request_qparams_alphanumeric_filter_repeated):
    datasets = get_resources(None, request_qparams_alphanumeric_filter_repeated['request_params'],
                             get_default_schema("resource"))
    assert datasets[2] == request_qparams_alphanumeric_filter_repeated['expected_result']
