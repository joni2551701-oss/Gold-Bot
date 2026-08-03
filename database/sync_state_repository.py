"""
Database Layer — Sync State repository (Phase 59.5: Historical Data
Collection & Validation Foundation, TASK 2). Mirrors
database/raw_candle_repository.py's own structure (CRUD only, no
business logic, idempotent schema init in __init__).
"""

from datetime import datetime, timezone
from typing import Optional

from database.database import Database
from database.models import init_sync_state_schema
from database.sync_state_models import SyncState
from core_layer.logger.logger import setup_logger

logger = setup_logger("SyncStateRepository")

_SYNC_STATE_SELECT_COLUMNS = "SELECT provider, symbol, timeframe, last_timestamp, updated_at"


def _row_to_record(row) -> SyncState:
    return SyncState(
        provider=row["provider"],
        symbol=row["symbol"],
        timeframe=row["timeframe"],
        last_timestamp=datetime.fromisoformat(row["last_timestamp"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


class SyncStateRepository:
    """Handles CRUD operations for the 'sync_state' table. Database access only -- no collection/provider logic."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_sync_state_schema(conn)

    def get_sync_state(self, provider: str, symbol: str, timeframe: str) -> Optional[SyncState]:
        """Returns None when no sync state exists yet for this key -- never raises for a lookup miss."""
        with self.db as conn:
            cursor = conn.execute(
                _SYNC_STATE_SELECT_COLUMNS + " FROM sync_state WHERE provider = ? AND symbol = ? AND timeframe = ?",
                (provider, symbol, timeframe),
            )
            row = cursor.fetchone()
            return _row_to_record(row) if row else None

    def update_sync_state(self, provider: str, symbol: str, timeframe: str, last_timestamp: datetime) -> SyncState:
        """
        Upserts the (provider, symbol, timeframe) row: UPDATE if a row
        already exists (same check-then-branch idiom as
        SubscriptionRepository._update()/create_subscription()),
        otherwise INSERT. Re-reads and returns the row as actually
        written (same "return the canonical DB-truth object" idiom as
        SubscriptionRepository.create_subscription()), not a
        client-side reconstruction -- so the returned `updated_at`
        always matches what was actually persisted.
        """
        updated_at = datetime.now(timezone.utc).isoformat()
        with self.db as conn:
            cursor = conn.execute(
                "UPDATE sync_state SET last_timestamp = ?, updated_at = ? "
                "WHERE provider = ? AND symbol = ? AND timeframe = ?",
                (last_timestamp.isoformat(), updated_at, provider, symbol, timeframe),
            )
            if cursor.rowcount == 0:
                conn.execute(
                    "INSERT INTO sync_state (provider, symbol, timeframe, last_timestamp, updated_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (provider, symbol, timeframe, last_timestamp.isoformat(), updated_at),
                )

        return self.get_sync_state(provider, symbol, timeframe)

    def get_all_sync_states(self) -> list:
        """Every tracked (provider, symbol, timeframe)'s current sync state -- for a future /sync_status listing."""
        with self.db as conn:
            cursor = conn.execute(_SYNC_STATE_SELECT_COLUMNS + " FROM sync_state")
            return [_row_to_record(row) for row in cursor.fetchall()]
