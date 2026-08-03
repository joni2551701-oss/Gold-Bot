# MODULE_MAP.md -- data_layer/market_memory/persistence

| File | Role |
|---|---|
| `__init__.py` | data_layer.market_memory.persistence -- GoldBot v1.1 Market Data Foundation: Persistent Memory |
| `cache_policy.py` | CachePolicy -- freshness, TTL and eviction for the persistent cache |
| `integrity.py` | Integrity checks for candle series (DD-064). v1.1 Phase 1, module 6. |
| `memory_codec.py` | MemoryCodec -- serialize/restore a MarketMemory to/from bytes, with schema |
| `persistence_metrics.py` | PersistenceMetrics -- counters for the Persistent Memory Layer (module 6). |
| `persistent_store.py` | Persistent storage backends (DD-069) and the PersistentMemoryStore -- |
| `readiness.py` | ReadinessService -- the cross-cutting Readiness API (DD-065). v1.1 Phase 1, |
| `smart_cache_adapter.py` | SmartCacheAdapter -- a durable BootstrapCache (module-5 contract) over the |
| `snapshot_store.py` | SnapshotStore -- atomic, retained snapshots of a MarketMemory over a |

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Table is mechanically generated from each file's own first docstring line.*
