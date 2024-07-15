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

