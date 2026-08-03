# Backtesting Engine (Phase 60.2)

**Not wired into the live bot.** Same "real function, not live-wired"
posture as every phase before it. Nothing in `core/pipeline.py` or
any Telegram routing surface constructs or reads anything in
`backtesting_layer/backtest_engine/backtest_engine.py`/`data_feed.py`/`backtest_result.py`
this phase.

## The one hard rule

Per the Director's own instruction: *"Backtesting hech qachon `if
backtest: ... else: ...` shaklida yozilmaydi."* No file in this phase
branches on "am I backtesting or live." Instead:

```
LIVE:   data_layer.live_data.market_data.MarketDataNormalizer.get_candles()  -> List[Candle]
REPLAY: backtesting.replay_feed.ReplayFeed.window()            -> List[Candle]
              \                                    /
               v                                  v
         backtesting.data_feed.IDataFeed.get_candles(count) -> List[Candle]
                              |
                              v
         context.context_orchestrator.build_context_snapshot(candles, htf_bias)
                              |
                              v
         (everything downstream: strategies/, signals/, ai/, decision/, risk/ --
          all unmodified, all already source-agnostic)
```

`IDataFeed` has two implementations: `LiveDataFeed` (wraps
`MarketDataNormalizer`, same call `core/pipeline.py`'s own live
`market_data` stage already makes) and `ReplayDataFeed` (wraps a
`backtesting_layer.replay_engine.replay_feed.ReplayFeed`, Phase 60.1). Neither `strategies/`
nor `signal_layer/signal_engine/signal_engine.py` needed to change at all — TASK 1's own
reuse audit found they already only depend on `ContextSnapshot`, never
on a candle source directly.

## The full chain

```
backtesting.replay_engine.ReplayEngine (Phase 60.1)
        |  candles, via ReplayDataFeed (IDataFeed)
        v
context.context_orchestrator.build_context_snapshot()      -- unmodified
        |
        v
context.market_phase.compute_market_phase()                -- unmodified
        |
        v
signals.signal_engine.SignalEngine().generate_signals()     -- unmodified
        |  (runs strategies/ internally)
        v
signals.signal_quality.compute_signal_quality()             -- unmodified
        |
        v
ai.ai_analyzer.AIAnalyzer().analyze()                        -- unmodified
        |
        v
decision.decision_engine.DecisionEngine().evaluate()          -- unmodified
        |
        v
risk.risk_manager.RiskManager().evaluate()                     -- unmodified
        |
        v
signals.adapter.from_signal_candidate()  -> SignalSchema       -- unmodified
        |
        v (only if decision.action == APPROVE and risk_result.approved)
lifecycle.paper_trade.create_paper_trade()/open_paper_trade()  -- unmodified
        |
        v
