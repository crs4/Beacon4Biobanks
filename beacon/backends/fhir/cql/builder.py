import logging

from beacon.backends.fhir.cql.codesystems import FHIR_CODE_SYSTEMS
from beacon.backends.fhir.cql.parameters import Parameter, Custodian

LOG = logging.getLogger(__name__)

_QUERY_SPECIMEN_TPL = "library Retrieve\n" + \
                      "using FHIR version '4.0.0'\n" + \
                      "include FHIRHelpers version '4.0.0'\n\n" + \
                      "\n".join([f"codesystem {key}: '{value}'" for (key, value) in FHIR_CODE_SYSTEMS.items()]) + \
                      "\n\ncontext Specimen" + \
                      "\n\ndefine Patient:\n singleton from ([Patient])" + \
                      "\n\ndefine InInitialPopulation:\n" + \
                      "  {constraints}"

_QUERY_PATIENT_TPL = "library Retrieve\n" + \
                     "using FHIR version '4.0.0'\n" + \
                     "include FHIRHelpers version '4.0.0'\n\n" + \
                     "\n".join([f"codesystem {key}: '{value}'" for (key, value) in FHIR_CODE_SYSTEMS.items()]) + \
                     "\n\ncontext Patient" + \
                     "\n\ndefine Patient:\n singleton from ([Patient])" + \
                     "\n\ndefine InInitialPopulation:\n" + \
                     "  {constraints}\n" + \
                     "define Gender:\n" + \
                     "  Patient.gender \n" + \
                     "define AgeClass:\n" + \
                     "  (AgeInYears() div 10) * 10"


def create_cql_parameter_constraint(parameter: Parameter):
    return parameter.get_cql_clause()


def create_cql(parameters, scope, collection_id=None):
    assert scope in ('biosamples', 'individuals')

    constraints = []
    for p in parameters:
        constraints.append(create_cql_parameter_constraint(p))

    if collection_id:
        c = Custodian(collection_id)
        constraints.append(c.get_condition())

    if len(constraints) > 0:  # Only if there are some parameters
        constraints = ' and \n'.join(constraints)
    else:
        constraints = 'exists(from [Patient] P)'

    tpl = _QUERY_SPECIMEN_TPL if scope == 'biosamples' else _QUERY_PATIENT_TPL
    cql = tpl.format(constraints=constraints)
    LOG.debug(cql)
    return cql
