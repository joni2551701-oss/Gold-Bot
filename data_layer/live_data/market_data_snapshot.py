"""
Data Layer — Market Data Snapshot foundation (Phase 59 Preparation,
TASK 1: Raw Market Data Persistence Audit).

Audit finding this closes: the "signals" database table
(database/models.py's init_schema()) stores no candle data, no
timeframe of the underlying market data, and its own "symbol" column
is never actually populated (database/signal_repository.py's
save_signal_record() hardcodes data["symbol"] = "" -- see
docs/PHASE59_VALIDATION.md's audit note). There is today no way to
reconstruct the market state a signal was generated from, later, for
replay/backtesting/AI research/analytics.

MarketDataSnapshot is a lightweight, standalone identity/fingerprint
record for a candle window -- NOT a full candle store. Per this task's
own explicit boundary ("Database migration majburiy emas" / a DB
migration is not mandatory), this module does not add a database
table, and does not persist anything: it is a pure, in-memory
dataclass plus one adapter function, the same "foundation, not a
rewrite" posture every Phase A/AC module before it has used. It is not
wired into core/pipeline.py in this phase -- a future, separately-
approved phase would be the one to call capture_market_data_snapshot()
inside a live pipeline run and decide where its result travels.

Extended by Phase 59.1 (Market Data Provider Abstraction, TASK 4):
`provider` and `data_quality` were added as optional, additive fields
-- `provider` names which MarketDataProvider (data_layer/providers/,
Phase 59.1) supplied the candles (e.g. "twelvedata"); `data_quality`
carries an already-computed DataQualityResult.valid/score summary
(Phase A8, data_layer/data_validation/data_quality.py) rather than recomputing anything.
Both default to None, so the one existing call site inside
capture_market_data_snapshot() (and any existing test) is unaffected
unless it opts in.

NAMING NOTE -- read before using this module: data_layer/live_data/market_data.py
already defines MarketSnapshot (a live, in-process, multi-timeframe
container of candles + per-timeframe quality flags, returned by
MarketDataNormalizer.get_snapshot(), used within a single pipeline run
and never persisted). MarketDataSnapshot (this module) is a distinct,
single-timeframe, persistence-oriented identity record -- it does not
wrap, replace, or extend MarketSnapshot, and MarketSnapshot is
untouched by this phase. The name is intentionally close (matching
this phase's own brief verbatim), so this distinction is called out
explicitly, the same disambiguation discipline
context_layer/context_engine/snapshot.py's ContextSnapshotSchema (vs. the real
ContextSnapshot) already established.
"""

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence

from data_layer.providers.twelve_data_client import Candle


@dataclass(frozen=True)
class MarketDataSnapshot:
    """
    Identity: market_snapshot_id (generate_market_snapshot_id()),
        created_at (when this record was built).
    Market: symbol, timeframe -- the caller's real values (e.g.
        "XAUUSD"/"M15"), not read from the candles themselves (a
        Candle carries no symbol/timeframe of its own).
    Window: candle_count, first_timestamp, last_timestamp -- describe
        the exact candle window this snapshot represents. All three
        are honest None/0 on an empty candle list, never fabricated.
    candles_reference: a deterministic content fingerprint (see
        compute_candles_reference()) of (symbol, timeframe, count,
        first/last timestamp) -- enough to verify later that a
        re-fetch of the same symbol/timeframe/window from the market
        data provider reproduces the same window. It is NOT a foreign
        key into a stored candle table -- no such table exists in this
        codebase today, and adding one is out of this task's scope
        (see this module's own docstring). Full raw-OHLC persistence
        remains a deliberately deferred, separately-approved future
        step.
    provider: which MarketDataProvider (data_layer/providers/, Phase 59.1)
        supplied the candles this snapshot describes (e.g.
        "twelvedata") -- None if the caller doesn't know/supply one
        (e.g. an existing Phase 59 caller predating providers/).
    data_quality: an already-computed quality summary string (e.g.
        "OK"/"WARNING_GAP"/"ERROR_NO_DATA", the same vocabulary
        data_layer/live_data/market_data.py's MarketSnapshot.quality dict and
        data_layer/data_validation/data_quality.py's DataQualityResult already use) -- never
        recomputed here, None if the caller doesn't supply one.
    """
    market_snapshot_id: str
    created_at: datetime
    symbol: str
    timeframe: str
    candle_count: int
    first_timestamp: Optional[datetime]
    last_timestamp: Optional[datetime]
    candles_reference: str
    provider: Optional[str] = None
    data_quality: Optional[str] = None

    def to_dict(self) -> dict:
        """JSON-safe dict -- every datetime field rendered as an ISO-8601 string."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["first_timestamp"] = self.first_timestamp.isoformat() if self.first_timestamp else None
        data["last_timestamp"] = self.last_timestamp.isoformat() if self.last_timestamp else None
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def generate_market_snapshot_id() -> str:
    """Same generation convention as every other Phase A/AC identity field (str(uuid.uuid4())) -- not a new scheme."""
    return str(uuid.uuid4())


def compute_candles_reference(symbol: str, timeframe: str, candle_count: int,
                               first_timestamp: Optional[datetime],
                               last_timestamp: Optional[datetime]) -> str:
    """
    A deterministic, 16-character hex fingerprint of the window shape
    -- the same (symbol, timeframe, count, first/last timestamp) tuple
    always produces the same reference, so two snapshots of the same
    window (e.g. computed on two separate pipeline runs) are directly
    comparable without storing the candles themselves.
    """
    first = first_timestamp.isoformat() if first_timestamp else "none"
    last = last_timestamp.isoformat() if last_timestamp else "none"
    payload = f"{symbol}|{timeframe}|{candle_count}|{first}|{last}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def capture_market_data_snapshot(
    candles: Sequence[Candle],
    symbol: str,
    timeframe: str,
    *,
    provider: Optional[str] = None,
    data_quality: Optional[str] = None,
) -> MarketDataSnapshot:
    """
    Builds a MarketDataSnapshot from an already-fetched candle list --
    the minimum required input. Never raises: an empty candle list
    produces a snapshot with candle_count=0 and both timestamps None,
    not an exception -- the same fail-safe posture every other
    foundation module in this codebase uses. Computes nothing about
    market structure or quality -- data_layer/data_validation/data_quality.py (Phase A8)
    remains the one place candle quality is assessed; this module only
    records identity/window metadata for later reconstruction.
    `provider`/`data_quality` (Phase 59.1, TASK 4) are optional,
    keyword-only, and relayed as-is -- never computed here.
    """
    first_timestamp = candles[0].timestamp if candles else None
    last_timestamp = candles[-1].timestamp if candles else None
    candle_count = len(candles)

    return MarketDataSnapshot(
        market_snapshot_id=generate_market_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol=symbol,
        timeframe=timeframe,
        candle_count=candle_count,
        first_timestamp=first_timestamp,
        last_timestamp=last_timestamp,
        candles_reference=compute_candles_reference(
            symbol, timeframe, candle_count, first_timestamp, last_timestamp
        ),
        provider=provider,
        data_quality=data_quality,
    )
