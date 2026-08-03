# Adaptive Intelligence Layer Foundation — Reuse Audit (Phase 60.7, TASK 1)

Read before any new code was written, per the Director's own
`exists? -> extend -> new module` rule. Scope: `lifecycle/paper_trade.py`,
`lifecycle/paper_trade_monitor.py`, `analytics/`, `database/learning_repository.py`,
plus `backtesting/backtest_engine.py` (the one real caller of both
`lifecycle/` modules above).

## Goal

"Closed trade event qayerdan olinadi aniqlash" — find where a closed
trade event actually originates in this codebase today.

## Finding 1 (structural): the only real closed-trade producer is the Backtest Engine

`core/pipeline.py` — the live cycle — **never imports or references
`lifecycle.paper_trade` at all** (confirmed by a full grep: zero
matches). No MT5/broker execution is wired (`execution_layer/execution_engine/execution_engine.py`
remains an inert stub, per every prior phase's own audit), so a live
cycle never creates a `PaperTrade` in the first place — there is no
"real" closed trade to observe outside of a backtest run.

`backtesting/backtest_engine.py`'s `_process_candidate()` (Phase 60.2)
is the only place in this codebase that calls `create_paper_trade()`
→ `open_paper_trade()` → `check_paper_trade_against_candles()` — the
full CREATED → OPEN → CLOSED lifecycle `lifecycle/paper_trade.py`/
`paper_trade_monitor.py` already implement. This is the real
observation point Phase 60.7's Learning Event Bridge (TASK 2) must
read from.

## Finding 2 (a real bug, found and fixed): the Backtest Engine never actually captured a closed trade

Reading `_process_candidate()` line by line surfaced a genuine defect,
independent of anything Phase 60.7 itself needed to build:

```python
paper_trade = create_paper_trade(signal_schema)
open_paper_trade(paper_trade)                              # return value discarded
check_paper_trade_against_candles(paper_trade, forward_candles)  # return value discarded
```

Both `open_paper_trade()` and `check_paper_trade_against_candles()`
are pure functions over a **frozen** `PaperTrade` dataclass — each
returns a *new* `PaperTradeTransitionResult` with an updated `.trade`,
never mutates its argument. Because neither return value was captured,
the local `paper_trade` variable stayed at `TradeState.CREATED`
forever: `check_paper_trade_against_candles()`'s own status guard
("Cannot monitor a trade that is not OPEN") caused it to immediately
no-op on every single call, and `compute_signal_performance(...,
paper_trade=paper_trade, ...)` downstream always read a trade whose
`.status` was `CREATED` and `.result` was `None`.

**Practical effect**: every backtest run since Phase 60.2 opened
trades (`trades_opened` counted correctly) but never actually resolved
a single one to `TP`/`SL`/`BE`/`EXPIRED` — `SignalPerformance.result`
was silently `None` for every trade, every time. This was invisible in
Phase 60.2's own test suite because no existing test asserted a
non-`None` `result` after a real backtest run (only counts and
`strategy_id` were checked).

**Fix** (confined to `backtesting/backtest_engine.py`, three lines,
no change to `strategies/`, `signals/`, `decision/`, or `risk/`):

```python
paper_trade = create_paper_trade(signal_schema)
paper_trade = open_paper_trade(paper_trade).trade
paper_trade = check_paper_trade_against_candles(paper_trade, forward_candles).trade
```

A regression test (`test_approved_candidates_paper_trade_actually_resolves`,
`tests/backtesting/test_backtest_engine.py`) was added: the test
fixture's default entry price (4065.0) is far outside the seeded
candles' 1995–2005 range, so entry is provably never touched and the
trade must resolve to `EXPIRED` — asserting exactly that proves the
transition is now captured. Per the Director's own explicit "never
hide a fundamental problem found during validation" instruction (first
stated during Phase 60.2), this is disclosed here prominently, in
`backtest_engine.py`'s own module docstring, and in the Phase 60.7
final report — not silently patched around.

This fix is why Phase 60.7's TASK 2 (Learning Event Bridge) can now
observe a real `TradeState.CLOSED` `PaperTrade` with a real
`TP`/`SL`/`BE`/`EXPIRED` result at all — before this fix, the bridge
would have had nothing but permanently-`CREATED`, `result=None` trades
to read from, regardless of how correctly TASK 2 itself was built.

## Finding 3: what already exists vs. what TASK 2–7 must add

| Module | Shape | Verdict |
|---|---|---|
| `lifecycle/paper_trade.py`/`paper_trade_monitor.py` | Real, correct, now-actually-reached CLOSED-state trades (Finding 2). | Read-only input to the new bridge — untouched otherwise. |
| `analytics/signal_performance.py` | `compute_signal_performance()` already builds a `SignalPerformance` from a closed `PaperTrade` — session/market_phase/timeframe/r_multiple all real. | Reused directly as one of the Learning Event Bridge's inputs, not duplicated. |
| `learning/outcome_analyzer.py` (Phase 60.6) | `analyze_trade_result(paper_trade, context, performance, htf_bias)` → `TradeAnalysis` (reasons, lesson). | Reused directly — the bridge calls this, does not reimplement trade analysis. |
| `learning/models.py` (Phase 60.6) | `LearningRecord` — `strategy_name`/`market_phase`/`session`/`timeframe`/`result`/`r_multiple`/`failure_type`/`success_pattern`/`created_at`. Missing the six fields the Director's own brief names for TASK 3 (`htf_bias`, `volatility_state`, `fundamental_bias`, `confidence_score`, `engine_version`, `sample_size`). | Extended additively (TASK 3) — every new field `Optional`, defaulting `None`/a fixed default, so every Phase 60.6 caller/test keeps working unmodified. |
| `database/learning_repository.py` (Phase 60.6) | `LearningRepository.record()` already append-only; nothing calls it yet (Phase 60.6's own disclosed gap). | TASK 2's bridge becomes the first real caller. Schema extended additively (TASK 3) alongside `learning/models.py`. |
| `learning/pattern_detector.py` (Phase 60.6) | Groups by `(strategy_name, session, market_phase)` only — no `htf_bias`/`volatility_state`/minimum-sample gate beyond a flat `min_occurrences=3` default. | Extended (TASK 4), not replaced — `detect_patterns()`'s existing signature/behavior stays backward compatible; new optional grouping dimensions and a named `MIN_PATTERN_SAMPLE` constant are additive. |
| No confidence engine anywhere | Nothing in this codebase computes a LOW/MEDIUM/HIGH confidence from sample size + consistency + recency + performance. | New `learning/confidence.py` (TASK 5) — genuinely new, no existing module to extend. |
| `ai/learning_context.py` (Phase 60.6) | `{recent_failures, successful_patterns, strategy_stats}` only. | Extended (TASK 6) with `patterns`/`failures`/`regimes`/`confidence` fields the Director's brief names — additive, existing fields/behavior unchanged. |
| No regime-memory module anywhere | Nothing persists a Trending/Range/High-volatility/Low-volatility/News-event observation. | New `learning/regime_memory.py` (TASK 7) — genuinely new. |

## Rules confirmed still held

- No change to `core/pipeline.py`, `strategies/`, `signals/`,
  `decision/`, or `risk/` anywhere in this audit or the fix above.
- The Backtest Engine fix does not alter `DecisionEngine`/`RiskManager`/
  any strategy's own output — it only makes an already-computed
  transition result *visible* to the code that was already trying to
  read it.
