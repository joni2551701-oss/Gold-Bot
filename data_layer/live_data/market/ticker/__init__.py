"""data_layer/live_data/market/ticker -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `ticker.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `ticker.py`.
"""
from data_layer.live_data.market.ticker.ticker import (
    dataclass,
    datetime,
    Optional,
    Ticker,
)

__all__ = [
    "dataclass",
    "datetime",
    "Optional",
    "Ticker",
]
