"""data_layer/live_data/market/market_structure -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_structure.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_structure.py`.
"""
from data_layer.live_data.market.market_structure.market_structure import (
    dataclass,
    Optional,
    MarketStructureView,
)

__all__ = [
    "dataclass",
    "Optional",
    "MarketStructureView",
]
