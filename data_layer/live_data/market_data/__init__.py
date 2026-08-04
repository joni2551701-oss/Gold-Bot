"""data_layer/live_data/market_data -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_data.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_data.py`.
"""
from data_layer.live_data.market_data.market_data import (
    List,
    Dict,
    dataclass,
    field,
    timedelta,
    Config,
    TwelveDataClient,
    Candle,
    classify_api_error,
    setup_logger,
    logger,
    MarketSnapshot,
    MarketDataNormalizer,
)

__all__ = [
    "List",
    "Dict",
    "dataclass",
    "field",
    "timedelta",
    "Config",
    "TwelveDataClient",
    "Candle",
    "classify_api_error",
    "setup_logger",
    "logger",
    "MarketSnapshot",
    "MarketDataNormalizer",
]
