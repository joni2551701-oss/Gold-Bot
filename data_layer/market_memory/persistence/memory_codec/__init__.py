"""data_layer/market_memory/persistence/memory_codec -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `memory_codec.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `memory_codec.py`.
"""
from data_layer.market_memory.persistence.memory_codec.memory_codec import (
    annotations,
    gzip,
    hashlib,
    json,
    dataclass,
    datetime,
    timezone,
    Dict,
    List,
    Tuple,
    Candle,
    MarketMemory,
    SCHEMA_VERSION,
    SnapshotMetadata,
    MemoryCodec,
)

__all__ = [
    "annotations",
    "gzip",
    "hashlib",
    "json",
    "dataclass",
    "datetime",
    "timezone",
    "Dict",
    "List",
    "Tuple",
    "Candle",
    "MarketMemory",
    "SCHEMA_VERSION",
    "SnapshotMetadata",
    "MemoryCodec",
]
