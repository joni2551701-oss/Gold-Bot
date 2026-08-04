"""core_layer/gateway/service_registry -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `service_registry.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `service_registry.py`.
"""
from core_layer.gateway.service_registry.service_registry import (
    annotations,
    Dict,
    List,
    Optional,
    ServiceManifest,
    ServiceKind,
    RegisteredService,
    ServiceHandler,
    build_graph,
    validate,
    resolution_order,
    DuplicateServiceError,
    ServiceNotFoundError,
    ServiceRegistry,
)

__all__ = [
    "annotations",
    "Dict",
    "List",
    "Optional",
    "ServiceManifest",
    "ServiceKind",
    "RegisteredService",
    "ServiceHandler",
    "build_graph",
    "validate",
    "resolution_order",
    "DuplicateServiceError",
    "ServiceNotFoundError",
    "ServiceRegistry",
]
