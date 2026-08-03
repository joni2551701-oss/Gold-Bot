# Validation Guide

How a Phase 59 Real Market Validation run is actually carried out with
the foundation pieces that exist today (`docs/PHASE59_VALIDATION.md`'s
"Real Market Validation Foundation" section lists exactly what each
piece is and which gaps remain open). Companion to
`docs/DATA_COLLECTION_RULES.md` (what gets recorded and why) — this
document is about *how* to run a validation cycle with what already
exists, not what to build next.

## Hard boundaries (unchanged for the whole validation period)

- No real order is ever opened. No broker/MT5 execution is connected —
  `execution/` stays inert.
- Strategy logic (`strategies/`, `signals/`) is not changed.
- Decision thresholds (`decision_layer/decision_engine/decision_engine.py`) are not changed.
- Only observation and dataset collection happen during validation —
  see `CLAUDE.md`'s "Trading Safety" section, which this document does
  not override.

## What "running a validation cycle" means today

There is no single command that does all of this automatically yet
(see `docs/PHASE59_VALIDATION.md`'s "Known gaps"). A validation cycle
is the following steps, run manually or by a small external script,
once per pipeline run (or on whatever cadence the operator chooses)
during the test window:

1. **Run the pipeline normally.** `core/pipeline.py`'s
   `TradingPipeline.run()` executes exactly as it does in production —
   nothing in this phase changes its behavior. Its result dict already
   contains `signal_history` (one `SignalSchema` per candidate,
   `market_phase` included as of this phase's TASK 2),
   `context_snapshot`, and `market_phase`.
2. **Store the candles.** Call
   `database_layer.market_repository.raw_candle_repository.RawCandleRepository.save_market_candles()`
   with the provider's real `MarketCandle` list (e.g.
   `TwelveDataProvider.get_candles()`'s output) so the window is
   available for later backtesting. This is opt-in — `core/pipeline.py`
   does not call it automatically.
3. **Track each signal's paper trade.** For a signal you want to
   validate, call `trade_monitoring_layer.paper_trading.paper_trade.create_paper_trade(signal)`,
   then `open_paper_trade()` once price reaches the entry zone. On
   each later cycle, call
   `trade_monitoring_layer.paper_trading.paper_trade_monitor.check_paper_trade_against_candles(trade,
   candles)` against the accumulated candle window (from step 2) to
   let it resolve to `TP`/`SL`/`EXPIRED` on its own — see
   `lifecycle/README.md`.
4. **Build a SignalPerformance per resolved trade.** Call
   `backtesting_layer.statistics.signal_performance.compute_signal_performance(signal,
   paper_trade=trade, session=..., market_phase=...)` once a trade has
   closed or been cancelled.
5. **Record failures.** For any signal whose paper trade resolves to
   `SL`, optionally call
   `ai_layer.knowledge_ai.knowledge_base.journal.failure_analysis.create_failure_analysis_entry()` with a
   short `reason`/`context` note — see `docs/DATA_COLLECTION_RULES.md`
   for what belongs in these fields.
6. **Generate the report.** Once the accumulated `SignalSchema`/
   `SignalPerformance` lists span the desired window, call
   `backtesting_layer.statistics.validation_report.build_validation_report(signals,
   performances, period_start, period_end)` and
   `format_validation_report()` for the text report, or
   `platform_layer.telegram.owner.validation_commands.get_validation_report()` for the
   same thing wrapped in a `ProviderCommandResult`. Neither is wired
   into the live Telegram bot — see `platform_layer/telegram/owner/README.md`.

## Metrics gathered

Exactly the ones `docs/PHASE59_VALIDATION.md` names, each with its
real source:

| Metric | Where it comes from |
|---|---|
| Total / BUY / SELL signal counts | `SignalSchema.direction` across the window's `signal_history` |
| Per-strategy Win/Loss/Winrate/Average R | `backtesting_layer.statistics.strategy_report.build_strategy_report()`, fed by `SignalPerformance.result`/`r_multiple` |
| Best session / best market phase | `backtesting_layer.statistics.validation_report.build_validation_report()`'s `best_session`/`best_market_phase` (highest win rate among decided TP/SL results, ties broken by more signals) |
| Failure patterns | `ai_layer.knowledge_ai.knowledge_base.journal.failure_analysis.FailureAnalysisEntry` records, one per `SL` result an operator chose to annotate |

`profit_loss` and any drawdown/equity metric are **not** gathered —
`SignalPerformance.profit_loss` stays an honest `None` (see
`backtesting_layer/statistics/signal_performance.py`'s own docstring); no PnL simulation
exists in this codebase.

## When Phase 59 is considered complete

Per the Director's own acceptance criteria: all of the following must
be true before validation is considered done and a post-validation
decision (proceed to v0.4 AI Assistant / refine strategy / tune
Context Engine) is made —

- [ ] 7-14 days of continuous market dataset collected (`raw_candles`
      rows spanning the window, via step 2 above).
- [ ] Signal history exists for the window (`signal_history` captured
      per cycle, linked to context via `SignalSchema.context_id`).
- [ ] Paper trades exist for a representative sample of signals, with
      real `TP`/`SL`/`EXPIRED`/`CANCELLED` results (steps 3-4 above).
- [ ] Strategy statistics exist (`build_strategy_report()` output is
      non-empty for at least one real strategy).
- [ ] Session statistics exist (`best_session` is not `None`).
- [ ] Market phase statistics exist (`best_market_phase` is not `None`).
- [ ] `build_validation_report()`/`format_validation_report()` run
      successfully end-to-end against the real accumulated dataset,
      producing the `GoldBot Validation Report` shape without error.

None of these criteria require any change to `strategies/`, `signals/`
signal logic, `risk_layer/risk_engine/risk_manager.py`, or
`decision_layer/decision_engine/decision_engine.py` — a validation run that satisfies all
seven is complete using only the foundation this document describes.
