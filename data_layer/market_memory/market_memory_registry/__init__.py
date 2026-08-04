"""data_layer/market_memory/market_memory_registry -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_memory_registry.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_memory_registry.py`.
"""
from data_layer.market_memory.market_memory_registry.market_memory_registry import (
    annotations,
    threading,
    Dict,
    List,
    Mapping,
    Optional,
    MemoryMode,
    MarketMemory,
    DEFAULT_TIMEFRAME_CAPACITY,
    DuplicateAssetError,
    UnknownAssetError,
    MarketMemoryRegistry,
    build_default_registry,
)

__all__ = [
    "annotations",
    "threading",
    "Dict",
    "List",
    "Mapping",
    "Optional",
    "MemoryMode",
    "MarketMemory",
    "DEFAULT_TIMEFRAME_CAPACITY",
    "DuplicateAssetError",
    "UnknownAssetError",
    "MarketMemoryRegistry",
    "build_default_registry",
]
