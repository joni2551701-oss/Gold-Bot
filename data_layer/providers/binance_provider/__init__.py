"""data_layer/providers/binance_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `binance_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `binance_provider.py`.
"""
from data_layer.providers.binance_provider.binance_provider import (
    List,
    Optional,
    Tuple,
    MarketCandle,
    MarketDataProvider,
    ProviderStatus,
    SUPPORTED_SYMBOLS,
    SUPPORTED_TIMEFRAMES,
    BinanceProvider,
)

__all__ = [
    "List",
    "Optional",
    "Tuple",
    "MarketCandle",
    "MarketDataProvider",
    "ProviderStatus",
    "SUPPORTED_SYMBOLS",
    "SUPPORTED_TIMEFRAMES",
    "BinanceProvider",
]
