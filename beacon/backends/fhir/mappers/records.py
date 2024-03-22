"""
Mapper for ejprd project. It will convert FHIR Resources from the Sample Locator to models compliant with the EJPRD
project
"""
from beacon.backends.fhir.mappings import get_beacon_code_from_fhir_extension, get_codesystem_prefix


def map_dataset(orgs_resources):
    """
    Maps an Organization FHIR resource describing a Collection the model of datasets
    """

    description_extension = "https://fhir.bbmri.de/StructureDefinition/OrganizationDescription"
    description = ""
    for d in orgs_resources["extension"]:
        if d["url"] == description_extension:
            description = d["valueString"]

    identifier = orgs_resources["id"]

    return {
        "_id": identifier,
        "id": identifier,
        "name": orgs_resources["name"],
        "description": description,
        "type": ["BiobankDataset"],
        "externalUrl": "",
        "organization": [
            orgs_resources['partOf']['name']
        ],
        "createDateTime": "",
        "updateDateTime": "",
    }


def map_biosamples(biosamples_resources):
    """
    Reads FHIR specimen resources and creates biosamples documents, having the same structures as the
    documents get from the mongodb endpoint
    """
    docs = []
    for entry in biosamples_resources['entry']:
        resource = entry['resource']
        doc = {
            'id': resource['identifier'][0]['value'],
            # TODO: At the moment the biosampleStatus is static: check if we can infer different values from incoming information
            "biosampleStatus": {
                "id": "EFO:0009654",
                "label": "reference sample"
            },
            # TODO: Same as above
            "sampleOriginType": {
                "id": "OBI:0001479",
                "label": "specimen from organism"
            },
            "sampleOriginDetail": [
                _get_beacon_ontology_field(c) for c in resource['collection']['bodySite']['coding']
            ]
        }
        # if 'collectedDateTime' in resource['collection']:
        #     doc['collectionDate'] = resource['collection']['collectedDateTime']

        beacon_spec_info = get_beacon_specimen_info_from_fhir_extension(resource['extension'])

        doc.update(beacon_spec_info)
        docs.append(doc)
    return docs


def get_beacon_specimen_info_from_fhir_extension(fhir_extensions):
    beacon_spec_info = dict()
    for extension in fhir_extensions:
        try:
            beacon_field = get_beacon_code_from_fhir_extension(extension["url"])
        except KeyError:
            pass
        else:
            if 'valueCodeableConcept' in extension:
                codes = extension["valueCodeableConcept"]["coding"]
                beacon_spec_info[beacon_field] = \
                    [_get_beacon_ontology_field(c) for c in codes]
            elif 'valueReference' in extension:
                beacon_spec_info[get_beacon_code_from_fhir_extension(extension["url"])] = \
                    f'{extension["valueReference"]["reference"]}'

    return beacon_spec_info


def _get_beacon_ontology_field(fhir_code):
    field = {'id': f'{get_codesystem_prefix(fhir_code["system"])}:{fhir_code["code"]}'}
    try:
        field.update({'label': fhir_code['display']})
    except KeyError:
        pass
    return field


def map_individuals(patient_resources):
    return patient_resources
