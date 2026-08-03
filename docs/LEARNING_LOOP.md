# Learning Loop Foundation (Phase 60.6)

**Not wired into the live bot.** Same "real function, not live-wired"
posture as every phase before it. Nothing in `core/pipeline.py`,
`decision/`, `risk/`, `execution/`, `strategies/`, or `signals/` is
touched or called by anything in this phase.

**The one hard rule** (per the Director's own brief): this phase
builds a foundation for *future* learning, not an autonomous learner.

```
✅ observe
✅ analyze
✅ report

❌ change a strategy parameter
❌ change a confidence threshold
❌ change risk sizing
❌ influence a live trade decision
```

Nothing in this phase reads `LearningRecord.failure_type`/
`success_pattern` or a `PatternInsight` back into `strategies/`,
`decision/`, or `risk/` to alter behavior. The loop stops at
*reporting* — Phase 60.7 / v0.4's own "Adaptive Intelligence Layer"
(Learning Memory → AI Analyst → Strategy Improvement Suggestions →
**Owner Approval**) is the future, separately-approved step that would
ever close the loop back into a change, and even then gated by an
explicit human approval, never automatic.

## Architecture / Data flow

```
lifecycle.paper_trade.PaperTrade (already CLOSED)
      |
      v
learning.outcome_analyzer.analyze_trade_result()      -- TASK 3
      |  (+ context.context_orchestrator.ContextSnapshot,
      |     context.htf_bias.HTFBiasResult,
      |     analytics.signal_performance.SignalPerformance --
      |     all already-computed, read-only inputs)
      v
TradeAnalysis (result, reasons, lesson)
      |
      v  (caller builds, this phase does not persist TradeAnalysis itself)
learning.models.LearningRecord                         -- TASK 2
      |
      v
database.learning_repository.LearningRepository.record()  -- TASK 5
      |  (append-only -- learning_records table)
      v
learning.pattern_detector.detect_patterns()             -- TASK 4
      |
      +--> analytics.learning_report.build_learning_report()   -- TASK 6
      |         (best/worst condition over the last N records)
      |
      +--> ai.learning_context.build_learning_context()        -- TASK 7
                (recent_failures / successful_patterns / strategy_stats,
                 AI-facing input only -- no explanation/recommendation
                 text is generated here, that is left to a future AI
                 consumer, itself bound by the same advisory-only
                 AIAnalyzerInterface contract every ai/ module already
                 respects)

telegram.owner.learning_commands                        -- TASK 8
      (/learning_status, /patterns, /failures, /best_conditions --
       thin wrappers over the above, not live-wired)
```

## TASK 1: Reuse audit

Full findings in `docs/LEARNING_LOOP_AUDIT.md`. Summary: no existing
pattern-detection module, no existing `learning/` package, no
Gemini/AI training-data exporter anywhere in this codebase.
`analytics/signal_performance.py`'s `SignalPerformance` shares 7 of
`LearningRecord`'s 11 fields but is an in-memory, computed-on-demand
analytics type with no persistence story — a different lifecycle from
an append-only learning memory, so it was not reused directly (only
its field *shape* informed `LearningRecord`'s design).
`ai/journal/failure_analysis.py`'s `FailureAnalysisEntry` is
loss-specific by contract; TASK 3 needed a shape covering wins and
losses alike, so a new, disclosed near-duplicate type was built rather
than broadening `FailureAnalysisEntry` past its own stated purpose.

## TASK 2: `learning/models.py`

`LearningRecord` (`record_id`, `trade_id`, `signal_id`,
`strategy_name`, `market_phase`, `session`, `timeframe`, `result`,
`r_multiple`, `failure_type`, `success_pattern`, `created_at`) +
`create_learning_record()`. `id` is deliberately excluded from this
dataclass — same convention `database/audit_log_models.py`'s
`AuditLogEntry` already established (a database auto-increment id is
repository-internal, and a record built here has no row yet).

## TASK 3: `learning/outcome_analyzer.py`

`TradeAnalysis` (`trade_id`, `result`, `reasons`, `lesson`) +
`analyze_trade_result(paper_trade, context=None, performance=None,
htf_bias=None)`. Purely observational: reads only already-detected
structural facts (BOS/CHoCH presence, liquidity sweep presence, order
block/FVG presence from `ContextSnapshot`; HTF-direction alignment
from an optional `HTFBiasResult`) — no new structure detection, no new
HTF bias computation. `lesson` is a disclosed pattern match for the
Director's own worked example shape ("Avoid London reversal without
BOS") when a loss is both against HTF bias and has no confirmed
structural break, with a generic fallback (`"Review: ..."`/
`"Repeat: ..."`) otherwise — never a fabricated conclusion `reasons`
doesn't already support.

## TASK 4: `learning/pattern_detector.py`

`PatternInsight` + `detect_patterns(records, min_occurrences=3,
high_threshold=0.65)` + `filter_high_failure_patterns()`/
`filter_high_success_patterns()`/`format_pattern_insight()`. Groups
`LearningRecord`s by `(strategy_name, session, market_phase)` — the
same three real, structured dimensions
`analytics/context_report.py` already groups `SignalPerformance` by —
and classifies each group `HIGH_SUCCESS`/`HIGH_FAILURE`/`MIXED` off
its win rate, reusing `analytics.strategy_report.compute_win_rate()`
directly. Does **not** parse `failure_type`/`success_pattern` free
text into structured sub-conditions — the single most common string in
a group is surfaced as an illustrative example only, never as a
generalized rule.

## TASK 5: `database/learning_models.py` + `learning_repository.py`

`LearningRecordRow` (mirrors `LearningRecord`'s fields plus a real
database `id`) + `LearningRepository`, mirroring
`database/audit_log_repository.py`'s structure exactly: `record()`,
`get_recent()`, `get_by_strategy()`, `count()` — **no `update()`/
`delete()` method exists**, append-only by design, per the Director's
own brief ("append only, tarix o'chirilmaydi, auditga mos").
`init_learning_schema()` (new `learning_records` table, indexed on
`strategy_name`/`session`/`trade_id`) was added to `database/models.py`,
the same file every other schema already lives in.

## TASK 6: `analytics/learning_report.py`

`LearningReport` (`total_records`, `best_condition`, `worst_condition`)
+ `build_learning_report(records, min_occurrences=3)` +
`format_learning_report()`. Reuses `detect_patterns()` directly,
picking the highest- and lowest-win-rate `PatternInsight` — matching
the Director's own "Last 100 trades / Best condition / Worst
condition" worked example shape. The brief's own illustrative example
additionally names an HTF-alignment detail ("H4 bullish") under Best
Condition; `LearningRecord` carries no such structured field, so this
report reproduces the shape with the three real dimensions
(`session`/`strategy_name`/`market_phase`), not a fabricated fourth
one.

## TASK 7: `ai/learning_context.py`

`LearningContext` (`recent_failures`, `successful_patterns`,
`strategy_stats`) + `build_learning_context(records, patterns=None,
limit=5)`, matching the Director's own JSON shape exactly via
`to_dict()`. Bundles already-computed data only — generates no
explanation/conclusion/recommendation text itself; that is explicitly
left to a future AI consumer, per the brief's own "AI: Faqat
tushuntirish, xulosa, tavsiya" boundary, itself still bound by
`AIAnalyzerInterface`'s advisory-only contract.

## TASK 8: `telegram/owner/learning_commands.py`

`get_learning_status()`, `get_patterns_report()`,
`get_failures_report()`, `get_best_conditions_report()` — the future
`/learning_status`, `/patterns`, `/failures`, `/best_conditions`
commands. Thin wrappers only, same "compute from supplied data, don't
fetch" posture as every prior phase's owner-command module. Not
registered into `telegram/commands.py`, not called from
`telegram/command_router.py` or `telegram/handlers.py`.

## Safety rules (restated)

- No file in `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
  `strategies/`, or `signals/` was read, imported, or modified by this
  phase.
- No module in this phase mutates a strategy parameter, a confidence
  threshold, or a risk-sizing value — every function here is a pure,
  read-only observer over already-computed data.
- No module in this phase is called from `core/pipeline.py`,
  `telegram/handlers.py`, `telegram/command_router.py`, or
  `telegram/commands.py`.
- `LearningRepository` is append-only by construction — no
  `update()`/`delete()` method exists, so a `LearningRecord`, once
  persisted, cannot be silently altered or removed.

## Future AI training plan

Per the Director's own roadmap: Phase 60.6 is the last piece before an
**Adaptive Intelligence Layer** (Phase 60.7 / v0.4-adjacent):

```
Learning Memory
        |
        v
AI Analyst
        |
        v
Strategy Improvement Suggestions
        |
        v
Owner Approval
```

`ai/learning_context.py`'s `LearningContext` is the concrete input
shape that future AI Analyst step would consume. Every step after
"Learning Memory" in that diagram remains unbuilt and unapproved —
this phase does not implement, wire, or scope any of it; it only
ensures a real, structured, append-only memory exists for that future
work to read from.

## Known gaps (disclosed, not hidden)

- `failure_type`/`success_pattern` remain free text with no fixed
  taxonomy — same disclosed gap `ai.journal.failure_analysis.FailureAnalysisEntry.reason`
  already carries.
- `learning/outcome_analyzer.py`'s HTF-alignment/structural reasons
  depend on the caller supplying a real `ContextSnapshot`/
  `HTFBiasResult` — with neither supplied, `analyze_trade_result()`
  still returns a valid `TradeAnalysis`, just with empty `reasons`.

---

# Phase 60.7 — Adaptive Intelligence Layer Foundation

Full reuse-audit findings: `docs/ADAPTIVE_INTELLIGENCE_AUDIT.md`. This
section documents what TASK 1-7 actually built on top of Phase 60.6.

**The one hard rule** (unchanged, restated): still
`observe -> analyze -> report`. No file in this phase changes a
strategy parameter, a confidence threshold, or a risk value, and none
of `core/pipeline.py`/`strategies/`/`signals/`/`decision/`/`risk/` was
touched.

## TASK 1: Learning Integration Audit — and a real bug fixed

The audit found `core/pipeline.py` never constructs a `PaperTrade` at
all (no live execution is wired) — the *only* real closed-trade
producer in this codebase is `backtesting/backtest_engine.py`. Reading
it line by line surfaced a genuine Phase 60.2 defect:
`_process_candidate()` called `open_paper_trade()`/
`check_paper_trade_against_candles()` without capturing either
function's returned (new, since `PaperTrade` is frozen) `.trade` — so
every backtest's `PaperTrade` stayed at `TradeState.CREATED` forever,
and `SignalPerformance.result` was silently `None` for every trade,
every run, since Phase 60.2 shipped. **Fixed** (three lines, confined
to `backtesting/backtest_engine.py`, no change to `strategies/`,
`decision/`, or `risk/`): both calls' returned `.trade` are now
threaded through. A regression test
(`test_approved_candidates_paper_trade_actually_resolves`) proves a
trade now actually resolves to a real result. Disclosed prominently
here and in `backtest_engine.py`'s own module docstring, per the
Director's standing "never hide a fundamental problem found during
validation" instruction.

## TASK 2: `learning/trade_event_bridge.py`

`build_learning_record_from_trade()` + `bridge_closed_trade()` — the
first real caller of `LearningRepository.record()`, closing Phase
60.6's own disclosed gap. Reuses `analyze_trade_result()` directly;
`bridge_closed_trade()` is this package's one disclosed exception to
"does not persist anything itself" (dependency injection of an
already-built `LearningRepository`, the same posture
`telegram/*_service.py` already uses).

## TASK 3: Enhanced Learning Schema (additive)

`LearningRecord`/`LearningRecordRow`/the `learning_records` table all
gained six new fields (`htf_bias`, `volatility_state`,
`fundamental_bias`, `confidence_score`, `engine_version`,
`sample_size`) — every one `Optional`, defaulting `None` (except
`engine_version`, which defaults to the new `LEARNING_ENGINE_VERSION =
"60.7"` constant). The table migration is `PRAGMA table_info()`-guarded
(`_migrate_learning_records_schema()`), the same pattern
`signals`/`users` already established — purely additive, every Phase
60.6 caller/test keeps working unmodified (verified: the full Phase
60.6 test suite passes unchanged against the extended schema).

## TASK 4: Advanced Pattern Detector

`detect_patterns()`'s grouping key extended from `(strategy_name,
session, market_phase)` to a 5-tuple including `htf_bias`/
`volatility_state` — purely additive, since every Phase 60.6 record
has both new fields `None`, producing identical groups for any
pre-existing record set. A new `MIN_PATTERN_SAMPLE = 20` constant is
exported for `learning.confidence` (TASK 5) to consume — `detect_patterns()`'s
own `min_occurrences` exclusion gate is deliberately left at its
original default of 3 (the Director's "Samples: 5 -> LOW /Samples: 100
-> HIGH" example is about a confidence *label*, not an exclusion
threshold — see TASK 5). The grouping logic itself was extracted into
a new, separately-exposed `group_records_for_patterns()` helper
(a behavior-preserving refactor, verified against the full existing
test suite) so TASK 6 could reuse it without duplicating the grouping.

## TASK 5: `learning/confidence.py`

`PatternConfidence` + `compute_pattern_confidence()` — LOW/MEDIUM/HIGH
from four disclosed 0.0-1.0 sub-scores (sample size, consistency,
recency, performance). Sample size is a **multiplicative gate**
(`overall_score = sample_size_score * mean(consistency, recency,
performance)`), not a fourth additive term — a plain four-way average
would let a tiny, otherwise-perfect pattern reach HIGH, which
contradicts the Director's own worked example directly. This was
caught by writing the worked-example test *before* trusting the first
draft's formula — the initial additive design produced HIGH for a
5-sample pattern, failing the test, and was corrected before this
phase closed.

## TASK 6: AI Memory Adapter (`ai/learning_context.py`)

`LearningContext` gained four new fields (`patterns`, `failures`,
`regimes`, `confidence`) alongside the unchanged Phase 60.6 three
(`recent_failures`, `successful_patterns`, `strategy_stats`).
`patterns`/`failures` reuse `detect_patterns()`/
`filter_high_failure_patterns()`/`format_pattern_insight()` directly;
`confidence` reuses `group_records_for_patterns()` (TASK 4) +
`compute_pattern_confidence()` (TASK 5); `regimes` is relayed as a
caller-supplied `Sequence[str]` (e.g. from
`learning.regime_memory.format_regime_summary()`, TASK 7) rather than
this module importing `learning.regime_memory` directly — loose
coupling, so `ai/learning_context.py`'s own dependency set didn't need
to grow again once that module existed. Still context only: none of
the four new fields is itself an explanation/conclusion/recommendation.

## TASK 7: `learning/regime_memory.py`

`RegimeObservation` + `RegimeMemory` + `record_from_context()` +
`format_regime_summary()` — an in-memory, per-process log of the
Director's own five named regimes. Four (`TRENDING`/`RANGE`/
`HIGH_VOLATILITY`/`LOW_VOLATILITY`) map directly onto
`context.market_regime.MarketRegime`'s real enum values via
`record_from_context()`; `NEWS_EVENT` has no detector behind it
anywhere in this codebase (same disclosed gap
`context_layer/fundamental/economic_events.py` already carries) and is only recorded
when a caller supplies it explicitly — never fabricated.
`format_regime_summary()` produces exactly the `Sequence[str]` shape
TASK 6's `regimes=` parameter expects, closing the loop between TASK 6
and TASK 7 without either module importing the other's internals.

## Known gaps (Phase 60.7, disclosed, not hidden)

- `confidence_score`/`sample_size` on `LearningRecord` stay honest
  `None` hooks unless a caller explicitly populates them — no
  automatic per-record sample-size computation exists (see
  `LearningRecord`'s own docstring for why).
- `RegimeMemory` is in-memory only, per-process — restarting the
  process loses every observation; persistence is a separate, future
  step, same posture every other `learning/` module (besides
  `trade_event_bridge.py`'s own one exception) already discloses.

## Phase 60.8: Safe Integration Layer, TASK 3 — Learning Auto Hook

Closes the gap Phase 60.7 itself disclosed above ("nothing in this
codebase yet calls `bridge_closed_trade()` from a real pipeline"):
`backtesting/backtest_engine.py`'s `_process_candidate()` now calls
`bridge_closed_trade()` for every `PaperTrade` that reaches
`TradeState.CLOSED`, immediately after `compute_signal_performance()`
so `context`/`performance`/`htf_bias` are all available to pass
through. `BacktestEngine.__init__` gained an injectable
`learning_repository: Optional[LearningRepository] = None` parameter
(same DI convention as every other dependency), defaulting to a real
`LearningRepository()`.

A `bridge_closed_trade()` failure (e.g. a database error) is caught
and logged (`logger.warning`), never allowed to fail the backtest
itself — see `tests/backtesting/test_backtest_engine.py::test_a_learning_repository_failure_does_not_crash_the_backtest`.
Learning stays a pure, non-critical observer: a persistence problem in
`learning/`'s one disclosed exception must never break the thing it is
observing.

**Live trading still records nothing to Learning.** `core/pipeline.py`
never constructs a `PaperTrade` (re-confirmed by Phase 60.8's own
TASK 1 audit, `docs/PHASE60_8_INTEGRATION_AUDIT.md`) — the only real
`CLOSED`-`PaperTrade` producer in this codebase remains
`backtesting/backtest_engine.py`. Live learning integration is
deferred until a real MT5/broker execution lifecycle exists to produce
a real closed trade to observe — a separate, future, explicitly-
approvable step, per the Director's own TASK 3 instruction.
