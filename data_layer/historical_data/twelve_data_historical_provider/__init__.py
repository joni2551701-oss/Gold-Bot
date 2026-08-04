"""data_layer/historical_data/twelve_data_historical_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `twelve_data_historical_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `twelve_data_historical_provider.py`.
"""
from data_layer.historical_data.twelve_data_historical_provider.twelve_data_historical_provider import (
    annotations,
    datetime,
    timezone,
    List,
    Optional,
    TwelveDataClient,
    Candle,
    ProviderHealth,
    ProviderStatus,
    ProviderCapabilities,
    HistoricalProvider,
    TwelveDataHistoricalProvider,
)

__all__ = [
    "annotations",
    "datetime",
    "timezone",
    "List",
    "Optional",
    "TwelveDataClient",
    "Candle",
    "ProviderHealth",
    "ProviderStatus",
    "ProviderCapabilities",
    "HistoricalProvider",
    "TwelveDataHistoricalProvider",
]
