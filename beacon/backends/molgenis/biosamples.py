import logging
from typing import Optional

from beacon.exceptions import OperationNotSupported
from beacon.request.model import Granularity

LOG = logging.getLogger(__name__)


def get_biosamples(entry_id: str, qparams, schema, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_biosample_with_id(entry_id: str, qparams, schema, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_filtering_terms_of_biosample(entry_id: str, qparams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_variants_of_biosample(entry_id: Optional[str], granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_analyses_of_biosample(entry_id: Optional[str], granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_runs_of_biosample(entry_id: Optional[str], granularity=Granularity.COUNT):
    raise OperationNotSupported()
