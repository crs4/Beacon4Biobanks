import logging

from beacon import conf
from beacon.backends.fhir.mappings import _UNSUPPORTED_FILTERS
from beacon.request import RequestParams
from beacon.request.model import Granularity

LOG = logging.getLogger(__name__)


def build_meta(qparams: RequestParams, entity_schema,
               returned_granularity: Granularity):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'beaconId': conf.beacon.beacon_id,
        'apiVersion': conf.beacon.api_version,
        'returnedGranularity': returned_granularity,
        'receivedRequestSummary': qparams.summary(),
        'returnedSchemas': [entity_schema] if entity_schema is not None else []
    }
    return meta


def build_response_summary(exists, num_total_results):
    if num_total_results is None:
        return {
            'exists': exists
        }
    else:
        return {
            'exists': exists,
            'numTotalResults': num_total_results
        }


def build_response_by_dataset(data, response_dict, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""
    list_of_responses = []
    for k, v in response_dict.items():
        response = {
            'id': '',  # TODO: Set the name of the dataset/cohort
            'setType': '',  # TODO: Set the type of collection
            'exists': num_total_results > 0,
            'resultsCount': num_total_results,
            'dataset': k,
            'results': v,
            # 'info': None,
            'resultsHandover': None,  # build_results_handover
        }
        list_of_responses.append(response)

    return list_of_responses


def build_response(data, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""

    response = {
        'id': '',  # TODO: Set the name of the dataset/cohort
        'setType': '',  # TODO: Set the type of collection
        'exists': num_total_results > 0,
        'resultsCount': num_total_results,
        'results': data,
        # 'info': None,
        'resultsHandover': None,  # build_results_handover
    }

    return response


########################################
# Resultset Response
########################################
def build_beacon_resultset_response(data, num_total_results, qparams: RequestParams, func_response_type, entity_schema,
                                    unsupported_filters=None):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resultSets': [build_response(data, num_total_results, qparams, func_response_type)]
        },
        'beaconHandovers': conf.service.handovers if conf.service.handovers is not None else []
    }

    if unsupported_filters is not None and len(unsupported_filters) > 0:
        beacon_response.update({
            "info": {
                "warnings": {
                    "unsupportedFilters": unsupported_filters
                }
            }
        })
    return beacon_response


def build_beacon_resultset_response_by_dataset(data, list_of_dataset_dicts, num_total_results, qparams: RequestParams,
                                               func_response_type, entity_schema):
    """"
    Transform data into the Beacon response format.
    """
    response_dict = {}
    LOG.debug(list_of_dataset_dicts)

    for dataset_dict in list_of_dataset_dicts:
        dataset_id = dataset_dict['dataset']
        response_dict[dataset_id] = []

    for dataset_dict in list_of_dataset_dicts:
        for datas in dataset_dict['ids']:
            if isinstance(datas, str):
                dict_2 = {'id': datas}
                dataset_id = dataset_dict['dataset']
                response_dict[dataset_id] = []
                response_dict[dataset_id].append(dict_2)
                LOG.debug(response_dict)

            else:
                for doc in data:
                    LOG.debug(isinstance(doc, dict))
                    LOG.debug(doc)
                    try:
                        if doc['id'] in datas['biosampleIds']:
                            dataset_id = dataset_dict['dataset']
                            response_dict[dataset_id].append(doc)
                    except Exception:
                        pass
                LOG.debug(response_dict[dataset_id])

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resultSets': [
                build_response_by_dataset(data, response_dict, num_total_results, qparams, func_response_type)]
        },
        'beaconHandovers': conf.service.handovers if conf.service.handovers is not None else []
    }
    return beacon_response


########################################
# Count Response
########################################

