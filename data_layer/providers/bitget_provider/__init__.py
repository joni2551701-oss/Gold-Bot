"""data_layer/providers/bitget_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `bitget_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `bitget_provider.py`.
"""
from data_layer.providers.bitget_provider.bitget_provider import (
    List,
    Optional,
    Tuple,
    config,
    MarketCandle,
    MarketDataProvider,
    ProviderStatus,
    SUPPORTED_SYMBOLS,
    SUPPORTED_TIMEFRAMES,
    BitgetProvider,
)

__all__ = [
    "List",
    "Optional",
    "Tuple",
    "config",
    "MarketCandle",
    "MarketDataProvider",
    "ProviderStatus",
    "SUPPORTED_SYMBOLS",
    "SUPPORTED_TIMEFRAMES",
    "BitgetProvider",
]
