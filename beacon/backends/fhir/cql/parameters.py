class Parameter:
    CONDITION = ""

    def __init__(self):
        self.conditions = []

    def add_condition_parameters(self, **kwargs):
        self.conditions.append(kwargs)

    def get_condition_parameters(self):
        return self.conditions

    def get_cql_clause(self):
        clause = ' or '.join([self.CONDITION.format(**params) for params in self.get_condition_parameters()])
        return f"({clause})"


class BMI(Parameter):
    CONDITION = "exists(from [Patient -> Observation: Code '39156-5' from loinc] O " \
                "where (O.value as Quantity) {operator} {value} 'kg/m2')"


class BodyWeightKg(Parameter):
    CONDITION = "exists(from [Patient -> Observation: Code '29463-7' from loinc] O " \
                "where (O.value as Quantity) {operator} {value} 'kg')"


class DateOfDiagnosis(Parameter):
    CONDITION = "exists(from [Patient -> Condition] C where FHIRHelpers.ToDateTime(C.onset) {operator} @{value})"


class DiagnosisIndividuals(Parameter):
    CONDITION = "exists([Patient -> Condition: Code '{code}' from {code_system} ])"


class DiagnosisBiosamples(Parameter):
    CONDITION = "exists(from Specimen.extension E where E.url = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis'" \
                " and ({code_system}.id in E.value.coding.system and '{code}' in E.value.coding.code))"


class AgeAtDiagnosisBiosample(Parameter):
    CONDITION = "exists(from [Patient -> Condition] C where (C.onset as Age) {operator} {value} or " \
                "AgeInYearsAt(FHIRHelpers.ToDateTime(C.onset)) {operator} {value})"


class AgeAtDiagnosisIndividual(Parameter):
    CONDITION = "exists(from [Condition] C where (C.onset as Age) {operator} {value} or " \
                "AgeInYearsAt(FHIRHelpers.ToDateTime(C.onset)) = Ceiling(7))"


class YearOfBirth(Parameter):
    CONDITION = "exists(from [Patient] P where (Today() - {value} year) {operator} FHIRHelpers.ToDate(P.birthDate))"


class SampleType(Parameter):
    CONDITION = "exists(from [Specimen] S where S.type.coding contains Code '{value}' from SampleMaterialType)"


class SamplingDate(Parameter):
    CONDITION = "FHIRHelpers.ToDateTime(Specimen.collection.collected) {operator} @{value}"


class SexBiosample(Parameter):

    def get_cql_clause(self):
        clause = ' or '.join(
            ["P.gender = '{value}'".format(**params) for params in self.get_condition_parameters()])
        return f"(exists from [Patient] P where ({clause}))"


class SexIndividual(Parameter):
    CONDITION = "Patient.gender = '{value}'"


class StorageTemperature(Parameter):
    # CONDITION = "exists(from Specimen.extension E where E.url = '{extension}' " \
    #            "and E.value.coding contains Code '{code}' from {code_system})"
    CONDITION = "exists from [Specimen] s where exists(from S.extension E where E.url = '{extension}' " \
                "and E.value.coding contains Code '{code}' from {code_system})"


class Custodian(Parameter):
    def __init__(self, collection_id):
        self.collection_id = collection_id

    def get_condition(self):
        # return f"exists(from Specimen.extension E where E.value.identifier.value = '{self.collection_id}')"
        return f" exists(from [Specimen] S where exists (from S.extension E where E.value.identifier.value = '{self.collection_id}'))"


# class SmokingHabit():
#     def __init__(self):
#         self._condition_statement = 'exists'
#         self._from_clause = "from [Patient -> Observation: Code '72166-2' from loinc] O"
#         self._where_clause = "O.value.coding contains Code '{smoking_habit_loinc_code}' from loinc".format(
#             smoking_habit_loinc_code=self._ontology_value
#         )
#
#     def get_cql_clause(self):
#         pass  # Not implemented
#
#
# class FastingStatus(Parameter):
#     def __init__(self):
#         self._where_clause = "Specimen.collection.fastingStatus.coding contains Code '{fasting_status_code}' from " \
#                              "FastingStatus".format(fasting_status_code=self.ontology_value)
#
#     def get_cql_clause(self):
#         pass  # Not implemented

def get_cql_parameter_factory(parameter_type, scope='biosamples'):
    return {
        'diagnosis': DiagnosisBiosamples if scope == 'biosamples' else DiagnosisIndividuals,
        'sex': SexBiosample if scope == 'biosamples' else SexIndividual,
        'sampling_date': SamplingDate,
        'sample_type': SampleType,
        'storage_temperature': StorageTemperature,
        'age_at_diagnosis': AgeAtDiagnosisBiosample if scope == 'biosamples' else AgeAtDiagnosisIndividual,
        'year_of_birth': YearOfBirth,
        'bmi': BMI,
        'body_weight': BodyWeightKg,
        'date_of_diagnosis': DateOfDiagnosis
    }[parameter_type]
