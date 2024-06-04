from dataclasses import dataclass
from typing import Optional, List


@dataclass
class EntryType:
    type: str
    default_schema: str


@dataclass
class ServiceParams:
    backend: str
    schemas: str
    default_beacon_granularity: str
    max_beacon_granularity: str
    documentation_url: str
    environment: str
    entry_types: List[EntryType]
    handovers: Optional[List]
    default_number_of_items_per_request: Optional[int] = 100
    auth_key: Optional[str] = None
    legacy_filters_enabled: Optional[bool] = False


@dataclass
class GA4GHParams:
    service_type_group: str = "org.ga4gh"
    service_type_artifact: str = "beacon"
    service_type_version: str = "1.0"


@dataclass
class BeaconParams:
    beacon_id: str
    beacon_name: str
    api_version: str
    uri: str


@dataclass
class OrganizationParams:
    id: str
    name: str
    address: str
    description: str
    welcome_url: str
    contact_url: str
    logo_url: str
    info: Optional[str] = ""


@dataclass
class ProjectParams:
    description: str
    version: str
    welcome_url: str
    alternative_url: str
    create_datetime: str
    update_datetime: str


@dataclass
class ServerParams:
    beacon_host: str
    beacon_port: int
    beacon_tls_enabled: bool
    beacon_tls_client: bool


@dataclass
class MolgenisParams:
    url: str
    user: Optional[str]
    password: Optional[str]
    base_resource_url: str
    base_resource_check_url: Optional[str]
    alternative_base_resource_url: Optional[str]


@dataclass
class FHIRStoreParams:
    url: str
    user: Optional[str]
    password: Optional[str]


@dataclass
class IdpParams:
    user_info_url: str
    jwk_set_url: str
    issuer: str
    audience: Optional[str]


@dataclass
class BeaconConfig:
    service: ServiceParams
    ga4gh: GA4GHParams
    beacon: BeaconParams
    organization: OrganizationParams
    project: ProjectParams
    server: Optional[ServerParams]
    molgenis: Optional[MolgenisParams]
    fhir: Optional[FHIRStoreParams]
    idp: Optional[IdpParams]

