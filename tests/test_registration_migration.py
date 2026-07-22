"""
V2 Phase 3 -- database.models._backfill_registration_state() tests.

Simulates a pre-Phase-3 'users' table (every column up through Phase
61.5's trial_started_at, but no registration_step/registration_completed)
via hand-written SQL, then calls init_user_schema() (the real migration
path UserRepository() triggers on construction) and verifies the
backfill: a row with phone_hash already set is treated as already
having completed registration under the old (optional Phone Share)
model, one without still needs the now-mandatory Phone Share step but
not Language (never gated for pre-existing users either).
"""

import sqlite3
from datetime import datetime, timezone

from database.database import Database
from database.models import init_user_schema


def _create_pre_phase3_users_table(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT UNIQUE NOT NULL,
            username TEXT,
            language TEXT DEFAULT 'UZ',
            trading_style TEXT DEFAULT 'Intraday',
            risk_percent REAL DEFAULT 2.0,
            timeframe TEXT DEFAULT 'M15',
            created_at TEXT NOT NULL,
            updated_at TEXT,
            strategy TEXT DEFAULT 'Liquidity Sweep',
            notifications_enabled INTEGER DEFAULT 1,
            status TEXT DEFAULT 'NEW',
            last_activity TIMESTAMP,
            phone_hash TEXT,
            trial_started_at TEXT
        );
        """
    )
    conn.commit()


def _insert_pre_phase3_user(conn, telegram_id, phone_hash=None):
    conn.execute(
        "INSERT INTO users (telegram_id, username, language, trading_style, risk_percent, "
        "timeframe, created_at, phone_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (telegram_id, "alice", "UZ", "Intraday", 2.0, "M15", datetime.now(timezone.utc).isoformat(), phone_hash),
    )
    conn.commit()


def test_pre_existing_user_with_phone_hash_backfills_as_complete():
    db = Database()
    with db as conn:
        _create_pre_phase3_users_table(conn)
        _insert_pre_phase3_user(conn, "111", phone_hash="already-hashed-value")

    with db as conn:
        init_user_schema(conn)

    with db as conn:
        row = conn.execute(
            "SELECT registration_step, registration_completed FROM users WHERE telegram_id = ?", ("111",)
        ).fetchone()

    assert row["registration_step"] == "COMPLETE"
    assert row["registration_completed"] == 1


def test_pre_existing_user_without_phone_hash_backfills_as_phone_step():
    db = Database()
    with db as conn:
        _create_pre_phase3_users_table(conn)
        _insert_pre_phase3_user(conn, "222", phone_hash=None)

    with db as conn:
        init_user_schema(conn)

    with db as conn:
        row = conn.execute(
            "SELECT registration_step, registration_completed FROM users WHERE telegram_id = ?", ("222",)
        ).fetchone()

    assert row["registration_step"] == "PHONE"
    assert row["registration_completed"] == 0


def test_backfill_never_reopens_a_completed_registration_on_second_migration_call():
    """Idempotency: calling init_user_schema() twice must not re-run the backfill and flip state."""
    db = Database()
    with db as conn:
        _create_pre_phase3_users_table(conn)
        _insert_pre_phase3_user(conn, "111", phone_hash="already-hashed-value")

    with db as conn:
        init_user_schema(conn)
    with db as conn:
        init_user_schema(conn)

    with db as conn:
        row = conn.execute(
            "SELECT registration_step, registration_completed FROM users WHERE telegram_id = ?", ("111",)
        ).fetchone()

    assert row["registration_step"] == "COMPLETE"
    assert row["registration_completed"] == 1


def test_a_brand_new_table_gets_column_defaults_not_the_backfill():
    """
    A table created fresh (already via the current init_user_schema())
    never passes through _backfill_registration_state() -- new rows
    get the CREATE TABLE column defaults (LANGUAGE/incomplete), not the
    pre-existing-user backfill rule.
    """
    from database.user_repository import UserRepository

    repo = UserRepository()
    user = repo.create_user("333", username="brandnew")

    assert user.registration_step == "LANGUAGE"
    assert user.registration_completed is False
