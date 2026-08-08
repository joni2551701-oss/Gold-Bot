"""data_layer/live_data/twelve_data_price_source -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `twelve_data_price_source.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Added REAL-DATA-008 (real
current-price stream source over TwelveData's /price endpoint).
"""
from data_layer.live_data.twelve_data_price_source.twelve_data_price_source import (
    annotations,
    datetime,
    timezone,
    List,
    Optional,
    setup_logger,
    TwelveDataClient,
    CandleSource,
    PriceProvider,
    StreamEvent,
    ProviderHealth,
    ProviderStatus,
    ProviderCapabilities,
    logger,
    TwelveDataPriceSource,
)

__all__ = [
    "annotations",
    "datetime",
    "timezone",
    "List",
    "Optional",
    "setup_logger",
    "TwelveDataClient",
    "CandleSource",
    "PriceProvider",
    "StreamEvent",
    "ProviderHealth",
    "ProviderStatus",
    "ProviderCapabilities",
    "logger",
    "TwelveDataPriceSource",
]
