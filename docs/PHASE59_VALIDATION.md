# Phase 59 Validation Report Contract

Documentation foundation only — no new module, no code. This document
fixes, in advance of Phase 59 Real Market Validation actually starting,
exactly how a 7-day live test's result will be measured, so the metric
definitions are not invented after the fact from whatever happened to
get logged. Part of Phase 59 Preparation, TASK 5.

## Test Period

**7 days**, continuous, during the pipeline's normal scheduled run
window (`.github/workflows/trading_bot.yml`'s cron, every 5 minutes
during trading hours — unchanged by this phase). Every `TradingPipeline.run()`
cycle in that window is in scope; no cycle is excluded after the fact.

## What this document does NOT do

- Does not start Phase 59 itself, and does not change
  `core/pipeline.py`, any strategy, Decision Engine, Risk Manager, or
  the AI layer.
- Does not mandate a dashboard, a Telegram command, or a report
  generator be built in this phase — the metric *definitions* below
  are the deliverable; a generator that actually produces this report
  from real data is separately-approvable future work.
- Does not claim every metric below is fully computable today. Each
  section states plainly which foundation (this phase's or an earlier
  phase's) already supplies the data, and which piece remains a real,
  disclosed gap.

## Signal

| Metric | Source | Status |
|---|---|---|
| Total signals | `SignalSchema` records built by `core/pipeline.py`'s `signal_history` stage (AC-03), one per candidate per cycle | Available today — count `len(signal_history)` across all cycles in the window. |
| BUY / SELL split | `SignalSchema.direction` | Available today. |
| Confidence distribution | `SignalSchema.confidence_score` (relayed from `SignalQualityResult.score`, Phase A4) | Available today. |

`signal_history` is **not persisted** across pipeline runs today (see
"Known gaps" below) — a report generator would need to either read it
from each run's logs/result dict as the 7 days progress, or a future,
separately-approved persistence step.

## Strategy

| Strategy | Real identifier |
|---|---|
| Liquidity Sweep | `"LIQUIDITY_SWEEP_STRATEGY"` (`SignalSchema.strategy_name`, matches `StrategyDefinition.id`, Phase A11) |
| FVG | `"FVG_STRATEGY"` |
| AMD | `"AMD_STRATEGY"` |

Per-strategy win/loss/RR aggregation is `analytics/strategy_report.py`'s
`build_strategy_report()` (Phase 59 Preparation, TASK 3) — the exact
`Liquidity Sweep: 100 trades, Win: 62, Loss: 38, RR: 2.1` shape this
document's own brief names. **Gap**: `build_strategy_report()` needs a
`List[SignalPerformance]`, which needs a `result` per signal
(`"TP"`/`"SL"`/`"BE"`/`"EXPIRED"`) — that only exists once a
`PaperTrade` (`lifecycle/paper_trade.py`, TASK 2) has actually been
opened and closed for the signal. Nothing in this codebase opens or
monitors a `PaperTrade` automatically yet (see `lifecycle/README.md`'s
"Future Roadmap") — during Phase 59 itself, closing each paper trade
is still a manual or separately-built-monitor step.

## Market Context

| Metric | Source | Status |
|---|---|---|
| Session | `ContextSnapshotSchema.session.current_session` (Phase A16) / `SignalPerformance.session` | Available today per-cycle; not yet attached to a persisted signal record. |
| Regime | `ContextSnapshotSchema.regime` (Phase A7/A16) | Available today. |
| Market phase | `MarketPhaseResult.phase` (AC-02) / `SignalPerformance.market_phase` | Available today per-cycle. |

All three are already computed every cycle by `core/pipeline.py` and
returned in `run()`'s result dict (`"context_snapshot"`,
`"market_phase"`) — the gap is the same as Signal's: nothing persists
them alongside a signal's eventual result yet.

## Result

| Value | Meaning | Source |
|---|---|---|
| `TP` | Take-profit hit | `PaperTrade.result` (`lifecycle/paper_trade.py`) |
| `SL` | Stop-loss hit | `PaperTrade.result` |
| `BE` | Closed at breakeven | `PaperTrade.result` |
| `expired` | Entry zone never reached before the setup invalidated | `PaperTrade.result == "EXPIRED"` |

