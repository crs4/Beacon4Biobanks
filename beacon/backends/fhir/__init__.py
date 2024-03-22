from beacon import conf

fhir_base_url = f"{conf.fhir.url}"
fhir_specimen_url = f"{fhir_base_url}/Specimen"
fhir_patient_url = f"{fhir_base_url}/Patient"
fhir_organization_url = f"{fhir_base_url}/Organization"
fhir_json_header = {'Content-type': 'application/fhir+json'}
max_items = 11000
library_version = '0.1.1'
measure_version = '0.1.1'
evaluation_year_start = "1900"
evaluation_year_end = "2100"
