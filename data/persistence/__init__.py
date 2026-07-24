"""
data.persistence -- GoldBot v1.1 Market Data Foundation: Persistent Memory
Layer (Phase 1 module 6). The single official durable storage layer under
MarketMemory.

Serializes/restores MarketMemory to a swappable storage backend, with
atomic snapshots (DD-067), retention (DD-068), backend abstraction
(DD-069), snapshot metadata (DD-070), safe restore (DD-071), integrity
checks (DD-064) and a cross-cutting Readiness API (DD-065).

- memory_codec.py        -- serialize/deserialize + versioning + metadata
- integrity.py           -- missing/duplicate/ordering/continuity (DD-064)
- persistent_store.py    -- StorageBackend abstraction + backends +
                            PersistentMemoryStore (persist/restore/recover)
- snapshot_store.py      -- atomic write + retention + metadata
- cache_policy.py        -- freshness / TTL / eviction
- readiness.py           -- ReadinessService.get_readiness (DD-065)
- smart_cache_adapter.py -- SmartDataCache-backed BootstrapCache
- persistence_metrics.py -- metrics

This package never imports from telegram/, ai/, decision/, risk/,
strategies/, signals/, context/, or database/.
"""

from data.persistence.memory_codec import (
    MemoryCodec, SnapshotMetadata, SCHEMA_VERSION,
)
from data.persistence.integrity import IntegrityReport, check_integrity
from data.persistence.persistent_store import (
    StorageBackend, InMemoryStorageBackend, FileStorageBackend,
    PersistentMemoryStore, RestoreResult,
)
from data.persistence.snapshot_store import SnapshotStore, SNAPSHOT_SLOTS
from data.persistence.cache_policy import CachePolicy
from data.persistence.readiness import ReadinessService, Readiness
from data.persistence.persistence_metrics import PersistenceMetrics
from data.persistence.smart_cache_adapter import SmartCacheAdapter

__all__ = [
    "SmartCacheAdapter",
    "MemoryCodec", "SnapshotMetadata", "SCHEMA_VERSION",
    "IntegrityReport", "check_integrity",
    "StorageBackend", "InMemoryStorageBackend", "FileStorageBackend",
    "PersistentMemoryStore", "RestoreResult",
    "SnapshotStore", "SNAPSHOT_SLOTS",
    "CachePolicy",
    "ReadinessService", "Readiness",
    "PersistenceMetrics",
]
