from typing import Optional

from beacon.exceptions import OperationNotSupported
from beacon.request.model import RequestParams


def get_cohorts(entry_id: Optional[str], qparams: RequestParams):
    raise OperationNotSupported()


def get_cohort_with_id(entry_id: Optional[str], qparams: RequestParams):
    raise OperationNotSupported()


def get_individuals_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    raise OperationNotSupported()


def get_filtering_terms_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    raise OperationNotSupported()
