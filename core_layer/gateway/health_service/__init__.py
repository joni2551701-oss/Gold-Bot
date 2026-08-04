"""core_layer/gateway/health_service -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `health_service.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `health_service.py`.
"""
from core_layer.gateway.health_service.health_service import (
    annotations,
    Enum,
    Callable,
    Dict,
    GatewayHealth,
    HealthCheck,
    HealthService,
)

__all__ = [
    "annotations",
    "Enum",
    "Callable",
    "Dict",
    "GatewayHealth",
    "HealthCheck",
    "HealthService",
]
