"""
Data Layer — Historical Data Collector (Phase 59.5: Historical Data
Collection & Validation Foundation, TASK 1).

Fetches candles from an existing MarketDataProvider (data/providers/,
Phase 59.1/59.2) for an explicit [start, end) window and persists them
via the existing RawCandleRepository.save_market_candles() (Phase
59.3/Phase 59 Real Market Validation Foundation) -- this module writes
no new fetch or storage logic of its own, it only composes the two.

Never runs core/pipeline.py, never touches signals/, decision/, risk/,
strategies/, or ai/, and is never called from anywhere in the live
pipeline -- a standalone, foundation-only entry point a human or a
future, separately-approved scheduler would invoke.

Honest gap, disclosed rather than worked around: neither
data.twelve_data_client.TwelveDataClient.fetch_candles() nor
data.providers.base_provider.MarketDataProvider.get_candles() accepts
a start/end date range -- both are "most recent N candles" calls only
(no TwelveData start_date/end_date support exists in this codebase
today). This module does not add that capability to the client/provider
layer (would be a provider-layer feature change, out of this
foundation phase's additive-only scope) -- instead it requests the
largest single window the provider can serve in one call
(MAX_FETCH_LIMIT below) and filters the result down to [start, end)
client-side. For a window narrower than one provider call already
covers (e.g. a 7-14 day M15 validation window, per
docs/PHASE59_VALIDATION.md), this is a complete, real result; for a
window wider than one call covers, the result is honestly partial --
CollectionResult.requested_start/requested_end vs.
actual_start/actual_end let a caller detect and disclose the
difference rather than silently believing it got everything asked
for. A provider-level date-range fetch is future work, not built here.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from data.data_quality import INTERVAL_DELTAS
from database.raw_candle_repository import RawCandleRepository
from core.logger import setup_logger

if TYPE_CHECKING:
    from data.providers.base_provider import MarketCandle, MarketDataProvider
    from database.sync_state_repository import SyncStateRepository

logger = setup_logger("HistoricalDataCollector")

# TwelveData's own documented ceiling for a single time_series call's
# outputsize -- see data/twelve_data_client.py's own BASE_URL/params
# (this module does not change that client). A ceiling, not a target:
# collect_historical_candles() only requests as many candles as the
# requested [start, end) window implies (via INTERVAL_DELTAS), capped
# at this value.
MAX_FETCH_LIMIT = 5000


@dataclass(frozen=True)
class CollectionResult:
    """
    requested_start/requested_end: the window the caller asked for.
    actual_start/actual_end: the earliest/latest candle timestamp
        actually returned by the provider and kept after filtering --
        None if no candles were returned at all. Comparing these
        against the requested window is how a caller detects a
        partial result (see module docstring's disclosed gap).
    fetched_count: candles the provider returned, before filtering to
        [start, end).
    saved_count: candles actually inserted by
        RawCandleRepository.save_market_candles() -- excludes
        already-saved duplicates, same convention as that method's own
        return value.
    """
    symbol: str
    timeframe: str
    provider: str
    requested_start: datetime
    requested_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    fetched_count: int
    saved_count: int


def collect_historical_candles(
    provider: 'MarketDataProvider',
    symbol: str,
    timeframe: str,
    start: datetime,
    end: datetime,
    raw_candle_repository: Optional[RawCandleRepository] = None,
) -> CollectionResult:
    """
    Fetches up to MAX_FETCH_LIMIT candles from `provider`, keeps only
    those with `start <= timestamp < end`, and saves the kept candles
    via RawCandleRepository.save_market_candles() (constructs a
    default RawCandleRepository() if none is supplied, same optional-
    dependency convention as TwelveDataProvider's own `client`
    parameter). Never raises for "no data" -- an empty provider
    response or an empty [start, end) window both produce a
    CollectionResult with fetched_count=saved_count=0, actual_start/
    actual_end=None, not an exception. A raised exception from the
    provider itself (e.g. get_candles() re-raising a network/API
    error, see TwelveDataProvider.get_candles()'s own docstring) is
    not caught here -- it propagates, since this function has no
    "degrade to empty" policy of its own to apply on top of the
    provider's.
    """
    interval_delta = INTERVAL_DELTAS.get(timeframe)
    if interval_delta is not None and end > start:
        estimated_count = int((end - start) / interval_delta) + 1
        limit = min(MAX_FETCH_LIMIT, max(1, estimated_count))
    else:
        limit = MAX_FETCH_LIMIT

    fetched: List['MarketCandle'] = provider.get_candles(symbol, timeframe, limit)
    kept = [c for c in fetched if start <= c.timestamp < end]

    repository = raw_candle_repository or RawCandleRepository()
    saved_count = repository.save_market_candles(kept, provider=provider.get_provider_name())

    actual_start = min((c.timestamp for c in kept), default=None)
    actual_end = max((c.timestamp for c in kept), default=None)

    logger.info(
        f"Historical collection: {symbol}|{timeframe}|{provider.get_provider_name()} "
        f"fetched={len(fetched)} kept={len(kept)} saved={saved_count} "
        f"window=[{start.isoformat()}, {end.isoformat()})"
    )

    return CollectionResult(
        symbol=symbol,
        timeframe=timeframe,
        provider=provider.get_provider_name(),
        requested_start=start,
        requested_end=end,
        actual_start=actual_start,
        actual_end=actual_end,
        fetched_count=len(fetched),
        saved_count=saved_count,
    )


def sync_historical_candles(
    provider: 'MarketDataProvider',
    symbol: str,
    timeframe: str,
    sync_state_repository: 'SyncStateRepository',
    raw_candle_repository: Optional[RawCandleRepository] = None,
    end: Optional[datetime] = None,
    lookback: Optional[datetime] = None,
) -> CollectionResult:
    """
    Phase 59.5, TASK 2 -- the incremental layer on top of
    collect_historical_candles(). Reads the sync state for
    (provider, symbol, timeframe) via `sync_state_repository`:

    - If a prior sync state exists, `start` is one interval past its
      `last_timestamp` (never re-fetches/re-saves the last candle
      already synced -- RawCandleRepository's own UNIQUE constraint
      would silently no-op a re-fetch anyway, but this avoids the
      redundant provider call in the first place, this task's own
      "10000 candle qayta yuklanmasin" requirement).
    - If no prior sync state exists, `start` defaults to `lookback`
      (caller-supplied) -- this module does not invent its own
      default lookback window; a caller with no opinion should pass
      `end - N` explicitly. Raises ValueError if neither a prior sync
      state nor `lookback` is available, rather than guessing a
      window.

    After a successful collect_historical_candles() call, advances the
    sync state to the new `actual_end` -- but only if at least one
    candle was actually saved (a zero-candle result, e.g. the market
    was closed for that window, does not move the watermark forward,
    so the next sync retries the same window rather than silently
    skipping it).
    """
    end = end or datetime.now(timezone.utc)
    provider_name = provider.get_provider_name()

    existing_state = sync_state_repository.get_sync_state(provider_name, symbol, timeframe)
    interval_delta = INTERVAL_DELTAS.get(timeframe)

    if existing_state is not None:
        start = existing_state.last_timestamp + interval_delta if interval_delta else existing_state.last_timestamp
    elif lookback is not None:
        start = lookback
    else:
        raise ValueError(
            f"No prior sync state for {provider_name}|{symbol}|{timeframe} and no `lookback` "
            "supplied -- sync_historical_candles() does not invent a default window."
        )

    result = collect_historical_candles(
        provider, symbol, timeframe, start, end, raw_candle_repository=raw_candle_repository
    )

    if result.saved_count > 0 and result.actual_end is not None:
        sync_state_repository.update_sync_state(provider_name, symbol, timeframe, result.actual_end)

    return result
