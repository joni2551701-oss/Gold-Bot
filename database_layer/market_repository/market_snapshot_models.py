"""
Database Layer — Market Snapshot persistence model (Phase 59.3, TASK
2: Raw Market Storage Foundation).

NAMING NOTE -- read before using this module: data_layer.live_data.market_data_snapshot.MarketDataSnapshot
(Phase 59 Preparation/59.1) already exists -- a standalone, IN-MEMORY
identity/fingerprint record for a candle window, deliberately never
persisted ("Database migration majburiy emas" in that phase). This
module, MarketSnapshotRecord, is the PERSISTED counterpart added this
phase -- same core identity fields (market_snapshot_id, symbol,
timeframe, candle_count, first_timestamp, last_timestamp,
candles_reference), plus provider/data_quality (Phase 59.1's own later
additive fields on MarketDataSnapshot), now with a real 'market_snapshots'
table row behind it. from_market_data_snapshot() below is the one
adapter between the two -- MarketDataSnapshot itself is untouched by
this phase.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from data_layer.live_data.market_data_snapshot import MarketDataSnapshot


@dataclass(frozen=True)
class MarketSnapshotRecord:
    """Mirrors the 'market_snapshots' table row shape. `id` intentionally excluded, same convention as database.admin_models.AdminRecord/database.raw_candle_models.RawCandle."""
    market_snapshot_id: str
    symbol: str
    timeframe: str
    candle_count: int
    candles_reference: str
    created_at: datetime
    provider: Optional[str] = None
    first_timestamp: Optional[datetime] = None
    last_timestamp: Optional[datetime] = None
    data_quality: Optional[str] = None


def from_market_data_snapshot(snapshot: 'MarketDataSnapshot') -> MarketSnapshotRecord:
    """
    Builds a MarketSnapshotRecord from an already-built, in-memory
    MarketDataSnapshot (Phase 59 Preparation/59.1) -- a direct field
    copy, computes nothing new. The one bridge between that phase's
    deliberately-unpersisted foundation and this phase's real table.
    """
    return MarketSnapshotRecord(
        market_snapshot_id=snapshot.market_snapshot_id,
        symbol=snapshot.symbol,
        timeframe=snapshot.timeframe,
        candle_count=snapshot.candle_count,
        candles_reference=snapshot.candles_reference,
        created_at=snapshot.created_at,
        provider=snapshot.provider,
        first_timestamp=snapshot.first_timestamp,
        last_timestamp=snapshot.last_timestamp,
        data_quality=snapshot.data_quality,
    )
