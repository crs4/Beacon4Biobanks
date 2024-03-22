import base64
import logging
import secrets
import uuid
from datetime import datetime, timedelta

import requests
from aiohttp import web

from beacon.backends.fhir import fhir_base_url, fhir_json_header, library_version, measure_version, \
    evaluation_year_start, evaluation_year_end, max_items
from beacon.backends.fhir.cql.models import EvaluationMeasure, Library, Measure, Population
from beacon.backends.fhir.mappings import get_filters
from beacon.request.model import Operator, Granularity

complementary_operator = {
    Operator.EQUAL: Operator.EQUAL,
    Operator.NOT: Operator.NOT,
    Operator.GREATER: Operator.LESS,
    Operator.GREATER_EQUAL: Operator.LESS_EQUAL,
    Operator.LESS_EQUAL: Operator.GREATER_EQUAL
}

LOG = logging.getLogger(__name__)


def _perform_request(method, url, json=None, params=None):
    try:
        res = requests.request(method, url,
                               json=json.get_resource() if json is not None else None,
                               params=params if params is not None else None,
                               headers=fhir_json_header)
    except requests.exceptions.ConnectionError:
        raise web.HTTPInternalServerError(reason="Error contacting data service")

    LOG.debug("Performing request to %s" % url)
    if res.status_code not in (200, 201):
        LOG.debug("Error performing the request. Returned code %s" % res.status_code)
        raise Exception(res.json())
    return res.json()


def get_results(cql, granularity, subject):
    # step 1: encode the input cql
    base64_cql = encode(cql)
    library_url = generate_uuid()
    LOG.debug("Creating Library")
    LOG.debug(cql)
    # step 2: create the Library resource for the CQL query
    library = Library(version_id=library_version, last_updated=generate_creation_timestamp(),
                      data=base64_cql.decode('ascii'), id=generate_id(), url=library_url)
    _perform_request('POST', f"{fhir_base_url}/Library", library)
    LOG.debug("Library created")

    # step 3: create the measure associated with the Library
    populations = [Population(expression="InInitialPopulation", code="initial-population")]
    measure = Measure(stratifiers=[], populations=populations, version_id=measure_version,
                      last_updated=generate_creation_timestamp(),
                      subject=subject, library_url=library_url, id=generate_id())

    LOG.debug("Creating Measure")
    LOG.debug(measure.get_resource())
    created_measure = _perform_request('POST', f"{fhir_base_url}/Measure", measure)
    LOG.debug("Measure created")
    # step 4: execute the evaluation of the measure and get the List resource reference, containing the Specimen(s)
    # matching the results of the query
    measure_id = created_measure["id"]
    report_type = EvaluationMeasure.SUBJECT_LIST if granularity == Granularity.RECORD else EvaluationMeasure.POPULATION
    evaluation_measure = EvaluationMeasure(period_start=evaluation_year_start, period_end=evaluation_year_end,
                                           report_type=report_type)
    LOG.debug("Evaluating Measure")
    LOG.debug(evaluation_measure.get_resource())
    evaluation_measure_results = _perform_request(
        'POST',
        f"{fhir_base_url}/Measure/{measure_id}/$evaluate-measure",
        json=evaluation_measure
    )
    LOG.debug("Measure evaluated")
    LOG.debug(evaluation_measure_results)

    num = evaluation_measure_results['group'][0]['population'][0]['count']
    if granularity == Granularity.RECORD and num > 0:
        list_id = evaluation_measure_results['group'][0]['population'][0]['subjectResults']['reference'][5:]
        # get results from the measures list; at the moment it gets overall results
        params = {'_list': list_id, '_count': max_items}
        fhir_entries = _perform_request('GET', f"{fhir_base_url}/Specimen", params=params)
        beacon_records = fhir_entries
        num = len(beacon_records)
    else:
        beacon_records = []
        # num = evaluation_measure_results['group'][0]['population'][0]['count']
    return num, beacon_records


def get_biosample_results(cql, granularity):
    return get_results(cql, granularity, 'Specimen')


def get_individuals_results(cql, granularity):
    return get_results(cql, granularity, 'Patient')


def get_datasets_resources(dataset_id=None):
    """
    Function to get information about Collections from the FHIR store
    """
    datasets = []
    if dataset_id is None:
        response = _perform_request('GET', f"{fhir_base_url}/Organization", params={'type': '|Collection'})
        if response['total'] > 0:
            for collection in response['entry']:
                biobank_data = _perform_request('GET',
                                                f'{fhir_base_url}/{collection["resource"]["partOf"]["reference"]}')
                collection["resource"]["partOf"] = biobank_data
                datasets.append(collection['resource'])
    else:
        collection = _perform_request('GET', f"{fhir_base_url}/Organization/{dataset_id}")
        biobank_data = _perform_request('GET', f'{fhir_base_url}/{collection["partOf"]["reference"]}')
        collection["partOf"] = biobank_data
        datasets.append(collection)
    return datasets


def convert_date(beacon_input_date):
    beacon_datetime = datetime.strptime(beacon_input_date, '%Y%m%d')
    return beacon_datetime.strftime('%Y-%m-%d')


def transform_donor_age_filter_into_birth_date_filter(filter):
    now = datetime.today()
    years = int(filter.value)
    computed_date = now - timedelta(days=365 * years)
    filter.value = computed_date.strftime('%Y-%m-%d')
    filter.operator = complementary_operator[filter.operator]


def generate_uuid():
    # generates a urn unique id for FHIR resources, as for example "urn:uuid:367d2ebc-9bf9-40b0-b34f-9e35a681abcc"
    return 'urn:uuid:{uuid}'.format(uuid=uuid.uuid1())


def generate_creation_timestamp():
    return f"{datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f%z')[:-3]}Z"


def generate_id():
    return secrets.token_hex(8)


def get_filtering_terms_results(scope=None):
    return [ft for ft in get_filters() if scope is None or scope in ft['scope']]


def encode(string):
    return base64.b64encode(string.encode('ascii'))
