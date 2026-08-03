"""
SnapshotIO -- portable export / import of a snapshot (v1.1 Phase 1,
module 9; amendments 1, 4, 5).

Export wraps a snapshot's blob and its SnapshotManifest (amendment 1) into
a self-describing envelope. Import parses an envelope, runs a compatibility
check (amendment 4: schema version, core version major, asset present) and
then a transaction (amendment 5: BEGIN -> VERIFY -> STORE -> REGISTER ->
COMMIT, rolling back the stored blob on any failure).

Reuse (Art. 11): serialization/verification via module-6 MemoryCodec,
integrity via module-6 check_series, blob storage via the module-9
SnapshotLifecycle. SnapshotIO adds only the portable envelope + the
compatibility gate; it re-implements neither serialization nor storage.
This module never imports from any layer above data/.
"""

from __future__ import annotations

import base64
from datetime import datetime
from typing import Optional, Tuple

from data_layer.live_data.candle_clock import CandleClock
from data_layer.market_memory.persistence.memory_codec import MemoryCodec, SCHEMA_VERSION
from data_layer.market_memory.persistence.integrity import check_series
from data_layer.snapshots.catalog import (
    SnapshotCatalog, CatalogEntry, SnapshotManifest, utcnow,
)
from data_layer.snapshots.snapshot_state import (
    SnapshotState, VerifyState, CORE_VERSION, can_transition,
)
from data_layer.snapshots.lifecycle import SnapshotLifecycle, SnapshotNotFoundError

ENVELOPE_FORMAT_VERSION = 1


class SnapshotIncompatibleError(ValueError):
    """Raised when an imported snapshot fails the compatibility check (amendment 4)."""


class SnapshotImportError(ValueError):
    """Raised when an import envelope is malformed."""


def _major(version: str) -> str:
    return version.split(".", 1)[0] if version else ""


class SnapshotIO:
    def __init__(self, lifecycle: SnapshotLifecycle, catalog: SnapshotCatalog,
                 codec: Optional[MemoryCodec] = None,
                 clock: Optional[CandleClock] = None):
        self._lifecycle = lifecycle
        self._catalog = catalog
        self._codec = codec or MemoryCodec()
        self._clock = clock or CandleClock()

    # -- export ---------------------------------------------------------
    def export(self, snapshot_id: str) -> dict:
        """Produce a portable envelope (manifest + base64 blob)."""
        entry = self._catalog.get(snapshot_id)
        if entry is None:
            raise SnapshotNotFoundError(snapshot_id)
        blob = self._lifecycle.load_blob(snapshot_id)
        if blob is None:
            raise SnapshotNotFoundError(f"{snapshot_id}: blob missing")
        envelope = {
            "format_version": ENVELOPE_FORMAT_VERSION,
            "manifest": entry.manifest().as_dict(),
            "blob_b64": base64.b64encode(blob).decode("ascii"),
        }
        # non-destructive EXPORTED marker (only when the transition is legal)
        if can_transition(entry.state, SnapshotState.EXPORTED):
            entry.state = SnapshotState.EXPORTED
            self._catalog.update(entry)
        return envelope

    # -- import (transactional) ----------------------------------------
    def import_(self, envelope: dict, label: str = "imported",
                now: Optional[datetime] = None) -> CatalogEntry:
        now = now or utcnow()
        manifest, blob = self._parse(envelope)
        self._check_compatible(manifest)                  # amendment 4

        # BEGIN -> VERIFY -> STORE -> REGISTER -> COMMIT (amendment 5)
        verify_state = self._verify_blob(blob)            # VERIFY
        snapshot_id = manifest.snapshot_id
        stored = False
        try:
            self._lifecycle.store_blob(snapshot_id, blob)  # STORE
            stored = True
            entry = CatalogEntry(
                snapshot_id=snapshot_id, asset=manifest.asset, label=label,
                created_at=now, size_bytes=len(blob),
                metadata_hash=manifest.metadata_hash,
                schema_version=manifest.schema_version,
                core_version=manifest.core_version,
                state=SnapshotState.IMPORTED, verify_state=verify_state)
            self._catalog.register(entry)                 # REGISTER
            return entry                                  # COMMIT
        except Exception:
            if stored:
                self._lifecycle.delete_blob(snapshot_id)  # ROLLBACK
            raise

    # -- helpers --------------------------------------------------------
    @staticmethod
    def _parse(envelope: dict) -> Tuple[SnapshotManifest, bytes]:
        try:
            manifest = SnapshotManifest.from_dict(envelope["manifest"])
            blob = base64.b64decode(envelope["blob_b64"])
        except (KeyError, TypeError, ValueError) as exc:
            raise SnapshotImportError(f"malformed envelope: {exc}")
        return manifest, blob

    @staticmethod
    def _check_compatible(manifest: SnapshotManifest) -> None:
        errors = []
        if manifest.schema_version != SCHEMA_VERSION:
            errors.append(
                f"schema_version {manifest.schema_version} != {SCHEMA_VERSION}")
        if _major(manifest.core_version) != _major(CORE_VERSION):
            errors.append(
                f"core_version {manifest.core_version} incompatible "
                f"with {CORE_VERSION}")
        if not manifest.asset:
            errors.append("asset missing")
        if errors:
            raise SnapshotIncompatibleError("; ".join(errors))

    def _verify_blob(self, blob: bytes) -> VerifyState:
        ok = False
        try:
            meta, timeframes = self._codec.deserialize(blob)
            ok = self._codec.verify_hash(meta, timeframes) and all(
                check_series(cs, tf, self._clock).ok
                for tf, cs in timeframes.items())
        except Exception:
            ok = False
        return VerifyState.VERIFIED if ok else VerifyState.FAILED
