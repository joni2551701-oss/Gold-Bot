# Phase 66.4 Audit — AI Coaching Intelligence Foundation (TASK 0)

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). This is the mandatory TASK 0 audit for Phase 66.4 — before
any new module is created, every package the brief names is checked for
an existing Coaching model, Coaching Runtime, Coaching Manager,
Coaching Registry, existing contract, or anything that could be
extended instead of duplicated.

## Packages audited

### `ai/learning/` (Phase 66.3, LOCKed)

- **Nima mavjud?** `LearningRecord` (`id`, `user_id`, `topic`, `level`,
  `confidence`, `notes`, `source`, `status`, `created_at`),
  `LearningTopic`/`LearningLevel`/`LearningSource`/`LearningStatus`
  enums, `LearningRuntime` (CRUD: `create`/`get`/`list`/`update`/
  `archive`). No Coaching model, Runtime, Manager, or Registry of any
  kind.
- **Nima qayta ishlatiladi?** `LearningRecord` is read type-only by
  this phase's own `learning_adapter.py` (TASK 4) — the exact upstream
  contract for the Learning → Coaching pipeline stage the brief's own
  diagram names. Never modified.
- **Nima mos emas?** Nothing about `LearningRecord`'s own shape needs
  changing — `ai/learning/` is LOCKed (Director acceptance, this
  session) and this phase adds zero fields to it (LOCK's own "additive
  only" terms are not invoked this phase — no new field was needed).
- **Nima yangi yaratiladi?** Nothing in `ai/learning/` itself; a new,
  separate `ai/coaching/learning_adapter.py` performs the mapping.

### `ai/trade_journal/` (Phase 66.2, LOCKed)

- **Nima mavjud?** `TradeJournalEntry` (`journal_id`, `chart_id`,
  `trade_id`, `symbol`, `timeframe`, `direction`, `entry`, `sl`, `tp`,
  `result`, `confidence`, `reason`, `lesson`, `mistakes`, `created_at`),
  `ReplayContext`, `TradeJournalRuntime` (CRUD). No Coaching concept.
- **Nima qayta ishlatiladi?** `TradeJournalEntry` is read type-only by
  this phase's `journal_adapter.py` (TASK 5) — `lesson`/`mistakes`/
  `reason` are the fields a Coaching input can honestly relay without
  inference.
- **Nima mos emas?** N/A — not extended, only read type-only.
- **Nima yangi yaratiladi?** A new, separate `ai/coaching/journal_adapter.py`.

### `ai/chart_intelligence/` (Phase 66.1, LOCKed)

- **Nima mavjud?** `ChartAnalysis`/`ChartContext`/`ChartRuntime`. No
  Coaching concept.
- **Nima qayta ishlatiladi?** Nothing — the brief's own TASK 4/5 name
  only Learning and Trade Journal as Coaching's input sources, not
  Chart Intelligence directly (Coaching reads Learning/Journal, which
  themselves already compose Chart Intelligence upstream).
- **Nima yangi yaratiladi?** N/A.

### `ai/trading_analyst/` (Phase 66.0, LOCKed)

- **Nima mavjud?** `TradingAnalysis`/`TradingAnalysisInput`/
  `TradingAnalystRuntime`. No Coaching concept.
- **Nima qayta ishlatiladi?** Nothing — same reasoning as Chart
  Intelligence above; not a direct Coaching input source per the
  brief.
- **Nima yangi yaratiladi?** N/A.

### `ai/explanation/`

- **Nima mavjud?** `ExplanationBuilder`/`ExplanationEngine`/
  `ExplanationInput`/`ExplanationOutput` — a template-based text
  generator composed by `IntelligenceRuntime.run()` and several `66.x`
  Runtimes (Trading Analyst, Chart Intelligence). No Coaching model,
  Runtime, or Registry.
- **Nima qayta ishlatiladi?** Nothing this phase — TASK 3's own
  instruction is "LLM yo'q, Reasoning yo'q, Inference yo'q" for
  `CoachingRuntime`; composing `ExplanationBuilder` would require the
  Runtime to synthesize `message`/`recommendation` text from
  `LearningRecord`/`TradeJournalEntry` data, which is real inference
  work forbidden this phase. `CoachingRecommendation.message`/
  `recommendation` are caller-supplied fields (TASK 2), the same
  "relayed, never generated" posture every prior `66.x` phase's
  primitive-only contract already established.
- **Nima mos emas?** Its own composition pattern doesn't fit a
  CRUD-only, no-inference Runtime.
- **Nima yangi yaratiladi?** N/A — not composed by this phase at all.

### `ai/conversation/`

- **Nima mavjud?** `ConversationEngine`/`ConversationState`, a
  deterministic session/message log, no Coaching concept.
- **Nima qayta ishlatiladi?** Nothing — not named as a Coaching input
  source by the brief, and `CoachingRuntime`'s own CRUD-only, no-LLM
  posture has no session/message concept to log.
- **Nima yangi yaratiladi?** N/A.

### `knowledge/`

- **Nima mavjud?** `KnowledgeCategory` (SMC/WYCKOFF/RISK/PSYCHOLOGY/
  EXAMPLES/FAQ), `KnowledgeManager.search()` — a static
  content-category taxonomy for knowledge articles. No Coaching model.
- **Nima qayta ishlatiladi?** Nothing — `CoachingTopic` (TASK 2) is a
  distinct, per-user coaching-topic vocabulary (not yet finalized in
  the brief's own field list beyond the enum name), not a content
  category. Same "coincidental overlap, not duplication" conclusion
  `docs/PHASE66_3_AUDIT.md` already reached for `LearningTopic` vs.
  `KnowledgeCategory`.
- **Nima yangi yaratiladi?** `CoachingTopic` (TASK 2), a new enum
  local to `ai/coaching/models.py`.

### `analytics/`

- **Nima mavjud?** `performance_metrics.py` (win rate/Sharpe/drawdown/
  profit factor), `strategy_report.py`, `learning_report.py` — all
  statistical/performance computation. No Coaching concept.
- **Nima qayta ishlatiladi?** Nothing — the brief's own header states
  this phase "Risk hisoblamaydi" and never computes anything; `analytics/`
  is explicitly out of scope, same conclusion as every prior `66.x`
  phase's own audit.
- **Nima yangi yaratiladi?** N/A.

### `database/`

- **Nima mavjud?** Real, wired persistence for several concerns
  (signals, learning outcome records, emergency states, etc.). No
  Coaching table or repository.
- **Nima qayta ishlatiladi?** Nothing — `ai/coaching/` must not import
  `database/` at all (brief's own isolation list, TASK 8); `CoachingRuntime`
  is in-memory only, same "Foundation, not a real persistence layer"
  convention every `66.x` Runtime already established.
- **Nima yangi yaratiladi?** N/A.

### `learning/` (top-level, Phase 60.6/60.7)

- **Nima mavjud?** `LearningRecord` (trade-outcome pattern statistics,
  DB-persisted) — already reviewed and rejected for reuse in
  `docs/PHASE66_3_AUDIT.md`. No Coaching concept.
- **Nima qayta ishlatiladi?** Nothing — same conclusion as Phase
  66.3's own audit; this phase does not touch `learning/` either.
- **Nima yangi yaratiladi?** N/A.

### `coaching/` (top-level package)

- **Nima mavjud?** **Does not exist.** Confirmed via
  `ls /home/user/Gold-Bot/coaching` (no such directory) and a
  repo-wide `grep -ril "coaching" --include="*.py"` outside `tests/`,
  which returns only docstring mentions inside `ai/learning/` and
  `ai/trade_journal/` referencing a *future* Coaching phase (written
  during Phase 66.2/66.3 themselves) — no actual Coaching code
  anywhere in the codebase.
- **Nima qayta ishlatiladi?** N/A — nothing exists.
- **Nima yangi yaratiladi?** `ai/coaching/` — the entire package (TASK
  1).

## Conclusion — genuine gap, TASK 1's package decision

Per Constitution Article 11 step 2 ("can an existing module be extended
without breaking its contract"): no existing package in this codebase
has a Coaching model, Runtime, Manager, or Registry of any kind — not
`ai/learning/`, not `ai/trade_journal/`, not `knowledge/`, not
`analytics/`, not the top-level `learning/`. This is a genuine gap
(step 1 and step 2 both answer NO).

**Decision: `ai/coaching/` — a new subpackage inside the
already-existing `ai/` top-level package**, following the exact
precedent `ai/trading_analyst/` (66.0), `ai/chart_intelligence/`
(66.1), `ai/trade_journal/` (66.2), and `ai/learning/` (66.3) all
already set — per this phase's own TASK 1 instruction. No new
top-level package is created (Module Reuse Principle's highest-cost
option, correctly avoided).

**No naming collision this phase**: `CoachingRecommendation`,
`CoachingTopic`, `CoachingPriority`, `CoachingType`, `CoachingStatus`,
and `CoachingRuntime` are all new names — no pre-existing bare class
name collision anywhere in the codebase to document (unlike Phase
66.2's `TradeJournalEntry` and Phase 66.3's `LearningRecord`
namesake situations).

## Related documents

- `docs/PHASE66_3_AUDIT.md` — the immediately preceding phase's own
  audit, whose two-namesake naming-collision discipline this audit
  checked against (and found not applicable this phase).
- `docs/ai/AI_COACHING.md` — this phase's own full documentation
  (TASK 10).
- `docs/constitution/CONSTITUTION.md` Article 3 — the zero-exception
  `ai/` → `decision/`/`risk/`/`execution/` import rule this phase's
  models are checked against, plus this phase's own isolation list
  (TASK 8).
