import json
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
from aiohttp import web
from aiohttp_middlewares import cors_middleware

from beacon.request.routes import routes
from beacon.response import middlewares
from tests.conf.conftest import disease_single_filter_into_array_v3_spec, not_supported_filter, \
    empty_filter, disease_v4_and_v3_specs_filter_different_instances, \
    sex_filter, specimen_type_multiple_internal_transcoding_filter, \
    specimen_type_multiple_values_filter, phenotype_filter, \
    multiple_values_both_supported_and_unsupported_filter, age_this_year_filter, \
    age_at_diagnosis_filter, disease_single_filter_string_v3_spec, disease_single_filter_into_array_v4_spec, \
    disease_single_filter_string_v4_spec, disease_v4_and_v3_specs_filter_same_array, sex_filter_value_not_allowed, \
    specimen_type_value_not_allowed

NO_VALID_FILTERS_RESPONSE = b'No valid query params provided. At least one supported and valid parameter should be provided'
INVALID_DISEASE_QUERY_PARAMS = b'Invalid query: different ontology specs combined in the same array for Disease filter parameter'
BIOSAMPLES_ENDPOINT = 'api/biosamples'

GET_BIOSAMPLE_RESULTS_PATH = 'beacon.backends.fhir.utils.get_biosample_results'
GET_RESULT_PATH = 'beacon.backends.fhir.utils.get_results'

get_results_mock = MagicMock()
get_results_mock.return_value = (0, [])


def create_app():
    beacon = web.Application(
        middlewares=[web.normalize_path_middleware(), middlewares.error_middleware, cors_middleware(
            origins=["https://beacon-network-test.ega-archive.org", "https://beacon-network-test2.ega-archive.org",
                     "https://beacon-network-demo.ega-archive.org", "https://beacon-network-demo2.ega-archive.org",
                     "http://localhost:3000", "http://localhost:3010",
                     "https://beacon-network-cineca-demo.ega-archive.org"])]
    )
    beacon.add_routes(routes)
    return beacon


@pytest.mark.asyncio
async def get_beacon_client(aiohttp_client):
    return await aiohttp_client(create_app(), server_kwargs={'port': 5050})


def get_json(content):
    return json.loads(content)


@pytest.mark.asyncio
async def test_get_service_info(aiohttp_client):
    beacon_client = await get_beacon_client(aiohttp_client)
    resp = await beacon_client.get("/api/service-info")
    content = await(resp.content.read())
    json_response = get_json(content)
    assert resp.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_single_disease_code_array_v3_spec(aiohttp_client,
                                                                   disease_single_filter_into_array_v3_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(disease_single_filter_into_array_v3_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_single_disease_code_string_v3_spec(aiohttp_client,
                                                                    disease_single_filter_string_v3_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(disease_single_filter_string_v3_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_single_disease_code_array_v4_spec(aiohttp_client,
                                                                   disease_single_filter_into_array_v4_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(disease_single_filter_into_array_v4_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_single_disease_code_string_v4_spec(aiohttp_client,
                                                                    disease_single_filter_string_v4_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(disease_single_filter_string_v4_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_single_disease_code_not_supported_filter(aiohttp_client, not_supported_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(not_supported_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_empty_filter(aiohttp_client, empty_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(empty_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_multiple_disease_code_old_and_new_specs(aiohttp_client,
                                                                         disease_v4_and_v3_specs_filter_different_instances):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT,
                                 data=json.dumps(disease_v4_and_v3_specs_filter_different_instances))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_multiple_disease_code_old_and_new_specs_same_array(aiohttp_client,
                                                                                    disease_v4_and_v3_specs_filter_same_array):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT,
                                 data=json.dumps(disease_v4_and_v3_specs_filter_same_array))
    assert r.status == 400
    content = await(r.content.read())
    assert content == INVALID_DISEASE_QUERY_PARAMS


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_sex(aiohttp_client, sex_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(sex_filter))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_sex_not_allowed_value(aiohttp_client, sex_filter_value_not_allowed):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(sex_filter_value_not_allowed))
    assert r.status == 400
    content = await(r.content.read())
    assert content == b'Invalid query: value ncit:C36843 not allowed for filter ncit:C28421'


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_sample_type_multiple_internal_transcoding(aiohttp_client,
                                                                           specimen_type_multiple_internal_transcoding_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT,
                                 data=json.dumps(specimen_type_multiple_internal_transcoding_filter))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_sample_type_multiple_values(aiohttp_client, specimen_type_multiple_values_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(specimen_type_multiple_values_filter))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_sample_type_not_allowed_value(aiohttp_client, specimen_type_value_not_allowed):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(specimen_type_value_not_allowed))
    assert r.status == 400
    content = await(r.content.read())
    assert content == b'Invalid query: value obi:0002694 not allowed for filter ncit:C70713'


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_unsupported_filters_only(aiohttp_client, phenotype_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(phenotype_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_supported_and_unsupported_filters(aiohttp_client,
                                                                multiple_values_both_supported_and_unsupported_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT,
                                 data=json.dumps(multiple_values_both_supported_and_unsupported_filter))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_age_this_year(aiohttp_client, age_this_year_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(age_this_year_filter))
    assert r.status == 400


@pytest.mark.asyncio
@patch(GET_BIOSAMPLE_RESULTS_PATH, MagicMock())
@patch(GET_RESULT_PATH, get_results_mock)
async def test_get_biosamples_by_age_at_diagnosis(aiohttp_client, age_at_diagnosis_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(BIOSAMPLES_ENDPOINT, data=json.dumps(age_at_diagnosis_filter))
    assert r.status == 200
