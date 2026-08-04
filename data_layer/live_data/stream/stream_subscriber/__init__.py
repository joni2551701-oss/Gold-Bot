"""data_layer/live_data/stream/stream_subscriber -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_subscriber.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_subscriber.py`.
"""
from data_layer.live_data.stream.stream_subscriber.stream_subscriber import (
    ABC,
    abstractmethod,
    Callable,
    StreamEvent,
    StreamSubscriber,
    CallbackSubscriber,
)

__all__ = [
    "ABC",
    "abstractmethod",
    "Callable",
    "StreamEvent",
    "StreamSubscriber",
    "CallbackSubscriber",
]
