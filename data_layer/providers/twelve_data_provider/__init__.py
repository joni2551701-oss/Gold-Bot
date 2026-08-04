"""data_layer/providers/twelve_data_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `twelve_data_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `twelve_data_provider.py`.
"""
from data_layer.providers.twelve_data_provider.twelve_data_provider import (
    List,
    Optional,
    Tuple,
    classify_api_error,
    classify_empty_response,
    MarketCandle,
    MarketDataProvider,
    ProviderStatus,
    TwelveDataClient,
    setup_logger,
    logger,
    SUPPORTED_SYMBOLS,
    TwelveDataProvider,
)

__all__ = [
    "List",
    "Optional",
    "Tuple",
    "classify_api_error",
    "classify_empty_response",
    "MarketCandle",
    "MarketDataProvider",
    "ProviderStatus",
    "TwelveDataClient",
    "setup_logger",
    "logger",
    "SUPPORTED_SYMBOLS",
    "TwelveDataProvider",
]
