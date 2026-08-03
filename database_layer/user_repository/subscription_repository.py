import sqlite3
from typing import List, Optional
from datetime import datetime, timezone

from database_layer.database_manager.database import Database
from database_layer.database_manager.models import init_subscription_schema
from database_layer.user_repository.subscription_models import SubscriptionRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("SubscriptionRepository")

# Phase 50 query optimization: named columns matching exactly what
# _row_to_record() reads, instead of SELECT * -- deliberately excludes
# 'id' and 'updated_at' (not part of SubscriptionRecord). Row access
# below is by column name (sqlite3.Row), so column order is irrelevant.
_SUBSCRIPTION_SELECT_COLUMNS = "SELECT telegram_id, plan, status, started_at, expires_at"


def _row_to_record(row) -> SubscriptionRecord:
    return SubscriptionRecord(
        telegram_id=row["telegram_id"],
        plan=row["plan"],
        status=row["status"],
        started_at=datetime.fromisoformat(row["started_at"]),
        expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
    )


class SubscriptionRepository:
    """
    Handles CRUD operations for the 'subscriptions' table.
    Database access only -- no Telegram logic, no plan/billing
    decisions. Mirrors the UserRepository/AdminRepository pattern.
    """

    def __init__(self):
        self.db = Database()
        # Idempotent (CREATE TABLE IF NOT EXISTS): safe to call on every
        # construction, never crashes if the schema already exists.
        with self.db as conn:
            init_subscription_schema(conn)

    def subscription_exists(self, telegram_id) -> bool:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT 1 FROM subscriptions WHERE telegram_id = ?", (str(telegram_id),)
            )
            return cursor.fetchone() is not None

    def create_subscription(
        self,
        telegram_id,
        plan: str = "FREE",
        status: str = "ACTIVE",
        expires_at: Optional[datetime] = None,
    ) -> Optional[SubscriptionRecord]:
        """
        Inserts a new subscription with safe defaults. Returns None
        (no insert performed) if telegram_id already has one -- never
        raises for a duplicate, whether caught up front or via a lost
        race against a concurrent insert (IntegrityError on the
        UNIQUE constraint).
        """
        if self.subscription_exists(telegram_id):
            logger.info(f"Subscription already exists: telegram_id={telegram_id}")
            return None

        started_at = datetime.now(timezone.utc).isoformat()
        expires_at_iso = expires_at.isoformat() if expires_at else None
        query = """
        INSERT INTO subscriptions (
            telegram_id, plan, status, started_at, expires_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (str(telegram_id), plan, status, started_at, expires_at_iso, started_at)

        with self.db as conn:
            try:
                conn.execute(query, params)
            except sqlite3.IntegrityError as e:
                logger.warning(f"Duplicate subscription insert prevented: telegram_id={telegram_id} ({e})")
                return None

        return self.get_subscription(telegram_id)

    def get_subscription(self, telegram_id) -> Optional[SubscriptionRecord]:
        with self.db as conn:
            cursor = conn.execute(
                _SUBSCRIPTION_SELECT_COLUMNS + " FROM subscriptions WHERE telegram_id = ?", (str(telegram_id),)
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def _update(self, telegram_id, **fields) -> bool:
        allowed = {"plan", "status", "expires_at"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return False

        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        set_clause = ", ".join(f"{col} = ?" for col in updates)
        params = list(updates.values()) + [str(telegram_id)]

        with self.db as conn:
            cursor = conn.execute(
                f"UPDATE subscriptions SET {set_clause} WHERE telegram_id = ?", params
            )
            return cursor.rowcount > 0

    def update_plan(self, telegram_id, plan: str) -> bool:
        return self._update(telegram_id, plan=plan)

    def update_status(self, telegram_id, status: str) -> bool:
        return self._update(telegram_id, status=status)

    def get_all_subscriptions(self) -> List[SubscriptionRecord]:
        with self.db as conn:
            cursor = conn.execute(_SUBSCRIPTION_SELECT_COLUMNS + " FROM subscriptions")
            return [_row_to_record(row) for row in cursor.fetchall()]

    def count_by_plan(self, plan: str) -> int:
        """Count of subscriptions on a given plan (FREE/PREMIUM/VIP) -- same convention as UserRepository.count_by_status(). Used by telegram/owner/dashboard.py's /owner summary (Phase 61.5)."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM subscriptions WHERE plan = ?", (plan,))
            row = cursor.fetchone()
            return row["count"] if row else 0
