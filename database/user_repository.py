import sqlite3
from typing import List, Optional
from datetime import datetime, timezone

from database.database import Database
from database.models import init_user_schema
from database.user_models import UserRecord
from core.logger import setup_logger

logger = setup_logger("UserRepository")

# Phase 50 query optimization: named columns matching exactly what
# _row_to_record() reads, instead of SELECT * -- deliberately excludes
# 'id' (repository-internal rowid, not part of UserRecord) and
# 'updated_at' (also not part of UserRecord). Row access below is by
# column name (sqlite3.Row), so column order here is irrelevant.
_USER_SELECT_COLUMNS = (
    "SELECT telegram_id, username, language, trading_style, risk_percent, "
    "timeframe, created_at, strategy, notifications_enabled, status, last_activity, phone_hash, trial_started_at"
)


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
        status=row["status"],
        last_activity=row["last_activity"],
        phone_hash=row["phone_hash"],
        trial_started_at=row["trial_started_at"],
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
        status: str = "NEW",
    ) -> Optional[UserRecord]:
        """
        Inserts a new user with safe defaults. Returns None (no insert
        performed) if telegram_id already exists -- never raises for a
        duplicate, whether caught up front or via a lost race against
        a concurrent insert (IntegrityError on the UNIQUE constraint).
        A brand new user starts life as status=NEW (Phase 45); promotion
        to ACTIVE happens on their next real interaction, via
        update_last_activity() -- not at registration time.
        """
        if self.user_exists(telegram_id):
            logger.info(f"User already exists: telegram_id={telegram_id}")
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        query = """
        INSERT INTO users (
            telegram_id, username, language, trading_style,
            risk_percent, timeframe, created_at, strategy, notifications_enabled, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            str(telegram_id), username, language, trading_style, risk_percent,
            timeframe, created_at, strategy, notifications_enabled, status,
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
                _USER_SELECT_COLUMNS + " FROM users WHERE telegram_id = ?", (str(telegram_id),)
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def count_users(self) -> int:
        """Total registered users. Used by AdminService statistics."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            row = cursor.fetchone()
            return row["count"] if row else 0

    def get_all_users(self) -> List[UserRecord]:
        """All registered users. Used by AdminService.broadcast()."""
        with self.db as conn:
            cursor = conn.execute(_USER_SELECT_COLUMNS + " FROM users")
            return [_row_to_record(row) for row in cursor.fetchall()]

    def count_active_users(self) -> int:
        """
        Users with notifications_enabled=1 -- the closest available
        "active" signal (no dedicated activity-tracking column exists;
        Phase 41 audit chose not to add one for a single display field).
        """
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM users WHERE notifications_enabled = 1")
            row = cursor.fetchone()
            return row["count"] if row else 0

    def count_users_created_today(self) -> int:
        """Users whose created_at falls on today's UTC date."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM users WHERE date(created_at) = date('now')")
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
            "status", "last_activity", "phone_hash", "trial_started_at",
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

    def enable_notifications(self, telegram_id) -> bool:
        return self.update_user(telegram_id, notifications_enabled=True)

    def disable_notifications(self, telegram_id) -> bool:
        return self.update_user(telegram_id, notifications_enabled=False)

    def get_notification_users(self) -> List[UserRecord]:
        """
        Users with notifications_enabled=1 -- the recipient list for a
        notification-respecting broadcast/signal send (Phase 43).
        """
        with self.db as conn:
            cursor = conn.execute(_USER_SELECT_COLUMNS + " FROM users WHERE notifications_enabled = 1")
            return [_row_to_record(row) for row in cursor.fetchall()]

    def update_status(self, telegram_id, status: str) -> bool:
        """
        Sets the user's lifecycle status directly (NEW/ACTIVE/BANNED).
        Deliberately separate from subscription plan/status (Phase 42) --
        this table never stores FREE/PREMIUM/VIP.
        """
        return self.update_user(telegram_id, status=status)

    def get_status(self, telegram_id) -> Optional[str]:
        """The user's lifecycle status, or None if telegram_id is unknown."""
        user = self.get_user(telegram_id)
        return user.status if user is not None else None

    def update_last_activity(self, telegram_id) -> bool:
        """
        Updates last_activity to now, and promotes a NEW user to
        ACTIVE (Phase 45: "first successful interaction" -> ACTIVE). A
        BANNED user's status is left untouched here -- activity
        tracking must never silently un-ban someone. Returns False if
        telegram_id has no user row (nothing to update).
        """
        user = self.get_user(telegram_id)
        if user is None:
            return False

        fields = {"last_activity": datetime.now(timezone.utc).isoformat()}
        if user.status == "NEW":
            fields["status"] = "ACTIVE"

        return self.update_user(telegram_id, **fields)

    def get_active_users(self) -> List[UserRecord]:
        """Users with status='ACTIVE'."""
        with self.db as conn:
            cursor = conn.execute(_USER_SELECT_COLUMNS + " FROM users WHERE status = 'ACTIVE'")
            return [_row_to_record(row) for row in cursor.fetchall()]

    def count_by_status(self, status: str) -> int:
        """Count of users with the given lifecycle status (NEW/ACTIVE/BANNED)."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM users WHERE status = ?", (status,))
            row = cursor.fetchone()
            return row["count"] if row else 0

    def ban_user(self, telegram_id) -> bool:
        return self.update_user(telegram_id, status="BANNED")

    def activate_user(self, telegram_id) -> bool:
        return self.update_user(telegram_id, status="ACTIVE")

    def set_phone_hash(self, telegram_id, phone_hash: str) -> bool:
        """
        Records an already-hashed phone number (Phase 61.4 TASK 4) --
        this repository never receives or stores a raw phone number;
        hashing happens in core.phone_hash.hash_phone_number() before
        this method is ever called.
        """
        return self.update_user(telegram_id, phone_hash=phone_hash)

    def get_users_by_phone_hash(self, phone_hash: str) -> List[UserRecord]:
        """
        Every user row sharing this phone_hash -- used by
        ai/access/identity_checker.py (Phase 61.4 TASK 5) to detect the
        same phone number re-registering under a different telegram_id
        for repeated free trials. Ordinarily 0 or 1 rows; more than 1
        means exactly the abuse pattern that lookup exists to catch.
        """
        with self.db as conn:
            cursor = conn.execute(
                _USER_SELECT_COLUMNS + " FROM users WHERE phone_hash = ?", (phone_hash,)
            )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def set_trial_started_at(self, telegram_id, started_at_iso: str) -> bool:
        """
        Records the ISO-8601 timestamp this user's free trial started
        (Phase 61.5 TASK 4) -- same one-shot-set convention as
        `set_phone_hash()`. A caller (telegram/user_service.py) is
        responsible for only calling this once per user (a second call
        would silently reset the trial window, which is
        `telegram/user_service.py`'s job to prevent, not this
        repository's).
        """
        return self.update_user(telegram_id, trial_started_at=started_at_iso)
