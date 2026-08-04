"""data_layer/market_memory/persistence/smart_cache_adapter -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `smart_cache_adapter.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `smart_cache_adapter.py`.
"""
from data_layer.market_memory.persistence.smart_cache_adapter.smart_cache_adapter import (
    annotations,
    json,
    datetime,
    timezone,
    Optional,
    List,
    Dict,
    Tuple,
    Candle,
    CandleClock,
    StorageBackend,
    InMemoryStorageBackend,
    CachePolicy,
    SmartCacheAdapter,
)

__all__ = [
    "annotations",
    "json",
    "datetime",
    "timezone",
    "Optional",
    "List",
    "Dict",
    "Tuple",
    "Candle",
    "CandleClock",
    "StorageBackend",
    "InMemoryStorageBackend",
    "CachePolicy",
    "SmartCacheAdapter",
]
