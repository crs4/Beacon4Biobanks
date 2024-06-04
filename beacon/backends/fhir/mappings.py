"""
Filtering terms to support for biosamples:

Diagnosis: (Ontology) Orphanet or ICD and it queries "Sample content diagnosis" field of the Specimen resource
Sex: Decide whether to use ontology or alphanumeric as for the individuals
    - (Ontology) using (ncit:C16576, ncit:C20197, ncit:C124294, ncit:C17998)
    - Alphanumeric: in this case the id would be ncit:C28421
Specimen type: (Alphanumeric) id = ncit:C70713 and values taken from MIABIS
Age at diagnosis: (Alphanumeric) id = ncit:C156420, operator and value
"""

import logging

from beacon import conf

_PREFIXES_TO_EXTENDED = {
    'FastingStatus': 'http://terminology.hl7.org/CodeSystem/v2-0916',
    'SampleMaterialType': 'https://fhir.bbmri.de/CodeSystem/SampleMaterialType',
    'icd10': 'http://hl7.org/fhir/sid/icd-10',
    'icd10gm': 'http://fhir.de/CodeSystem/dimdi/icd-10-gm',
    'loinc': 'http://loinc.org',
    'ordo': 'http://www.orpha.net/ORDO/',
    'uberon': 'http://purl.obolibrary.org/obo/uberon.owl',
    'StorageTemperature': 'https://fhir.bbmri.de/CodeSystem/StorageTemperature',
    'icd-o-3': 'urn:oid:2.16.840.1.113883.6.43.1'
}

_EXTENDED_TO_PREFIXES = {v: k for k, v in _PREFIXES_TO_EXTENDED.items()}

_FILTERS = [{
    'id': 'icd10',
    'type': 'ontology',
    'label': 'Disease using an icd10 code (e.g., icd10:G18.0)',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'ordo',
    'type': 'ontology',
    'label': 'Disease using an orphanet code (e.g., ordo:Orphanet_589)',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'ncit:C28421',
    'type': 'alphanumeric',
    'label': 'Sex',
    'scopes': ['biosamples', 'individuals'],
    'allowed_values': [
        'ncit:C16576',  # Female
        'ncit:C20197',  # Male
        'ncit:C124294',
        'ncit:C17998',
    ]
}, {
    'id': 'ncit:C156420',
    'type': 'alphanumeric',
    'label': 'Age at diagnosis',
    'scopes': ['biosample', 'individual']
}, {
    'id': 'ncit:C83164',
    'type': 'alphanumeric',
    'label': 'Year of birth',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'ncit:C70713',
    'type': 'alphanumeric',
    'label': 'Biospecimen type',
    'allowed_values': [
        'obi:0000655',  # (blood specimen)
        'obi:0002512',  # (bone marrow)
        'obib:0000036',  # (buffy coat)
        'cl:2000001',  # (peripheral blood mononuclear cell)
        'obi:0100016',  # (blood plasma specime)
        'obi:0100017',  # (blood serum)
        'uberon:0007795',  # (ascites fluid)
        'obi:0002502',  # (cerebrospinal fluid)
        'obi:0002507',  # (saliva)
        'obi:0002503',  # (feces)
        'obi:0000651',  # (urine)
        'obi:0002599',  # (swab)
        'obi:2000009',  # (bodily fluid specimen)
        'obi:1200000',  # (FFPE specimen)
        'obi:0000922',  # (frozen specimen)
        'obi:0001472',  # (specimen with known storage state)
        'obi:0001051',  # (DNA extract)
        'obi:0000880',  # (RNA extract)
        'obi:0001479',  # (specimen from organism)
    ],
    'scopes': ['biosamples', 'individuals']
}]

_UNSUPPORTED_FILTERS = [
    'sio:SIO_010056',
    'edam:data_2295',
    'ncit:C124353'
]

