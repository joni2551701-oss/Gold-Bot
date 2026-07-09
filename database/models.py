import sqlite3
from core.logger import setup_logger

logger = setup_logger("DatabaseModels")

def init_schema(connection: sqlite3.Connection):
    """
    Defines and creates the signals table schema.
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
        closed_at TEXT
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (signals table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database schema: {e}")
        raise
