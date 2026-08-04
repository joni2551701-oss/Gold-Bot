"""data_layer/live_data/candle_clock -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `candle_clock.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `candle_clock.py`.
"""
from data_layer.live_data.candle_clock.candle_clock import (
    annotations,
    datetime,
    timedelta,
    timezone,
    TIMEFRAME_MINUTES,
    TIMEFRAME_ORDER,
    CandleClock,
)

__all__ = [
    "annotations",
    "datetime",
    "timedelta",
    "timezone",
    "TIMEFRAME_MINUTES",
    "TIMEFRAME_ORDER",
    "CandleClock",
]
