# Dataset Collection

How GoldBot collects a historical, persisted candle archive for future
backtesting and AI/analytics dataset work (Phase 59.5: Historical Data
Collection & Validation Foundation). Companion to
`docs/DATA_VALIDATION.md` (how the collected archive is audited) and
`docs/HISTORICAL_SYNC.md` (how repeated collection avoids re-fetching).

## Scope

This phase collects data. It does not trade, does not open orders, and
does not change `strategies/`, `decision/`, `risk/`, `execution/`,
`context/`, `signals/`, any Telegram handler, paper trading, any
existing `analytics/` module, or `core/pipeline.py`'s stage order.
Every module below is standalone and is never called from the live
pipeline.

## What collects the data

`data_layer/historical_data/historical_data_collector.py`'s `collect_historical_candles()`:

```python
collect_historical_candles(
    provider,       # a data_layer/providers/ MarketDataProvider, e.g. TwelveDataProvider()
    symbol,         # e.g. "XAUUSD"
    timeframe,      # e.g. "M15"
    start, end,     # the window to collect
    raw_candle_repository=None,  # defaults to a real RawCandleRepository()
) -> CollectionResult
```

It fetches from the provider and saves via the already-existing
`database_layer.market_repository.raw_candle_repository.RawCandleRepository.save_market_candles()`
(Phase 59.3/Phase 59 Real Market Validation Foundation) — this module
adds no new fetch or storage logic, it only composes the two.

## The one honest limitation

Neither `data_layer.providers.twelve_data_client.TwelveDataClient.fetch_candles()` nor
`data_layer.providers.base_provider.MarketDataProvider.get_candles()` accepts
a real `start_date`/`end_date` range — both are "give me the most
recent N candles" calls only. `collect_historical_candles()` does not
add that capability to the provider layer (an additive-only foundation
phase does not change provider contracts) — instead it requests the
largest single window the provider can serve in one call (capped at
`MAX_FETCH_LIMIT = 5000`, matching TwelveData's own documented
per-call ceiling) and filters the result down to `[start, end)`
client-side.

For a window at or under one provider call's own reach (e.g. a 7-14
day M15 validation window, per `docs/PHASE59_VALIDATION.md`), this
produces a complete result. For a wider window, the result is honestly
partial — `CollectionResult.actual_start`/`actual_end` (the earliest/
latest candle actually kept) let a caller detect and disclose the gap
against `requested_start`/`requested_end`, rather than silently
believing it collected everything asked for. A true provider-level
date-range fetch is future work, not built in this phase.

## Where it's stored

The existing `raw_candles` table (`database_layer/market_repository/raw_candle_repository.py`,
Phase 59.3) — `UNIQUE(symbol, timeframe, timestamp, provider)`, so
re-running a collection over an already-covered window is a safe,
cheap no-op (duplicates are skipped, not re-inserted or overwritten).
No new table is added for collection itself; see
`docs/HISTORICAL_SYNC.md` for the one new table this phase does add
(`sync_state`, for incremental resume).

## Running a collection

There is no automatic scheduler yet — a collection run is a manual or
externally-scheduled call, the same "foundation, not full wiring"
posture every module in this phase follows:

```python
from data_layer.providers.twelve_data_provider import TwelveDataProvider
from data_layer.historical_data.historical_data_collector import collect_historical_candles
from datetime import datetime, timedelta, timezone

provider = TwelveDataProvider()
end = datetime.now(timezone.utc)
start = end - timedelta(days=7)

result = collect_historical_candles(provider, "XAUUSD", "M15", start, end)
```

For repeated, resumable collection (avoiding a full re-fetch every
call), see `docs/HISTORICAL_SYNC.md`'s `sync_historical_candles()`.

## Owner visibility (foundation only)

`platform_layer/telegram/owner/dataset_commands.py`'s `get_dataset_status()` and
`get_history_status()` report on what's actually stored — see that
module's own docstring. Neither is wired into the live Telegram bot;
see `platform_layer/telegram/owner/README.md`.
