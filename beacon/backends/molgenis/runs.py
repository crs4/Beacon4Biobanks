from typing import Optional

from beacon.exceptions import OperationNotSupported
from beacon.request.model import RequestParams


def get_runs(entry_id: Optional[str], qparams: RequestParams, schema):
    raise OperationNotSupported()


def get_run_with_id(entry_id: Optional[str], qparams: RequestParams, schema):
    raise OperationNotSupported()


def get_variants_of_run(entry_id: Optional[str], qparams: RequestParams, schema):
    raise OperationNotSupported()


def get_analyses_of_run(entry_id: Optional[str], qparams: RequestParams, schema):
    raise OperationNotSupported()


def get_filtering_terms_of_run(entry_id: Optional[str], qparams: RequestParams, schema):
    raise OperationNotSupported()

