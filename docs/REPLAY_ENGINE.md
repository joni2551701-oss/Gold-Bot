# Historical Replay Engine (Phase 60.1)

**Not wired into the live bot.** Same "real function, not live-wired"
posture as every Owner Mode phase before it. Nothing in
`core/pipeline.py`, `strategies/`, `signals/`, `decision/`, `risk/`,
or `execution/` constructs or reads anything in `backtesting/` this
phase. No new database table (session state is in-memory only for
this process's lifetime — see "What this phase does NOT do" below).

## Why `backtesting/`, not a new `market/` package

Per the Director's own Phase 60.1 decision and `CLAUDE.md`'s Module
Reuse Principle: Replay is a service over existing Historical Data
(`database_layer.market_repository.raw_candle_repository.RawCandleRepository`, Phase
59.3/59.5), not a new business domain. A `market/` top-level package
was considered and rejected — `backtesting/` (a name already implied
by the Phase 60 roadmap, `docs/PHASE59_ARCHITECTURE_FREEZE.md`'s own
"v1.0 roadmap" section) is where Replay's actual first consumer
(Backtesting, Phase 60.2) will live anyway, and Paper Trading/AI
Learning/Strategy Debug/Education/Demo Mode are all future consumers
of the same engine, not separate domains needing separate packages.

## Architecture

```
core_layer.emergency-style "foundation, not wired" package:

database_layer/market_repository/raw_candle_repository.py (Phase 59.3/59.5, +Phase 60.1's
    own additive get_candles_range() -- TASK 1 reuse finding: the
    existing get_candles() only supports "most recent N", no date
    bound a fixed historical replay window needs)
        |
        v
backtesting_layer/replay_engine/replay_engine.py (TASK 5)
    loads the configured window once, converts each RawCandle into
    data_layer.providers.twelve_data_client.Candle -- the exact type
    data_layer.live_data.market_data.MarketDataNormalizer.get_candles() already
    returns to the live pipeline today
        |
        +-- backtesting_layer/replay_engine/replay_clock.py (TASK 3)   -- play/pause/resume/stop/speed/seek, a pure position state machine
        +-- backtesting_layer/replay_engine/replay_feed.py (TASK 4)    -- next/previous/jump/window/current candle access
        |
        v
backtesting_layer/replay_controller/replay_controller.py (TASK 6)
    the public session-management API -- start()/pause()/resume()/
    stop()/restart()/step()/get_status(), each keyed by a session_id.
    Owns one ReplaySession + ReplayEngine pair per session, in-memory.
        |
        v
backtesting_layer/replay_controller/replay_session.py (TASK 2)
    ReplaySession -- one replay run's identity/state (not candle
    traversal, not timing -- that's Feed's/Clock's job)
        |
        v
telegram/owner/replay_commands.py (TASK 8)
    replay_start()/replay_pause()/replay_stop()/replay_status() --
    thin wrappers, no new logic. Not registered into
    telegram/commands.py/command_router.py/handlers.py.
```

`backtesting_layer/replay_engine/replay_models.py` (TASK 2/7) holds the shared value types
every file above imports: `ReplayState` (enum), `ReplayConfig`,
`ReplayResult`, and `format_replay_report()` (TASK 7 — folded into
this file rather than given its own module, the Module Reuse
Principle applied at the package's own internal scope).

## State diagram

```
   PENDING
      |
      | play()
      v
   RUNNING <----------+
      |    \          |
      |     \ pause()  | resume()
      |      v         |
      |    PAUSED ------+
      |
      | stop()                    candles exhausted
      v                                  |
   STOPPED                               v
                                     FINISHED

restart() -- from any state, re-creates a fresh ReplayEngine under
   the SAME session_id, resetting to RUNNING with candles_replayed=0.
```

Every transition is driven by `ReplayController`, which keeps a
session's `ReplaySession` (identity/progress bookkeeping) and its
paired `ReplayEngine`'s `ReplayClock` (the actual play/pause/stop
state) in sync on every call — `ReplaySession.state` and
`ReplayEngine.clock.state` always agree after any controller method
returns.

## The one hard rule: Replay replaces only the data source

Per the Director's own explicit instruction, this phase (and every
phase built on top of it) must never:
- Modify `strategies/`, `signals/`, `decision_layer/decision_engine/decision_engine.py`, or
  `risk_layer/risk_engine/risk_manager.py`.
- Call any of the above from `backtesting/`.

`ReplayFeed.next_candle()`/`window()` return
`data_layer.providers.twelve_data_client.Candle` — the same type
`MarketDataNormalizer.get_candles()` already hands to
`context/`/`strategies/` in the live pipeline. This is deliberate:
whichever future phase (60.2 Backtesting, 60.3 Execution Simulator)
wires a Strategy to consume replayed candles instead of live ones,
Strategy's own code should not need to change at all — only the
source of the `List[Candle]` it's handed changes:

```
LIVE:   MarketDataNormalizer.get_candles() -> List[Candle] -> Strategy
REPLAY: ReplayFeed.window(N)                -> List[Candle] -> Strategy
```

This is also why the Backtesting Engine (60.2) and Execution Simulator
(60.3) results should be directly comparable to live trading results
later — same Strategy code, same candle shape, only the feed differs.

## API reference

