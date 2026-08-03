"""
Database Layer — Configuration Snapshot repository (Phase 59.6: Audit
& Observability Foundation, TASK 6). Mirrors
database/audit_log_repository.py's own structure (append-only, no
update/delete, idempotent schema init in __init__).
"""

from typing import List, Optional
from datetime import datetime

from database.database import Database
from database.models import init_config_snapshot_schema
from database.config_snapshot_models import ConfigSnapshotRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("ConfigSnapshotRepository")

_SNAPSHOT_SELECT_COLUMNS = "SELECT snapshot_id, feature_state, taken_at, taken_by, reason"


def _row_to_record(row) -> ConfigSnapshotRecord:
    return ConfigSnapshotRecord(
        snapshot_id=row["snapshot_id"],
        feature_state=row["feature_state"],
        taken_at=datetime.fromisoformat(row["taken_at"]),
        taken_by=row["taken_by"],
        reason=row["reason"],
    )


class ConfigSnapshotRepository:
    """Append-only persistence for ConfigSnapshotRecord -- database access only, no rollback/apply logic (see config_snapshot_models.py's own docstring)."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_config_snapshot_schema(conn)

    def save_snapshot(self, snapshot: ConfigSnapshotRecord) -> ConfigSnapshotRecord:
        """Persists an already-built ConfigSnapshotRecord (build one via config_snapshot_models.create_config_snapshot()). Returns the same record for a consistent "returns what it saved" convention with the rest of this package."""
        query = "INSERT INTO config_snapshots (snapshot_id, feature_state, taken_at, taken_by, reason) VALUES (?, ?, ?, ?, ?)"
        params = (snapshot.snapshot_id, snapshot.feature_state, snapshot.taken_at.isoformat(), snapshot.taken_by, snapshot.reason)

        with self.db as conn:
            conn.execute(query, params)

        return snapshot

    def get_latest(self) -> Optional[ConfigSnapshotRecord]:
        """The most recently taken snapshot, or None if none exist yet -- never raises for an empty table."""
        with self.db as conn:
            cursor = conn.execute(
                _SNAPSHOT_SELECT_COLUMNS + " FROM config_snapshots ORDER BY taken_at DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def get_all(self, limit: int = 50) -> List[ConfigSnapshotRecord]:
        """Most recent `limit` snapshots, newest first."""
        with self.db as conn:
            cursor = conn.execute(
                _SNAPSHOT_SELECT_COLUMNS + " FROM config_snapshots ORDER BY taken_at DESC LIMIT ?",
                (limit,),
            )
            return [_row_to_record(row) for row in cursor.fetchall()]
