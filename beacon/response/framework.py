"""
Beacon Framework Configuration Endpoints.
"""
from aiohttp import web

from beacon import conf
from beacon.schemas import get_entry_types


async def configuration(request):
    meta = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/sections/beaconInformationalResponseMeta.json',
        'beaconId': conf.beacon.beacon_id,
        'apiVersion': conf.beacon.api_version,
        'returnedSchemas': []
    }

    response = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/configuration/beaconConfigurationSchema.json',
        'maturityAttributes': {
            'productionStatus': 'DEV'
        },
        'securityAttributes': {
            'defaultGranularity': 'record',
            'securityLevels': ['PUBLIC', 'REGISTERED', 'CONTROLLED']
        },
        'entryTypes': get_entry_types()
    }

    configuration_json = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconConfigurationResponse.json',
        'meta': meta,
        'response': response
    }

    return web.json_response(configuration_json)


async def entry_types(request):
    meta = {
        'beaconId': conf.beacon.beacon_id,
        'apiVersion': conf.beacon.api_version,
        'returnedSchemas': []
    }

    response = {
        "entryTypes": get_entry_types()
    }

    entry_types_json = {
        'meta': meta,
        'response': response
    }

    return web.json_response(entry_types_json)


async def beacon_map(request):
    meta = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/sections/beaconInformationalResponseMeta.json',
        'beaconId': conf.beacon.beacon_id,
        'apiVersion': conf.beacon.api_version,
        'returnedSchemas': []
    }
    endpointSets = {
        "analysis": {
            "entryType": "analysis",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/analyses/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}analyses",
            "singleEntryUrl": f"{conf.beacon.uri}analyses/{{id}}",
            "endpoints": {
                "genomicVariation": {
                    "returnedEntryType": "genomicVariation",
                    "url": f"{conf.beacon.uri}analyses/{{id}}/g_variants"
                },
            }
        },
        "biosample": {
            "entryType": "biosample",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/biosamples/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}biosamples",
            "singleEntryUrl": f"{conf.beacon.uri}biosamples/{{id}}",
            "endpoints": {
                "analysis": {
                    "returnedEntryType": "analysis",
                    "url": f"{conf.beacon.uri}biosamples/{{id}}/analyses"
                },
                "genomicVariation": {
                    "returnedEntryType": "genomicVariation",
                    "url": f"{conf.beacon.uri}biosamples/{id}/g_variants"
                },
                "run": {
                    "returnedEntryType": "run",
                    "url": f"{conf.beacon.uri}biosamples/{id}/runs"
                },
            }
        },
        "cohort": {
            "entryType": "cohort",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/cohorts/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}cohorts",
            "singleEntryUrl": f"{conf.beacon.uri}cohorts/{{id}}",
            "filteringTermsUrl": f"{conf.beacon.uri}filtering_terms/cohorts",
            "endpoints": {
                "analysis": {
                    "returnedEntryType": "analysis",
                    "url": f"{conf.beacon.uri}cohorts/{id}/analyses"
                },
                "individual": {
                    "returnedEntryType": "individual",
                    "url": f"{conf.beacon.uri}cohorts/{id}/individuals"
                },
                "run": {
                    "returnedEntryType": "run",
                    "url": f"{conf.beacon.uri}cohorts/{id}/runs"
                }
            }
        },
        "dataset": {
            "entryType": "dataset",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/datasets/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}datasets",
            "singleEntryUrl": f"{conf.beacon.uri}datasets/{{id}}",
            "filteringTermsUrl": f"{conf.beacon.uri}filtering_terms/datasets",
            "endpoints": {
                "analysis": {
                    "returnedEntryType": "analysis",
                    "url": f"{conf.beacon.uri}datasets/{id}/analyses"
                },
                "biosample": {
                    "returnedEntryType": "biosample",
                    "url": f"{conf.beacon.uri}datasets/{id}/biosamples"
                },
                "genomicVariation": {
                    "returnedEntryType": "genomicVariation",
                    "url": f"{conf.beacon.uri}datasets/{id}/g_variants"
                },
                "individual": {
                    "returnedEntryType": "individual",
                    "url": f"{conf.beacon.uri}datasets/{id}/individuals"
                },
                "run": {
                    "returnedEntryType": "run",
                    "url": f"{conf.beacon.uri}datasets/{id}/runs"
                }
            }
        },
        "genomicVariation": {
            "entryType": "genomicVariation",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/genomicVariations/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}g_variants",
            "singleEntryUrl": f"{conf.beacon.uri}g_variants/{id}",
            "endpoints": {
                "analysis": {
                    "returnedEntryType": "analysis",
                    "url": f"{conf.beacon.uri}g_variants/{{id}}/analyses"
                },
                "biosample": {
                    "returnedEntryType": "biosample",
                    "url": f"{conf.beacon.uri}g_variants/{{id}}/biosamples"
                },
                "individual": {
                    "returnedEntryType": "individual",
                    "url": f"{conf.beacon.uri}g_variants/{{id}}/individuals"
                },
                "run": {
                    "returnedEntryType": "run",
                    "url": f"{conf.beacon.uri}g_variants/{{id}}/runs"
                }
            }
        },
        "individual": {
            "entryType": "individual",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/individuals/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}individuals",
            "singleEntryUrl": f"{conf.beacon.uri}individuals/{{id}}",
            "filteringTermsUrl": f"{conf.beacon.uri}filtering_terms/individuals",
            "endpoints": {
                "analysis": {
                    "returnedEntryType": "analysis",
                    "url": f"{conf.beacon.uri}individuals/{{id}}/analyses"
                },
                "biosample": {
                    "returnedEntryType": "biosample",
                    "url": f"{conf.beacon.uri}individuals/{{id}}/biosamples"
                },
                "genomicVariation": {
                    "returnedEntryType": "genomicVariation",
                    "url": f"{conf.beacon.uri}individuals/{{id}}/g_variants"
                },
                "run": {
                    "returnedEntryType": "run",
                    "url": f"{conf.beacon.uri}individuals/{{id}}/runs"
                }
            }
        },
        "run": {
            "entryType": "run",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/runs/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}runs",
            "singleEntryUrl": f"{conf.beacon.uri}runs/{{id}}",
            "endpoints": {
                "analysis": {
                    "returnedEntryType": "analysis",
                    "url": f"{conf.beacon.uri}runs/{{id}}/analyses"
                },
                "genomicVariation": {
                    "returnedEntryType": "genomicVariation",
                    "url": f"{conf.beacon.uri}runs/{{id}}/g_variants"
                },
            }
        },
        "resource": {
            "entryType": "resource",
            "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/runs/endpoints.json",
            "rootUrl": f"{conf.beacon.uri}catalogs",
            "singleEntryUrl": f"{conf.beacon.uri}catalogs/{{id}}",
            "endpoints": {
            }
        }
    }
    response = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/configuration/beaconMapSchema.json',
        "endpointSets": {k: v for k, v in endpointSets.items() if k in get_entry_types()}
    }

    beacon_map_json = {
        'meta': meta,
        'response': response
    }

    return web.json_response(beacon_map_json)
