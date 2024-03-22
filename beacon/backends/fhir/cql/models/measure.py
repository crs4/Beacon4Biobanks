from beacon.backends.fhir.cql.models import FHIRResource
from beacon.backends.fhir.cql.models.population import Population
from beacon.backends.fhir.cql.models.stratifier import Stratifier


class Measure(FHIRResource):
    def __init__(self, stratifiers: list[Stratifier], populations: list[Population], version_id, last_updated, subject,
                 library_url, id):
        self.stratifiers = stratifiers
        self.populations = populations
        self.version_id = version_id
        self.last_updated = last_updated
        self.subject = subject
        self.library_url = library_url
        self.id = id
        super(Measure, self).__init__({
            "group": [{
                "stratifier": [s.get_resource() for s in self.stratifiers],
                "population": [p.get_resource() for p in self.populations],
            }],
            "meta": {
                "versionId": self.version_id,
                "lastUpdated": self.last_updated,
            },
            "subjectCodeableConcept": {
                "coding": [{
                    "system": "http://hl7.org/fhir/resource-types",
                    "code": self.subject
                }]
            },
            "resourceType": "Measure",
            "library": [
                self.library_url
            ],
            "id": self.id,
            "scoring": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/measure-scoring",
                    "code": "cohort"
                }]
            }
        })
