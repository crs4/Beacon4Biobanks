import logging
from typing import Optional

from beacon.exceptions import OperationNotSupported
from beacon.request.model import Granularity

LOG = logging.getLogger(__name__)


def get_datasets(entry_id, qparams, granularity=None):
    raise OperationNotSupported()


def get_dataset_with_id(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_variants_of_dataset(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_biosamples_of_dataset(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_individuals_of_dataset(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def filter_public_datasets(requested_datasets_ids):
    raise OperationNotSupported()


def get_filtering_terms_of_dataset(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_runs_of_dataset(entry_id: Optional[str], granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_analyses_of_dataset(entry_id: Optional[str], qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()
