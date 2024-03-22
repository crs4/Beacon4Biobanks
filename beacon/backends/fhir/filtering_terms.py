from typing import Optional

from beacon.backends.fhir.utils import get_filtering_terms_results
from beacon.request.model import RequestParams


def get_filtering_terms(entry_id: Optional[str], qparams: RequestParams):
    terms = get_filtering_terms_results()
    return None, len(terms), terms
