# IMPLEMENTATION.md -- data_layer/market_memory/persistence

## `cache_policy.py`

CachePolicy -- freshness, TTL and eviction for the persistent cache

Classes: `CachePolicy`

## `integrity.py`

Integrity checks for candle series (DD-064). v1.1 Phase 1, module 6.

Classes: `IntegrityReport`

Top-level functions: `check_series()`, `check_integrity()`

## `memory_codec.py`

MemoryCodec -- serialize/restore a MarketMemory to/from bytes, with schema

Classes: `SnapshotMetadata`, `MemoryCodec`

## `persistence_metrics.py`

PersistenceMetrics -- counters for the Persistent Memory Layer (module 6).

Classes: `PersistenceMetrics`

## `persistent_store.py`

Persistent storage backends (DD-069) and the PersistentMemoryStore --

Classes: `StorageBackend`, `InMemoryStorageBackend`, `FileStorageBackend`, `RestoreResult`, `PersistentMemoryStore`

## `readiness.py`

ReadinessService -- the cross-cutting Readiness API (DD-065). v1.1 Phase 1,

Classes: `Readiness`, `ReadinessService`

## `smart_cache_adapter.py`

SmartCacheAdapter -- a durable BootstrapCache (module-5 contract) over the

Classes: `SmartCacheAdapter`

## `snapshot_store.py`

SnapshotStore -- atomic, retained snapshots of a MarketMemory over a

Classes: `SnapshotWriteError`, `SnapshotStore`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
