# data_layer / market_memory / persistence

**Module**

## Purpose

data_layer.market_memory.persistence -- GoldBot v1.1 Market Data Foundation: Persistent Memory
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

## Files

- `__init__.py` -- data_layer.market_memory.persistence -- GoldBot v1.1 Market Data Foundation: Persistent Memory
- `cache_policy.py` -- CachePolicy -- freshness, TTL and eviction for the persistent cache
- `integrity.py` -- Integrity checks for candle series (DD-064). v1.1 Phase 1, module 6.
- `memory_codec.py` -- MemoryCodec -- serialize/restore a MarketMemory to/from bytes, with schema
- `persistence_metrics.py` -- PersistenceMetrics -- counters for the Persistent Memory Layer (module 6).
- `persistent_store.py` -- Persistent storage backends (DD-069) and the PersistentMemoryStore --
- `readiness.py` -- ReadinessService -- the cross-cutting Readiness API (DD-065). v1.1 Phase 1,
- `smart_cache_adapter.py` -- SmartCacheAdapter -- a durable BootstrapCache (module-5 contract) over the
- `snapshot_store.py` -- SnapshotStore -- atomic, retained snapshots of a MarketMemory over a

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `cache_policy.py`: class `CachePolicy`
- `integrity.py`: class `IntegrityReport`
- `integrity.py`: function `check_series()`
- `integrity.py`: function `check_integrity()`
- `memory_codec.py`: class `SnapshotMetadata`
- `memory_codec.py`: class `MemoryCodec`
- `persistence_metrics.py`: class `PersistenceMetrics`
- `persistent_store.py`: class `StorageBackend`
- `persistent_store.py`: class `InMemoryStorageBackend`
- `persistent_store.py`: class `FileStorageBackend`
- `persistent_store.py`: class `RestoreResult`
- `persistent_store.py`: class `PersistentMemoryStore`
- `readiness.py`: class `Readiness`
- `readiness.py`: class `ReadinessService`
- `smart_cache_adapter.py`: class `SmartCacheAdapter`
- `snapshot_store.py`: class `SnapshotWriteError`
- `snapshot_store.py`: class `SnapshotStore`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
