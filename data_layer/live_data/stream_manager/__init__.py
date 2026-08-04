"""data_layer/live_data/stream_manager -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_manager.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_manager.py`.
"""
from data_layer.live_data.stream_manager.stream_manager import (
    annotations,
    datetime,
    Dict,
    List,
    Any,
    PriceStream,
    StreamState,
    StreamManager,
)

__all__ = [
    "annotations",
    "datetime",
    "Dict",
    "List",
    "Any",
    "PriceStream",
    "StreamState",
    "StreamManager",
]
