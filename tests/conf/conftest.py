import pytest

from beacon.backends.fhir.cql.parameters import DiagnosisBiosamples, DiagnosisIndividuals, SampleType, SexBiosample, \
    SexIndividual
from beacon.request.model import Operator


@pytest.fixture(scope='session', autouse=True)
def single_disease_biosample_parameter():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo', 'extension': ''}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)))"}


@pytest.fixture(scope='session', autouse=True)
def multiple_diseases_biosample_parameter():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo', 'extension': ''},
                    {'code': 'Orphanet_457260', 'code_system': 'ordo', 'extension': ''}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)) or exists(from Specimen.extension E where \
E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' and (ordo.id in E.value.coding.system and \
'Orphanet_457260' in E.value.coding.code)))"}


@pytest.fixture(scope='session', autouse=True)
def multiple_diseases_biosample_parameter_miscellaneous_type():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo', 'extension': ''},
                    {'code': 'Orphanet_457260', 'code_system': 'ordo'}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)) or exists(from Specimen.extension E where \
E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' and (ordo.id in E.value.coding.system and \
'Orphanet_457260' in E.value.coding.code)))"}


@pytest.fixture(scope='session', autouse=True)
def multiple_disease_individual_parameter():
    p = DiagnosisIndividuals()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo'}, {'code': 'Orphanet_457260', 'code_system': 'ordo'}]
    return {'parameter': p,
            'expected_cql': '(exists([Patient -> Condition: Code \'Orphanet_166\' from ordo ]) or exists([Patient -> Condition: Code \'Orphanet_457260\' from ordo ]))'}


@pytest.fixture(scope='session', autouse=True)
def single_disease_individual_parameter():
    p = DiagnosisIndividuals()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo'}]
    return {'parameter': p,
            'expected_cql': '(exists([Patient -> Condition: Code \'Orphanet_166\' from ordo ]))'}


@pytest.fixture(scope='session', autouse=True)
def single_sample_type_parameter():
    p = SampleType()
    p.conditions = [{'operator': Operator.EQUAL, 'value': 'bone-marrow'}]
    return {'parameter': p,
            'expected_cql': '(exists(from [Specimen] S where S.type.coding contains Code \'bone-marrow\' from SampleMaterialType))'
            }


@pytest.fixture(scope='session', autouse=True)
def multiple_sample_type_parameter():
    p = SampleType()
    p.conditions = [{'operator': Operator.EQUAL, 'value': 'whole-blood'},
                    {'operator': Operator.EQUAL, 'value': 'dried-whole-blood'}]
    return {'parameter': p,
            'expected_cql': '(exists(from [Specimen] S where S.type.coding contains Code \'whole-blood\' from SampleMaterialType) or exists(from [Specimen] S where S.type.coding contains Code \'dried-whole-blood\' from SampleMaterialType))'
            }


@pytest.fixture(scope='session', autouse=True)
def single_sex_biosample_parameter():
    p = SexBiosample()
    p.conditions = [{'operator': Operator.EQUAL, 'value': 'female'}]
    return {'parameter': p,
            'expected_cql': '(exists from [Patient] P where (P.gender = \'female\'))'
            }


@pytest.fixture(scope='session', autouse=True)
def multiple_sex_biosample_parameter():
    p = SexBiosample()
    p.conditions = [{'operator': Operator.EQUAL, 'value': 'female'}, {'operator': Operator.EQUAL, 'value': 'male'}]
    return {'parameter': p,
            'expected_cql': '(exists from [Patient] P where (P.gender = \'female\' or P.gender = \'male\'))'
            }


@pytest.fixture(scope='session', autouse=True)
def single_sex_individual_parameter():
    p = SexIndividual()
    p.conditions = [{'operator': Operator.EQUAL, 'value': 'female'}]
    return {'parameter': p,
            'expected_cql': '(Patient.gender = \'female\')'
            }


@pytest.fixture
def multiple_sex_individual_parameter():
    p = SexIndividual()
    p.conditions = [{'operator': Operator.EQUAL, 'value': 'female'}, {'operator': Operator.EQUAL, 'value': 'male'}]
    return {'parameter': p,
            'expected_cql': '(Patient.gender = \'female\' or Patient.gender = \'male\')'
            }


@pytest.fixture(scope='session', autouse=True)
def single_disease_biosample_parameter_as_custom():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo'}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)))"}


@pytest.fixture(scope='session', autouse=True)
def multiple_diseases_biosample_parameter_as_custom():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo'},
                    {'code': 'Orphanet_457260', 'code_system': 'ordo'}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)) or exists(from Specimen.extension E where \
E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' and (ordo.id in E.value.coding.system and \
'Orphanet_457260' in E.value.coding.code)))"}


@pytest.fixture(scope='session', autouse=True)
def disease_single_filter():
    return {
        "meta": {
            "apiVersion": "v2.0"
        },
        "query": {
            "filters": [
                {"id": ["Orphanet_166"]}
            ]
            , "requestedGranularity": "count"
        }
    }


@pytest.fixture(scope='session', autouse=True)
def not_supported_filter():
    return {
        "meta": {
            "apiVersion": "v2.0"
        },
        "query": {
            "filters": [
                {"id": ["Xxx_xxx"]}
            ]
            , "requestedGranularity": "count"
        }
    }


@pytest.fixture(scope='session', autouse=True)
def empty_filter():
    return {
        "meta": {
            "apiVersion": "v2.0"
        },
        "query": {
            "filters": [

            ]
            , "requestedGranularity": "count"
        }
    }


@pytest.fixture(scope='session', autouse=True)
def disease_v4_and_v3_specs_filter():
    return {
        "meta": {
            "apiVersion": "v2.0"
        },
        "query": {
            "filters": [
                {
                    "id": ["ordo:Orphanet_166"]}, {
                    "id": ["Orphanet_457260"]}]
            , "requestedGranularity": "count"
        }
    }


@pytest.fixture(scope='session', autouse=True)
def sex_filter():
    return {
        "meta": {
            "apiVersion": "2.0",
            "requestedGranularity": "count"
        },
        "query": {
            "filters": [{
                "id": "ncit:C28421",
                "operator": "=",
                "value": ["ncit:C16576", "ncit:C20197"]
            }]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def specimen_type_multiple_internal_transcoding_filter():
    return {
        "meta": {
            "apiVersion": "2.0",
            "requestedGranularity": "count"
        },
        "query": {
            "filters": [{
                "id": "ncit:C70713",
                "operator": "=",
                "value": ["obi:0000655"]
            }]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def specimen_type_multiple_values_filter():
    return {
        "meta": {
            "apiVersion": "2.0",
            "requestedGranularity": "count"
        },
        "query": {
            "filters": [{
                "id": "ncit:C70713",
                "operator": "=",
                "value": ["obi:0002512", "obi:0000036"]
            }]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def phenotype_filter():
    return {
        "meta": {
            "apiVersion": "2.0",
            "requestedGranularity": "count"
        },
        "query": {
            "filters": [{
                "id": "sio:SIO_010056",
                "operator": "=",
                "value": "hp:0001251"
            }]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def multiple_values_both_supported_and_unsupported_filter():
    return {
        "meta": {
            "apiVersion": "v0.2"
        },
        "query": {
            "filters": [
                {
                    "id": [
                        "Orphanet_2593",
                        "ordo:Orphanet_2594"
                    ]
                },
                {
                    "id": "NCIT_C28421",
                    "operator": "=",
                    "value": [
                        "NCIT_C16576",
                        "NCIT_C20197",
                        "NCIT_C124294",
                        "NCIT_C17998"
                    ]
                },
                {
                    "id": "NCIT_C83164",
                    "operator": ">=",
                    "value": "0"
                },
                {
                    "id": "NCIT_C83164",
                    "operator": "<=",
                    "value": "100"
                },
                {
                    "id": "NCIT_C124353",
                    "operator": ">=",
                    "value": "0"
                },
                {
                    "id": "NCIT_C124353",
                    "operator": "<=",
                    "value": "100"
                },
                {
                    "id": "NCIT_C156420",
                    "operator": ">=",
                    "value": "0"
                },
                {
                    "id": "NCIT_C156420",
                    "operator": "<=",
                    "value": "100"
                }
            ]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def age_this_year_filter():
    return {
        "meta": {
            "apiVersion": "v0.2"
        },
        "query": {
            "filters": [
                {
                    "id": "ncit:C83164",
                    "operator": ">=",
                    "value": "1956"
                },
                {
                    "id": "ncit:C83164",
                    "operator": "<=",
                    "value": "2024"
                }
            ]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def age_at_diagnosis_filter():
    return {
        "meta": {
            "apiVersion": "v0.2"
        },
        "query": {
            "filters": [
                {
                    "id": "ncit:C156420",
                    "operator": ">=",
                    "value": "0"
                },
                {
                    "id": "ncit:C156420",
                    "operator": "<=",
                    "value": "100"
                }
            ]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def causative_genes_filter():
    return {
        "meta": {
            "apiVersion": "2.0",
            "requestedGranularity": "count"
        },
        "query": {
            "filters": [{
                "id": "edam:data_2295",
                "operator": "=",
                "value": ["FOXD3"]
            }]
        }
    }


@pytest.fixture(scope='session', autouse=True)
def symptom_onset_filter():
    return {
        "meta": {
            "apiVersion": "2.0",
            "requestedGranularity": "count"
        },
        "query": {
            "filters": [{
                "id": "ncit:C124353",
                "operator": "=",
                "value": 1985
            }]
        }
    }
