# learning/

## Purpose
Learning Loop Foundation (Phase 60.6). Observes already-closed trades
and already-detected market context, classifies win/loss conditions,
and reports what has been observed — **it does not learn
autonomously**. Nothing in this package (or anywhere downstream of it
in this phase) changes a strategy parameter, a confidence threshold,
or a risk value. `observe -> analyze -> report`, never
`observe -> mutate`. See `docs/LEARNING_LOOP.md` for the full
architecture, data flow, and safety rules.

## Flow
```
lifecycle.paper_trade.PaperTrade (already CLOSED)
      |
      v
learning.outcome_analyzer.analyze_trade_result()
      |
      v
TradeAnalysis (result, reasons, lesson)
      |
      v  (caller builds a LearningRecord from this + other context)
learning.models.LearningRecord
      |
      v
database.learning_repository.LearningRepository.record()   -- append-only
      |
      v
learning.pattern_detector.detect_patterns()
      |
      +--> analytics.learning_report / ai.learning_context / telegram.owner.learning_commands
```

## Responsibilities

### `models.py`
`LearningRecord` (`record_id`, `trade_id`, `signal_id`,
`strategy_name`, `market_phase`, `session`, `timeframe`, `result`,
`r_multiple`, `failure_type`, `success_pattern`, `created_at`) +
`create_learning_record()`. A disclosed near-duplicate of
`analytics.signal_performance.SignalPerformance`'s shared fields (see
TASK 1's reuse audit, `docs/LEARNING_LOOP_AUDIT.md`) — a different
lifecycle (meant to be persisted append-only, not computed on demand).

### `outcome_analyzer.py`
`TradeAnalysis` + `analyze_trade_result(paper_trade, context=None,
performance=None, htf_bias=None)` — explains a single closed trade
using only already-detected structural facts (BOS/CHoCH/liquidity
sweep/order block/FVG presence, HTF-direction alignment). No new
structure detection, no new HTF bias computation.

### `pattern_detector.py`
`PatternInsight` + `detect_patterns(records, min_occurrences=3,
high_threshold=0.65)` + `filter_high_failure_patterns()`/
`filter_high_success_patterns()`/`format_pattern_insight()`. Groups
`LearningRecord`s by `(strategy_name, session, market_phase)` and
classifies each group's win rate, reusing
`analytics.strategy_report.compute_win_rate()` directly.

## What this package does NOT do
- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy or a decision.
- Does not call `decision/`, `risk/`, `execution/`, `strategies/`, or
  `signals/` — none of those packages are imported anywhere in this
  package.
- Does not mutate a strategy parameter, confidence threshold, or risk
  value — every function here is a pure, read-only observer.
- Does not persist anything itself — `database/learning_repository.py`
  (a separate package) owns persistence; `learning/` stays in-memory
  only.
- Is not wired into `core/pipeline.py` — a foundation package only,
  same posture as `backtesting/`/`execution/simulator/` before it.

## Input
An already-closed `lifecycle.paper_trade.PaperTrade`, optionally
paired with an already-built `context.context_orchestrator.ContextSnapshot`,
`context.htf_bias.HTFBiasResult`, and
`analytics.signal_performance.SignalPerformance` (`outcome_analyzer.py`);
an already-built `Sequence[LearningRecord]` (`pattern_detector.py`).

## Output
`TradeAnalysis` (`outcome_analyzer.py`); `List[PatternInsight]`
(`pattern_detector.py`).

## Dependencies
`outcome_analyzer.py` imports `context.htf_bias.HTFBias` (a real,
runtime import, needed for enum comparison) plus, `TYPE_CHECKING`-only,
`context.context_orchestrator.ContextSnapshot`,
`context.htf_bias.HTFBiasResult`,
`analytics.signal_performance.SignalPerformance`, and
`lifecycle.paper_trade.PaperTrade`. `pattern_detector.py` imports
`analytics.strategy_report.compute_win_rate` (real, runtime import,
reused directly) and `learning.models` (same package). `models.py`
imports nothing beyond stdlib. None of the three import `database/`,
`telegram/`, `decision/`, `risk/`, `execution/`, `strategies/`, or
`signals/`.

## Future Roadmap
Per the Director's own roadmap, this is the last foundation piece
before an **Adaptive Intelligence Layer** (Phase 60.7 / v0.4-adjacent):
`Learning Memory -> AI Analyst -> Strategy Improvement Suggestions ->
Owner Approval`. Every step after "Learning Memory" remains unbuilt
and unapproved. Also unbuilt: the actual observation wiring itself —
nothing in this codebase yet calls `LearningRepository.record()` from
a real closed `PaperTrade`; that connection is a separate, future,
explicitly-approvable step.
