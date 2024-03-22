import pytest

from beacon.backends.molgenis.rsql.parameters import Parameter


@pytest.fixture
def parameter_in_operator():
    return Parameter('param', 'in', ['value_1', 'value_2'])


@pytest.fixture
def parameter_country():
    return Parameter('country', 'in', ['C1', 'C2'])


@pytest.fixture
def parameter_or_operator():
    return Parameter('param', '=q=', ['value_1', 'value_2'])


def test_param_creation(parameter_in_operator):
    assert parameter_in_operator.attribute == 'param'
    assert parameter_in_operator.operator == 'in'
    assert parameter_in_operator.values == ['value_1', 'value_2']
    assert parameter_in_operator.get_values() == ['value_1', 'value_2']
    new_values = ['value_3', 'value_4']
    parameter_in_operator.set_values(new_values)
    assert parameter_in_operator.get_values() == ['value_3', 'value_4']
