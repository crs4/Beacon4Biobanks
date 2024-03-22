from beacon.backends.fhir.cql.models import FHIRResource


class Stratifier(FHIRResource):
    def __init__(self, expression, code):
        self.expression = expression
        self.code = code
        super(Stratifier, self).__init__({
            "criteria": {
                "expression": self.expression,
                "language": "text/cql"
            },
            "code": {
                "text": self.code
            }
        })
