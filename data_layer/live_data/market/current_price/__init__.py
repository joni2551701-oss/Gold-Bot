"""data_layer/live_data/market/current_price -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `current_price.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `current_price.py`.
"""
from data_layer.live_data.market.current_price.current_price import (
    dataclass,
    datetime,
    Optional,
    MarketPrice,
    read_current_price,
)

__all__ = [
    "dataclass",
    "datetime",
    "Optional",
    "MarketPrice",
    "read_current_price",
]
