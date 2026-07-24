"""
Database Layer — Runtime Feature repository (Phase 59.7: Runtime
Feature Toggle Center, TASK 3). Mirrors
database/sync_state_repository.py's own structure (upsert via
check-then-branch UPDATE/INSERT, idempotent schema init in __init__).

CRUD surface: create + update are unified into set_feature() (an
upsert, same convention as SyncStateRepository.update_sync_state()) --
"create" is simply the first call for a given feature name, "update"
is every call after. get_feature() is read-one, get_all_features() is
list-all.
"""

from typing import List, Optional
from datetime import datetime, timezone

from database.database import Database
from database.models import init_runtime_feature_schema
from database.runtime_feature_models import RuntimeFeatureRecord
from core.logger import setup_logger

logger = setup_logger("RuntimeFeatureRepository")

_RUNTIME_FEATURE_SELECT_COLUMNS = "SELECT feature, enabled, created_at, updated_at, updated_by, reason"


def _row_to_record(row) -> RuntimeFeatureRecord:
    return RuntimeFeatureRecord(
        feature=row["feature"],
        enabled=bool(row["enabled"]),
        created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
        updated_at=datetime.fromisoformat(row["updated_at"]),
        updated_by=row["updated_by"],
        reason=row["reason"],
    )


class RuntimeFeatureRepository:
    """Handles CRUD operations for the 'runtime_features' table. Database access only -- no dependency/audit/snapshot logic (that's configuration/runtime_feature_manager.py's job, same phase)."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_runtime_feature_schema(conn)

    def get_feature(self, feature: str) -> Optional[RuntimeFeatureRecord]:
        """Returns None when no persisted row exists yet for this feature -- never raises for a lookup miss."""
        with self.db as conn:
            cursor = conn.execute(
                _RUNTIME_FEATURE_SELECT_COLUMNS + " FROM runtime_features WHERE feature = ?", (feature,)
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def set_feature(
        self, feature: str, enabled: bool, updated_by: Optional[str] = None, reason: Optional[str] = None
    ) -> RuntimeFeatureRecord:
        """
        Upserts the row for `feature`: UPDATE if it already exists
        (only `enabled`/`updated_at`/`updated_by`/`reason` change --
        `created_at` is never touched by an UPDATE), otherwise INSERT
        (stamps `created_at` for the first and only time). Re-reads
        and returns the row as actually written, same "canonical
        DB-truth" idiom as SyncStateRepository.update_sync_state().
        """
        now = datetime.now(timezone.utc).isoformat()
        with self.db as conn:
            cursor = conn.execute(
                "UPDATE runtime_features SET enabled = ?, updated_at = ?, updated_by = ?, reason = ? WHERE feature = ?",
                (int(enabled), now, updated_by, reason, feature),
            )
            if cursor.rowcount == 0:
                conn.execute(
                    "INSERT INTO runtime_features (feature, enabled, created_at, updated_at, updated_by, reason) VALUES (?, ?, ?, ?, ?, ?)",
                    (feature, int(enabled), now, now, updated_by, reason),
                )

        return self.get_feature(feature)

    def get_all_features(self) -> List[RuntimeFeatureRecord]:
        """Every persisted runtime feature -- the full state a Feature Loader (TASK 4) reads on load()/reload()."""
        with self.db as conn:
            cursor = conn.execute(_RUNTIME_FEATURE_SELECT_COLUMNS + " FROM runtime_features")
            return [_row_to_record(row) for row in cursor.fetchall()]
