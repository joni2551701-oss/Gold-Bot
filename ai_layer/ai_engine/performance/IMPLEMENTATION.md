# AI Performance Intelligence (`ai/performance/`)

Phase 66.5 (AI Performance Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_5_AUDIT.md`'s TASK 0 audit — the sixth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/coaching/` (Phase 66.4).

## What this package is

A Foundation for structuring per-trade performance observations
(`PerformanceRecord`) and generic named metrics (`PerformanceMetric`)
derived from a trader's own Trade Journal records — quality scores,
discipline tracking, and pattern storage. AI still never decides a
trade: GoldBot's Trading Core and AI Analyst continue to be the only
source of any BUY/SELL/NO_TRADE decision. This phase builds the
contract and CRUD runtime only; it does not score, grade, or draw
conclusions itself.

### TASK 7 — Performance Intelligence features at Foundation level

The brief's three feature groups (Trade Quality, Behavior Tracking,
Pattern Storage) are satisfied by the models already defined in
`models.py`, with no dedicated code file — TASK 7's own instruction is
"Foundation darajasida qo'llab-quvvatlash... AI xulosa keyingi bosqich"
(support at Foundation level only; AI conclusions are a future phase):

- **Trade Quality** (Entry/Exit/Timing/Execution) — `PerformanceRecord.entry_quality`,
  `.exit_quality`, and `.notes` carry Timing/Execution observations as
  free text. All four are always caller-supplied (TASK 3's own rule:
  no scoring algorithm lives in this package).
- **Behavior Tracking** (Discipline/Patience/FOMO/Revenge/Overtrading)
  — represented as `PerformanceMetric.metric_name` free-text values
  (e.g. `"discipline_score"`, `"fomo_incidents"`, `"revenge_trade_count"`,
  `"overtrading_flag"`) rather than a new enum, the same "free text,
  no fixed taxonomy" posture `PerformanceRecord.result` already uses.
  `PerformanceCategory.DISCIPLINE`/`.PSYCHOLOGY` classify which of
  these a given `PerformanceRecord` concerns.
- **Pattern Storage** — "faqat saqlash" (storage only): `PerformanceRuntime`
  stores every record/metric as-is; recognizing a recurring pattern
  across records is explicitly a future, separately-briefed phase (see
  `docs/roadmap/AI_EVOLUTION.md`).

## What this package is not

- No signal generation, no BUY/SELL/NO_TRADE decision of any kind.
- No Risk computation, no Trading Core interaction of any kind.
- No LLM call, no Reasoning, no real inference anywhere — every quality
  score, metric value, and note is always caller-supplied, never
  generated or graded by this package.
- No database — SQLite/Postgres/Redis, none anywhere in this package.
  `PerformanceRuntime` stores records in an in-memory dict.
- No network call.
- No new top-level package — lives inside the existing `ai/`.
- No pattern-recognition algorithm, no AI-generated coaching text, no
  Strategy Intelligence — Director Notes for Phase 66.6 and beyond;
  this Foundation only classifies and stores individual performance
  observations.
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
- `docs/ai/AI_PERFORMANCE.md` — the full subsystem documentation.
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `ai/coaching/` — the sibling package this phase's `coaching_adapter.py`
  produces `CoachingRuntime.create()` kwargs for (structure only, no
  import needed).
- `analytics/` — the existing package this phase's `analytics_adapter.py`
  reuses `compute_win_rate()` from.
