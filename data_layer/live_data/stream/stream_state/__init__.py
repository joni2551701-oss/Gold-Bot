"""data_layer/live_data/stream/stream_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_state.py`.
"""
from data_layer.live_data.stream.stream_state.stream_state import (
    datetime,
    Optional,
    StreamEvent,
    StreamMode,
    StreamState,
)

__all__ = [
    "datetime",
    "Optional",
    "StreamEvent",
    "StreamMode",
    "StreamState",
]
