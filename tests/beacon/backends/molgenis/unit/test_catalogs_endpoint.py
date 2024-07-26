import json
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
from aiohttp import web
from aiohttp_middlewares import cors_middleware

from beacon.request.routes import routes
from beacon.response import middlewares
from tests.conf.conftest import disease_single_filter_into_array_v3_spec, phenotype_filter, \
    resource_type_biobank_filter, \
    resource_type_patient_registry_filter, resource_type_registry_filter_multiple_with_one_supported, \
    resource_type_registry_filter_multiple_all_unsupported, disease_v4_and_v3_specs_filter_different_instances, \
    country_filter, \
    disease_single_filter_into_array_v4_spec, disease_single_filter_string_v4_spec, disease_single_filter_string_v3_spec

VALID_FILTERS_RESPONSE = b'500: Connection to data source failed'
NO_VALID_FILTERS_RESPONSE = b'No valid query params provided. At least one supported and valid parameter should be provided'
CATALOGS_ENDPOINT = 'api/catalogs'

GET_RESOURCES_RESULTS_PATH = 'beacon.backends.molgenis.resources.get_resources_results'
MAP_RESOURCE_PATH = 'beacon.backends.molgenis.mappers.records.map_resource'

get_results_mock = MagicMock()
get_results_mock.return_value = {'items': [], 'total': 0}


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
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_single_disease_code_valid(aiohttp_client, disease_single_filter_into_array_v3_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_single_filter_into_array_v3_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_disease_multiple_specs(aiohttp_client,
                                                      disease_v4_and_v3_specs_filter_different_instances):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_v4_and_v3_specs_filter_different_instances))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_individuals_by_single_disease_code_array_v3_spec(aiohttp_client,
                                                                    disease_single_filter_into_array_v3_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_single_filter_into_array_v3_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_individuals_by_single_disease_code_string_v3_spec(aiohttp_client,
                                                                     disease_single_filter_string_v3_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_single_filter_string_v3_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_single_disease_code_array_v4_spec(aiohttp_client,
                                                                 disease_single_filter_into_array_v4_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_single_filter_into_array_v4_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_individuals_by_single_disease_code_string_v4_spec(aiohttp_client,
                                                                     disease_single_filter_string_v4_spec):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_single_filter_string_v4_spec))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_phenotype(aiohttp_client, phenotype_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(phenotype_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_resource_type_biobank(aiohttp_client, resource_type_biobank_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(resource_type_biobank_filter))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_resource_type_registry(aiohttp_client, resource_type_patient_registry_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(resource_type_patient_registry_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_resource_type_multiple_with_one_supported(aiohttp_client,
                                                                         resource_type_registry_filter_multiple_with_one_supported):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT,
                                 data=json.dumps(resource_type_registry_filter_multiple_with_one_supported))
    assert r.status == 200


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_get_catalogs_by_resource_type_multiple_all_unsupported(aiohttp_client,
                                                                      resource_type_registry_filter_multiple_all_unsupported):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT,
                                 data=json.dumps(resource_type_registry_filter_multiple_all_unsupported))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
@patch(GET_RESOURCES_RESULTS_PATH, get_results_mock)
@patch(MAP_RESOURCE_PATH, MagicMock())
async def test_country_filter(aiohttp_client, country_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(country_filter))
    assert r.status == 200
