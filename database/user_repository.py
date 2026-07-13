import sqlite3
from typing import Optional
from datetime import datetime, timezone

from database.database import Database
from database.models import init_user_schema
from database.user_models import UserRecord
from core.logger import setup_logger

logger = setup_logger("UserRepository")


def _row_to_record(row) -> UserRecord:
    return UserRecord(
        telegram_id=row["telegram_id"],
        username=row["username"],
        language=row["language"],
        trading_style=row["trading_style"],
        risk_percent=row["risk_percent"],
        timeframe=row["timeframe"],
        created_at=datetime.fromisoformat(row["created_at"]),
        strategy=row["strategy"],
        notifications_enabled=bool(row["notifications_enabled"]),
    )


class UserRepository:
    """
    Handles CRUD operations for the 'users' table.
    Database access only -- no Telegram logic, no command logic, no
    permission logic. Mirrors the SignalRepository pattern.
    """

    def __init__(self):
        self.db = Database()
        # Idempotent (CREATE TABLE IF NOT EXISTS): safe to call on every
        # construction, never crashes if the schema already exists.
        with self.db as conn:
            init_user_schema(conn)

    def user_exists(self, telegram_id) -> bool:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?", (str(telegram_id),)
            )
            return cursor.fetchone() is not None

    def create_user(
        self,
        telegram_id,
        username: Optional[str] = None,
        language: str = "UZ",
        trading_style: str = "Intraday",
        risk_percent: float = 2.0,
        timeframe: str = "M15",
        strategy: str = "Liquidity Sweep",
        notifications_enabled: bool = True,
    ) -> Optional[UserRecord]:
        """
        Inserts a new user with safe defaults. Returns None (no insert
        performed) if telegram_id already exists -- never raises for a
        duplicate, whether caught up front or via a lost race against
        a concurrent insert (IntegrityError on the UNIQUE constraint).
        """
        if self.user_exists(telegram_id):
            logger.info(f"User already exists: telegram_id={telegram_id}")
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        query = """
        INSERT INTO users (
            telegram_id, username, language, trading_style,
            risk_percent, timeframe, created_at, strategy, notifications_enabled
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            str(telegram_id), username, language, trading_style, risk_percent,
            timeframe, created_at, strategy, notifications_enabled,
        )

        with self.db as conn:
            try:
                conn.execute(query, params)
            except sqlite3.IntegrityError as e:
                logger.warning(f"Duplicate user insert prevented: telegram_id={telegram_id} ({e})")
                return None

        return self.get_user(telegram_id)

    def get_user(self, telegram_id) -> Optional[UserRecord]:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (str(telegram_id),)
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def count_users(self) -> int:
        """Total registered users. Used by AdminService statistics."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            row = cursor.fetchone()
            return row["count"] if row else 0

    def update_user(self, telegram_id, **fields) -> bool:
        """
        Updates one or more allowed columns for a user. Unknown field
        names are ignored (not written) rather than raising -- keeps
        UserService safe from a bad settings key crashing the bot.
        """
        allowed = {
            "username", "language", "trading_style", "risk_percent",
            "timeframe", "strategy", "notifications_enabled",
        }
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return False

        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        set_clause = ", ".join(f"{col} = ?" for col in updates)
        params = list(updates.values()) + [str(telegram_id)]

        with self.db as conn:
            cursor = conn.execute(
                f"UPDATE users SET {set_clause} WHERE telegram_id = ?", params
            )
            return cursor.rowcount > 0

    def update_language(self, telegram_id, language: str) -> bool:
        return self.update_user(telegram_id, language=language)

    def update_risk(self, telegram_id, risk_percent: float) -> bool:
        return self.update_user(telegram_id, risk_percent=risk_percent)

    def update_timeframe(self, telegram_id, timeframe: str) -> bool:
        return self.update_user(telegram_id, timeframe=timeframe)

    def update_strategy(self, telegram_id, strategy: str) -> bool:
        return self.update_user(telegram_id, strategy=strategy)

    def update_notifications(self, telegram_id, enabled: bool) -> bool:
        return self.update_user(telegram_id, notifications_enabled=enabled)
