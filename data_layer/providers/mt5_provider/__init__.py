"""data_layer/providers/mt5_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `mt5_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `mt5_provider.py`.
"""
from data_layer.providers.mt5_provider.mt5_provider import (
    List,
    Optional,
    Tuple,
    MarketCandle,
    MarketDataProvider,
    ProviderStatus,
    MT5Provider,
)

__all__ = [
    "List",
    "Optional",
    "Tuple",
    "MarketCandle",
    "MarketDataProvider",
    "ProviderStatus",
    "MT5Provider",
]
