class FHIRResource:

    def __init__(self, resource):
        self._resource = resource

    def get_resource(self):
        return self._resource


from .evaluation_measure import EvaluationMeasure
from .library import Library
from .measure import Measure
from .population import Population
