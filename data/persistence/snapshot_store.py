"""
SnapshotStore -- atomic, retained snapshots of a MarketMemory over a
storage backend. v1.1 Phase 1, module 6.

- Atomicity (DD-067): serialize -> write temp -> verify (round-trip hash)
  -> commit. A failed/incomplete write never corrupts the existing latest
  snapshot.
- Retention (DD-068): keeps at least three slots per asset -- latest,
  previous, recovery -- enabling future rollback.
- Metadata (DD-070): every snapshot carries SnapshotMetadata via the codec.

The backend is duck-typed (put/get/delete/exists/list_keys) so it can be
File, SQLite, Redis, S3, ... (DD-069). This module never imports from any
layer above data/.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Tuple, List, Dict

from core_layer.logger.logger import setup_logger
from data.twelve_data_client import Candle
from data.memory.market_memory import MarketMemory
from data.persistence.memory_codec import MemoryCodec, SnapshotMetadata

logger = setup_logger("SnapshotStore")

SNAPSHOT_SLOTS = ("latest", "previous", "recovery")


class SnapshotWriteError(Exception):
    """Raised when a snapshot write fails verification (commit aborted)."""


class SnapshotStore:
    """Atomic, retained per-asset snapshots over a storage backend."""

    def __init__(self, backend, codec: Optional[MemoryCodec] = None):
        self._backend = backend
        self._codec = codec or MemoryCodec()

    @staticmethod
    def _key(asset: str, slot: str) -> str:
        return f"{asset}/{slot}"

    def save(self, asset: str, memory: MarketMemory, now: datetime,
             bootstrap_version: str = "") -> SnapshotMetadata:
        """
        Atomically save `memory` as the latest snapshot for `asset`,
        rotating the old latest into `previous` and seeding `recovery`.
        Verifies the write (round-trip hash) before committing; on failure
        the existing latest is left untouched (DD-067).
        """
        payload, meta = self._codec.serialize(memory, now, bootstrap_version)

        # 1. write to a temporary key
        tmp = self._key(asset, "tmp")
        self._backend.put(tmp, payload)

        # 2. verify the written bytes round-trip and match the hash
        written = self._backend.get(tmp)
        if written is None:
            raise SnapshotWriteError("temp snapshot missing after write")
        vmeta, vtf = self._codec.deserialize(written)
        if not self._codec.verify_hash(vmeta, vtf):
            self._backend.delete(tmp)
            raise SnapshotWriteError("snapshot integrity hash mismatch")

        # 3. commit atomically: rotate latest -> previous, then latest
        latest = self._key(asset, "latest")
        if self._backend.exists(latest):
            self._backend.put(self._key(asset, "previous"),
                              self._backend.get(latest))
        self._backend.put(latest, written)
        # seed recovery once (a known-good baseline for rollback)
        recovery = self._key(asset, "recovery")
        if not self._backend.exists(recovery):
            self._backend.put(recovery, written)
        self._backend.delete(tmp)
        logger.info("SnapshotStore[%s] saved: %d candle(s), %d tf(s)",
                    asset, meta.candle_count, meta.timeframe_count)
        return meta

    def promote_recovery(self, asset: str) -> bool:
        """Promote the current latest to the recovery slot (known-good)."""
        latest = self._key(asset, "latest")
        if not self._backend.exists(latest):
            return False
        self._backend.put(self._key(asset, "recovery"),
                          self._backend.get(latest))
        return True

    def load(self, asset: str, slot: str = "latest") -> Optional[bytes]:
        return self._backend.get(self._key(asset, slot))

    def load_decoded(self, asset: str, slot: str = "latest"
                     ) -> Optional[Tuple[SnapshotMetadata, Dict[str, List[Candle]]]]:
        data = self.load(asset, slot)
        if data is None:
            return None
        return self._codec.deserialize(data)

    def available_slots(self, asset: str) -> List[str]:
        return [s for s in SNAPSHOT_SLOTS
                if self._backend.exists(self._key(asset, s))]
