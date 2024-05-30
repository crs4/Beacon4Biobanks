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

from aiohttp.web_exceptions import HTTPBadRequest

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
        'OBI_0000655',  # (blood specimen)
        'OBI_0002512',  # (bone marrow)
        'OBIB_0000036',  # (buffy coat)
        'CL_2000001',  # (peripheral blood mononuclear cell)
        'OBI_0100016',  # (blood plasma specime)
        'OBI_0100017',  # (blood serum)
        'UBERON_0007795',  # (ascites fluid)
        'OBI_0002502',  # (cerebrospinal fluid)
        'OBI_0002507',  # (saliva)
        'OBI_0002503',  # (feces)
        'OBI_0000651',  # (urine)
        'OBI_0002599',  # (swab)
        'OBI_2000009',  # (bodily fluid specimen)
        'OBI_1200000',  # (FFPE specimen)
        'OBI_0000922',  # (frozen specimen)
        'OBI_0001472',  # (specimen with known storage state)
        'OBI_0001051',  # (DNA extract)
        'OBI_0000880',  # (RNA extract)
        'OBI_0001479',  # (specimen from organism)
    ],
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'whole-blood',
    'label': 'Whole blood',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']

}, {
    'id': 'bone-marrow',
    'label': 'Bone marrow',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'buffy-coat',
    'label': 'Buffy-Coat',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'dried-whole-blood',
    'label': 'Dried whole blood',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'peripheral-blood-cells-vital',
    'label': 'Peripheral blood mononuclear cells (PBMCs, viable)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'blood-plasma',
    'label': 'Plasma',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'plasma-edta',
    'label': 'Plasma, EDTA',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'plasma-citrat',
    'label': 'Plasma, Citrat',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'plasma-heparin',
    'label': 'Plasma, Heparin',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'plasma-cell-free',
    'label': 'Plasma, cell free',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'plasma-other',
    'label': 'Plasma, other',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'blood-serum',
    'label': 'Serum',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'ascites',
    'label': 'Ascites',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'csf-liquor',
    'label': 'CSF/Liquor',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'saliva',
    'label': 'Saliva',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'stool-faeces',
    'label': 'Stool/Faeces',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'urine',
    'label': 'Urine',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'swab',
    'label': 'Swab',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'liquid-other',
    'label': 'Other liquid biosample/storage',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'tissue-ffpe',
    'label': 'Tissue FFPE',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'tumor-tissue-ffpe',
    'label': 'Tumor tissue (FFPE)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'normal-tissue-ffpe',
    'label': 'Normal tissue (FFPE)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'other-tissue-ffpe',
    'label': 'Other tissue (FFPE)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'tissue-frozen',
    'label': 'Tissue frozen',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'tumor-tissue-frozen',
    'label': 'Tumor tissue (frozen)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'normal-tissue-frozen',
    'label': 'Normal tissue (frozen)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'other-tissue-frozen',
    'label': 'Other tissue (frozen)',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'tissue-other',
    'label': 'Other tissue storage',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'dna',
    'label': 'DNA',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'cf-dna',
    'label': 'cfDNA',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'g-dna',
    'label': 'gDNA',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'rna',
    'label': 'RNA',
    'type': 'custom',
    'scopes': ['biosamples', 'individuals']
}, {
    'id': 'derivative-other',
    'label': 'Other derivative',
    'type': 'custom',
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
            'OBI_0000655': ['whole-blood', 'dried-whole-blood'],  # (blood specimen)
            'OBI_0002512': 'bone-marrow',  # (bone marrow)
            'OBIB_0000036': 'buffy-coat',  # (buffy coat)
            'CL_2000001': 'peripheral-blood-cells-vital',  # (peripheral blood mononuclear cell)
            'OBI_0100016': ['blood-plasma', 'plasma-edta', 'plasma-citrat', 'plasma-heparin', 'plasma-cell-free',
                            'plasma-other'],  # (blood plasma specimen)
            'OBI_0100017': 'blood-serum',  # (blood serum)
            'UBERON_0007795': 'ascites',  # (ascites fluid)
            'OBI_0002502': 'csf-liquor',  # (cerebrospinal fluid)
            'OBI_0002507': 'saliva',  # (saliva)
            'OBI_0002503': 'stool-faeces',  # (feces)
            'OBI_0000651': 'urine',  # (urine)
            'OBI_0002599': 'swab',  # (swab)
            'OBI_2000009': 'liquid-other',  # (bodily fluid specimen)
            'OBI_1200000': ['tissue-ffpe', 'tumor-tissue-ffpe', 'normal-tissue-ffpe', 'other-tissue-ffpe'],
            # (FFPE specimen)
            'OBI_0000922': ['tissue-frozen', 'tumor-tissue-frozen', 'normal-tissue-frozen', 'other-tissue-frozen'],
            'OBI_0001472': 'tissue-other',  # (specimen with known storage state)
            'OBI_0001051': ['dna', 'cf-dna', 'g-dna'],  # (DNA extract)
            'OBI_0000880': 'rna',  # (RNA extract)
            'OBI_0001479': 'derivative-other',  # (specimen from organism)
        }[v]
    }
}

_FHIR_EXTENSIONS_TO_BEACON = {
    'https://fhir.bbmri.de/StructureDefinition/StorageTemperature': 'measurements',
    'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis': 'histologicalDiagnosis',
    # 'https://fhir.bbmri.de/StructureDefinition/Custodian': 'custodian'
}


def get_codesystem_prefix(extended):
    LOG = logging.getLogger(__name__)
    LOG.debug("requiring_code: %s", extended)
    return _EXTENDED_TO_PREFIXES[extended]


def get_filters():
    return _FILTERS


def get_unsupported_filters():
    return _UNSUPPORTED_FILTERS


def get_cql_condition_arguments_from_beacon_filter(beacon_filter):
    try:
        return _FILTERS_TO_CQL[beacon_filter]
    except KeyError:
        raise HTTPBadRequest(text="Filter not supported")


def get_beacon_code_from_fhir_extension(extension):
    return _FHIR_EXTENSIONS_TO_BEACON[extension]
