"""
Database Layer — Sync State persistence model (Phase 59.5: Historical
Data Collection & Validation Foundation, TASK 2).

Tracks, per (provider, symbol, timeframe), the timestamp of the most
recently collected candle -- so
data/historical_data_collector.py's sync_historical_candles() can
resume from where it left off instead of re-fetching a large window
every call. Independent of every other table (no SQL foreign key,
same convention as every other table pair in this schema); no relation
to raw_candles beyond sharing the same (symbol, timeframe, provider)
values by convention, never enforced structurally.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class SyncState:
    """
    Mirrors the 'sync_state' table row shape. `id` is intentionally
    excluded -- repository-internal detail, not part of the record a
    caller needs (same convention as database.raw_candle_models.RawCandle).
    last_timestamp: the latest candle timestamp successfully collected
        and saved for this (provider, symbol, timeframe) -- not
        "now()", not "when this row was written".
    updated_at: when this sync state row was last written.
    """
    provider: str
    symbol: str
    timeframe: str
    last_timestamp: datetime
    updated_at: datetime


def create_sync_state(
    provider: str,
    symbol: str,
    timeframe: str,
    last_timestamp: datetime,
) -> SyncState:
    """Same datetime.now(timezone.utc)-stamped convention as database/raw_candle_models.py's create_raw_candle()."""
    return SyncState(
        provider=provider,
        symbol=symbol,
        timeframe=timeframe,
        last_timestamp=last_timestamp,
        updated_at=datetime.now(timezone.utc),
    )
