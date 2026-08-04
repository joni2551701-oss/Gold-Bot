"""
SnapshotLifecycle -- create / verify / archive / delete (v1.1 Phase 1,
module 9), with transactional writes (amendment 5) and locking
(amendment 2).

Reuse (Art. 11): serialization via module-6 MemoryCodec, blob storage via
a module-6 StorageBackend, integrity via module-6 check_series. Module 9
composes these -- it does not re-implement serialization or storage.

Transactions: create/import/delete run BEGIN -> STORE -> REGISTER ->
COMMIT, rolling back the stored blob if catalog registration fails, so the
catalog and storage never disagree. This module never imports from any
layer above data/.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Optional

from core_layer.logger.logger import setup_logger
from data_layer.market_memory.persistence.memory_codec import MemoryCodec
from data_layer.market_memory.persistence.persistent_store import StorageBackend
from data_layer.market_memory.persistence.integrity import check_series
from data_layer.live_data.candle_clock import CandleClock
from data_layer.market_memory.market_memory import MarketMemory
from data_layer.snapshots.catalog import (
    SnapshotCatalog, CatalogEntry, utcnow,
)
from data_layer.snapshots.snapshot_state import (
    SnapshotState, VerifyState, assert_transition, can_transition, CORE_VERSION,
)

logger = setup_logger("SnapshotLifecycle")


class SnapshotLockedError(RuntimeError):
    """Raised when archiving/deleting a snapshot that is in use (amendment 2)."""


class SnapshotNotFoundError(KeyError):
    pass


def _blob_key(snapshot_id: str) -> str:
    return f"blob/{snapshot_id}"


class SnapshotLifecycle:
    def __init__(self, backend: StorageBackend, catalog: SnapshotCatalog,
                 codec: Optional[MemoryCodec] = None,
                 clock: Optional[CandleClock] = None):
        self._backend = backend
        self._catalog = catalog
        self._codec = codec or MemoryCodec()
        self._clock = clock or CandleClock()

    # -- create (transactional) ----------------------------------------
    def create(self, asset: str, memory: MarketMemory, label: str = "snapshot",
               tags=(), now: Optional[datetime] = None,
               bootstrap_version: str = "") -> CatalogEntry:
        now = now or utcnow()
        blob, meta = self._codec.serialize(memory, now, bootstrap_version)
        snapshot_id = self._make_id(asset, now, meta.integrity_hash)
        stored = False
        try:                                            # BEGIN
            self._backend.put(_blob_key(snapshot_id), blob)   # STORE
            stored = True
            entry = CatalogEntry(
                snapshot_id=snapshot_id, asset=asset, label=label,
                created_at=now, size_bytes=len(blob),
                metadata_hash=meta.integrity_hash,
                schema_version=meta.schema_version,
                core_version=CORE_VERSION, state=SnapshotState.CREATED,
                verify_state=VerifyState.UNVERIFIED, tags=tuple(tags))
            self._catalog.register(entry)               # REGISTER
            return entry                                # COMMIT
        except Exception:
            if stored:
                self._backend.delete(_blob_key(snapshot_id))   # ROLLBACK
            raise

    # -- verify ---------------------------------------------------------
    def verify(self, snapshot_id: str) -> VerifyState:
        entry = self._require(snapshot_id)
        blob = self._backend.get(_blob_key(snapshot_id))
        ok = False
        if blob is not None:
            try:
                meta, timeframes = self._codec.deserialize(blob)
                ok = self._codec.verify_hash(meta, timeframes) and all(
                    check_series(cs, tf, self._clock).ok
                    for tf, cs in timeframes.items())
            except Exception:
                ok = False
        entry.verify_state = VerifyState.VERIFIED if ok else VerifyState.FAILED
        target = SnapshotState.VERIFIED if ok else SnapshotState.CORRUPTED
        if entry.state is not target and can_transition(entry.state, target):
            entry.state = target
        self._catalog.update(entry)
        return entry.verify_state

    # -- archive / delete ----------------------------------------------
    def archive(self, snapshot_id: str) -> CatalogEntry:
        entry = self._require(snapshot_id)
        if entry.in_use:
            raise SnapshotLockedError(f"{snapshot_id} is in use")
        assert_transition(entry.state, SnapshotState.ARCHIVED)
        entry.state = SnapshotState.ARCHIVED
        self._catalog.update(entry)
        return entry

    def delete(self, snapshot_id: str) -> None:
        entry = self._require(snapshot_id)
        if entry.in_use:
            raise SnapshotLockedError(f"{snapshot_id} is in use")
        # transaction: remove blob, then catalog entry
        self._backend.delete(_blob_key(snapshot_id))
        self._catalog.remove(snapshot_id)

    # -- locks (amendment 2) -------------------------------------------
    def lock(self, snapshot_id: str) -> None:
        entry = self._require(snapshot_id)
        entry.locks += 1
        self._catalog.update(entry)

    def unlock(self, snapshot_id: str) -> None:
        entry = self._require(snapshot_id)
        entry.locks = max(0, entry.locks - 1)
        self._catalog.update(entry)

    # -- blob access (for io / replay) ---------------------------------
    def load_blob(self, snapshot_id: str) -> Optional[bytes]:
        return self._backend.get(_blob_key(snapshot_id))

    def store_blob(self, snapshot_id: str, blob: bytes) -> None:
        self._backend.put(_blob_key(snapshot_id), blob)

    def delete_blob(self, snapshot_id: str) -> None:
        """Remove only the blob (catalog untouched) -- used for import rollback."""
        self._backend.delete(_blob_key(snapshot_id))

    # -- helpers --------------------------------------------------------
    def _require(self, snapshot_id: str) -> CatalogEntry:
        entry = self._catalog.get(snapshot_id)
        if entry is None:
            raise SnapshotNotFoundError(snapshot_id)
        return entry

    @staticmethod
    def _make_id(asset: str, now: datetime, integrity_hash: str) -> str:
        base = f"{asset}:{now.isoformat()}:{integrity_hash}"
        digest = hashlib.sha256(base.encode()).hexdigest()[:8]
        return f"{asset}-{int(now.timestamp())}-{digest}"
