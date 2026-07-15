"""
Database Layer — Raw Candle repository (Phase 59.3, TASK 2).
Mirrors database/admin_repository.py's own structure (CRUD only, no
business logic, idempotent schema init in __init__).
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from database.database import Database
from database.models import init_raw_candle_schema
from database.raw_candle_models import RawCandle
from core.logger import setup_logger

logger = setup_logger("RawCandleRepository")

_CANDLE_SELECT_COLUMNS = (
    "SELECT symbol, timeframe, timestamp, open, high, low, close, volume, provider, created_at"
)


def _row_to_record(row) -> RawCandle:
    return RawCandle(
        symbol=row["symbol"],
        timeframe=row["timeframe"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        open=row["open"],
        high=row["high"],
        low=row["low"],
        close=row["close"],
        volume=row["volume"],
        provider=row["provider"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class RawCandleRepository:
    """Handles CRUD operations for the 'raw_candles' table. Database access only -- no normalization, no provider logic."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_raw_candle_schema(conn)

    def save_candle(self, candle: RawCandle) -> bool:
        """
        Inserts one candle. Returns False (no insert performed) for a
        duplicate (symbol, timeframe, timestamp, provider) -- never
        raises for a duplicate, whether caught by a pre-check or a
        lost race (IntegrityError on the UNIQUE constraint), same
        posture as AdminRepository.add_admin().
        """
        query = """
        INSERT INTO raw_candles (symbol, timeframe, timestamp, open, high, low, close, volume, provider, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            candle.symbol, candle.timeframe, candle.timestamp.isoformat(),
            candle.open, candle.high, candle.low, candle.close, candle.volume,
            candle.provider, candle.created_at.isoformat(),
        )
        with self.db as conn:
            try:
                conn.execute(query, params)
                return True
            except sqlite3.IntegrityError:
                logger.info(
                    f"Duplicate raw candle skipped: {candle.symbol}|{candle.timeframe}|"
                    f"{candle.timestamp.isoformat()}|{candle.provider}"
                )
                return False

    def save_candles(self, candles: List[RawCandle]) -> int:
        """Saves each candle via save_candle(); returns the count actually inserted (duplicates excluded). Never raises: an empty list saves 0."""
        return sum(1 for candle in candles if self.save_candle(candle))

    def get_candles(
        self, symbol: str, timeframe: str, provider: Optional[str] = None, limit: int = 500
    ) -> List[RawCandle]:
        """Chronologically ascending (oldest first), most recent `limit` rows -- same ordering convention as data.twelve_data_client.TwelveDataClient.fetch_candles()."""
        with self.db as conn:
            if provider is not None:
                cursor = conn.execute(
                    _CANDLE_SELECT_COLUMNS + " FROM raw_candles "
                    "WHERE symbol = ? AND timeframe = ? AND provider = ? "
                    "ORDER BY timestamp DESC LIMIT ?",
                    (symbol, timeframe, provider, limit),
                )
            else:
                cursor = conn.execute(
                    _CANDLE_SELECT_COLUMNS + " FROM raw_candles "
                    "WHERE symbol = ? AND timeframe = ? "
                    "ORDER BY timestamp DESC LIMIT ?",
                    (symbol, timeframe, limit),
                )
            rows = cursor.fetchall()
            return [_row_to_record(row) for row in reversed(rows)]

    def count_candles(self, symbol: str, timeframe: str) -> int:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM raw_candles WHERE symbol = ? AND timeframe = ?",
                (symbol, timeframe),
            )
            row = cursor.fetchone()
            return row["count"] if row else 0