_FILTERS_TO_CQL = {
    'icd10': {
        'cql_parameter_class': 'diagnosis',
        'type': 'ontology',
        'extension': ''
    },
    'ordo': {
        'cql_parameter_class': 'diagnosis',
        'type': 'ontology',
        'extension': ''
    },
    'ncit:C28421': {
        'cql_parameter_class': 'sex',
        'type': 'alphanumeric',
        'extension': '',
        'values_mapper': lambda v: {
            'ncit:C16576': 'female',  # female
            'ncit:C20197': 'male',  # male
            'ncit:C124294': 'other',  # undetermined
            'ncit:C17998': 'unknown',  # other
        }[v]
    },
    'ncit:C156420': {
        'cql_parameter_class': 'age_at_diagnosis',
        'type': 'alphanumeric',
        'values_mapper': lambda v: v
    },
    'ncit:C83164': {
        'cql_parameter_class': 'year_of_birth',
        'type': 'alphanumeric',
        'values_mapper': lambda v: v
    },
    'ncit:C70713': {
        'cql_parameter_class': 'sample_type',
        'type': 'alphanumeric',
        'fhir_codesystem': 'SampleMaterialType',
        'values_mapper': lambda v: {
            'obi:0000655': ['whole-blood', 'dried-whole-blood'],  # (blood specimen)
            'obi:0002512': 'bone-marrow',  # (bone marrow)
            'obib:0000036': 'buffy-coat',  # (buffy coat)
            'cl:2000001': 'peripheral-blood-cells-vital',  # (peripheral blood mononuclear cell)
            'obi:0100016': ['blood-plasma', 'plasma-edta', 'plasma-citrat', 'plasma-heparin', 'plasma-cell-free',
                            'plasma-other'],  # (blood plasma specimen)
            'obi:0100017': 'blood-serum',  # (blood serum)
            'uberon:0007795': 'ascites',  # (ascites fluid)
            'obi:0002502': 'csf-liquor',  # (cerebrospinal fluid)
            'obi:0002507': 'saliva',  # (saliva)
            'obi:0002503': 'stool-faeces',  # (feces)
            'obi:0000651': 'urine',  # (urine)
            'obi:0002599': 'swab',  # (swab)
            'obi:2000009': 'liquid-other',  # (bodily fluid specimen)
            'obi:1200000': ['tissue-ffpe', 'tumor-tissue-ffpe', 'normal-tissue-ffpe', 'other-tissue-ffpe'],
            # (FFPE specimen)
            'obi:0000922': ['tissue-frozen', 'tumor-tissue-frozen', 'normal-tissue-frozen', 'other-tissue-frozen'],
            'obi:0001472': 'tissue-other',  # (specimen with known storage state)
            'obi:0001051': ['dna', 'cf-dna', 'g-dna'],  # (DNA extract)
            'obi:0000880': 'rna',  # (RNA extract)
            'obi:0001479': 'derivative-other',  # (specimen from organism)
        }[v]
    }
}

_FHIR_EXTENSIONS_TO_BEACON = {
    'https://fhir.bbmri.de/StructureDefinition/StorageTemperature': 'measurements',
    'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis': 'histologicalDiagnosis',
    # 'https://fhir.bbmri.de/StructureDefinition/Custodian': 'custodian'
}

if conf.service.legacy_filters_enabled:
    _FILTERS.extend([{
        "Orphanet_": {  # legacy filter for Orphanet code for to support old vp api spec
            "type": "custom",
            "attribute": "diagnosis_available",
            "label": "Disease using an orphanet code (e.g., Orphanet_589)",
            "scopes": ["biosamples", "individuals"]
        }}
    ])

    _FILTERS_TO_CQL.update({
        'Orphanet_': {
            'cql_parameter_class': 'diagnosis',
            'type': 'custom',
            'fhir_codesystem': 'ordo',
            'extension': ''
        },
        'NCIT_C28421': {
            'cql_parameter_class': 'sex',
            'type': 'alphanumeric',
            'extension': '',
            'values_mapper': lambda v: {
                'NCIT_C16576': 'female',  # female
                'NCIT_C20197': 'male',  # male
                'NCIT_C124294': 'other',  # undetermined
                'NCIT_C17998': 'unknown',  # other
            }[v]
        },
        'NCIT_C156420': {
            'cql_parameter_class': 'age_at_diagnosis',
            'type': 'alphanumeric',
            'values_mapper': lambda v: v
        },
        'NCIT_C83164': {
            'cql_parameter_class': 'year_of_birth',
            'type': 'alphanumeric',
            'values_mapper': lambda v: v
        },
    })


def get_codesystem_prefix(extended):
    LOG = logging.getLogger(__name__)
    LOG.debug("requiring_code: %s", extended)
    return _EXTENDED_TO_PREFIXES[extended]


def get_filters():
    return _FILTERS


def get_unsupported_filters():
    return _UNSUPPORTED_FILTERS


def get_cql_condition_arguments_from_beacon_filter(beacon_filter, unsupported_filters):
    try:
        return _FILTERS_TO_CQL[beacon_filter]
    except KeyError:
        if beacon_filter not in unsupported_filters:
            unsupported_filters.append(beacon_filter)
        raise KeyError


def get_beacon_code_from_fhir_extension(extension):
    return _FHIR_EXTENSIONS_TO_BEACON[extension]
