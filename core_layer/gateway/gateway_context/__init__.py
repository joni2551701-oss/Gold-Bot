"""core_layer/gateway/gateway_context -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `gateway_context.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `gateway_context.py`.
"""
from core_layer.gateway.gateway_context.gateway_context import (
    annotations,
    itertools,
    dataclass,
    field,
    datetime,
    timezone,
    Callable,
    Optional,
    Principal,
    utcnow,
    GatewayContext,
    new_context,
)

__all__ = [
    "annotations",
    "itertools",
    "dataclass",
    "field",
    "datetime",
    "timezone",
    "Callable",
    "Optional",
    "Principal",
    "utcnow",
    "GatewayContext",
    "new_context",
]
