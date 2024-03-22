import logging
from typing import Optional

from beacon.exceptions import OperationNotSupported
from beacon.request.model import RequestParams, Granularity

LOG = logging.getLogger(__name__)


def get_individuals(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_individual_with_id(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_variants_of_individual(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_biosamples_of_individual(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams, schema, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams, schema, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()

