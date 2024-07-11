import pytest

from beacon.backends.fhir.cql.builder import create_cql_parameter_constraint
from beacon.backends.fhir.cql.parameters import DiagnosisBiosamples


@pytest.fixture
def multiple_diseases_parameter():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo', 'extension': ''},
                    {'code': 'Orphanet_457260', 'code_system': 'ordo', 'extension': ''}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
             and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)) or exists(from Specimen.extension E where \
             E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' and (ordo.id in E.value.coding.system and \
             'Orphanet_457260' in E.value.coding.code)))"}


@pytest.fixture
def single_disease_parameter():
    p = DiagnosisBiosamples()
    p.conditions = [{'code': 'Orphanet_166', 'code_system': 'ordo', 'extension': ''}]
    return {'parameter': p,
            'expected_cql': "(exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis' \
             and (ordo.id in E.value.coding.system and 'Orphanet_166' in E.value.coding.code)))"
    }


def test_create_cql_parameter_constraint_when_diagnosis_biosamples_multiple_param(multiple_diseases_parameter):
    cql = create_cql_parameter_constraint(multiple_diseases_parameter['parameter'])
    assert cql == multiple_diseases_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_diagnosis_biosamples_single_param(single_disease_parameter):
    cql = create_cql_parameter_constraint(single_disease_parameter['parameter'])
    assert cql == single_disease_parameter['expected_cql']