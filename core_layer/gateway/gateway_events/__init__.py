"""core_layer/gateway/gateway_events -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `gateway_events.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `gateway_events.py`.
"""
from core_layer.gateway.gateway_events.gateway_events import (
    annotations,
    dataclass,
    field,
    datetime,
    Enum,
    Callable,
    Optional,
    GatewayEventName,
    GatewayEvent,
    EventSink,
)

__all__ = [
    "annotations",
    "dataclass",
    "field",
    "datetime",
    "Enum",
    "Callable",
    "Optional",
    "GatewayEventName",
    "GatewayEvent",
    "EventSink",
]
