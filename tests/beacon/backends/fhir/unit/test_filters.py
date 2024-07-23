import pytest

from beacon.backends.fhir.cql.parameters import DiagnosisBiosamples, SexBiosample
from beacon.backends.fhir.filters import _match_ids_to_ontologies, apply_filters, apply_ontology_filter, \
    apply_alphanumeric_filter, apply_custom_filter
from beacon.request.model import OntologyFilter, Similarity, AlphanumericFilter, Operator, CustomFilter
from tests.conf.conftest import single_disease_biosample_parameter, multiple_diseases_biosample_parameter, \
    single_sex_biosample_parameter, multiple_sex_biosample_parameter, single_disease_biosample_parameter_as_custom, \
    multiple_diseases_biosample_parameter_as_custom, multiple_diseases_biosample_parameter_miscellaneous_type


def test_match_ids_to_ontologies_false():
    ids = ['Orphanet_1', 'Orphanet_2']
    assert not _match_ids_to_ontologies(ids)


def test_match_ids_to_ontologies_true():
    ids = ['ordo:Orphanet_1', 'ordo:Orphanet_2']
    assert _match_ids_to_ontologies(ids)


def test_match_ids_to_ontologies_string_false():
    id = 'Orphanet_1'
    assert not _match_ids_to_ontologies(id)


def test_match_ids_to_ontologies_string_true():
    id = 'ordo:Orphanet_1'
    assert _match_ids_to_ontologies(id)


