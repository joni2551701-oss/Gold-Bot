# AI Performance Intelligence (`ai/performance/`)

Phase 66.5 (AI Performance Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_5_AUDIT.md`'s TASK 0 audit — the sixth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/coaching/` (Phase 66.4). Per the Director's own
framing: this phase builds the AI's foundation for understanding trade
performance — quality scores, discipline tracking, pattern storage —
so a future Senior Trading AI can answer "What did the trader do? →
What was the outcome? → Where was the mistake? → Which habit keeps
repeating?" AI still never decides a trade; GoldBot's Trading Core and
AI Analyst remain the only source of any BUY/SELL/NO_TRADE decision.

## Position in the pipeline

The brief's own diagram:

```
Trading Core → Trade Journal (66.2) → Learning (66.3) → Coaching (66.4)
   → Performance Intelligence (66.5) → Strategy Intelligence (66.6)
```

Performance Intelligence never evaluates a trade, never opens a
position, never gives a signal, and performs no real AI inference of
any kind. It never touches `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `telegram/`, `database/`,
`voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
`portfolio/`, `research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` (TASK 8/9's own
isolation list).

## Model (TASK 2)

- `models.py` — `PerformanceCategory` (7-value vocabulary: ENTRY/
  EXIT/RISK/DISCIPLINE/TIMING/PSYCHOLOGY/STRATEGY). `PerformanceRecord`
  (TASK 2's own field list — `id`, `user_id`, `trade_id`, `journal_id`,
  `result`, `direction`, `entry_quality`, `exit_quality`,
  `discipline_score`, `risk_score`, `confidence_score`, `notes`,
  `created_at` — extended additively with `archived: bool = False` so
  TASK 3's `archive()` has a lifecycle field to archive onto, the same
  precedent `ai_layer.knowledge_ai.learning_engine.models.LearningRecord`'s own `source`/`status`
  fields established). `PerformanceMetric` (TASK 2's own field list:
  `metric_name`, `value`, `period`, `created_at` — a generic named
  observation, distinct from `backtesting_layer.statistics.performance_metrics.PerformanceMetrics`,
  see "Naming note" below). `generate_performance_id()` — a stateless
  uuid4 generator.

### Naming note: `PerformanceMetric` vs `analytics.PerformanceMetrics`

Documented in `docs/PHASE66_5_AUDIT.md`, not a defect: a *different*,
fixed-shape portfolio-aggregate type with a similar bare name already
exists at `backtesting_layer.statistics.performance_metrics.PerformanceMetrics` (plural,
Phase 60.4 — `total_trades`/`win_rate`/`expectancy`/`profit_factor`/
etc., computed from `SignalPerformance.r_multiple`). This package's
`PerformanceMetric` (singular) is a distinct, non-colliding
fully-qualified path serving a genuinely different purpose: a generic,
free-form named observation, not a fixed portfolio report. Never
imported alongside the `analytics/` one. Mirrors the same "naming
collision, not duplication" resolution the codebase already applied
twice before (`TradeJournalEntry`, `LearningRecord`).

## Runtime (TASK 3)

`performance_runtime.py`'s `PerformanceRuntime` is CRUD-only, exactly
as the brief requires ("AI xulosa bermaydi. GPT chaqirmaydi. Scoring
algoritm yaratmaydi."): `create()`/`get()`/`list()`/`update_notes()`/
`archive()`, nothing else. In-memory only — a private dict, the same
"Foundation, not a real persistence layer" convention
`ai/coaching/coaching_runtime.py`'s own `_records` dict already
established. `update_notes()` only ever mutates `notes`; every other
field is immutable after `create()`. `archive()` sets `archived=True`
and never deletes a record. Owner-gated: every method re-checks
`ai_layer.ai_engine.performance.access.is_performance_intelligence_enabled_for()`
itself.

## Journal Adapter (TASK 4)

`journal_adapter.py`'s `journal_entry_to_performance_input()` is a
pure mapping — TASK 4's own instruction: "win/loss o'zi hisoblamaydi,
sabab topmaydi" (does not compute win/loss itself, does not find a
cause). It reads an existing `TradeJournalEntry` (`ai/trade_journal/`,
Phase 66.2) type-only. `entry_quality`/`exit_quality`/
`discipline_score`/`risk_score` are deliberately absent — mirrors
`ai_layer.personal_ai.senior.journal_adapter.journal_entry_to_coaching_input()`'s own
"field deliberately omitted" precedent exactly. The one file in
`ai/performance/` permitted to import `ai_layer.knowledge_ai.knowledge_base.trade_journal.models`.

## Coaching Adapter (TASK 5)

`coaching_adapter.py`'s `performance_record_to_coaching_input()` is a
pure mapping — TASK 5's own instruction: "Faqat structure" (structure
only). It reads this package's own `PerformanceRecord` and returns a
plain, untyped dict of `CoachingRuntime.create()`-shaped keyword
arguments — `topic`/`priority`/`type`/`recommendation` are deliberately
absent, since `PerformanceRecord` has no topic-shaped field to relay
without inferring one. Unlike `ai_layer.personal_ai.senior.learning_adapter.py`, this
adapter never imports `ai_layer.personal_ai.senior.models` or
`ai_layer.personal_ai.senior.coaching_runtime` at all — no import is needed to return
a dict, mirroring `ai_layer.personal_ai.senior.journal_adapter.py`'s own actual shape.

