"""data_layer/snapshots/manager -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `manager.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `manager.py`.
"""
from data_layer.snapshots.manager.manager import (
    annotations,
    itertools,
    datetime,
    Dict,
    List,
    Optional,
    CandleClock,
    MarketMemory,
    MemoryCodec,
    StorageBackend,
    EventBus,
    Event,
    EventType,
    SnapshotCatalog,
    CatalogEntry,
    utcnow,
    SnapshotRegistry,
    SnapshotLifecycle,
    SnapshotPolicy,
    SnapshotCleanup,
    SnapshotIO,
    SnapshotMetrics,
    VerifyState,
    SnapshotManager,
)

__all__ = [
    "annotations",
    "itertools",
    "datetime",
    "Dict",
    "List",
    "Optional",
    "CandleClock",
    "MarketMemory",
    "MemoryCodec",
    "StorageBackend",
    "EventBus",
    "Event",
    "EventType",
    "SnapshotCatalog",
    "CatalogEntry",
    "utcnow",
    "SnapshotRegistry",
    "SnapshotLifecycle",
    "SnapshotPolicy",
    "SnapshotCleanup",
    "SnapshotIO",
    "SnapshotMetrics",
    "VerifyState",
    "SnapshotManager",
]
