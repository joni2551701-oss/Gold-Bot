"""context_layer/context_engine/candle -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `candle.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `candle.py`.
"""
from context_layer.context_engine.candle.candle import (
    IntEnum,
    Candle,
    CandleDirection,
    direction,
    is_bullish,
    is_bearish,
    is_doji,
    body_size,
    upper_wick,
    lower_wick,
    range_size,
    body_ratio,
)

__all__ = [
    "IntEnum",
    "Candle",
    "CandleDirection",
    "direction",
    "is_bullish",
    "is_bearish",
    "is_doji",
    "body_size",
    "upper_wick",
    "lower_wick",
    "range_size",
    "body_ratio",
]
