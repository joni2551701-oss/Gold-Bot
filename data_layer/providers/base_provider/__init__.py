"""data_layer/providers/base_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `base_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `base_provider.py`.
"""
from data_layer.providers.base_provider.base_provider import (
    ABC,
    abstractmethod,
    asdict,
    dataclass,
    datetime,
    List,
    Optional,
    Tuple,
    MarketCandle,
    ProviderStatus,
    DataProvider,
    MarketDataProvider,
)

__all__ = [
    "ABC",
    "abstractmethod",
    "asdict",
    "dataclass",
    "datetime",
    "List",
    "Optional",
    "Tuple",
    "MarketCandle",
    "ProviderStatus",
    "DataProvider",
    "MarketDataProvider",
]