### `backtesting_layer/replay_engine/replay_models.py`
- `ReplayState`: `PENDING` / `RUNNING` / `PAUSED` / `STOPPED` / `FINISHED`.
- `ReplayConfig(symbol, timeframe, start, end, provider=None, speed=1.0)` — frozen.
- `ReplayResult(symbol, timeframe, state, candles_total, candles_replayed, speed, started_at=None, finished_at=None)` — frozen; `.progress` (0.0-1.0), `.finished` (bool), `.duration_seconds` (float or None) are derived properties.
- `format_replay_report(result: ReplayResult) -> str` — the future `/replay_status` payload text.

### `backtesting_layer/replay_controller/replay_session.py`
- `ReplaySession(config, candles_total=0)` — `.session_id` (uuid4), `.state`, `.candles_total`, `.candles_replayed`, `.started_at`, `.finished_at`.
- `.mark_running()` / `.mark_paused()` / `.mark_stopped()` / `.mark_finished()` / `.record_progress(n)` (high-water mark, never decreases) / `.to_result() -> ReplayResult`.

### `backtesting_layer/replay_engine/replay_clock.py`
- `ReplayClock(speed=1.0)` — `.state`, `.speed`, `.position` (starts at `-1`, same "before the first candle" convention as `ReplayFeed.cursor`).
- `.play()` / `.pause()` / `.resume()` / `.stop()` / `.finish()` / `.set_speed(v)` (raises `ValueError` for `v <= 0`) / `.seek(position)` (clamped to `>= -1`) / `.advance() -> int` (moves by `max(1, int(speed))` positions only while `RUNNING`).
- `.is_running` / `.is_paused` / `.is_stopped` properties.

### `backtesting_layer/replay_engine/replay_feed.py`
- `ReplayFeed(candles: List[Candle])` — `.candles`, `.cursor` (starts at `-1`), `.total`, `.is_exhausted`.
- `.current_candle()` / `.next_candle()` / `.previous_candle()` / `.jump(index)` (clamped to `[-1, total-1]`) / `.window(size) -> List[Candle]` (last `size` candles up to and including the cursor).

### `backtesting_layer/replay_engine/replay_engine.py`
- `ReplayEngine(config: ReplayConfig, raw_candle_repository=None)` — loads the configured window once via `RawCandleRepository.get_candles_range()`, owns `.feed`/`.clock`.
- `.candles_total` / `.candles_replayed` / `.is_finished` properties.
- `.step() -> Optional[Candle]` — advances clock+feed together (a no-op unless `clock.is_running`); marks the clock `FINISHED` once the feed is exhausted.
- `.seek(index) -> Optional[Candle]` — jumps both clock and feed to the same position.

### `backtesting_layer/replay_controller/replay_controller.py`
- `ReplayController()` — one process-local `{session_id: (ReplaySession, ReplayEngine)}` map.
- `.start(config) -> ReplaySession` / `.pause(session_id)` / `.resume(session_id)` / `.stop(session_id)` / `.restart(session_id)` / `.step(session_id) -> Optional[Candle]` / `.get_status(session_id) -> Optional[ReplayResult]` — all except `start()` return `None` for an unknown `session_id`.

### `telegram/owner/replay_commands.py`
- `replay_start(symbol, timeframe, start, end, provider=None, speed=1.0) -> ProviderCommandResult` — message includes `session_id=<uuid>` on its first line.
- `replay_pause(session_id)` / `replay_stop(session_id)` / `replay_status(session_id) -> ProviderCommandResult`.
- One module-level `_default_controller` holds every session for this process's lifetime.

## What this phase does NOT do

- Does not persist `ReplaySession` to a database table — a session
  that must survive a restart is a future, separately-approved step
  (same "in-memory only, foundation phase" posture
  `trade_monitoring_layer/paper_trading/paper_trade.py`'s own `PaperTrade` used before any
  persistence existed for it).
- Does not call `strategies/`, `signals/`, `decision/`, or `risk/` —
  `ReplayEngine.step()` returns a `Candle`; what a caller does with it
  is entirely out of scope here.
- Does not register `/replay_start`/`/replay_pause`/`/replay_stop`/
  `/replay_status` into `telegram/commands.py`/`command_router.py`/
  `handlers.py` — same posture as every Owner Mode module.
- Does not build a real-time, wall-clock-paced player — `speed` means
  "candles per manual `step()` call," not "candles per second." A
  background thread/scheduler is not something any Phase 60.1
  consumer needs yet, per `CLAUDE.md`'s "no unnecessary refactor" rule.

## Future wiring plan

```
docs/REPLAY_ENGINE.md (Phase 60.1 -- foundation, this document)
        |
        v
backtesting/replay_*.py, telegram/owner/replay_commands.py (Phase 60.1 -- real logic, not wired)
        |
        v
A future, separately-approved phase (60.2 Backtesting Engine per the
current roadmap):
  - A Strategy-facing adapter that feeds ReplayFeed.window(N) into
    context/strategies/ instead of MarketDataNormalizer.get_candles()
  - A fill model, slippage model, spread simulation (Backtesting's
    own scope, not Replay's)
  - Persisting ReplaySession for a resumable, restart-surviving replay
  - telegram/commands.py/command_router.py registration, using
    telegram/owner/security.py's require_role() for the per-command
    minimum-OwnerRole gate (same pattern as every other Owner Mode
    module's own documented roadmap)
```
