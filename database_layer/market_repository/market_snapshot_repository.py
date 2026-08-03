"""
Database Layer — Market Snapshot repository (Phase 59.3, TASK 2).
Mirrors database_layer/user_repository/admin_repository.py's own structure.
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from database_layer.database_manager.database import Database
from database_layer.database_manager.models import init_market_snapshot_schema
from database_layer.market_repository.market_snapshot_models import MarketSnapshotRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("MarketSnapshotRepository")

_SNAPSHOT_SELECT_COLUMNS = (
    "SELECT market_snapshot_id, symbol, timeframe, provider, candle_count, "
    "first_timestamp, last_timestamp, candles_reference, data_quality, created_at"
)


def _row_to_record(row) -> MarketSnapshotRecord:
    return MarketSnapshotRecord(
        market_snapshot_id=row["market_snapshot_id"],
        symbol=row["symbol"],
        timeframe=row["timeframe"],
        provider=row["provider"],
        candle_count=row["candle_count"],
        first_timestamp=datetime.fromisoformat(row["first_timestamp"]) if row["first_timestamp"] else None,
        last_timestamp=datetime.fromisoformat(row["last_timestamp"]) if row["last_timestamp"] else None,
        candles_reference=row["candles_reference"],
        data_quality=row["data_quality"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class MarketSnapshotRepository:
    """Handles CRUD operations for the 'market_snapshots' table. Database access only."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_market_snapshot_schema(conn)

    def save_snapshot(self, record: MarketSnapshotRecord) -> bool:
        """Inserts one snapshot. Returns False for a duplicate market_snapshot_id (its own UNIQUE constraint) -- never raises."""
        query = """
        INSERT INTO market_snapshots (
            market_snapshot_id, symbol, timeframe, provider, candle_count,
            first_timestamp, last_timestamp, candles_reference, data_quality, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            record.market_snapshot_id, record.symbol, record.timeframe, record.provider,
            record.candle_count,
            record.first_timestamp.isoformat() if record.first_timestamp else None,
            record.last_timestamp.isoformat() if record.last_timestamp else None,
            record.candles_reference, record.data_quality, record.created_at.isoformat(),
        )
        with self.db as conn:
            try:
                conn.execute(query, params)
                return True
            except sqlite3.IntegrityError:
                logger.warning(f"Duplicate market_snapshot_id insert prevented: {record.market_snapshot_id}")
                return False

    def get_snapshot(self, market_snapshot_id: str) -> Optional[MarketSnapshotRecord]:
        with self.db as conn:
            cursor = conn.execute(
                _SNAPSHOT_SELECT_COLUMNS + " FROM market_snapshots WHERE market_snapshot_id = ?",
                (market_snapshot_id,),
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def get_recent_snapshots(self, symbol: str, timeframe: str, limit: int = 20) -> List[MarketSnapshotRecord]:
        """Most recent `limit` snapshots for (symbol, timeframe), newest first. Empty list if none."""
        with self.db as conn:
            cursor = conn.execute(
                _SNAPSHOT_SELECT_COLUMNS + " FROM market_snapshots "
                "WHERE symbol = ? AND timeframe = ? ORDER BY created_at DESC LIMIT ?",
                (symbol, timeframe, limit),
            )
            return [_row_to_record(row) for row in cursor.fetchall()]
