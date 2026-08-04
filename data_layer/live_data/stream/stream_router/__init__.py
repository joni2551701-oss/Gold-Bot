"""data_layer/live_data/stream/stream_router -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_router.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_router.py`.
"""
from data_layer.live_data.stream.stream_router.stream_router import (
    dataclass,
    field,
    Dict,
    List,
    StreamEvent,
    StreamSubscriber,
    RouteResult,
    StreamRouter,
)

__all__ = [
    "dataclass",
    "field",
    "Dict",
    "List",
    "StreamEvent",
    "StreamSubscriber",
    "RouteResult",
    "StreamRouter",
]
