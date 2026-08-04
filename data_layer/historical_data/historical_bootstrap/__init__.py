"""data_layer/historical_data/historical_bootstrap -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `historical_bootstrap.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `historical_bootstrap.py`.
"""
from data_layer.historical_data.historical_bootstrap.historical_bootstrap import (
    annotations,
    datetime,
    timedelta,
    timezone,
    Optional,
    List,
    Dict,
    Mapping,
    setup_logger,
    CandleClock,
    TIMEFRAME_ORDER,
    Candle,
    MarketMemory,
    CandleSource,
    BootstrapState,
    BootstrapStrategy,
    BootstrapProgress,
    BootstrapMetrics,
    HistoricalProvider,
    BootstrapCache,
    GapRecovery,
    BootstrapEventHook,
    logger,
    HistoricalBootstrap,
)

__all__ = [
    "annotations",
    "datetime",
    "timedelta",
    "timezone",
    "Optional",
    "List",
    "Dict",
    "Mapping",
    "setup_logger",
    "CandleClock",
    "TIMEFRAME_ORDER",
    "Candle",
    "MarketMemory",
    "CandleSource",
    "BootstrapState",
    "BootstrapStrategy",
    "BootstrapProgress",
    "BootstrapMetrics",
    "HistoricalProvider",
    "BootstrapCache",
    "GapRecovery",
    "BootstrapEventHook",
    "logger",
    "HistoricalBootstrap",
]
