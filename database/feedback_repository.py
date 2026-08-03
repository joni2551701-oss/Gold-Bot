from typing import List, Optional
from datetime import datetime, timezone

from database.database import Database
from database.models import init_feedback_schema
from database.feedback_models import FeedbackRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("FeedbackRepository")


def _row_to_record(row) -> FeedbackRecord:
    return FeedbackRecord(
        id=row["id"],
        telegram_id=row["telegram_id"],
        message=row["message"],
        status=row["status"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class FeedbackRepository:
    """
    Handles CRUD operations for the 'feedback' table.
    Database access only -- no Telegram logic, no command logic.
    Mirrors the UserRepository/AdminRepository pattern. Unlike those
    tables, there is no UNIQUE constraint here: multiple feedback
    entries per telegram_id are expected and valid.
    """

    def __init__(self):
        self.db = Database()
        # Idempotent (CREATE TABLE IF NOT EXISTS): safe to call on every
        # construction, never crashes if the schema already exists.
        with self.db as conn:
            init_feedback_schema(conn)

    def create_feedback(self, telegram_id, message: str) -> Optional[FeedbackRecord]:
        """Inserts a new feedback entry with status=OPEN and returns the created row."""
        created_at = datetime.now(timezone.utc).isoformat()
        query = """
        INSERT INTO feedback (telegram_id, message, status, created_at)
        VALUES (?, ?, 'OPEN', ?)
        """
        params = (str(telegram_id), message, created_at)

        with self.db as conn:
            cursor = conn.execute(query, params)
            feedback_id = cursor.lastrowid

        return self.get_feedback(feedback_id)

    def get_feedback(self, feedback_id) -> Optional[FeedbackRecord]:
        with self.db as conn:
            cursor = conn.execute("SELECT * FROM feedback WHERE id = ?", (feedback_id,))
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def get_all_feedback(self, limit: int = 50) -> List[FeedbackRecord]:
        """Most recent `limit` feedback entries, newest first."""
        with self.db as conn:
            cursor = conn.execute(
                "SELECT * FROM feedback ORDER BY created_at DESC, id DESC LIMIT ?", (limit,)
            )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def update_status(self, feedback_id, status: str) -> bool:
        with self.db as conn:
            cursor = conn.execute(
                "UPDATE feedback SET status = ? WHERE id = ?", (status, feedback_id)
            )
            return cursor.rowcount > 0

    def count_open_feedback(self) -> int:
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM feedback WHERE status = 'OPEN'")
            row = cursor.fetchone()
            return row["count"] if row else 0
