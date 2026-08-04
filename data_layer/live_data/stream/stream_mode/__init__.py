"""data_layer/live_data/stream/stream_mode -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_mode.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_mode.py`.
"""
from data_layer.live_data.stream.stream_mode.stream_mode import (
    datetime,
    timezone,
    Enum,
    Optional,
    StreamMode,
    is_weekend,
    is_market_open,
    resolve_mode,
)

__all__ = [
    "datetime",
    "timezone",
    "Enum",
    "Optional",
    "StreamMode",
    "is_weekend",
    "is_market_open",
    "resolve_mode",
]
