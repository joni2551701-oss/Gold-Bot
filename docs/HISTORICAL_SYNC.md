# Historical Sync

How repeated historical collection avoids re-fetching the same window
every time (Phase 59.5: Historical Data Collection & Validation
Foundation, TASK 2). Companion to `docs/DATASET_COLLECTION.md` (the
one-shot `collect_historical_candles()` this builds on).

## The problem

`data_layer/historical_data/historical_data_collector.py`'s `collect_historical_candles()`
(TASK 1) takes an explicit `[start, end)` window every call. Calling
it repeatedly on a schedule with the same wide window would re-fetch
and re-request candles the archive already has — wasteful of API
calls, and (per this task's own brief) something a "10000 candle
qayta yuklanmasin" (don't re-download 10,000 candles every time)
requirement explicitly rules out.

## The fix: `sync_state`

A new, fully isolated table (`database_layer/market_repository/sync_state_repository.py`/
`sync_state_models.py`, no SQL foreign key to any other table) — one
row per `(provider, symbol, timeframe)`, storing the timestamp of the
most recently collected candle:

```python
@dataclass(frozen=True)
class SyncState:
    provider: str
    symbol: str
    timeframe: str
    last_timestamp: datetime
    updated_at: datetime
```

`SyncStateRepository.get_sync_state(provider, symbol, timeframe)` reads
it (`None` if no sync has ever happened for that key).
`update_sync_state(provider, symbol, timeframe, last_timestamp)`
upserts it — `UPDATE` if a row already exists, otherwise `INSERT`
(the same check-then-branch idiom `SubscriptionRepository._update()`/
`create_subscription()` already established), always returning the row
as actually persisted.

## `sync_historical_candles()`

`data_layer/historical_data/historical_data_collector.py`'s incremental entry point:

```python
sync_historical_candles(
    provider, symbol, timeframe,
    sync_state_repository,
    raw_candle_repository=None,
    end=None,       # defaults to now()
    lookback=None,  # only used when no prior sync state exists
) -> CollectionResult
```

1. Reads the sync state for `(provider.get_provider_name(), symbol,
   timeframe)`.
2. **If a prior sync state exists**, `start` is set to one timeframe
   interval past its `last_timestamp` — the already-synced candle is
   never re-requested.
3. **If no prior sync state exists**, `start` is the caller-supplied
   `lookback`. This module invents no default lookback window itself —
   a caller with no opinion must pass `end - N` explicitly.
   `ValueError` is raised if neither a prior sync state nor `lookback`
   is available, rather than guessing a window.
4. Delegates to `collect_historical_candles()` for the actual fetch +
   save (TASK 1 logic, unmodified, reused not duplicated).
5. **Only if at least one candle was actually saved**, advances the
   sync state forward to the collection's own `actual_end`. A
   zero-candle result (e.g. the market was closed for that window)
   does not move the watermark — the next sync call retries the same
   window rather than silently skipping it.

## Running an incremental sync

```python
from data_layer.providers.twelve_data_provider import TwelveDataProvider
from database_layer.market_repository.sync_state_repository import SyncStateRepository
from data_layer.historical_data.historical_data_collector import sync_historical_candles
from datetime import datetime, timedelta, timezone

provider = TwelveDataProvider()
sync_repo = SyncStateRepository()

# First call: no prior state, so lookback is required.
sync_historical_candles(
    provider, "XAUUSD", "M15", sync_repo,
    lookback=datetime.now(timezone.utc) - timedelta(days=7),
)

# Every subsequent call: resumes automatically from where it left off.
sync_historical_candles(provider, "XAUUSD", "M15", sync_repo)
```

There is no automatic scheduler yet — invoking this on a recurring
cadence (e.g. hourly) is a future, separately-approved wiring step,
the same "foundation, not full wiring" posture every module in this
phase follows. `core/pipeline.py` never calls this function.

## Owner visibility (foundation only)

`telegram/owner/dataset_commands.py`'s `get_sync_status(provider,
symbol, timeframe)` reports the current watermark as text ("no sync
state yet" or "last synced <timestamp>"). Not wired into the live
Telegram bot; see `telegram/owner/README.md`.
