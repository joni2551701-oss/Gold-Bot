import sqlite3
from core.logger import setup_logger

logger = setup_logger("DatabaseModels")

def init_schema(connection: sqlite3.Connection):
    """
    Defines and creates the signals table schema, then migrates any
    pre-existing table (created before Phase 39) to include the newer
    display columns. Safe to call on every construction: CREATE TABLE
    IF NOT EXISTS is a no-op once the table exists, and the migration
    step below only adds a column that isn't already there.
    """
    query = """
    CREATE TABLE IF NOT EXISTS signals (
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
        closed_at TEXT,
        strategy TEXT DEFAULT 'UNKNOWN',
        timeframe TEXT DEFAULT 'M15',
        rr_ratio REAL DEFAULT 0,
        ai_decision TEXT DEFAULT 'N/A',
        risk_status TEXT DEFAULT 'N/A',
        risk_amount REAL DEFAULT 0,
        signal_status TEXT DEFAULT 'NEW'
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (signals table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database schema: {e}")
        raise

    _migrate_signals_schema(connection)
    _create_signals_indexes(connection)


def _create_signals_indexes(connection: sqlite3.Connection):
    """
    Phase 50 index audit: 'status' (SignalRepository.get_open_signals()/
    get_closed_signals()) and 'created_at' (get_latest_signal()/
    get_recent_signals()'s ORDER BY) are the two columns actually
    filtered/sorted on today. signal_id already has an implicit index
    via its UNIQUE constraint, so it is not duplicated here.
    CREATE INDEX IF NOT EXISTS is idempotent -- safe on every
    construction, including against a database that already has these
    indexes from a prior run.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status)",
        "CREATE INDEX IF NOT EXISTS idx_signals_created_at ON signals(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create signals indexes: {e}")
        raise


def _migrate_signals_schema(connection: sqlite3.Connection):
    """
    Adds the Phase 39 display columns to a 'signals' table created
    before this phase. SQLite has no "ADD COLUMN IF NOT EXISTS", so
    each column's presence is checked via PRAGMA table_info first --
    on a fresh table (already created with all columns above) every
    column is already present and this is a no-op.
    """
    new_columns = [
        ("strategy", "TEXT DEFAULT 'UNKNOWN'"),
        ("timeframe", "TEXT DEFAULT 'M15'"),
        ("rr_ratio", "REAL DEFAULT 0"),
        ("ai_decision", "TEXT DEFAULT 'N/A'"),
        ("risk_status", "TEXT DEFAULT 'N/A'"),
        ("risk_amount", "REAL DEFAULT 0"),
        ("signal_status", "TEXT DEFAULT 'NEW'"),
    ]

    try:
        cursor = connection.execute("PRAGMA table_info(signals)")
        existing_columns = {row[1] for row in cursor.fetchall()}
    except sqlite3.Error as e:
        logger.error(f"Failed to inspect signals table for migration: {e}")
        raise

    migrated = False
    for column_name, column_def in new_columns:
        if column_name in existing_columns:
            continue
        try:
            connection.execute(f"ALTER TABLE signals ADD COLUMN {column_name} {column_def}")
            logger.info(f"Migrated signals table: added column '{column_name}'.")
            migrated = True
        except sqlite3.Error as e:
            logger.error(f"Failed to add column '{column_name}' to signals table: {e}")
            raise

    if migrated:
        connection.commit()


def init_user_schema(connection: sqlite3.Connection):
    """
    Defines and creates the users table schema (Telegram user profile
    foundation), then migrates any pre-existing table (created before
    Phase 40/45) to include the newer settings/lifecycle columns. No
    relation to the signals table -- separate, independently-initialized
    table.
    """
    query = """
    CREATE TABLE IF NOT EXISTS users (
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
        last_activity TIMESTAMP
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (users table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize users schema: {e}")
        raise

    _migrate_users_schema(connection)
    _create_users_indexes(connection)


def _create_users_indexes(connection: sqlite3.Connection):
    """
    Phase 50 index audit: 'status' is filtered by get_active_users()/
    count_by_status(); 'created_at' is filtered by
    count_users_created_today() (via date(created_at) = date('now') --
    note this specific function-wrapped predicate will not itself be
    accelerated by a plain B-tree index, but the column is kept
    indexed for any future direct created_at range query). telegram_id
    already has an implicit index via its UNIQUE constraint, so it is
    not duplicated here. CREATE INDEX IF NOT EXISTS is idempotent.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_users_status ON users(status)",
        "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create users indexes: {e}")
        raise