## Analytics Adapter (TASK 6)

`analytics_adapter.py`'s `performance_records_to_win_rate_metric()`
reuses `backtesting_layer.statistics.strategy_report.compute_win_rate()` directly — a
plain, zero-division-safe `(wins, losses) -> float` utility already
reused by `backtesting_layer/statistics/performance_metrics.py` itself. Full reuse of
`backtesting_layer.statistics.performance_metrics.compute_performance_metrics()` does
**not** fit: it requires `SignalPerformance.r_multiple`, a field
`PerformanceRecord` carries no equivalent of, and synthesizing one from
a quality score would be fabrication — that gap is documented, not
worked around, in `docs/PHASE66_5_AUDIT.md` (TASK 0, question 2) and
this module's own docstring.

## Performance Intelligence Features (TASK 7)

Satisfied at Foundation level with no dedicated code file, per the
brief's own "Foundation darajasida qo'llab-quvvatlash... AI xulosa
keyingi bosqich" instruction — see `ai/performance/README.md`'s own
"TASK 7" section for the full mapping:

- **Trade Quality** (Entry/Exit/Timing/Execution) —
  `PerformanceRecord.entry_quality`/`.exit_quality`/`.notes`.
- **Behavior Tracking** (Discipline/Patience/FOMO/Revenge/
  Overtrading) — `PerformanceMetric.metric_name` free-text values,
  classified by `PerformanceCategory.DISCIPLINE`/`.PSYCHOLOGY`.
- **Pattern Storage** — "faqat saqlash" (storage only);
  `PerformanceRuntime` stores every record/metric as-is. Recognizing a
  recurring pattern across records is a future, separately-briefed
  phase.

## Owner Mode (TASK 8)

`access.py`'s `is_performance_intelligence_enabled_for(role, flags)`
requires **both**
`configuration.feature_flags.FeatureFlags.enable_performance_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/coaching/access.py`'s shape exactly.

## Memory Preparation (TASK 9)

`memory_adapter.py`'s `performance_memory_key(record) -> str` builds a
plain string key (`"performance:{user_id}:{id}"`) for a future,
separately-approved phase to use once real Memory storage is wired —
this module never imports `ai_layer.knowledge_ai.memory_manager` at all, since
`ai/memory/models.py`'s `MemoryScope` enum has no member shaped for a
performance record and adding one is out of this phase's own scope.
Mirrors `ai_layer.knowledge_ai.learning_engine.memory_adapter.memory_reference_key()`'s own
precedent exactly.

## What it is not

- No signal generation, no BUY/SELL/NO_TRADE decision of any kind.
- No Risk computation, no Trading Core interaction of any kind.
- No real AI inference — every quality score, metric value, and note
  is always caller-supplied, never generated or graded by this
  package.
- No database — `PerformanceRuntime` is in-memory only.
- No LLM, no network call.
- No new top-level package — lives inside the existing `ai/`.
- No pattern-recognition algorithm, no AI-generated coaching text, no
  Strategy Intelligence — Director Notes for Phase 66.6 and beyond.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `telegram/`, `database/`, `voice/`,
  `assistant/`, `media/`, `broadcast/`, `academy/`, `portfolio/`,
  `research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` — zero exceptions, permanently
  enforced by `tests/ai/performance/test_ai_performance_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_5_AUDIT.md`, `docs/PHASE66_5_FREEZE.md` — full
  documentation of this phase.
- `ai/performance/README.md` — the package's own top-level README.
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `ai/coaching/` — the sibling package this phase's `coaching_adapter.py`
  produces `CoachingRuntime.create()`-shaped kwargs for (structure
  only, no import needed).
- `analytics/` — the existing package this phase's `analytics_adapter.py`
  reuses `compute_win_rate()` from.
- `docs/ai/AI_COACHING.md` — the immediately preceding phase's own
  documentation.
