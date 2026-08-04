"""
SnapshotRegistry -- the query API over the catalog (v1.1 Phase 1,
module 9). Read-only views; mutation goes through the lifecycle/manager.
This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from data_layer.snapshots.catalog import SnapshotCatalog, CatalogEntry


class SnapshotRegistry:
    def __init__(self, catalog: SnapshotCatalog):
        self._catalog = catalog

    def get(self, snapshot_id: str) -> Optional[CatalogEntry]:
        return self._catalog.get(snapshot_id)

    def list(self, asset: Optional[str] = None) -> List[CatalogEntry]:
        entries = (self._catalog.by_asset(asset) if asset
                   else self._catalog.all())
        return sorted(entries, key=lambda e: e.created_at)

    def latest(self, asset: str) -> Optional[CatalogEntry]:
        entries = self._catalog.by_asset(asset)
        return max(entries, key=lambda e: e.created_at, default=None)

    def find(self, asset: Optional[str] = None, label: Optional[str] = None,
             tag: Optional[str] = None, since: Optional[datetime] = None,
             until: Optional[datetime] = None) -> List[CatalogEntry]:
        out = []
        for e in self.list(asset):
            if label is not None and e.label != label:
                continue
            if tag is not None and tag not in e.tags:
                continue
            if since is not None and e.created_at < since:
                continue
            if until is not None and e.created_at > until:
                continue
            out.append(e)
        return out
