"""data_layer/live_data/market/market_manager -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_manager.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_manager.py`.
"""
from data_layer.live_data.market.market_manager.market_manager import (
    dataclass,
    datetime,
    List,
    Optional,
    Candle,
    MarketPrice,
    read_current_price,
    LiquidityState,
    MarketData,
    MarketStateSnapshot,
    MarketStructureView,
    RegimeState,
    SessionState,
    TrendState,
    VolatilityLevel,
    MarketState,
    MarketManager,
)

__all__ = [
    "dataclass",
    "datetime",
    "List",
    "Optional",
    "Candle",
    "MarketPrice",
    "read_current_price",
    "LiquidityState",
    "MarketData",
    "MarketStateSnapshot",
    "MarketStructureView",
    "RegimeState",
    "SessionState",
    "TrendState",
    "VolatilityLevel",
    "MarketState",
    "MarketManager",
]
