"""data_layer/market_memory/data_cache -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `data_cache.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `data_cache.py`.
"""
from data_layer.market_memory.data_cache.data_cache import (
    os,
    json,
    List,
    Dict,
    Any,
    datetime,
    timezone,
    timedelta,
    MarketDataNormalizer,
    MarketSnapshot,
    Candle,
    setup_logger,
    Config,
    logger,
    SmartDataCache,
)

__all__ = [
    "os",
    "json",
    "List",
    "Dict",
    "Any",
    "datetime",
    "timezone",
    "timedelta",
    "MarketDataNormalizer",
    "MarketSnapshot",
    "Candle",
    "setup_logger",
    "Config",
    "logger",
    "SmartDataCache",
]
