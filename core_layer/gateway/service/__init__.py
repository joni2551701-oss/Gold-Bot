"""core_layer/gateway/service -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `service.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `service.py`.
"""
from core_layer.gateway.service.service import (
    annotations,
    Any,
    Callable,
    ServiceManifest,
    ServiceState,
    assert_transition,
    ServiceCircuitBreaker,
    GatewayContext,
    ServiceHandler,
    RegisteredService,
)

__all__ = [
    "annotations",
    "Any",
    "Callable",
    "ServiceManifest",
    "ServiceState",
    "assert_transition",
    "ServiceCircuitBreaker",
    "GatewayContext",
    "ServiceHandler",
    "RegisteredService",
]
