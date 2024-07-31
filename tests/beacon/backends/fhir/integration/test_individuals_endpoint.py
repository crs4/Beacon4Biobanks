import json

import requests

from tests.beacon.backends.fhir.integration import get_headers, get_base_uri
from tests.beacon.backends.fhir.integration.fixtures import (query_single_orphacode_string_v3,
                                                             query_single_orphacode_array_v3, \
                                                             query_single_orphacode_string_v4,
                                                             query_single_orphacode_array_v4,
                                                             query_multiple_orphacodes_array,
                                                             query_multiple_orphacodes_array_v3_v4_combined, \
                                                             query_multiple_orphacodes_and_filter,
                                                             query_sex_single_value, query_sex_multiple_value,
                                                             query_sex_multiple_value_not_allowed, query_age_this_year,
                                                             query_unsupported_param, \
                                                             query_both_supported_and_unsupported,
                                                             query_disease_code_and_sex,
                                                             query_sample_type_transcoded_to_single_code,
                                                             query_sample_type_transcoded_to_multiple_code, \
                                                             query_empty_filter, query_age_of_diagnosis)

uri = f'{get_base_uri()}/api/individuals'
headers = get_headers()


def get_request_body(query):
    return {"meta": {"apiVersion": "v2.0"}, "query": query}


def test_query_individuals_by_single_orphacode_v3_string(query_single_orphacode_string_v3):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_single_orphacode_string_v3['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_single_orphacode_string_v3['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_by_single_orphacode_v3_array(query_single_orphacode_array_v3):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_single_orphacode_array_v3['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_single_orphacode_array_v3['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_by_single_orphacode_v4_string(query_single_orphacode_string_v4):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_single_orphacode_string_v4['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_single_orphacode_string_v4['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_by_single_orphacode_v4_array(query_single_orphacode_array_v4):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_single_orphacode_array_v4['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_single_orphacode_array_v4['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_multiple_orphacodes_array(query_multiple_orphacodes_array):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_multiple_orphacodes_array['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_multiple_orphacodes_array['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_multiple_orphacodes_array_v3_v4(query_multiple_orphacodes_array_v3_v4_combined):
    r = requests.post(url=uri, headers=headers,
                      json=get_request_body(query_multiple_orphacodes_array_v3_v4_combined['query']), verify=False)
    assert r.status_code == 400
    assert query_multiple_orphacodes_array_v3_v4_combined['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_individuals_multiple_orphacodes_and_filter(query_multiple_orphacodes_and_filter):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_multiple_orphacodes_and_filter['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_multiple_orphacodes_and_filter['expected_individuals_count'] == \
           json.loads(r.content)['responseSummary']["numTotalResults"]


def test_query_individuals_sex_single_value(query_sex_single_value):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_sex_single_value['query']), verify=False)
    assert r.status_code == 200
    assert query_sex_single_value['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_sex_multiple_value(query_sex_multiple_value):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_sex_multiple_value['query']), verify=False)
    assert r.status_code == 200
    assert query_sex_multiple_value['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_sex_multiple_value_not_allowed(query_sex_multiple_value_not_allowed):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_sex_multiple_value_not_allowed['query']),
                      verify=False)
    assert r.status_code == 400
    assert query_sex_multiple_value_not_allowed['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_individuals_age_this_year(query_age_this_year):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_age_this_year['query']), verify=False)
    assert r.status_code == 400
    assert query_age_this_year['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_individuals_unsupported_param(query_unsupported_param):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_unsupported_param['query']), verify=False)
    assert r.status_code == 400
    assert query_unsupported_param['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_individuals_both_supported_and_unsupported(query_both_supported_and_unsupported):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_both_supported_and_unsupported['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_both_supported_and_unsupported['expected_individuals_count'] == \
           json.loads(r.content)['responseSummary']["numTotalResults"]
    assert query_both_supported_and_unsupported['unsupported_filters'] == \
           json.loads(r.content)['response']['resultSets'][0]['info']['warnings']['unsupportedFilters']


def test_query_individuals_by_disease_and_sex(query_disease_code_and_sex):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_disease_code_and_sex['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_disease_code_and_sex['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]


def test_query_individuals_by_sample_type_single_code_transcoding(query_sample_type_transcoded_to_single_code):
    r = requests.post(url=uri, headers=headers,
                      json=get_request_body(query_sample_type_transcoded_to_single_code['query']), verify=False)
    assert r.status_code == 200
    assert query_sample_type_transcoded_to_single_code['expected_individuals_count'] == \
           json.loads(r.content)['responseSummary']["numTotalResults"]


def test_query_individuals_by_sample_type_multiple_code_transcoding(query_sample_type_transcoded_to_multiple_code):
    r = requests.post(url=uri, headers=headers,
                      json=get_request_body(query_sample_type_transcoded_to_multiple_code['query']), verify=False)
    assert r.status_code == 200
    assert query_sample_type_transcoded_to_multiple_code['expected_individuals_count'] == \
           json.loads(r.content)['responseSummary']["numTotalResults"]


def test_query_individuals_empty_filter(query_empty_filter):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_empty_filter['query']), verify=False)
    assert r.status_code == 400
    assert query_empty_filter['expected_error'] == json.loads(r.content)['errorMessage']


def test_query_individuals_by_age_of_diagnosis(query_age_of_diagnosis):
    r = requests.post(url=uri, headers=headers, json=get_request_body(query_age_of_diagnosis['query']),
                      verify=False)
    assert r.status_code == 200
    assert query_age_of_diagnosis['expected_individuals_count'] == json.loads(r.content)['responseSummary'][
        "numTotalResults"]
