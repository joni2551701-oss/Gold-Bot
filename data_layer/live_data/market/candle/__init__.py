"""data_layer/live_data/market/candle -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `candle.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `candle.py`.
"""
from data_layer.live_data.market.candle.candle import (
    asdict,
    dataclass,
    datetime,
    Optional,
    Candle,
)

__all__ = [
    "asdict",
    "dataclass",
    "datetime",
    "Optional",
    "Candle",
]
