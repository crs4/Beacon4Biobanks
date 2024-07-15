from beacon.backends.fhir.cql.builder import create_cql_parameter_constraint
from tests.conf.conftest import single_disease_biosample_parameter, multiple_diseases_biosample_parameter, \
    single_sample_type_parameter, single_disease_individual_parameter, multiple_disease_individual_parameter, \
    multiple_sample_type_parameter, single_sex_biosample_parameter, multiple_sex_biosample_parameter, \
    single_sex_individual_parameter, multiple_sex_individual_parameter


def test_create_cql_parameter_constraint_when_diagnosis_biosamples_multiple_param(
        multiple_diseases_biosample_parameter):
    cql = create_cql_parameter_constraint(multiple_diseases_biosample_parameter['parameter'])
    assert cql == multiple_diseases_biosample_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_diagnosis_biosamples_single_param(single_disease_biosample_parameter):
    cql = create_cql_parameter_constraint(single_disease_biosample_parameter['parameter'])
    assert cql == single_disease_biosample_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_sample_type_single_param(single_sample_type_parameter):
    cql = create_cql_parameter_constraint(single_sample_type_parameter['parameter'])
    assert cql == single_sample_type_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_sample_type_nultiple_param(multiple_sample_type_parameter):
    cql = create_cql_parameter_constraint(multiple_sample_type_parameter['parameter'])
    assert cql == multiple_sample_type_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_diagnosis_individuals_multiple_param(
        multiple_disease_individual_parameter):
    cql = create_cql_parameter_constraint(multiple_disease_individual_parameter['parameter'])
    assert cql == multiple_disease_individual_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_diagnosis_individuals_single_param(
        single_disease_individual_parameter):
    cql = create_cql_parameter_constraint(single_disease_individual_parameter['parameter'])
    assert cql == single_disease_individual_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_sex_biosamples_single_param(single_sex_biosample_parameter):
    cql = create_cql_parameter_constraint(single_sex_biosample_parameter['parameter'])
    assert cql == single_sex_biosample_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_sex_biosamples_multiple_param(multiple_sex_biosample_parameter):
    cql = create_cql_parameter_constraint(multiple_sex_biosample_parameter['parameter'])
    assert cql == multiple_sex_biosample_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_sex_individuals_single_param(single_sex_individual_parameter):
    cql = create_cql_parameter_constraint(single_sex_individual_parameter['parameter'])
    assert cql == single_sex_individual_parameter['expected_cql']


def test_create_cql_parameter_constraint_when_sex_individuals_single_param(multiple_sex_individual_parameter):
    cql = create_cql_parameter_constraint(multiple_sex_individual_parameter['parameter'])
    assert cql == multiple_sex_individual_parameter['expected_cql']
