import json

import pytest
from aiohttp import web
from aiohttp_middlewares import cors_middleware

from beacon.request.routes import routes
from beacon.response import middlewares
from tests.conf.conftest import disease_single_filter, phenotype_filter, resource_type_biobank_filter, \
    resource_type_patient_registry_filter, resource_type_registry_filter_multiple_with_one_supported, \
    resource_type_registry_filter_multiple_all_unsupported, disease_v4_and_v3_specs_filter, country_filter

VALID_FILTERS_RESPONSE = b'500: Connection to data source failed'
NO_VALID_FILTERS_RESPONSE = b'No valid query params provided. At least one supported and valid parameter should be provided'
CATALOGS_ENDPOINT = 'api/catalogs'


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
async def test_get_catalogs_by_single_disease_code_valid(aiohttp_client, disease_single_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_single_filter))
    assert r.status == 500
    content = await(r.content.read())
    assert content == VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_get_catalogs_by_disease_multiple_specs(aiohttp_client, disease_v4_and_v3_specs_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(disease_v4_and_v3_specs_filter))
    assert r.status == 500
    content = await(r.content.read())
    assert content == VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_get_catalogs_by_phenotype(aiohttp_client, phenotype_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(phenotype_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_get_catalogs_by_resource_type_biobank(aiohttp_client, resource_type_biobank_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(resource_type_biobank_filter))
    assert r.status == 500
    content = await(r.content.read())
    assert content == VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_get_catalogs_by_resource_type_registry(aiohttp_client, resource_type_patient_registry_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(resource_type_patient_registry_filter))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_get_catalogs_by_resource_type_multiple_with_one_supported(aiohttp_client,
                                                                         resource_type_registry_filter_multiple_with_one_supported):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT,
                                 data=json.dumps(resource_type_registry_filter_multiple_with_one_supported))
    assert r.status == 500
    content = await(r.content.read())
    assert content == VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_get_catalogs_by_resource_type_multiple_all_unsupported(aiohttp_client,
                                                                      resource_type_registry_filter_multiple_all_unsupported):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT,
                                 data=json.dumps(resource_type_registry_filter_multiple_all_unsupported))
    assert r.status == 400
    content = await(r.content.read())
    assert content == NO_VALID_FILTERS_RESPONSE


@pytest.mark.asyncio
async def test_country_filter(aiohttp_client, country_filter):
    beacon_client = await get_beacon_client(aiohttp_client)
    r = await beacon_client.post(CATALOGS_ENDPOINT, data=json.dumps(country_filter))
    assert r.status == 500
    content = await(r.content.read())
    assert content == VALID_FILTERS_RESPONSE
