from beacon.backends.fhir.cql.models import FHIRResource


class Population(FHIRResource):
    def __init__(self, expression, code):
        self.expression = expression
        self.code = code
        super(Population, self).__init__({
            "criteria": {
                "expression": self.expression,
                "language": "text/cql"
            },
            "code": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/measure-population",
                    "code": self.code
                }]
            }
        })
