"""SnapshotMetrics -- infrastructure metrics (module 9)."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from data_layer.snapshots.catalog import CatalogEntry
from data_layer.snapshots.snapshot_state import SnapshotState, VerifyState


class SnapshotMetrics:
    @staticmethod
    def snapshot(entries: List[CatalogEntry]) -> Dict:
        total = len(entries)
        total_size = sum(e.size_bytes for e in entries)
        per_asset: Dict[str, int] = {}
        for e in entries:
            per_asset[e.asset] = per_asset.get(e.asset, 0) + 1
        last_created: Optional[datetime] = max(
            (e.created_at for e in entries), default=None)
        verified = sum(1 for e in entries
                       if e.verify_state is VerifyState.VERIFIED)
        failed = sum(1 for e in entries
                     if e.verify_state is VerifyState.FAILED)
        archived = sum(1 for e in entries
                       if e.state is SnapshotState.ARCHIVED)
        return {
            "count": total,
            "total_size_bytes": total_size,
            "per_asset": per_asset,
            "last_created": last_created.isoformat() if last_created else None,
            "verified": verified,
            "verify_failed": failed,
            "archived": archived,
            "in_use": sum(1 for e in entries if e.in_use),
        }
