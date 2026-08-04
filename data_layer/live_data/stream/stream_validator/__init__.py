"""data_layer/live_data/stream/stream_validator -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `stream_validator.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `stream_validator.py`.
"""
from data_layer.live_data.stream.stream_validator.stream_validator import (
    dataclass,
    datetime,
    timedelta,
    timezone,
    Optional,
    StreamEvent,
    ValidationResult,
    StreamValidator,
)

__all__ = [
    "dataclass",
    "datetime",
    "timedelta",
    "timezone",
    "Optional",
    "StreamEvent",
    "ValidationResult",
    "StreamValidator",
]
