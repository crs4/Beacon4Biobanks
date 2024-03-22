import logging
from typing import Optional

from beacon.backends.fhir.mappers.records import map_dataset
from beacon.backends.fhir.utils import get_datasets_resources
from beacon.exceptions import OperationNotSupported
from beacon.request.model import RequestParams, Granularity
from beacon.schemas import get_schema_from_query_params

LOG = logging.getLogger(__name__)


def get_datasets(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    fhir_resources = get_datasets_resources()
    datasets = list(map(map_dataset, fhir_resources))
    return get_schema_from_query_params("dataset", qparams), len(datasets), datasets


def get_dataset_with_id(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    fhir_resources = get_datasets_resources(entry_id)
    datasets = list(map(map_dataset, fhir_resources))
    return get_schema_from_query_params("dataset", qparams), len(datasets), datasets


def get_variants_of_dataset(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_biosamples_of_dataset(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_individuals_of_dataset(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def filter_public_datasets(requested_datasets_ids):
    return get_datasets(None, None)[2]


def get_filtering_terms_of_dataset(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_runs_of_dataset(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()


def get_analyses_of_dataset(entry_id: Optional[str], qparams: RequestParams, granularity=Granularity.COUNT):
    raise OperationNotSupported()
