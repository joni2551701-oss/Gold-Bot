# Phase 66.5 — AI Performance Intelligence Foundation — Foundation Reuse Audit

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). Audits `analytics/`, `ai/trade_journal/`, `ai/coaching/`,
`ai/learning/`, and `database/` before writing any Phase 66.5 code,
per this phase's own TASK 0 instruction. Confirms Phase 66.4 (AI
Coaching Intelligence) is locked (`docs/PHASE66_4_FREEZE.md` exists)
before starting, as this brief's own status line requires.

## TASK 0's four questions

### 1. Performance modeli mavjudmi?

**Yo'q, aynan shu shaklda emas.** `backtesting_layer/statistics/performance_metrics.py`
(Phase 60.4) already defines a `PerformanceMetrics` (plural) dataclass
— but it is a fixed-shape, 11-field portfolio-wide aggregate report
(`total_trades`, `win_rate`, `expectancy`, `profit_factor`,
`max_drawdown`, `recovery_factor`, `risk_adjusted_return`, ...),
computed from a sequence of `backtesting_layer.statistics.signal_performance.SignalPerformance`
objects (which carry `r_multiple`). This brief's own `PerformanceMetric`
(singular) is a generic, free-form key/value observation
(`metric_name`/`value`/`period`/`created_at`) meant for AI-layer
storage of a single named metric ("discipline_score" this week) — a
genuinely different shape and purpose, not a duplicate. This mirrors
the exact naming-collision-but-not-duplication pattern
`docs/PHASE66_2_AUDIT.md` (`TradeJournalEntry`) and
`docs/PHASE66_3_AUDIT.md` (`LearningRecord`) both already resolved:
same-domain name, different fully-qualified path, never imported
alongside each other, serving a different purpose.

No `PerformanceRecord`-shaped model (per-trade quality/discipline/risk
scores linked to a journal entry) exists anywhere in this codebase.

### 2. Analytics modulidan foydalanish mumkinmi?

**Qisman.** `backtesting_layer.statistics.strategy_report.compute_win_rate()` (a plain
`(wins, losses) -> float` utility, already reused by
`backtesting_layer/statistics/performance_metrics.py` itself) is directly reusable over
`PerformanceRecord.result` counts — `ai/performance/analytics_adapter.py`
reuses it rather than reimplementing a win-rate formula. Full reuse of
`backtesting_layer.statistics.performance_metrics.compute_performance_metrics()` is
**not** directly wireable: it requires `SignalPerformance.r_multiple`,
a field `PerformanceRecord` does not carry (and synthesizing one from
`result`/scores would be fabrication, forbidden). This gap is
documented, not worked around — a future phase that wants full
expectancy/profit-factor metrics over `PerformanceRecord` data needs
its own, separately-briefed r_multiple-shaped bridge.

### 3. Trade Journal ma'lumotlari yetarlimi?

**TASK 4's mapping uchun yetarli, TASK 2's barcha fieldlari uchun
emas.** `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry` (Phase 66.2)
already carries `trade_id`, `journal_id` (as its own `journal_id`),
`result`, `direction`, `confidence`, `lesson`, `reason` — enough to
populate `PerformanceRecord.trade_id`/`.journal_id`/`.result`/
`.direction`/`.confidence_score`/`.notes` via a pure mapping (TASK
4's own scope). `TradeJournalEntry` has **no** field shaped for
`entry_quality`/`exit_quality`/`discipline_score`/`risk_score` —
these four are always `None` unless a caller supplies them directly
to `PerformanceRuntime.create()`; `journal_adapter.py` never invents
them (TASK 4's own rule: "win/loss o'zi hisoblamaydi, sabab
topmaydi").

### 4. Duplicate PerformanceMetric yaratish kerakmi?

**Yo'q.** See question 1 — `PerformanceMetric` (this phase) and
`PerformanceMetrics` (Phase 60.4, `analytics/`) are different shapes
for different consumers (a generic AI-layer observation vs. a fixed
portfolio report). Both are kept; neither is renamed, moved, or
removed (Constitution Article 9). Documented here so the distinction
is never re-litigated as an oversight.

## Precedent confirmed (Article 7 Reuse Principle — reuse the pattern)

Read `ai/trade_journal/`, `ai/learning/`, and `ai/coaching/` (all four
files each: `models.py`, `access.py`, `*_runtime.py`, adapters,
`memory_adapter.py`) end to end. Every `66.x` AI Foundation phase
already established one consistent shape this phase reuses exactly:

- `models.py`: `@dataclass(frozen=True)` records + enums, every field
  a primitive, no Trading Core object reference (Article 3).
- `access.py`: `is_X_enabled_for(role, flags) -> bool`, gated by one
  dedicated `FeatureFlags` field AND `role == AIRole.OWNER`.
- `*_runtime.py`: CRUD-only over a private `Dict[str, Record]`,
  in-memory (no `database/` import), every method re-checks access
  independently, `dataclasses.replace()` for updates.
- `*_adapter.py`: pure mapping functions, `EntryType -> Dict[str, Any]`
  kwargs for the target runtime's own `create()`, never calls
  `create()` itself, never infers a caller-scoped field.
- `memory_adapter.py`: a single `*_memory_key(record) -> str`
  function, **never imports `ai_layer.knowledge_ai.memory_manager`** (`ai/learning/memory_adapter.py`'s
  and `ai/trade_journal/memory_adapter.py`'s own documented reason:
  no `MemoryScope` member is shaped for this record type, and adding
  one is out of this phase's scope).

**TASK 1's own file tree omits `memory_adapter.py`** even though TASK
9 explicitly requires `performance_memory_key()`. Resolved the same
way this session's Owner Snapshot v1.1 phase resolved an analogous
gap (TASK 1's field list omitting `signals_today`, needed by TASK 3):
add the file additively, inside the already-being-created package —
not a new top-level module, just one more file alongside the other
six TASK 1 already lists, matching every sibling `66.x` package's own
real structure (`trade_journal/`, `learning/`, and `coaching/` all
have a `memory_adapter.py` none of their own original TASK 1 briefs
enumerated either, going by their current on-disk shape).

## Isolation requirement

`ai/performance/` never imports `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `telegram/`, `database/`,
`voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
`portfolio/`, `research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` — the same
isolation list `ai/coaching/README.md` already documents for its own
package, extended with `ai_layer.knowledge_ai.memory_manager` per this phase's own TASK 9 rule.
Enforced by `tests/ai/performance/test_ai_performance_isolation.py`
(AST-based, mirrors `tests/ai/coaching/test_ai_coaching_isolation.py`
exactly).

`ai/performance/journal_adapter.py` is the one file permitted to
import `ai_layer.knowledge_ai.knowledge_base.trade_journal.models` (type-only); `ai/performance/coaching_adapter.py`
is the one file permitted to import `ai_layer.personal_ai.senior.models`
(type-only) — mirrors `ai/coaching/journal_adapter.py`'s own "one file
permitted" precedent exactly. `ai/performance/analytics_adapter.py` is
the one file permitted to import `analytics.*`.

## Conclusion

No Director Decision pause required. Every model this phase needs is
either genuinely new (`PerformanceRecord`, `PerformanceMetric`,
`PerformanceCategory` — confirmed non-duplicate above) or already
exists and is reused outright (`compute_win_rate()`, the `AIRole`/
`FeatureFlags`/CRUD-runtime/adapter/memory-key patterns). Proceeding
to TASK 1.
