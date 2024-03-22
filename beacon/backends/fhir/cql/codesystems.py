FHIR_CODE_SYSTEMS = {
    'FastingStatus': 'http://terminology.hl7.org/CodeSystem/v2-0916',
    'SampleMaterialType': 'https://fhir.bbmri.de/CodeSystem/SampleMaterialType',
    'icd10': 'http://hl7.org/fhir/sid/icd-10',
    'icd10gm': 'http://fhir.de/CodeSystem/dimdi/icd-10-gm',
    'loinc': 'http://loinc.org',
    'ordo': 'http://www.orpha.net/ORDO/',
    'uberon': 'http://purl.obolibrary.org/obo/uberon.owl',
    'StorageTemperature': 'https://fhir.bbmri.de/CodeSystem/StorageTemperature'
}

FHIR_CODE_SYSTEMS_INV = {v: k for k, v in FHIR_CODE_SYSTEMS.items()}

FHIR_EXTENSIONS = {
    'StorageTemperature': 'https://fhir.bbmri.de/StructureDefinition/StorageTemperature',
    'Diagnosis': 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis',
    'Custodian': 'https://fhir.bbmri.de/StructureDefinition/Custodian'
}