lifecycle.paper_trade_monitor.check_paper_trade_against_candles()  -- unmodified
        |  (resolved immediately using the replay's own remaining candles)
        v
analytics.signal_performance.compute_signal_performance()      -- unmodified
        |
        v
backtesting.backtest_result.build_backtest_result()              -- Phase 60.2
        |  (wraps analytics.strategy_report.build_strategy_report(), unmodified)
        v
BacktestResult
```

Every stage above except the last is an already-existing, unmodified
function or class read directly from source this phase (TASK 1) —
`backtesting_layer/backtest_engine/backtest_engine.py` is pure orchestration, no new
Strategy/Signal/Decision/Risk logic anywhere.

## Reuse audit findings (TASK 1)

- `strategies/`/`signal_layer/signal_engine/signal_engine.py` were already source-agnostic
  (they consume `ContextSnapshot`, never a candle source) — the actual
  seam needing `IDataFeed` is one level up, at the live pipeline's
  `market_data` stage vs. Phase 60.1's `ReplayFeed`.
- `RawCandleRepository.get_candles()` needed the additive
  `get_candles_range()` method (built in Phase 60.1, TASK 1) — reused
  here unchanged.
- `trade_monitoring_layer.paper_trading.paper_trade_monitor.check_paper_trade_against_candles(trade,
  candles)` was built (Phase 59.4) expecting to walk a *forward* candle
  window to resolve TP/SL/EXPIRED — a perfect fit for backtesting,
  since the whole future of the replay is already loaded in memory;
  no polling/waiting loop is needed the way a live monitor would need
  one.
- The exact eligibility gate for opening a paper trade
  (`decision.action == DecisionAction.APPROVE and risk_result.approved`)
  was copied verbatim from `core/pipeline.py`'s own `run()` — read
  directly this phase to guarantee the same APPROVE/REJECT/NO_TRADE
  outcome a live cycle would reach for the same inputs.

## Deliberate differences from live (documented, not trading-logic changes)

- **Every** approved+risk-approved candidate opens a `PaperTrade` in
  this engine, not just the single highest-confidence one per cycle.
  `core/pipeline.py` picks one winner per cycle because at most one
  Telegram message may be sent to a user; a backtest's purpose is
  measuring every strategy's own performance, so this engine tracks
  all of them. `DecisionEngine`/`RiskManager` themselves are
  unmodified — only what a caller does with their already-unchanged
  output differs.
- **HTF Bias defaults to a neutral fallback** (`HTFBias.UNKNOWN`) at
  every step, via the exact same degrade path `core/pipeline.py`
  itself already falls back to on a live HTF fetch failure
  (`compute_htf_bias(MarketSnapshot(symbol=...))`). True multi-timeframe
  HTF replay (a Daily/H4/H1 `ReplayEngine` running in parallel) is out
  of scope for this phase — `BacktestEngine`'s `htf_bias_provider`
  parameter is the seam a future phase would use to supply a real one.
- **`signal_quality`/`explainability`/`features` stages**: TASK 1
  found `core/pipeline.py`'s own `signal_history` stage never passes
  `explanation`/`features` into `from_signal_candidate()` at all —
  only `quality` (`SignalQualityResult`) feeds `SignalSchema`. This
  engine computes `signal_quality` (faithful to what live actually
  uses) and skips `explainability`/`features` (advisory-only text/
  standardization that live itself never threads into `SignalSchema`
  either) — not a scope reduction, an accurate match of what the live
  `SignalSchema` construction actually reads.

## A fundamental bug found and fixed during this phase's own validation

**`backtesting_layer/replay_engine/replay_engine.py`'s `ReplayEngine.is_finished` had a
genuine infinite-loop bug for an empty candle dataset**, found while
testing `telegram/owner/backtest_commands.py`'s `backtest_run()`
against an unknown symbol (zero candles stored). Root cause: the
property was `self.feed.is_exhausted and self.feed.cursor >= 0`. For
zero candles, `ReplayFeed.jump()` always clamps the cursor back to
`-1` (there is no valid index `>= 0` to reach, since `total - 1 ==
-1`), so the `cursor >= 0` half of that condition could never become
`True` — `BacktestEngine.run()`'s `while not
self.replay_engine.is_finished:` loop would spin forever on any
symbol/timeframe with no stored candles. This is a real defect in
Phase 60.1 code (already shipped, CI green at the time), not a
Phase 60.2 test-design issue.

**Fix**: `is_finished` is now just `self.feed.is_exhausted` —
`ReplayFeed.is_exhausted` alone is already correct for every case
(`False` before any step on a non-empty feed, `True` once exhausted,
and correctly `True` immediately for a genuinely empty candle list).
The extra `cursor >= 0` guard was redundant for the non-empty case and
actively harmful for the empty case. A regression test
(`tests/backtesting/test_replay_engine.py::test_is_finished_true_immediately_for_an_empty_candle_range`)
now covers this specific edge case, bounded at 5 iterations so a
regression fails fast instead of hanging CI.

**Impact assessment**: this bug could only ever trigger on a
zero-candle dataset (an unconfigured symbol/timeframe, or a date range
with nothing stored) — every Phase 60.1 test seeded at least one
candle, so it was never exercised until Phase 60.2's
`backtest_commands.py` test deliberately used an unseeded symbol. No
trading logic was touched by this fix; it is entirely contained to
`ReplayEngine`'s own loop-termination condition.

## API reference

### `backtesting_layer/data_feed/data_feed.py`
- `IDataFeed` (ABC) — `get_candles(count) -> List[Candle]`.
- `LiveDataFeed(data_normalizer, symbol, interval)` — wraps `MarketDataNormalizer.get_candles()`.
- `ReplayDataFeed(replay_feed)` — wraps `ReplayFeed.window()`.

### `backtesting_layer/backtest_engine/backtest_engine.py`
- `BacktestEngine(config: ReplayConfig, raw_candle_repository=None, ai_analyzer=None, decision_engine=None, risk_manager=None, context_window=200, htf_bias_provider=None)` — every dependency injectable, defaults to the real unmodified classes.
- `.run() -> BacktestResult` — replays the full configured window, running the real chain at every step with enough candles for context.

### `backtesting_layer/backtest_report/backtest_result.py`
- `BacktestResult(symbol, timeframe, candles_processed, signals_generated, trades_opened, performances, strategy_report, started_at=None, finished_at=None)` — frozen; `.overall_win_rate` derived property.
- `build_backtest_result(...)` — wraps `analytics.strategy_report.build_strategy_report()`.
- `format_backtest_report(result) -> str` — the future `/backtest_report` payload text.

### `telegram/owner/backtest_commands.py`
- `backtest_run(symbol, timeframe, start, end, provider=None, speed=1.0) -> ProviderCommandResult` — runs a full `BacktestEngine` pass synchronously (unlike `replay_commands.py`'s session-based start/pause/stop API) and formats the result.

## What this phase does NOT do

- Does not compute PnL — `analytics.signal_performance.SignalPerformance.profit_loss`
  stays `None`, same honest hook that module already documents; no PnL
  computation exists anywhere in this codebase.
- Does not replay multiple timeframes together — HTF Bias is a fixed
  neutral fallback (see above), not a real multi-timeframe replay.
- Does not persist a `BacktestResult` to a database table.
- Does not register `/backtest_run` into `telegram/commands.py`/
  `command_router.py`/`handlers.py`.
- Does not touch `core/pipeline.py`, `strategies/`, `signals/`,
  `ai/ai_analyzer.py`, `decision_layer/decision_engine/decision_engine.py`, or
  `risk_layer/risk_engine/risk_manager.py` — every one of these was read, never written,
  this phase.

## Future wiring plan

```
docs/BACKTESTING_ENGINE.md (Phase 60.2 -- foundation, this document)
        |
        v
backtesting_layer/data_feed/data_feed.py, backtest_engine.py, backtest_result.py,
telegram/owner/backtest_commands.py (Phase 60.2 -- real logic, not wired)
        |
        v
A future, separately-approved phase (per the Director's own reordered
roadmap -- 60.3 Execution Simulator, 60.4 Performance Validation):
  - A real fill/slippage/spread model (Execution Simulator's own scope,
    not Backtesting's)
  - Real multi-timeframe HTF replay (a parallel Daily/H4/H1 ReplayEngine,
    fed into BacktestEngine's htf_bias_provider seam)
  - Persisting BacktestResult for a resumable, comparable-across-runs report
  - telegram/commands.py/command_router.py registration
```
