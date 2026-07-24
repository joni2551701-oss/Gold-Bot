"""
Snapshot catalog + manifest (v1.1 Phase 1, module 9).

The catalog is a metadata-only index of every snapshot (amendments 1, 3).
It persists via a StorageBackend so it survives restart and NEVER holds
candle data. This module never imports from any layer above data/.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from data.snapshots.snapshot_state import (
    SnapshotState, VerifyState, CORE_VERSION,
)


@dataclass(frozen=True)
class SnapshotManifest:
    """Portable manifest embedded in every export (amendment 1)."""
    snapshot_id: str
    schema_version: int
    core_version: str
    created_at: datetime
    asset: str
    metadata_hash: str

    def as_dict(self) -> dict:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "SnapshotManifest":
        return cls(
            snapshot_id=d["snapshot_id"], schema_version=d["schema_version"],
            core_version=d["core_version"],
            created_at=datetime.fromisoformat(d["created_at"]),
            asset=d["asset"], metadata_hash=d["metadata_hash"])


@dataclass
class CatalogEntry:
    snapshot_id: str
    asset: str
    label: str
    created_at: datetime
    size_bytes: int
    metadata_hash: str
    schema_version: int
    core_version: str = CORE_VERSION
    state: SnapshotState = SnapshotState.CREATED
    verify_state: VerifyState = VerifyState.UNVERIFIED
    locks: int = 0                       # >0 => IN_USE (amendment 2)
    tags: Tuple[str, ...] = ()

    @property
    def in_use(self) -> bool:
        return self.locks > 0

    def manifest(self) -> SnapshotManifest:
        return SnapshotManifest(
            snapshot_id=self.snapshot_id, schema_version=self.schema_version,
            core_version=self.core_version, created_at=self.created_at,
            asset=self.asset, metadata_hash=self.metadata_hash)

    def as_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id, "asset": self.asset,
            "label": self.label, "created_at": self.created_at.isoformat(),
            "size_bytes": self.size_bytes, "metadata_hash": self.metadata_hash,
            "schema_version": self.schema_version,
            "core_version": self.core_version, "state": self.state.value,
            "verify_state": self.verify_state.value, "locks": self.locks,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CatalogEntry":
        return cls(
            snapshot_id=d["snapshot_id"], asset=d["asset"], label=d["label"],
            created_at=datetime.fromisoformat(d["created_at"]),
            size_bytes=d["size_bytes"], metadata_hash=d["metadata_hash"],
            schema_version=d["schema_version"],
            core_version=d.get("core_version", CORE_VERSION),
            state=SnapshotState(d["state"]),
            verify_state=VerifyState(d["verify_state"]),
            locks=d.get("locks", 0), tags=tuple(d.get("tags", ())))


class SnapshotCatalog:
    """Metadata-only, persistable index of snapshots."""

    _INDEX_KEY = "catalog/index"

    def __init__(self, backend=None):
        self._backend = backend
        self._entries: Dict[str, CatalogEntry] = {}
        if backend is not None:
            self._load()

    def register(self, entry: CatalogEntry) -> None:
        self._entries[entry.snapshot_id] = entry
        self._save()

    def update(self, entry: CatalogEntry) -> None:
        self._entries[entry.snapshot_id] = entry
        self._save()

    def get(self, snapshot_id: str) -> Optional[CatalogEntry]:
        return self._entries.get(snapshot_id)

    def remove(self, snapshot_id: str) -> None:
        self._entries.pop(snapshot_id, None)
        self._save()

    def all(self) -> List[CatalogEntry]:
        return list(self._entries.values())

    def by_asset(self, asset: str) -> List[CatalogEntry]:
        return [e for e in self._entries.values() if e.asset == asset]

    # -- persistence ----------------------------------------------------
    def _save(self) -> None:
        if self._backend is None:
            return
        payload = json.dumps([e.as_dict() for e in self._entries.values()],
                             separators=(",", ":")).encode("utf-8")
        self._backend.put(self._INDEX_KEY, payload)

    def _load(self) -> None:
        data = self._backend.get(self._INDEX_KEY)
        if not data:
            return
        for d in json.loads(data.decode("utf-8")):
            e = CatalogEntry.from_dict(d)
            self._entries[e.snapshot_id] = e


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
