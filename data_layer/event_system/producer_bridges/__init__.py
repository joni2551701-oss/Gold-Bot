"""data_layer/event_system/producer_bridges -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `producer_bridges.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `producer_bridges.py`.
"""
from data_layer.event_system.producer_bridges.producer_bridges import (
    annotations,
    itertools,
    uuid,
    datetime,
    timezone,
    Callable,
    Optional,
    CandleEventHook,
    BootstrapEventHook,
    BootstrapState,
    EventBus,
    Event,
    EventType,
    EventPriority,
    CandleEventBridge,
    BootstrapEventBridge,
)

__all__ = [
    "annotations",
    "itertools",
    "uuid",
    "datetime",
    "timezone",
    "Callable",
    "Optional",
    "CandleEventHook",
    "BootstrapEventHook",
    "BootstrapState",
    "EventBus",
    "Event",
    "EventType",
    "EventPriority",
    "CandleEventBridge",
    "BootstrapEventBridge",
]
