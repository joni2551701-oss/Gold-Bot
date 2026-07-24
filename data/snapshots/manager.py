"""
SnapshotManager -- the facade that composes the module-9 snapshot
infrastructure (v1.1 Phase 1, module 9; amendment 6).

Wires together Catalog, Registry, Lifecycle, Policy, Cleanup, IO and
Metrics behind one API, and (optionally) emits SNAPSHOT.* events on the
module-7 Event Bus (amendment 6). Module 6 *creates & stores* snapshots;
module 9 *manages* them -- this facade is the management entry point.

Reuse (Art. 11): composes existing module-9 components and the module-6
codec/backend + module-7 bus. It re-implements none of them. It is a
foundation facade only -- it is never imported by core/pipeline.py, and
this module never imports from any layer above data/.
"""

from __future__ import annotations

import itertools
from datetime import datetime
from typing import Dict, List, Optional

from data.candle_clock import CandleClock
from data.memory.market_memory import MarketMemory
from data.persistence.memory_codec import MemoryCodec
from data.persistence.persistent_store import StorageBackend
from data.events.event_bus import EventBus
from data.events.event_model import Event, EventType
from data.snapshots.catalog import SnapshotCatalog, CatalogEntry, utcnow
from data.snapshots.registry import SnapshotRegistry
from data.snapshots.lifecycle import SnapshotLifecycle
from data.snapshots.policy import SnapshotPolicy
from data.snapshots.cleanup import SnapshotCleanup
from data.snapshots.snapshot_io import SnapshotIO
from data.snapshots.metrics import SnapshotMetrics
from data.snapshots.snapshot_state import VerifyState


class SnapshotManager:
    def __init__(self, backend: StorageBackend,
                 codec: Optional[MemoryCodec] = None,
                 clock: Optional[CandleClock] = None,
                 bus: Optional[EventBus] = None,
                 policy: Optional[SnapshotPolicy] = None):
        self._codec = codec or MemoryCodec()
        self._clock = clock or CandleClock()
        self._catalog = SnapshotCatalog(backend)
        self._lifecycle = SnapshotLifecycle(backend, self._catalog,
                                            self._codec, self._clock)
        self._registry = SnapshotRegistry(self._catalog)
        self._policy = policy or SnapshotPolicy()
        self._cleanup = SnapshotCleanup(self._catalog, self._lifecycle,
                                        self._policy)
        self._io = SnapshotIO(self._lifecycle, self._catalog,
                              self._codec, self._clock)
        self._bus = bus
        self._eid = itertools.count(1)

    # -- read views (via registry) -------------------------------------
    @property
    def registry(self) -> SnapshotRegistry:
        return self._registry

    def get(self, snapshot_id: str) -> Optional[CatalogEntry]:
        return self._registry.get(snapshot_id)

    def list(self, asset: Optional[str] = None) -> List[CatalogEntry]:
        return self._registry.list(asset)

    def latest(self, asset: str) -> Optional[CatalogEntry]:
        return self._registry.latest(asset)

    # -- lifecycle -----------------------------------------------------
    def create(self, asset: str, memory: MarketMemory, label: str = "snapshot",
               tags=(), now: Optional[datetime] = None,
               bootstrap_version: str = "") -> CatalogEntry:
        entry = self._lifecycle.create(asset, memory, label, tags, now,
                                       bootstrap_version)
        self._emit(EventType.SNAPSHOT_CREATED, entry, now)
        return entry

    def verify(self, snapshot_id: str,
               now: Optional[datetime] = None) -> VerifyState:
        vs = self._lifecycle.verify(snapshot_id)
        entry = self._catalog.get(snapshot_id)
        self._emit(EventType.SNAPSHOT_VERIFIED if vs is VerifyState.VERIFIED
                   else EventType.SNAPSHOT_CORRUPTED, entry, now)
        return vs

    def archive(self, snapshot_id: str,
                now: Optional[datetime] = None) -> CatalogEntry:
        entry = self._lifecycle.archive(snapshot_id)
        self._emit(EventType.SNAPSHOT_ARCHIVED, entry, now)
        return entry

    def delete(self, snapshot_id: str, now: Optional[datetime] = None) -> None:
        entry = self._catalog.get(snapshot_id)         # capture before removal
        self._lifecycle.delete(snapshot_id)
        self._emit(EventType.SNAPSHOT_DELETED, entry, now)

    # -- locks (amendment 2) -------------------------------------------
    def lock(self, snapshot_id: str) -> None:
        self._lifecycle.lock(snapshot_id)

    def unlock(self, snapshot_id: str) -> None:
        self._lifecycle.unlock(snapshot_id)

    # -- import / export (amendments 1, 4, 5) --------------------------
    def export(self, snapshot_id: str,
               now: Optional[datetime] = None) -> dict:
        envelope = self._io.export(snapshot_id)
        entry = self._catalog.get(snapshot_id)
        self._emit(EventType.SNAPSHOT_EXPORTED, entry, now)
        return envelope

    def import_(self, envelope: dict, label: str = "imported",
                now: Optional[datetime] = None) -> CatalogEntry:
        entry = self._io.import_(envelope, label, now)
        self._emit(EventType.SNAPSHOT_IMPORTED, entry, now)
        return entry

    # -- retention -----------------------------------------------------
    def cleanup(self, now: Optional[datetime] = None) -> List[str]:
        now = now or utcnow()
        affected = self._cleanup.run(now)
        if affected and self._bus is not None:
            self._bus.publish(Event(
                type=EventType.SNAPSHOT_CLEANUP, payload=list(affected),
                asset=None, event_id=f"sn{next(self._eid)}", timestamp=now,
                source="SnapshotManager"))
        return affected

    # -- metrics -------------------------------------------------------
    def metrics(self) -> Dict:
        return SnapshotMetrics.snapshot(self._catalog.all())

    # -- event emission (amendment 6) ----------------------------------
    def _emit(self, event_type: EventType, entry: Optional[CatalogEntry],
              now: Optional[datetime]) -> None:
        if self._bus is None or entry is None:
            return
        self._bus.publish(Event(
            type=event_type, payload=entry.snapshot_id, asset=entry.asset,
            event_id=f"sn{next(self._eid)}", timestamp=now or utcnow(),
            source="SnapshotManager", correlation_id=entry.snapshot_id))
