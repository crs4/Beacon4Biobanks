from beacon.backends.molgenis.utils import get_collection_uri

def _is_ordo_code(disease_code):
    return disease_code.startswith('ORPHA')

def _convert_ordo_code(disease_code):
    return f'ordo:Orphanet_{disease_code.split(":")[1]}'

def _map_eprd_v_2_0_0(record):
    """
    Maps a Collection result coming from the directory to the output dataset model
    """
    return {
        '@context': 'https://raw.githubusercontent.com/ejp-rd-vp/vp-api-specs/main/json-ld-contexts/ejprd-context.json',
        '@id': record['id'],
        '@type': ["obo:OBIB_0000616", "ejprd:Biobank"],
        'title': f'{record["biobank"]["name"]} - {record["name"]}',
        'description': record['description'] if 'description' in record else '',
        'landingPage': get_collection_uri(record['id']),
        'theme': [_convert_ordo_code(disease['id']) for disease in record['diagnosis_available'] if _is_ordo_code(disease['id'])],
        'personalData': True,
        'publisher': {
            '@id': f'http://hdl.handle.net/{record["biobank"]["pid"]}',
            '@type': ['foaf:Organization', 'obo:OBIB_0000623'],
            'title': record["biobank"]["name"],
            'description': record["biobank"]["description"] if "description" in record else None,
            "spatial": {
                "name": record["biobank"]["country"]["name"]
            }
        }
    }


def _map_eprd_v1_0_0(record):
    """
    Maps a Collection result coming from the directory to the output dataset model
    """
    return {
        'id': record['id'],
        'name': f'{record["biobank"]["name"]} - {record["name"]}',
        'description': record['description'] if 'description' in record else '',
        'type': 'BiobankDataset',
        'homepage': get_collection_uri(record['id']),
        'location': {
            'id': record['biobank']['country']['id'],
            'country': record['biobank']['country']['name']
        }
    }


def map_resource(schema_name):
    def mapper(record):
        if schema_name == "ejprd-resources-v1.0.0":
            return _map_eprd_v1_0_0(record)
        else:
            return _map_eprd_v_2_0_0(record)
    return mapper
