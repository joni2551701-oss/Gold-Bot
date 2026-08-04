# IMPLEMENTATION.md — data_layer/market_memory/persistence/persistent_store

## `persistent_store.py`

Public surface:

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

## Design Notes

Converted from a flat `persistent_store.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `persistent_store.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
