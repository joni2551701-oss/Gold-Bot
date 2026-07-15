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

- Nothing in this codebase yet calls `LearningRepository.record()` —
  no `core/pipeline.py` stage, no `backtesting/` hook, and no owner
  command builds a `LearningRecord` from a real closed `PaperTrade`
  today. Wiring that observation point is a separate, future,
  explicitly-approvable step (the same "foundation, not wired" gap
  every module in this phase discloses).
- `failure_type`/`success_pattern` remain free text with no fixed
  taxonomy — same disclosed gap `ai.journal.failure_analysis.FailureAnalysisEntry.reason`
  already carries.
- `learning/outcome_analyzer.py`'s HTF-alignment/structural reasons
  depend on the caller supplying a real `ContextSnapshot`/
  `HTFBiasResult` — with neither supplied, `analyze_trade_result()`
  still returns a valid `TradeAnalysis`, just with empty `reasons`.
