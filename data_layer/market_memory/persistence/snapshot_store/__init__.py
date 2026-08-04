"""data_layer/market_memory/persistence/snapshot_store -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `snapshot_store.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `snapshot_store.py`.
"""
from data_layer.market_memory.persistence.snapshot_store.snapshot_store import (
    annotations,
    datetime,
    Optional,
    Tuple,
    List,
    Dict,
    setup_logger,
    Candle,
    MarketMemory,
    MemoryCodec,
    SnapshotMetadata,
    logger,
    SNAPSHOT_SLOTS,
    SnapshotWriteError,
    SnapshotStore,
)

__all__ = [
    "annotations",
    "datetime",
    "Optional",
    "Tuple",
    "List",
    "Dict",
    "setup_logger",
    "Candle",
    "MarketMemory",
    "MemoryCodec",
    "SnapshotMetadata",
    "logger",
    "SNAPSHOT_SLOTS",
    "SnapshotWriteError",
    "SnapshotStore",
]
