import pytest

from beacon.backends.molgenis.rsql.builder import create_rsql_query
from beacon.backends.molgenis.rsql.parameters import Parameter


@pytest.fixture
def single_value_like_parameter():
    p = Parameter('name', '=q=', ['name_1'])
    return {
        'parameters': [p],
        'expected_rsql': '(name=like="name_1")'
    }


@pytest.fixture
def multiple_values_like_parameter():
    p = Parameter('name', '=q=', ['name_1', 'name_2'])
    return {
        'parameters': [p],
        'expected_rsql': '(name=like="name_1" or name=like="name_2")'
    }


@pytest.fixture
def multiple_instance_like_parameter():
    p1 = Parameter('name', '=q=', ['name_1', 'name_2'])
    p2 = Parameter('name', '=q=', ['name_3'])
    return {
        'parameters': [p1, p2],
        'expected_rsql': '(name=like="name_1" or name=like="name_2") and (name=like="name_3")'
    }


@pytest.fixture
def single_value_in_parameter():
    p = Parameter('description', 'in', ['desc_1'])
    return {
        'parameters': [p],
        'expected_rsql': '(description=in=(desc_1))'
    }


@pytest.fixture
def multiple_values_in_parameter():
    p = Parameter('description', 'in', ['desc_1', 'desc_2'])
    return {
        'parameters': [p],
        'expected_rsql': '(description=in=(desc_1,desc_2))'
    }


@pytest.fixture
def multiple_instances_in_parameter():
    p1 = Parameter('description', 'in', ['desc_1', 'desc_2'])
    p2 = Parameter('description', 'in', ['desc_3', 'desc_4'])
    return {
        'parameters': [p1, p2],
        'expected_rsql': '(description=in=(desc_1,desc_2)) and (description=in=(desc_3,desc_4))'
    }


@pytest.fixture
def multiple_parameters():
    p1 = Parameter('description', 'in', ['desc_1', 'desc_2'])
    p2 = Parameter('name', '=q=', ['name_1', 'name_2'])
    return {
        'parameters': [p1, p2],
        'expected_rsql': '(description=in=(desc_1,desc_2)) and (name=like="name_1" or name=like="name_2")'
    }


def test_like_param_single_value(single_value_like_parameter):
    """
    Tests the creation of an rsql clause for a single parameter with operator =q=
    """
    rsql = create_rsql_query(single_value_like_parameter['parameters'])
    assert single_value_like_parameter['expected_rsql'] == rsql


def test_like_param_multiple_values(multiple_values_like_parameter):
    """
    Tests the creation of an rsql clause for a single parameter with operator =q= and multiple values
    The resulting RSQL put the values in or
    """
    rsql = create_rsql_query(multiple_values_like_parameter['parameters'])
    assert multiple_values_like_parameter['expected_rsql'] == rsql


def test_like_param_multiple_instance(multiple_instance_like_parameter):
    """
    Tests the creation of an rsql clause for a single parameter with operator =q= and multiple instance
    The resulting RSQL clause puts values of an instance in or and the different instances in and
    """
    rsql = create_rsql_query(multiple_instance_like_parameter['parameters'])
    assert multiple_instance_like_parameter['expected_rsql'] == rsql


def test_in_param_single_value(single_value_in_parameter):
    """
    Tests the creation of an rsql clause for a single parameter with operator in
    """
    rsql = create_rsql_query(single_value_in_parameter['parameters'])
    assert single_value_in_parameter['expected_rsql'] == rsql


def test_in_param_multiple_values(multiple_values_in_parameter):
    """
    Tests the creation of an rsql clause for a single parameter with operator in and multiple values
    The resulting rsql puts the values in or
    """
    rsql = create_rsql_query(multiple_values_in_parameter['parameters'])
    assert multiple_values_in_parameter['expected_rsql'] == rsql


def test_in_param_multiple_instances(multiple_instances_in_parameter):
    """
    Tests the creation of an rsql clause for a single parameter with operator in and multiple instances
    The resulting rsql puts the instances' values in and
    """
    rsql = create_rsql_query(multiple_instances_in_parameter['parameters'])
    assert multiple_instances_in_parameter['expected_rsql'] == rsql


def test_multiple_params_of_different_type(multiple_parameters):
    """
    Tests the creation of an rsql clause for a different parameters
    The resulting rsql puts the parameters in and
    """
    rsql = create_rsql_query(multiple_parameters['parameters'])
    assert multiple_parameters['expected_rsql'] == rsql
