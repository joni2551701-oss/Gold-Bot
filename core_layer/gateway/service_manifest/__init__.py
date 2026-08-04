"""core_layer/gateway/service_manifest -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `service_manifest.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `service_manifest.py`.
"""
from core_layer.gateway.service_manifest.service_manifest import (
    annotations,
    dataclass,
    field,
    timedelta,
    Enum,
    Tuple,
    ServiceKind,
    HealthPolicy,
    ServiceManifest,
)

__all__ = [
    "annotations",
    "dataclass",
    "field",
    "timedelta",
    "Enum",
    "Tuple",
    "ServiceKind",
    "HealthPolicy",
    "ServiceManifest",
]
