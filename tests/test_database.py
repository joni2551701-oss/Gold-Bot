"""
Phase 47 — Database Audit tests.

Schema shape, defaults, duplicate prevention, and migration safety
across all five tables (users, admins, signals, subscriptions,
feedback). No signal-generation, AI, or pipeline logic is exercised
here -- pure persistence layer.
"""

import sqlite3

import config


def _columns(table: str) -> dict:
    conn = sqlite3.connect(config.Config.DB_PATH)
    try:
        return {row[1]: row[4] for row in conn.execute(f"PRAGMA table_info({table})")}
    finally:
        conn.close()


def test_users_table_schema_and_defaults():
    from database_layer.user_repository.user_repository import UserRepository

    UserRepository()
    cols = _columns("users")
    for field in (
        "id", "telegram_id", "username", "language", "risk_percent",
        "strategy", "timeframe", "notifications_enabled", "status",
        "last_activity", "created_at",
    ):
        assert field in cols, f"users.{field} missing"
    assert cols["language"] == "'UZ'"
    assert cols["status"] == "'NEW'"
    assert cols["notifications_enabled"] == "1"


def test_users_duplicate_telegram_id_blocked_and_update_works():
    from database_layer.user_repository.user_repository import UserRepository

    repo = UserRepository()
    created = repo.create_user(telegram_id="42", username="alice")
    assert created is not None

    duplicate = repo.create_user(telegram_id="42", username="bob")
    assert duplicate is None, "duplicate telegram_id must not create a second row"

    assert repo.update_user("42", risk_percent=5.0) is True
    assert repo.get_user("42").risk_percent == 5.0


def test_admins_table_schema():
    from database_layer.user_repository.admin_repository import AdminRepository

    AdminRepository()
    cols = _columns("admins")
    for field in ("id", "telegram_id", "role", "created_at"):
        assert field in cols
    assert cols["role"] == "'ADMIN'"


def test_signals_table_schema():
    from database_layer.trade_repository.signal_repository import SignalRepository

    SignalRepository()
    cols = _columns("signals")
    for field in (
        "symbol", "direction", "strategy", "timeframe",
        "entry_zone_min", "stop_loss", "take_profit_1", "rr_ratio",
        "confidence_score", "ai_decision", "risk_status", "signal_status",
        "created_at",
    ):
        assert field in cols, f"signals.{field} missing"


def test_signals_save_read_history():
    from database_layer.trade_repository.signal_repository import SignalRepository

    repo = SignalRepository()
    repo.create_signal({
        "signal_id": "sig-db-1",
        "symbol": "XAUUSD",
        "direction": "BUY",
        "entry_zone_min": 2000.0,
        "entry_zone_max": 2000.0,
        "stop_loss": 1990.0,
        "take_profit_1": 2030.0,
        "take_profit_2": 0.0,
        "risk_percent": 0.0,
        "lot_size": 0.0,
        "strategy_name": "Liquidity Sweep",
        "confidence_score": 0.8,
        "ai_explanation": "test",
    })

    row = repo.get_signal("sig-db-1")
    assert row is not None
    assert row["symbol"] == "XAUUSD"

    latest = repo.get_latest_signal()
    assert latest is not None
    assert latest["signal_id"] == "sig-db-1"

    history = repo.get_recent_signals(limit=5)
    assert len(history) == 1


def test_subscriptions_table_schema():
    from database_layer.user_repository.subscription_repository import SubscriptionRepository

    SubscriptionRepository()
    cols = _columns("subscriptions")
    for field in ("telegram_id", "plan", "status", "started_at", "expires_at"):
        assert field in cols
    assert cols["plan"] == "'FREE'"
    assert cols["status"] == "'ACTIVE'"


def test_feedback_table_schema():
    from database_layer.user_repository.feedback_repository import FeedbackRepository

    FeedbackRepository()
    cols = _columns("feedback")
    for field in ("id", "telegram_id", "message", "status", "created_at"):
        assert field in cols
    assert cols["status"] == "'OPEN'"


def test_migration_old_signals_table_backfills_phase39_columns():
    """A signals table created before Phase 39 must gain the display columns without losing data."""
    conn = sqlite3.connect(config.Config.DB_PATH)
    conn.execute("""
        CREATE TABLE signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_id TEXT UNIQUE NOT NULL,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            entry_zone_min REAL NOT NULL,
            entry_zone_max REAL NOT NULL,
            stop_loss REAL NOT NULL,
            take_profit_1 REAL NOT NULL,
            take_profit_2 REAL NOT NULL,
            risk_percent REAL NOT NULL,
            lot_size REAL NOT NULL,
            strategy_name TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            ai_explanation TEXT,
            status TEXT DEFAULT 'OPEN',
            result TEXT DEFAULT 'OPEN',
            created_at TEXT NOT NULL,
            closed_at TEXT
        );
    """)
    conn.execute("""
        INSERT INTO signals (signal_id, symbol, direction, entry_zone_min, entry_zone_max,
            stop_loss, take_profit_1, take_profit_2, risk_percent, lot_size, strategy_name,
            confidence_score, ai_explanation, created_at)
        VALUES ('legacy-1', 'XAUUSD', 'BUY', 2000.0, 2000.0, 1995.0, 2010.0, 0.0, 0.0, 0.0,
            'Legacy', 0.7, 'legacy', '2025-06-01T00:00:00+00:00')
    """)
    conn.commit()
    conn.close()

    from database_layer.trade_repository.signal_repository import SignalRepository

    repo = SignalRepository()  # triggers migration
    row = repo.get_signal("legacy-1")
    assert row is not None
    assert row["confidence_score"] == 0.7  # original data intact
    assert row["strategy"] == "UNKNOWN"
    assert row["signal_status"] == "NEW"

    SignalRepository()  # second run must not raise (idempotent, no duplicate-column error)


def test_migration_old_users_table_backfills_phase40_and_phase45_columns():
    """A users table created before Phase 40/45 must gain settings + lifecycle columns without losing data."""
    conn = sqlite3.connect(config.Config.DB_PATH)
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT UNIQUE NOT NULL,
            username TEXT,
            language TEXT DEFAULT 'UZ',
            trading_style TEXT DEFAULT 'Intraday',
            risk_percent REAL DEFAULT 2.0,
            timeframe TEXT DEFAULT 'M15',
            created_at TEXT NOT NULL,
            updated_at TEXT
        );
    """)
    conn.execute("""
        INSERT INTO users (telegram_id, username, created_at)
        VALUES ('123', 'oldie', '2025-01-01T00:00:00+00:00')
    """)
    conn.commit()
    conn.close()

    from database_layer.user_repository.user_repository import UserRepository

    repo = UserRepository()  # triggers migration
    row = repo.get_user("123")
    assert row is not None
    assert row.username == "oldie"  # original data intact
    assert row.strategy == "Liquidity Sweep"
    assert row.notifications_enabled is True
    assert row.status == "NEW"
    assert row.last_activity is None

    UserRepository()  # second run must not raise (idempotent)


def test_migration_adds_subscriptions_table_to_pre_phase42_database():
    """A database with users/admins but no subscriptions table must gain it safely."""
    from database_layer.user_repository.user_repository import UserRepository
    from database_layer.user_repository.admin_repository import AdminRepository

    UserRepository()
    AdminRepository()

    conn = sqlite3.connect(config.Config.DB_PATH)
    tables_before = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert "subscriptions" not in tables_before

    from database_layer.user_repository.subscription_repository import SubscriptionRepository

    SubscriptionRepository()

    conn = sqlite3.connect(config.Config.DB_PATH)
    tables_after = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert "subscriptions" in tables_after
