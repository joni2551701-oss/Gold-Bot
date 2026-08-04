# data_layer/market_memory/persistence/persistent_store

**Canonical module** (persistent_store) — GEL-001 package form.

## Purpose

See `IMPLEMENTATION.md` and the module docstring in `persistent_store.py`.

## Public API

- `annotations`
- `os`
- `threading`
- `ABC`
- `abstractmethod`
- `dataclass`
- `datetime`
- `Optional`
- `Dict`
- `List`
- `setup_logger`
- `MarketMemory`
- `CandleSource`
- `CandleClock`
- `MemoryCodec`
- `SnapshotMetadata`
- `SnapshotStore`
- `SNAPSHOT_SLOTS`
- `check_series`
- `PersistenceMetrics`
- `logger`
- `StorageBackend`
- `InMemoryStorageBackend`
- `FileStorageBackend`
- `RestoreResult`
- `PersistentMemoryStore`

## Import

    from data_layer.market_memory.persistence.persistent_store import <name>

---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `persistent_store.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
