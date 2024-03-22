import logging
from typing import Dict, List, Optional

from beacon.request.model import RequestParams

LOG = logging.getLogger(__name__)

VARIANTS_PROPERTY_MAP = {
    "assemblyId": "position.assemblyId",
    "referenceName": "position.refseqId",
    "start": "position.start",
    "end": "position.end",
    "referenceBases": "referenceBases",
    "alternateBases": "alternateBases",
    "variantType": "variantType",
    "variantMinLength": None,
    "variantMaxLength": None,
    "mateName": None,
    "gene": "molecularAttributes.geneIds",
    "aachange": "molecularAttributes.aminoacidChanges"
}


def generate_position_filter_start(key: str, value: List[int]):
    pass


def generate_position_filter_end(key: str, value: List[int]):
    pass


def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    pass


def get_variants(entry_id: Optional[str], qparams: RequestParams):
    pass


def get_variant_with_id(entry_id: Optional[str], qparams: RequestParams):
    pass


def get_biosamples_of_variant(entry_id: Optional[str], qparams: RequestParams):
    pass


def get_individuals_of_variant(entry_id: Optional[str], qparams: RequestParams):
    pass


def get_runs_of_variant(entry_id: Optional[str], qparams: RequestParams):
    pass


def get_analyses_of_variant(entry_id: Optional[str], qparams: RequestParams):
    pass


def get_filtering_terms_of_genomicvariation(entry_id: Optional[str], qparams: RequestParams):
    pass
