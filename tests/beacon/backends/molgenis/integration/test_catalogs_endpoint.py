import json
import requests

from tests.beacon.backends.molgenis.integration import get_base_uri
from tests.beacon.backends.molgenis.integration.fixtures import query_single_orphacode_string_v3, \
    query_single_orphacode_string_v4, \
    query_multiple_orphacode_array_v3, query_multiple_orphacode_array_v4, query_multiple_orphacode_and_filters, \
    query_country, \
    query_by_resource_type_with_unsupported_filters, query_unsupported_filters, query_empty_filter, \
    query_multiple_orphacodes_array_v3_v4_combined

uri = f'{get_base_uri()}/api/catalogs'


def get_request_body(query):
    return {"meta": {"apiVersion": "v2.0"}, "query": query}


def get_resources(response_content):
    return json.loads(response_content)['response']['resultSets'][0]['results']


def test_query_catalogs_by_single_orphacode_v3_string(query_single_orphacode_string_v3):
    r = requests.post(url=uri, json=get_request_body(query_single_orphacode_string_v3['query']), verify=False)
    assert r.status_code == 200
    resources = get_resources(r.content)
    assert len(resources) == query_single_orphacode_string_v3['expected_count']
    for r in resources:
        assert r['id'] in query_single_orphacode_string_v3['expected_resources_ids']


def test_query_catalogs_by_single_orphacode_v4_string(query_single_orphacode_string_v4):
    r = requests.post(url=uri, json=get_request_body(query_single_orphacode_string_v4['query']), verify=False)
    assert r.status_code == 200
    resources = get_resources(r.content)
    assert len(resources) == query_single_orphacode_string_v4['expected_count']
    for r in resources:
        assert r['id'] in query_single_orphacode_string_v4['expected_resources_ids']


def test_query_catalogs_by_multiple_orphacode_v3(query_multiple_orphacode_array_v3):
    r = requests.post(url=uri, json=get_request_body(query_multiple_orphacode_array_v3['query']), verify=False)
    assert r.status_code == 200
    resources = get_resources(r.content)
    assert len(resources) == query_multiple_orphacode_array_v3['expected_count']
    for r in resources:
        assert r['id'] in query_multiple_orphacode_array_v3['expected_resources_ids']


def test_query_catalogs_by_multiple_orphacode_v4(query_multiple_orphacode_array_v4):
    r = requests.post(url=uri, json=get_request_body(query_multiple_orphacode_array_v4['query']), verify=False)
    assert r.status_code == 200
    resources = get_resources(r.content)
    assert len(resources) == query_multiple_orphacode_array_v4['expected_count']
    for r in resources:
        assert r['id'] in query_multiple_orphacode_array_v4['expected_resources_ids']


def test_query_catalogs_by_multiple_orphacode_and(query_multiple_orphacode_and_filters):
    r = requests.post(url=uri, json=get_request_body(query_multiple_orphacode_and_filters['query']), verify=False)
    assert r.status_code == 200
    resources = get_resources(r.content)
    assert len(resources) == query_multiple_orphacode_and_filters['expected_count']
    for r in resources:
        assert r['id'] in query_multiple_orphacode_and_filters['expected_resources_ids']


def test_query_catalogs_by_country(query_country):
    r = requests.post(url=uri, json=get_request_body(query_country['query']), verify=False)
    assert r.status_code == 200
    resources = get_resources(r.content)
    assert len(resources) == query_country['expected_count']
    for r in resources:
        assert r['id'] in query_country['expected_resources_ids']


def test_query_by_resource_type_with_unsupported_filters(query_by_resource_type_with_unsupported_filters):
    r = requests.post(url=uri, json=get_request_body(query_by_resource_type_with_unsupported_filters['query']),
                      verify=False)
    assert r.status_code == 200
    assert json.loads(r.content)['response']['resultSets'][0]['resultsCount'] == \
           query_by_resource_type_with_unsupported_filters['expected_count']


def test_query_unsupported_filters(query_unsupported_filters):
    r = requests.post(url=uri, json=get_request_body(query_unsupported_filters['query']), verify=False)
    assert r.status_code == 400
    assert query_unsupported_filters['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_empty_filter(query_empty_filter):
    r = requests.post(url=uri, json=get_request_body(query_empty_filter['query']), verify=False)
    assert r.status_code == 400
    assert query_empty_filter['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_catalogs_multiple_orphacodes_array_v3_v4(query_multiple_orphacodes_array_v3_v4_combined):
    r = requests.post(url=uri, json=get_request_body(query_multiple_orphacodes_array_v3_v4_combined['query']),
                      verify=False)
    assert r.status_code == 400
    assert query_multiple_orphacodes_array_v3_v4_combined['expected_error'] == json.loads(r.content)['errorMessage']
