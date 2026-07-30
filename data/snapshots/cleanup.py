"""
SnapshotCleanup -- applies a SnapshotPolicy to remove/rotate snapshots
(v1.1 Phase 1, module 9). Locked (in-use) and protected snapshots are
never removed. Clock-injected. This module never imports from any layer
above data/.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from data.snapshots.catalog import SnapshotCatalog
from data.snapshots.policy import SnapshotPolicy
from data.snapshots.lifecycle import SnapshotLifecycle, SnapshotLockedError


class SnapshotCleanup:
    def __init__(self, catalog: SnapshotCatalog, lifecycle: SnapshotLifecycle,
                 policy: SnapshotPolicy):
        self._catalog = catalog
        self._lifecycle = lifecycle
        self._policy = policy

    def run(self, now: datetime) -> List[str]:
        """Remove/rotate policy-violating snapshots; return affected ids."""
        removable = self._policy.select_removable(self._catalog.all(), now)
        affected = []
        for entry in removable:
            try:
                if self._policy.archive_instead_of_delete and \
                        entry.state.value != "archived":
                    self._lifecycle.archive(entry.snapshot_id)
                else:
                    self._lifecycle.delete(entry.snapshot_id)
                affected.append(entry.snapshot_id)
            except SnapshotLockedError:
                continue          # became locked mid-run; skip
        return affected
