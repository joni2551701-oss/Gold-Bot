"""core_layer/gateway/service_breaker -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `service_breaker.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `service_breaker.py`.
"""
from core_layer.gateway.service_breaker.service_breaker import (
    annotations,
    datetime,
    timedelta,
    Enum,
    Optional,
    BreakerState,
    ServiceCircuitBreaker,
)

__all__ = [
    "annotations",
    "datetime",
    "timedelta",
    "Enum",
    "Optional",
    "BreakerState",
    "ServiceCircuitBreaker",
]
