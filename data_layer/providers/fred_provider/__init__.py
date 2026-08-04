"""data_layer/providers/fred_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `fred_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `fred_provider.py`.
"""
from data_layer.providers.fred_provider.fred_provider import (
    uuid,
    datetime,
    timezone,
    Optional,
    ProviderStatus,
    FundamentalDataPoint,
    FundamentalDataProvider,
    FundamentalSnapshot,
    SERIES_INTEREST_RATE,
    SERIES_INFLATION,
    SERIES_DOLLAR_INDEX,
    SUPPORTED_SERIES,
    FredProvider,
)

__all__ = [
    "uuid",
    "datetime",
    "timezone",
    "Optional",
    "ProviderStatus",
    "FundamentalDataPoint",
    "FundamentalDataProvider",
    "FundamentalSnapshot",
    "SERIES_INTEREST_RATE",
    "SERIES_INFLATION",
    "SERIES_DOLLAR_INDEX",
    "SUPPORTED_SERIES",
    "FredProvider",
]
