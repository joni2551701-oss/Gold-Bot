import sqlite3
from typing import List, Optional
from datetime import datetime, timezone

from database.database import Database
from database.models import init_admin_schema
from database.admin_models import AdminRecord
from core.logger import setup_logger

logger = setup_logger("AdminRepository")

# Phase 50 query optimization: named columns matching exactly what
# _row_to_record() reads, instead of SELECT * -- deliberately excludes
# 'id' (not part of AdminRecord). Row access below is by column name
# (sqlite3.Row), so column order is irrelevant.
_ADMIN_SELECT_COLUMNS = "SELECT telegram_id, role, created_at"


def _row_to_record(row) -> AdminRecord:
    return AdminRecord(
        telegram_id=row["telegram_id"],
        role=row["role"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class AdminRepository:
    """
    Handles CRUD operations for the 'admins' table.
    Database access only -- no Telegram logic, no permission logic.
    Mirrors the UserRepository pattern.
    """

    def __init__(self):
        self.db = Database()
        # Idempotent (CREATE TABLE IF NOT EXISTS): safe to call on every
        # construction, never crashes if the schema already exists.
        with self.db as conn:
            init_admin_schema(conn)

    def add_admin(self, telegram_id, role: str = "ADMIN") -> Optional[AdminRecord]:
        """
        Inserts a new admin. Returns None (no insert performed) if
        telegram_id is already an admin -- never raises for a
        duplicate, whether caught up front or via a lost race against
        a concurrent insert (IntegrityError on the UNIQUE constraint).
        """
        if self.is_admin(telegram_id):
            logger.info(f"Admin already exists: telegram_id={telegram_id}")
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        query = "INSERT INTO admins (telegram_id, role, created_at) VALUES (?, ?, ?)"
        params = (str(telegram_id), role, created_at)

        with self.db as conn:
            try:
                conn.execute(query, params)
            except sqlite3.IntegrityError as e:
                logger.warning(f"Duplicate admin insert prevented: telegram_id={telegram_id} ({e})")
                return None

        return self.get_admin(telegram_id)

    def remove_admin(self, telegram_id) -> bool:
        with self.db as conn:
            cursor = conn.execute(
                "DELETE FROM admins WHERE telegram_id = ?", (str(telegram_id),)
            )
            return cursor.rowcount > 0

    def get_admin(self, telegram_id) -> Optional[AdminRecord]:
        with self.db as conn:
            cursor = conn.execute(
                _ADMIN_SELECT_COLUMNS + " FROM admins WHERE telegram_id = ?", (str(telegram_id),)
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def is_admin(self, telegram_id) -> bool:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT 1 FROM admins WHERE telegram_id = ?", (str(telegram_id),)
            )
            return cursor.fetchone() is not None

    def get_all_admins(self) -> List[AdminRecord]:
        with self.db as conn:
            cursor = conn.execute(_ADMIN_SELECT_COLUMNS + " FROM admins")
            return [_row_to_record(row) for row in cursor.fetchall()]
