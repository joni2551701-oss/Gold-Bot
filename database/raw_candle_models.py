"""
Database Layer — Raw Candle persistence model (Phase 59.3, TASK 2:
Raw Market Storage Foundation).

The first real database migration added by any Phase A/AC/Phase-59
module in this codebase's history -- every prior raw-market-data
foundation (data/market_data_snapshot.py, Phase 59 Preparation/59.1)
deliberately stayed in-memory-only ("Database migration majburiy
emas"). This phase's own brief explicitly asks for persisted storage
("Saqlash... Muhim: Backtest uchun" -- storage, important for
backtesting), which an in-memory-only record cannot serve once the
one-shot `main.py` process exits. The new 'raw_candles' table is
additive and fully isolated: CREATE TABLE IF NOT EXISTS, its own
UNIQUE constraint, its own indexes -- it never touches, migrates, or
reads the pre-existing 'signals'/'users'/'subscriptions'/'feedback'/
'admins' tables.

NAMING NOTE -- read before using this module: three other "candle"
shapes already exist in this codebase, none of which this model
replaces or wraps: data.twelve_data_client.Candle (timestamp+OHLC
only, the real type the live pipeline uses in-memory),
data.providers.base_provider.MarketCandle (the Phase 59.1/59.2
provider-layer standard shape, symbol+timeframe+OHLC+volume+provider,
also in-memory only), and database.signal_record.SignalRecord (an
unrelated per-SIGNAL persistence wrapper, not a candle at all).
RawCandle (this module) is the one PERSISTENCE-oriented candle shape --
a single OHLCV row as stored in the new 'raw_candles' table, with an
explicit `provider` field distinguishing which data source it came
from (see database/raw_candle_repository.py's UNIQUE(symbol,
timeframe, timestamp, provider) constraint -- the same window from two
different providers is two distinct rows, never merged/overwritten).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from data.providers.base_provider import MarketCandle


@dataclass(frozen=True)
class RawCandle:
    """
    Mirrors the 'raw_candles' table row shape. `id` is intentionally
    excluded -- repository-internal detail, not part of the record a
    caller needs (same convention as database.admin_models.AdminRecord).
    volume stays Optional[float] -- an honest None when the source
    provider doesn't supply it (see MarketCandle's own docstring on
    why volume is never fabricated), never coerced to 0.0.
    """
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    provider: str
    created_at: datetime
    volume: Optional[float] = None


def create_raw_candle(
    symbol: str,
    timeframe: str,
    timestamp: datetime,
    open: float,
    high: float,
    low: float,
    close: float,
    provider: str,
    volume: Optional[float] = None,
) -> RawCandle:
    """Same str(uuid.uuid4())-free, datetime.now(timezone.utc)-stamped convention as database/signal_record.py's create_signal_record() -- created_at is when this record was built, not when the candle's own timestamp occurred."""
    return RawCandle(
        symbol=symbol,
        timeframe=timeframe,
        timestamp=timestamp,
        open=open,
        high=high,
        low=low,
        close=close,
        volume=volume,
        provider=provider,
        created_at=datetime.now(timezone.utc),
    )


def from_market_candle(candle: 'MarketCandle', provider: Optional[str] = None) -> RawCandle:
    """
    Phase 59 Real Market Validation Foundation, TASK 3 -- the bridge
    this codebase was missing between the provider layer's own
    standard output (data/providers/base_provider.py's MarketCandle,
    Phase 59.1/59.2) and this table's persisted row shape. A direct
    field copy, computes nothing new -- the same "adapter, not a new
    detector" posture data/market_data_snapshot.py's
    capture_market_data_snapshot() and database/market_snapshot_models.py's
    from_market_data_snapshot() already established.

    `provider` here overrides `candle.provider` when supplied (for a
    caller that already knows which provider it asked, e.g. before
    Phase 59.3's provider-stamping reached every code path). Raises
    ValueError if neither is available -- a genuine data-integrity gap
    (a raw candle with no known source defeats the whole point of the
    `provider` column and this table's own UNIQUE constraint), not a
    data-driven condition this function should silently paper over.
    """
    resolved_provider = provider or candle.provider
    if not resolved_provider:
        raise ValueError(
            "from_market_candle() requires a provider -- neither candle.provider "
            "nor an explicit provider argument was supplied"
        )

    return create_raw_candle(
        symbol=candle.symbol,
        timeframe=candle.timeframe,
        timestamp=candle.timestamp,
        open=candle.open,
        high=candle.high,
        low=candle.low,
        close=candle.close,
        provider=resolved_provider,
        volume=candle.volume,
    )
