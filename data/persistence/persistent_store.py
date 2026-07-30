"""
Persistent storage backends (DD-069) and the PersistentMemoryStore --
the high-level persist / restore / recover API for MarketMemory.
v1.1 Phase 1, module 6.

- StorageBackend is fully backend-agnostic (DD-069): File now, and
  SQLite/PostgreSQL/Redis/S3/Cloud later, without changing Core.
- Restore is safe (DD-071): deserialize -> integrity check -> hydrate;
  if integrity fails, memory is NOT modified and the restore is aborted
  (the caller marks readiness FAILED).

This module never imports from any layer above data/.
"""

from __future__ import annotations

import os
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List

from core.logger import setup_logger
from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleSource
from data.candle_clock import CandleClock
from data.persistence.memory_codec import MemoryCodec, SnapshotMetadata
from data.persistence.snapshot_store import SnapshotStore, SNAPSHOT_SLOTS
from data.persistence.integrity import check_series
from data.persistence.persistence_metrics import PersistenceMetrics

logger = setup_logger("PersistentMemoryStore")


# -- storage backends (DD-069) -----------------------------------------
class StorageBackend(ABC):
    """Backend-agnostic byte store (File/SQLite/Redis/S3/... behind this)."""

    @abstractmethod
    def put(self, key: str, data: bytes) -> None: ...
    @abstractmethod
    def get(self, key: str) -> Optional[bytes]: ...
    @abstractmethod
    def delete(self, key: str) -> None: ...
    @abstractmethod
    def exists(self, key: str) -> bool: ...
    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]: ...


class InMemoryStorageBackend(StorageBackend):
    """RAM backend (tests / ephemeral)."""

    def __init__(self):
        self._store: Dict[str, bytes] = {}
        self._lock = threading.RLock()

    def put(self, key, data):
        with self._lock:
            self._store[key] = bytes(data)

    def get(self, key):
        with self._lock:
            return self._store.get(key)

    def delete(self, key):
        with self._lock:
            self._store.pop(key, None)

    def exists(self, key):
        with self._lock:
            return key in self._store

    def list_keys(self, prefix=""):
        with self._lock:
            return [k for k in self._store if k.startswith(prefix)]


class FileStorageBackend(StorageBackend):
    """
    Filesystem backend with atomic writes (temp file + os.replace), so a
    partial write never corrupts an existing key (reinforces DD-067).
    """

    def __init__(self, base_dir: str):
        self._base = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _path(self, key: str) -> str:
        safe = key.replace("/", "__")
        return os.path.join(self._base, safe)

    def put(self, key, data):
        path = self._path(key)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)          # atomic on POSIX

    def get(self, key):
        path = self._path(key)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return f.read()

    def delete(self, key):
        path = self._path(key)
        if os.path.exists(path):
            os.remove(path)

    def exists(self, key):
        return os.path.exists(self._path(key))

    def list_keys(self, prefix=""):
        out = []
        for name in os.listdir(self._base):
            key = name.replace("__", "/")
            if key.startswith(prefix):
                out.append(key)
        return out


# -- restore result -----------------------------------------------------
@dataclass
class RestoreResult:
    ok: bool
    slot: Optional[str] = None
    restored_candles: int = 0
    metadata: Optional[SnapshotMetadata] = None
    reason: str = ""


# -- high-level store ---------------------------------------------------
class PersistentMemoryStore:
    """Persist / restore / recover MarketMemory via the snapshot store."""

    def __init__(self, backend: StorageBackend,
                 codec: Optional[MemoryCodec] = None,
                 clock: Optional[CandleClock] = None,
                 metrics: Optional[PersistenceMetrics] = None):
        self._codec = codec or MemoryCodec()
        self._snapshots = SnapshotStore(backend, self._codec)
        self._clock = clock or CandleClock()
        self._metrics = metrics or PersistenceMetrics()

    @property
    def metrics(self) -> PersistenceMetrics:
        return self._metrics

    def persist(self, asset: str, memory: MarketMemory, now: datetime,
                bootstrap_version: str = "") -> SnapshotMetadata:
        meta = self._snapshots.save(asset, memory, now, bootstrap_version)
        self._metrics.snapshots_saved += 1
        self._metrics.candles_serialized += meta.candle_count
        return meta

    def restore(self, asset: str, memory: MarketMemory,
                slot: str = "latest") -> RestoreResult:
        """
        Safe restore (DD-071): deserialize -> integrity check -> hydrate.
        If integrity fails, memory is left untouched and the restore is
        aborted (caller marks readiness FAILED).
        """
        decoded = self._snapshots.load_decoded(asset, slot)
        if decoded is None:
            return RestoreResult(ok=False, slot=slot, reason="no snapshot")
        meta, timeframes = decoded

        # integrity check BEFORE touching memory (DD-064/DD-071)
        for tf, candles in timeframes.items():
            report = check_series(candles, tf, self._clock)
            if not report.ok:
                self._metrics.restore_failures += 1
                return RestoreResult(
                    ok=False, slot=slot, metadata=meta,
                    reason=f"integrity failed on {tf}: {report.as_dict()}")

        # integrity passed -> hydrate memory
        restored = 0
        for tf, candles in timeframes.items():
            if memory.has_timeframe(tf):
                memory.timeframe(tf).hydrate(candles,
                                             source=CandleSource.BOOTSTRAP)
                restored += len(candles)
        self._metrics.snapshots_restored += 1
        self._metrics.candles_restored += restored
        return RestoreResult(ok=True, slot=slot, restored_candles=restored,
                             metadata=meta)

    def recover(self, asset: str, memory: MarketMemory) -> RestoreResult:
        """Try latest, then previous, then recovery until one restores."""
        for slot in SNAPSHOT_SLOTS:
            result = self.restore(asset, memory, slot=slot)
            if result.ok:
                result.reason = f"recovered from {slot}"
                return result
        return RestoreResult(ok=False, reason="no valid snapshot in any slot")