def test_apply_filters_ontology_only_single_no_unsupported(single_disease_biosample_parameter):
    filters = [{'id': ['ordo:Orphanet_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == single_disease_biosample_parameter['parameter'].conditions
    assert result[1] == []


def test_apply_filters_ontology_only_single_with_unsupported(single_disease_biosample_parameter):
    filters = [{'id': ['ordo:Orphanet_166']}, {'id': ['xxx:Xxx_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == single_disease_biosample_parameter['parameter'].conditions
    assert result[1] == ['xxx:Xxx_166']


def test_apply_filters_ontology_only_multiple_no_unsupported(multiple_diseases_biosample_parameter):
    filters = [{'id': ['ordo:Orphanet_166']}, {'id': ['ordo:Orphanet_457260']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == multiple_diseases_biosample_parameter['parameter'].conditions
    assert result[1] == []


def test_apply_filters_ontology_only_multiple_with_unsupported(multiple_diseases_biosample_parameter):
    filters = [{'id': ['ordo:Orphanet_166']}, {'id': ['ordo:Orphanet_457260']}, {'id': ['xxx:Xxx_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == multiple_diseases_biosample_parameter['parameter'].conditions
    assert result[1] == ['xxx:Xxx_166']


def test_apply_filters_alphanumeric_only_single_no_unsupported(single_sex_biosample_parameter):
    filters = [{'id': 'ncit:C28421', 'operator': '=', 'value': ['ncit:C16576']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['sex'], SexBiosample)
    assert result[0].mapping['sex'].conditions == single_sex_biosample_parameter['parameter'].conditions
    assert result[1] == []


def test_apply_filters_alphanumeric_only_single_with_unsupported(single_sex_biosample_parameter):
    filters = [{'id': 'ncit:C28421', 'operator': '=', 'value': ['ncit:C16576']}, {'id': ['xxx:Xxx_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['sex'], SexBiosample)
    assert result[0].mapping['sex'].conditions == single_sex_biosample_parameter['parameter'].conditions
    assert result[1] == ['xxx:Xxx_166']


def test_apply_filters_alphanumeric_only_multiple_no_unsupported(multiple_sex_biosample_parameter):
    filters = [{'id': 'ncit:C28421', 'operator': '=', 'value': ['ncit:C16576', 'ncit:C20197']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['sex'], SexBiosample)
    assert result[0].mapping['sex'].conditions == multiple_sex_biosample_parameter['parameter'].conditions
    assert result[1] == []


def test_apply_filters_alphanumeric_only_multiple_with_unsupported(multiple_sex_biosample_parameter):
    filters = [{'id': 'ncit:C28421', 'operator': '=', 'value': ['ncit:C16576', 'ncit:C20197']}, {'id': ['xxx:Xxx_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['sex'], SexBiosample)
    assert result[0].mapping['sex'].conditions == multiple_sex_biosample_parameter['parameter'].conditions
    assert result[1] == ['xxx:Xxx_166']


def test_apply_filters_custom_only_single_no_unsupported(single_disease_biosample_parameter_as_custom):
    filters = [{'id': ['Orphanet_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == single_disease_biosample_parameter_as_custom[
        'parameter'].conditions
    assert result[1] == []


def test_apply_filters_custom_only_single_with_unsupported(single_disease_biosample_parameter_as_custom):
    filters = [{'id': ['Orphanet_166']}, {'id': ['xxx:Xxx_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == single_disease_biosample_parameter_as_custom[
        'parameter'].conditions
    assert result[1] == ['xxx:Xxx_166']


def test_apply_filters_custom_only_multiple_no_unsupported(multiple_diseases_biosample_parameter_as_custom):
    filters = [{'id': ['Orphanet_166']}, {'id': ['Orphanet_457260']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == multiple_diseases_biosample_parameter_as_custom[
        'parameter'].conditions
    assert result[1] == []


def test_apply_filters_custom_only_multiple_with_unsupported(multiple_diseases_biosample_parameter_as_custom):
    filters = [{'id': ['Orphanet_166']}, {'id': ['Orphanet_457260']}, {'id': ['xxx:Xxx_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == multiple_diseases_biosample_parameter_as_custom[
        'parameter'].conditions
    assert result[1] == ['xxx:Xxx_166']


def test_apply_filters_miscellaneous_no_unsupported(multiple_diseases_biosample_parameter_miscellaneous_type):
    filters = [{'id': ['ordo:Orphanet_166']}, {'id': ['Orphanet_457260']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == multiple_diseases_biosample_parameter_miscellaneous_type[
        'parameter'].conditions
    assert result[1] == []


def test_apply_filters_miscellaneous_with_unsupported(multiple_diseases_biosample_parameter_miscellaneous_type):
    filters = [{'id': ['ordo:Orphanet_166']}, {'id': ['Orphanet_457260']}, {'id': ['xxx:Xxx_166']},
               {'id': ['yyy:Yyy_166']}]
    result = apply_filters(filters)
    assert isinstance(result[0].mapping['diagnosis'], DiagnosisBiosamples)
    assert result[0].mapping['diagnosis'].conditions == multiple_diseases_biosample_parameter_miscellaneous_type[
        'parameter'].conditions
    assert result[1] == ['xxx:Xxx_166', 'yyy:Yyy_166']


def test_apply_filters_all_unsupported(multiple_diseases_biosample_parameter_miscellaneous_type):
    filters = [{'id': ['xxx:Xxx_166']}, {'id': ['yyy:Yyy_166']}]
    result = apply_filters(filters)
    assert result[0].mapping == {}
    assert result[1] == ['xxx:Xxx_166', 'yyy:Yyy_166']


def test_apply_ontology_filter(single_disease_biosample_parameter):
    filter = OntologyFilter(id=['ordo:Orphanet_457260'], scope=None, include_descendant_terms=False,
                            similarity=Similarity.EXACT)
    parameters = dict()
    apply_ontology_filter(parameters, filter, list())
    assert len(parameters) == 1
    assert parameters['diagnosis'].conditions == [{'code': 'Orphanet_457260', 'code_system': 'ordo', 'extension': ''}]


@pytest.mark.xfail(raises=KeyError)
def test_apply_ontology_filter_not_supported():
    filter = OntologyFilter(id=['xxx:Xxx_xxx'], scope=None, include_descendant_terms=False, similarity=Similarity.EXACT)
    parameters = dict()
    unsupported_filters = list()
    apply_ontology_filter(parameters, filter, unsupported_filters)
    assert len(unsupported_filters) == 1


def test_apply_alphanumeric_filter_string_value():
    filter = AlphanumericFilter(id='ncit:C28421', value=['ncit:C16576'], scope=None, operator=Operator.EQUAL)
    parameters = dict()
    apply_alphanumeric_filter(parameters, filter, list())
    assert len(parameters) == 1
    assert parameters['sex'].conditions == [{'operator': Operator.EQUAL, 'value': 'female'}]


def test_apply_alphanumeric_filter_list_value():
    filter = AlphanumericFilter(id='ncit:C28421', value=['ncit:C16576', 'ncit:C20197'], scope=None,
                                operator=Operator.EQUAL)
    parameters = dict()
    apply_alphanumeric_filter(parameters, filter, list())
    assert len(parameters) == 1
    assert parameters['sex'].conditions == [{'operator': Operator.EQUAL, 'value': 'female'},
                                            {'operator': Operator.EQUAL, 'value': 'male'}]


@pytest.mark.xfail(raises=KeyError)
def test_apply_alphanumeric_filter_not_supported():
    filter = AlphanumericFilter(id='Xxxx:yyyy', value=['ncit:C16576'], scope=None, operator=Operator.EQUAL)
    parameters = dict()
    unsupported_filters = list()
    apply_alphanumeric_filter(parameters, filter, unsupported_filters)
    assert len(unsupported_filters) == 1


def test_apply_custom_filter_string_value():
    filter = CustomFilter(id='Orphanet_166', scope=None)
    parameters = dict()
    apply_custom_filter(parameters, filter, list())
    assert len(parameters) == 1
    assert parameters['diagnosis'].conditions == [{'code': 'Orphanet_166', 'code_system': 'ordo'}]


@pytest.mark.xfail(raises=KeyError)
def test_apply_custom_filter_string_value_not_supported():
    filter = CustomFilter(id='Xxx_166', scope=None)
    parameters = dict()
    unsupported_filters = list()
    apply_custom_filter(parameters, filter, unsupported_filters)
    assert len(unsupported_filters) == 1


def test_apply_custom_filter_list_value():
    filter = CustomFilter(id=['Orphanet_166', 'Orphanet_457260'], scope=None)
    parameters = dict()
    apply_custom_filter(parameters, filter, list())
    assert len(parameters) == 1
    assert parameters['diagnosis'].conditions == [{'code': 'Orphanet_166', 'code_system': 'ordo'},
                                                  {'code': 'Orphanet_457260', 'code_system': 'ordo'}]


def test_apply_custom_filter_list_value_not_supported():
    filter = CustomFilter(id=['Xxx_xxx', 'Orphanet_457260'], scope=None)
    parameters = dict()
    unsupported_filters = list()
    apply_custom_filter(parameters, filter, unsupported_filters)
    assert len(unsupported_filters) == 1


def test_get_or_create_parameter():
    pass
