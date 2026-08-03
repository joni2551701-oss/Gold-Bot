"""
Database Layer — Raw Candle repository (Phase 59.3, TASK 2).
Mirrors database/admin_repository.py's own structure (CRUD only, no
business logic, idempotent schema init in __init__).
"""

import sqlite3
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

from database.database import Database
from database.models import init_raw_candle_schema
from database.raw_candle_models import RawCandle, from_market_candle
from core_layer.logger.logger import setup_logger

if TYPE_CHECKING:
    from data_layer.providers.base_provider import MarketCandle

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

    def save_market_candles(self, candles: List['MarketCandle'], provider: Optional[str] = None) -> int:
        """
        Phase 59 Real Market Validation Foundation, TASK 3 -- adapts
        each data_layer/providers/base_provider.MarketCandle (e.g.
        TwelveDataProvider.get_candles()'s real output) via
        database.raw_candle_models.from_market_candle() and saves it,
        closing the loop between the provider layer (Phase 59.1/59.2)
        and this table (Phase 59.3) for the first time. `provider`
        overrides each candle's own `.provider` when supplied. Returns
        the count actually inserted (duplicates excluded), same
        convention as save_candles(). Never raises for a duplicate;
        DOES raise (via from_market_candle()) if a candle has no
        provider at all and none was supplied -- a genuine data-
        integrity gap, not silently skipped.
        """
        raw_candles = [from_market_candle(candle, provider=provider) for candle in candles]
        return self.save_candles(raw_candles)

    def get_candles(
        self, symbol: str, timeframe: str, provider: Optional[str] = None, limit: int = 500
    ) -> List[RawCandle]:
        """Chronologically ascending (oldest first), most recent `limit` rows -- same ordering convention as data_layer.providers.twelve_data_client.TwelveDataClient.fetch_candles()."""
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

    def get_candles_range(
        self, symbol: str, timeframe: str, start: datetime, end: datetime, provider: Optional[str] = None
    ) -> List[RawCandle]:
        """
        Phase 60.1 (Historical Replay Engine, TASK 1 reuse audit) --
        get_candles() only supports "most recent N rows" (no date
        bound), which a Replay session over a fixed historical window
        needs. Additive: a new method, existing get_candles()
        untouched. Chronologically ascending (oldest first), same
        ordering convention as get_candles().
        """
        with self.db as conn:
            if provider is not None:
                cursor = conn.execute(
                    _CANDLE_SELECT_COLUMNS + " FROM raw_candles "
                    "WHERE symbol = ? AND timeframe = ? AND provider = ? "
                    "AND timestamp >= ? AND timestamp <= ? "
                    "ORDER BY timestamp ASC",
                    (symbol, timeframe, provider, start.isoformat(), end.isoformat()),
                )
            else:
                cursor = conn.execute(
                    _CANDLE_SELECT_COLUMNS + " FROM raw_candles "
                    "WHERE symbol = ? AND timeframe = ? "
                    "AND timestamp >= ? AND timestamp <= ? "
                    "ORDER BY timestamp ASC",
                    (symbol, timeframe, start.isoformat(), end.isoformat()),
                )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def count_candles(self, symbol: str, timeframe: str) -> int:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM raw_candles WHERE symbol = ? AND timeframe = ?",
                (symbol, timeframe),
            )
            row = cursor.fetchone()
            return row["count"] if row else 0