def _migrate_users_schema(connection: sqlite3.Connection):
    """
    Adds the Phase 40 settings columns and Phase 45 lifecycle columns
    (status, last_activity) to a 'users' table created before those
    phases. SQLite has no "ADD COLUMN IF NOT EXISTS", so each column's
    presence is checked via PRAGMA table_info first -- on a fresh
    table (already created with all columns above) every column is
    already present and this is a no-op. Idempotent: safe to call
    every time a UserRepository is constructed, including a second run
    against an already-migrated table (no duplicate-column error).
    """
    new_columns = [
        ("strategy", "TEXT DEFAULT 'Liquidity Sweep'"),
        ("notifications_enabled", "INTEGER DEFAULT 1"),
        ("status", "TEXT DEFAULT 'NEW'"),
        ("last_activity", "TIMESTAMP"),
    ]

    try:
        cursor = connection.execute("PRAGMA table_info(users)")
        existing_columns = {row[1] for row in cursor.fetchall()}
    except sqlite3.Error as e:
        logger.error(f"Failed to inspect users table for migration: {e}")
        raise

    migrated = False
    for column_name, column_def in new_columns:
        if column_name in existing_columns:
            continue
        try:
            connection.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}")
            logger.info(f"Migrated users table: added column '{column_name}'.")
            migrated = True
        except sqlite3.Error as e:
            logger.error(f"Failed to add column '{column_name}' to users table: {e}")
            raise

    if migrated:
        connection.commit()


def init_subscription_schema(connection: sqlite3.Connection):
    """
    Defines and creates the subscriptions table schema (Phase 42
    Subscription Foundation). Independent of the users/signals/admins
    tables -- linked to users via telegram_id, not a SQL foreign key
    (none of the other tables here use one either). Brand new table,
    so unlike init_schema()/init_user_schema() there is no pre-Phase-42
    column set to migrate from: CREATE TABLE IF NOT EXISTS alone is
    safe for both a fresh database and an existing one that simply
    doesn't have this table yet.
    """
    query = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        plan TEXT DEFAULT 'FREE',
        status TEXT DEFAULT 'ACTIVE',
        started_at TEXT NOT NULL,
        expires_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (subscriptions table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize subscriptions schema: {e}")
        raise


def init_feedback_schema(connection: sqlite3.Connection):
    """
    Defines and creates the feedback table schema (Phase 46 Feedback
    System Foundation). Independent of the other tables. Brand new
    table -- no migration needed (same reasoning as
    init_subscription_schema(), Phase 42): CREATE TABLE IF NOT EXISTS
    alone is safe for both a fresh database and an existing one that
    simply doesn't have this table yet. telegram_id/created_at use
    TEXT (not INTEGER/TIMESTAMP) to match every other table's
    convention in this schema (str(telegram_id), ISO-format
    timestamps) -- SQLite's dynamic typing makes this a pure
    consistency choice, not a functional one.
    """
    query = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'OPEN',
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (feedback table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize feedback schema: {e}")
        raise

    _create_feedback_indexes(connection)


def _create_feedback_indexes(connection: sqlite3.Connection):
    """
    Phase 50 index audit: 'status' is filtered by count_open_feedback();
    'created_at' is sorted on by get_all_feedback()'s ORDER BY.
    telegram_id has no current WHERE-clause usage anywhere in
    FeedbackRepository, so it is intentionally not indexed here (no
    query would benefit today -- see docs/DATABASE.md).
    CREATE INDEX IF NOT EXISTS is idempotent.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_feedback_status ON feedback(status)",
        "CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create feedback indexes: {e}")
        raise


def init_admin_schema(connection: sqlite3.Connection):
    """
    Defines and creates the admins table schema (Owner/Admin permission
    foundation). Independent of the signals/users tables.
    """
    query = """
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'ADMIN',
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (admins table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize admins schema: {e}")
        raise