This is `lifecycle.paper_trade.ALLOWED_PAPER_TRADE_RESULTS` verbatim —
chosen to match this report's own vocabulary exactly, deliberately
distinct from `database/signal_repository.py`'s pre-existing
`{"WIN","LOSS","BE","CANCELLED"}` (that vocabulary belongs to the real,
persisted `signals` table and is untouched by this phase — see
`lifecycle/paper_trade.py`'s own docstring for why the two are not
merged). **Gap**: as above, nothing decides `TP`/`SL`/`EXPIRED`
automatically yet — a live monitor comparing an `OPEN` `PaperTrade`'s
`stop_loss`/`take_profit` against fresh candles is future work.

## Risk

| Metric | Source | Status |
|---|---|---|
| Drawdown | Would need a running equity curve across closed `PaperTrade`s | **Gap** — no equity/account-balance simulation exists anywhere in this codebase (deliberately: `risk/risk_manager.py`'s `lot_size` is "a sizing suggestion for manual execution, never an order instruction" — see `risk/risk_manager.py`'s own docstring). |
| Max loss | The single worst `r_multiple` among closed `PaperTrade`s in the window | Computable once `SignalPerformance.r_multiple` values exist for the window (`analytics/signal_performance.py`, TASK 3) — same persistence gap as above. |
| Consecutive losses | A streak count over closed `PaperTrade`s in chronological order | Computable the same way, once results exist for the window — no dedicated helper exists yet; a report generator would compute this directly from an ordered `List[SignalPerformance]`. |

Per this phase's own boundary ("Risk o'zgarmaydi" — Risk Manager logic
does not change), none of the three above are computed by
`risk/risk_manager.py` — they are all post-hoc, read-only aggregations
over `PaperTrade`/`SignalPerformance` records a future report generator
would build.

## Known gaps (disclosed, not silently worked around)

1. **No cross-run persistence yet.** `signal_history`, `context_snapshot`,
   `market_phase` are all real, computed every cycle, and returned in
   `run()`'s result dict — but `main.py` is a one-shot process (exits
   after each cycle); nothing writes these to disk today. A report
   spanning 7 days needs either a log-scraping step or a future,
   separately-approved persistence phase.
2. **No automatic paper-trade lifecycle.** `lifecycle/paper_trade.py`
   provides `create_paper_trade()`/`open_paper_trade()`/
   `close_paper_trade()`/`cancel_paper_trade()`, and (Phase 59.4)
   `lifecycle/paper_trade_monitor.py`'s `check_paper_trade_against_candles()`
   can now decide TP/SL/EXPIRED given a candle window — all still pure,
   callable functions. Nothing in `core/pipeline.py` calls any of them
   yet: opening a trade on every `APPROVE`d decision automatically, and
   calling the monitor each cycle with accumulated candle history
   (`database/raw_candle_repository.py`, Phase 59.3, would supply that
   history), is explicitly out of scope — see `lifecycle/README.md`'s
   "Future Roadmap".
3. **No PnL / drawdown simulation.** `SignalPerformance.profit_loss` is
   always `None` — an honest hook, not a fabricated number (see
   `analytics/signal_performance.py`'s own docstring for why: it would
   need account-currency/lot-value sizing logic, out of scope for a
   "no risk logic changes" phase).

None of these gaps block Phase 59 from *starting* — signals, context,
and market phase are already real and observable per-cycle via logs
and `run()`'s result dict. They mean the **automated 7-day report**
this document specifies is not yet a runnable command; producing one
is the natural next, separately-approvable step once Phase 59 itself
is underway and real data exists to validate the report format
against.

## Relationship to the rest of Phase 59 Preparation

```
data/market_data_snapshot.py (TASK 1)  -- raw window identity/fingerprint
lifecycle/paper_trade.py (TASK 2)      -- simulated trade state machine
lifecycle/signal_state.py (TASK 4)     -- signal's own pipeline-stage state
analytics/signal_performance.py,       -- per-signal/per-strategy result
analytics/strategy_report.py (TASK 3)     aggregation
        |
        v
   This document (TASK 5) -- names exactly what a 7-day report measures,
   and which of the above already supplies it vs. remains future work.
```

## Roadmap

```
v0.3.5 COMPLETE
      |
      v
Phase 59 Preparation (this document + TASK 1-4, 6)
      |
      v
Phase 59 READY
      |
      v
7 Day Real Market Validation
      |
      v
Analytics Dataset
      |
      v
v0.4 AI Assistant
```
