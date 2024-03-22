import logging
from typing import List
from typing import Optional, Union

from aiohttp.web_request import Request
from humps import camelize
from pydantic.v1 import BaseModel
from strenum import StrEnum
from typing_extensions import Self

from beacon import conf

LOG = logging.getLogger(__name__)


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class IncludeResultsetResponses(StrEnum):
    ALL = "ALL",
    HIT = "HIT",
    MISS = "MISS",
    NONE = "NONE"


class Similarity(StrEnum):
    EXACT = "exact",
    HIGH = "high",
    MEDIUM = "medium",
    LOW = "low"


class Operator(StrEnum):
    EQUAL = "=",
    LESS = "<",
    GREATER = ">",
    NOT = "!",
    LESS_EQUAL = "<=",
    GREATER_EQUAL = ">="


class Granularity(StrEnum):
    BOOLEAN = "boolean",
    COUNT = "count",
    RECORD = "record"


class OntologyFilter(CamelModel):
    id: Union[str, List[str]]
    scope: Optional[str] = None
    include_descendant_terms: bool = False
    similarity: Similarity = Similarity.EXACT


class AlphanumericFilter(CamelModel):
    id: str
    value: Union[str, int, List[str], List[int]]
    scope: Optional[str] = None
    operator: Operator = Operator.EQUAL


class CustomFilter(CamelModel):
    id: Union[str, List[str]]
    scope: Optional[str] = None


class Pagination(CamelModel):
    skip: int = 0
    limit: int = conf.service.default_number_of_items_per_request


class RequestMeta(CamelModel):
    requested_schemas: List[str] = []
    api_version: str = conf.beacon.api_version


class RequestQuery(CamelModel):
    filters: List[dict] = []
    include_resultset_responses: IncludeResultsetResponses = IncludeResultsetResponses.HIT
    pagination: Pagination = Pagination()
    request_parameters: dict = {}
    test_mode: bool = False
    requested_granularity: Granularity = Granularity(conf.service.default_beacon_granularity)


class RequestParams(CamelModel):
    meta: RequestMeta = RequestMeta()
    query: RequestQuery = RequestQuery()

    def from_request(self, request: Request) -> Self:
        if request.method != "POST" or not request.has_body or not request.can_read_body:
            for k, v in request.query.items():
                if k == "requestedSchema":
                    self.meta.requested_schemas = [v]
                elif k == "skip":
                    self.query.pagination.skip = int(v)
                elif k == "limit":
                    self.query.pagination.limit = int(v)
                elif k == "includeResultsetResponses":
                    self.query.include_resultset_responses = IncludeResultsetResponses(v)
                else:
                    self.query.request_parameters[k] = v
        return self

    def summary(self):
        return {
            "apiVersion": self.meta.api_version,
            "requestedSchemas": self.meta.requested_schemas,
            "filters": self.query.filters,
            "requestParameters": self.query.request_parameters,
            "includeResultsetResponses": self.query.include_resultset_responses,
            "pagination": self.query.pagination.dict(),
            "requestedGranularity": self.query.requested_granularity,
            "testMode": self.query.test_mode
        }
