"""data_layer/event_system/event_bridge -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `event_bridge.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `event_bridge.py`.
"""
from data_layer.event_system.event_bridge.event_bridge import (
    annotations,
    ABC,
    abstractmethod,
    Event,
    EventBridge,
    NullBridge,
)

__all__ = [
    "annotations",
    "ABC",
    "abstractmethod",
    "Event",
    "EventBridge",
    "NullBridge",
]
