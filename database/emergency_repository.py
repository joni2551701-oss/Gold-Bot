"""
Database Layer — Emergency State repository (Phase 59.9: Emergency
Safety Layer Foundation, TASK 2). Mirrors database/audit_log_repository.py's
own structure (append-only, no update/delete, idempotent schema init in
__init__) rather than database/runtime_feature_repository.py's
upsert-per-name pattern -- an emergency transition history must never
be overwritten ("Tarix yo'qolmasligi kerak" per this task's own brief).
"""

from typing import List, Optional
from datetime import datetime

from database.database import Database
from database.models import init_emergency_state_schema
from database.emergency_models import EmergencyStateEntry, create_emergency_state_entry
from core_layer.logger.logger import setup_logger

logger = setup_logger("EmergencyRepository")

_EMERGENCY_STATE_SELECT_COLUMNS = "SELECT state, reason, source, changed_by, created_at, updated_at"


def _row_to_entry(row) -> EmergencyStateEntry:
    return EmergencyStateEntry(
        state=row["state"],
        reason=row["reason"],
        source=row["source"],
        changed_by=row["changed_by"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


class EmergencyRepository:
    """Append-only persistence for EmergencyStateEntry -- database access only, no dependency/audit logic (that's core_layer/emergency/emergency_manager.py's job, same phase)."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_emergency_state_schema(conn)

    def record_transition(
        self,
        state: str,
        reason: Optional[str] = None,
        source: str = "system",
        changed_by: Optional[str] = None,
    ) -> EmergencyStateEntry:
        """Builds (via create_emergency_state_entry()) and inserts one new row -- never an UPDATE, every call is a genuinely new history entry."""
        entry = create_emergency_state_entry(state, reason=reason, source=source, changed_by=changed_by)
        query = (
            "INSERT INTO emergency_states (state, reason, source, changed_by, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        params = (
            entry.state, entry.reason, entry.source, entry.changed_by,
            entry.created_at.isoformat(), entry.updated_at.isoformat(),
        )

        with self.db as conn:
            conn.execute(query, params)

        return entry

    def get_current_state(self) -> Optional[EmergencyStateEntry]:
        """The most recently recorded transition, or None if this repository has never recorded one yet -- the "current state" a fresh EmergencyManager (same repository, e.g. after a restart) reads back."""
        with self.db as conn:
            cursor = conn.execute(
                _EMERGENCY_STATE_SELECT_COLUMNS + " FROM emergency_states ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return _row_to_entry(row) if row else None

    def get_history(self, limit: int = 50) -> List[EmergencyStateEntry]:
        """Most recent `limit` transitions, newest first -- the full, never-lost history this task's own brief requires (NORMAL -> PAUSED -> NORMAL, etc.)."""
        with self.db as conn:
            cursor = conn.execute(
                _EMERGENCY_STATE_SELECT_COLUMNS + " FROM emergency_states ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            return [_row_to_entry(row) for row in cursor.fetchall()]
