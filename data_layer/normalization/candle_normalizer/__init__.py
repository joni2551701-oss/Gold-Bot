"""data_layer/normalization/candle_normalizer -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `candle_normalizer.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `candle_normalizer.py`.
"""
from data_layer.normalization.candle_normalizer.candle_normalizer import (
    replace,
    List,
    MarketCandle,
    stamp_provider,
    normalize_candle_list,
)

__all__ = [
    "replace",
    "List",
    "MarketCandle",
    "stamp_provider",
    "normalize_candle_list",
]
