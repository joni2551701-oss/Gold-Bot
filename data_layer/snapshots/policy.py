"""
SnapshotPolicy -- retention / rotation / expiration rules (v1.1 Phase 1,
module 9). Pure policy object; SnapshotCleanup applies it. This module
never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from data_layer.snapshots.catalog import CatalogEntry


@dataclass
class SnapshotPolicy:
    max_per_asset: Optional[int] = None            # retention (count)
    max_age: Optional[timedelta] = None            # expiration (age)
    protect_labels: Tuple[str, ...] = ("recovery",)  # never auto-removed
    archive_instead_of_delete: bool = True         # rotation vs deletion

    def select_removable(self, entries: List[CatalogEntry],
                         now: datetime) -> List[CatalogEntry]:
        """
        Entries that violate the policy and may be removed. Locked
        (in-use) and protected-label entries are never selected.
        """
        candidates = [e for e in entries
                      if not e.in_use and e.label not in self.protect_labels]
        removable = []

        # expiration (age)
        if self.max_age is not None:
            cutoff = now - self.max_age
            for e in candidates:
                if e.created_at < cutoff:
                    removable.append(e)

        # retention (count): keep the newest max_per_asset per asset
        if self.max_per_asset is not None:
            by_asset = {}
            for e in candidates:
                by_asset.setdefault(e.asset, []).append(e)
            for asset_entries in by_asset.values():
                ordered = sorted(asset_entries, key=lambda e: e.created_at,
                                 reverse=True)
                for e in ordered[self.max_per_asset:]:
                    if e not in removable:
                        removable.append(e)
        return removable
