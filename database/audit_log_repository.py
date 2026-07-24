"""
Database Layer — Audit Log repository (Phase 59.6: Audit &
Observability Foundation, TASK 2). Mirrors
database/raw_candle_repository.py's own structure (CRUD-ish only, no
business logic, idempotent schema init in __init__) -- except this
repository exposes no update/delete: an audit log is append-only by
design.
"""

from typing import List, Optional
from datetime import datetime

from database.database import Database
from database.models import init_audit_log_schema
from database.audit_log_models import AuditLogEntry, create_audit_log_entry
from core.logger import setup_logger

logger = setup_logger("AuditLogRepository")

_AUDIT_LOG_SELECT_COLUMNS = "SELECT actor, action, target, result, details, created_at"


def _row_to_record(row) -> AuditLogEntry:
    return AuditLogEntry(
        actor=row["actor"],
        action=row["action"],
        target=row["target"],
        result=row["result"],
        details=row["details"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class AuditLogRepository:
    """Append-only persistence for AuditLogEntry -- database access only, no permission/ownership logic."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_audit_log_schema(conn)

    def log_action(
        self,
        actor: str,
        action: str,
        target: Optional[str] = None,
        result: str = "SUCCESS",
        details: Optional[str] = None,
    ) -> AuditLogEntry:
        """Builds (via create_audit_log_entry()) and persists one entry. Never raises for a normal insert -- there is no uniqueness constraint to violate, every call is a genuinely new row."""
        entry = create_audit_log_entry(actor, action, target=target, result=result, details=details)
        query = "INSERT INTO audit_log (actor, action, target, result, details, created_at) VALUES (?, ?, ?, ?, ?, ?)"
        params = (entry.actor, entry.action, entry.target, entry.result, entry.details, entry.created_at.isoformat())

        with self.db as conn:
            conn.execute(query, params)

        return entry

    def get_recent(self, limit: int = 50) -> List[AuditLogEntry]:
        """Most recent `limit` entries, newest first -- the natural order for a human reviewing "what just happened"."""
        with self.db as conn:
            cursor = conn.execute(
                _AUDIT_LOG_SELECT_COLUMNS + " FROM audit_log ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def get_by_actor(self, actor: str, limit: int = 50) -> List[AuditLogEntry]:
        """Every entry for one actor, newest first -- for a future "what has owner X done" view."""
        with self.db as conn:
            cursor = conn.execute(
                _AUDIT_LOG_SELECT_COLUMNS + " FROM audit_log WHERE actor = ? ORDER BY created_at DESC LIMIT ?",
                (actor, limit),
            )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def count(self) -> int:
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM audit_log")
            row = cursor.fetchone()
            return row["count"] if row else 0
