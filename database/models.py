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
    foundation). No relation to the signals table -- separate,
    independently-initialized table.
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
        updated_at TEXT
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (users table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize users schema: {e}")
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