def build_beacon_count_response(data, num_total_results, qparams: RequestParams, func_response_type, entity_schema):
    """
    Transform data into the Beacon response format.
    """
    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.COUNT),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resultSets': [{
                "id": "",
                "type": entity_schema['entityType'] if entity_schema is not None else None,
                "exists": num_total_results > 0,
                "resultCount": num_total_results,
                "info": {
                    "resultCountDescription": {
                        "minRange": num_total_results,
                        "maxRange": num_total_results
                    },
                    "countType": "Overall number of{0}Biosamples hosted into one or more Biobanks in BBMRI Directory".format(
                        " Individuals related to " if entity_schema['entityType'] == 'individual' else " "),

                    'warnings': {
                        'unsupported filters': _UNSUPPORTED_FILTERS
                    }
                }
            }
            ]
        },
        'beaconHandovers': conf.service.handovers if conf.service.handovers is not None else []
    }
    return beacon_response


########################################
# Boolean Response
########################################

def build_beacon_boolean_response(data, num_total_results, qparams: RequestParams, func_response_type, entity_schema):
    """"
    Transform data into the Beacon response format.
    """
    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.BOOLEAN),
        'responseSummary': build_response_summary(num_total_results > 0, None),
        # TODO: 'extendedInfo': build_extended_info(),
        'beaconHandovers': conf.service.handovers if conf.service.handovers is not None else []
    }
    return beacon_response


########################################
# Collection Response
########################################

def build_beacon_collection_response(data, num_total_results, qparams: RequestParams, func_response_type,
                                     entity_schema, unsupported_filters=None):
    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'info': build_extended_info(),
        'beaconHandovers': conf.service.handovers if conf.service.handovers is not None else [],
        'response': {
            'collections': func_response_type(data, qparams)
        }
    }

    if unsupported_filters is not None and len(unsupported_filters) > 0:
        beacon_response.update({
            "info": {
                "warnings": {
                    "unsupportedFilters": unsupported_filters
                }
            }
        })

    return beacon_response


########################################
# Info Response
########################################

def build_beacon_info_response(qparams):
    beacon_response = {
        'meta': build_meta(qparams, None, Granularity.RECORD),
        'response': {
            'id': conf.beacon.beacon_id,
            'name': conf.beacon.beacon_name,
            'apiVersion': conf.beacon.api_version,
            'environment': conf.service.environment,
            'organization': {
                'id': conf.organization.id,
                'name': conf.organization.name,
                'description': conf.organization.description,
                'address': conf.organization.address,
                'welcomeUrl': conf.organization.welcome_url,
                'contactUrl': conf.organization.contact_url,
                'logoUrl': conf.organization.logo_url,
            },
            'description': conf.project.description,
            'version': conf.project.version,
            'welcomeUrl': conf.project.welcome_url,
            'alternativeUrl': conf.project.alternative_url,
            'createDateTime': conf.project.create_datetime,
            'updateDateTime': conf.project.update_datetime
        }
    }

    return beacon_response


########################################
# Service Info Response
########################################

def build_beacon_service_info_response():
    beacon_response = {
        'id': conf.beacon.beacon_id,
        'name': conf.beacon.beacon_name,
        'environment': conf.service.environment,
        'description': conf.project.description,
        'type': {
            'group': conf.ga4gh.service_type_group,
            'artifact': conf.ga4gh.service_type_artifact,
            'version': conf.ga4gh.service_type_version
        },
        'organization': {
            'name': conf.organization.name,
            'url': conf.organization.welcome_url
        },
        'contactUrl': conf.organization.contact_url,
        'documentationUrl': conf.service.documentation_url,
        'createdAt': conf.project.create_datetime,
        'updatedAt': conf.project.update_datetime,
        'version': conf.project.version
    }

    return beacon_response


########################################
# Filtering terms Response
########################################

def build_filtering_terms_response(data, num_total_results, qparams: RequestParams, func_response_type, entity_schema):
    """"
    Transform data into the Beacon response format.
    """
    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resources': data['resources'],
            'filteringTerms': data['filteringTerms']
        },
        'beaconHandovers': conf.service.handovers if conf.service.handovers is not None else []
    }
    return beacon_response


########################################
# Error Response
########################################

def build_error(non_accessible_datasets):
    """"
    Fills the `error` part in the response.
    This error only applies to partial errors which do not prevent the Beacon from answering.
    """

    message = f'You are not authorized to access some of the requested datasets: {non_accessible_datasets}'

    return {
        'error': {
            'errorCode': 401,
            'errorMessage': message
        }
    }
