"""data_layer/live_data/stream/stream_event -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_event.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_event.py`.
"""
from data_layer.live_data.stream.stream_event.stream_event import (
    asdict,
    dataclass,
    datetime,
    Optional,
    StreamEvent,
)

__all__ = [
    "asdict",
    "dataclass",
    "datetime",
    "Optional",
    "StreamEvent",
]
