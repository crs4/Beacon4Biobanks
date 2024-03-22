from typing import Optional

from beacon.backends.molgenis.mappers.filters import FILTER_SPEC
from beacon.request.model import RequestParams


def get_filtering_terms(entry_id: Optional[str], qparams: RequestParams):
    terms = [{
        'id': filter_id,
        'type': filter_spec['type'],
        'label': filter_spec['label'],
        'scope': [
            'catalogs'
        ]
    } for filter_id, filter_spec in FILTER_SPEC['terms'].items()]
    resources = FILTER_SPEC['resources']
    response = {
        'filteringTerms': terms,
        'resources': resources
    }
    return None, len(terms), response
