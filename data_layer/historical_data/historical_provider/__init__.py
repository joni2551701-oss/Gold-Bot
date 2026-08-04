"""data_layer/historical_data/historical_provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `historical_provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `historical_provider.py`.
"""
from data_layer.historical_data.historical_provider.historical_provider import (
    annotations,
    ABC,
    abstractmethod,
    datetime,
    List,
    Optional,
    Protocol,
    runtime_checkable,
    Dict,
    Tuple,
    Candle,
    ProviderHealth,
    ProviderCapabilities,
    HistoricalProvider,
    BootstrapCache,
    InMemoryBootstrapCache,
)

__all__ = [
    "annotations",
    "ABC",
    "abstractmethod",
    "datetime",
    "List",
    "Optional",
    "Protocol",
    "runtime_checkable",
    "Dict",
    "Tuple",
    "Candle",
    "ProviderHealth",
    "ProviderCapabilities",
    "HistoricalProvider",
    "BootstrapCache",
    "InMemoryBootstrapCache",
]
