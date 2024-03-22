from beacon.backends.fhir.cql.models import FHIRResource


class EvaluationMeasure(FHIRResource):
    SUBJECT_LIST = 'subject-list'
    POPULATION = 'population'

    def __init__(self, period_start, period_end, report_type):
        assert report_type in (self.SUBJECT_LIST, self.POPULATION)
        self.period_start = period_start
        self.period_end = period_end
        self.report_type = report_type

        super(EvaluationMeasure, self).__init__({
            "resourceType": "Parameters",
            "parameter": [{
                "name": "periodStart", "valueDate": self.period_start
            }, {
                "name": "periodEnd", "valueDate": self.period_end
            }, {
                "name": "reportType", "valueCode": self.report_type
            }]
        })
