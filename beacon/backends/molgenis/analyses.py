from typing import Optional

from beacon.exceptions import OperationNotSupported


def get_analyses(entry_id: Optional[str], qparams):
    raise OperationNotSupported()


def get_analysis_with_id(entry_id: Optional[str], qparams):
    raise OperationNotSupported()

def get_variants_of_analysis(entry_id: Optional[str], schema, qparams):
    raise OperationNotSupported()


def get_filtering_terms_of_analyse(entry_id: Optional[str], schema, qparams):
    raise OperationNotSupported()

