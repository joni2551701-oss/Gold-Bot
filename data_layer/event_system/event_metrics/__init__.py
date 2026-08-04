"""data_layer/event_system/event_metrics -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `event_metrics.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `event_metrics.py`.
"""
from data_layer.event_system.event_metrics.event_metrics import (
    annotations,
    defaultdict,
    Dict,
    EventType,
    EventMetrics,
)

__all__ = [
    "annotations",
    "defaultdict",
    "Dict",
    "EventType",
    "EventMetrics",
]
