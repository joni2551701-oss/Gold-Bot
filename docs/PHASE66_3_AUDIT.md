# Phase 66.3 Audit — AI Learning Intelligence Foundation (TASK 0)

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). This is the mandatory TASK 0 audit for Phase 66.3 — before
any new module is created, every package the brief names is checked
for an existing Learning model, Learning Runtime, Learning Manager,
Learning Registry, existing contract, existing model, or existing
persistence. Each question is answered **YES** or **NO** as the brief
requires.

## Packages audited

### `learning/` (top-level package, Phase 60.6/60.7)

- **Learning modeli bormi?** **YES** — `learning/models.py`'s
  `LearningRecord` (`record_id`, `trade_id`, `signal_id`,
  `strategy_name`, `market_phase`, `session`, `timeframe`, `result`,
  `r_multiple`, `failure_type`, `success_pattern`, `htf_bias`,
  `volatility_state`, `fundamental_bias`, `confidence_score`,
  `engine_version`, `sample_size`, `created_at`). This is a
  **trade-outcome pattern-statistics record** — every field describes
  one already-closed trade's own market context and result. It is
  **not** a per-user topic-mastery record: it has no `user_id`, no
  `topic`, no `level`. Different shape, different purpose from this
  phase's own `LearningRecord` (TASK 2).
- **Learning Runtime bormi?** **NO** — no class named `LearningRuntime`
  exists anywhere in `learning/`. The closest is
  `learning/outcome_analyzer.py`'s `analyze_trade_result()` (a pure
  function, not a CRUD runtime) and `learning/pattern_detector.py`'s
  `detect_patterns()` (statistical grouping, not CRUD).
- **Learning Manager bormi?** **NO** — no Manager class in `learning/`.
- **Learning Registry bormi?** **NO** — no Registry in `learning/`.
- **Existing contract bormi?** **YES**, but wrong shape — see
  `LearningRecord` above.
- **Existing model bormi?** **YES**, but wrong shape — see above.
- **Existing persistence bormi?** **YES** —
  `database_layer/journal_repository/learning_models.py`'s `LearningRecordRow` +
  `database_layer/journal_repository/learning_repository.py`'s `LearningRepository.record()`
  (real, append-only SQLite persistence, wired). This is exactly the
  kind of persistence Rule 3 forbids this phase's own Foundation from
  having — confirming `learning/`'s own contract cannot be reused
  without inheriting a database dependency chain.

**Conclusion**: `learning/` is a real, load-bearing, DB-persisted
trade-outcome observation system — a different concern from what this
phase builds (a per-user, in-memory topic-mastery Foundation). Not
reused; `ai/learning/` never imports `learning/` (confirmed by a
dedicated isolation test, since the brief's own Rule 2 list does not
explicitly name it but Rule 3's "no database" spirit forbids pulling
in `learning/`'s own DB-touching import chain).

### `ai/` (top-level package)

- **Learning modeli bormi?** **NO new dataclass**, but **YES, one
  directly relevant existing file**: `ai/learning_context.py`'s
  `LearningContext` (Phase 60.6, extended Phase 60.7) — a
  **read-only, already-computed-data bundle** (`recent_failures`,
  `successful_patterns`, `strategy_stats`, `patterns`, `failures`,
  `regimes`, `confidence`) built *from* `learning.models.LearningRecord`
  via `learning.pattern_detector`/`learning.confidence`/
  `analytics.strategy_report`. This is a **different concept
  entirely** — it packages statistical trade-pattern summaries for a
  *future AI explainer* to read, not a per-user learning-progress
  record with a `topic`/`level`. It also transitively imports
  `learning/` and `analytics/`, both out of scope for this phase's own
  narrow, database-free Foundation. **Not reused** — `ai/learning/`
  and `ai/learning_context.py` remain two separate, unrelated files
  (`ai.learning` the new package vs. `ai.learning_context` the
  existing single-file module — no Python namespace collision, and no
  import either direction).
- **Learning Runtime/Manager/Registry bormi?** **NO** — nothing in
  `ai/` (outside `ai/learning_context.py`'s own module-level functions)
  matches.

### `ai/trade_journal/` (Phase 66.2, LOCKed)

- **Existing contract bormi?** **YES** — `TradeJournalEntry`
  (`journal_id`, `chart_id`, `trade_id`, `symbol`, `timeframe`,
  `direction`, `entry`, `sl`, `tp`, `result`, `confidence`, `reason`,
  `lesson`, `mistakes`, `created_at`). This is the exact upstream
  contract TASK 4's `journal_adapter.py` reads type-only (never
  imports `ai.trade_journal` anywhere else in the new package) — a
  real composition, not a duplicate.
- **Learning model/Runtime/Manager/Registry bormi?** **NO** —
  `ai/trade_journal/` is CRUD-only over journal entries, no learning
  concept.

### `ai/chart_intelligence/` (Phase 66.1, LOCKed)

- **Learning model/Runtime/Manager/Registry/contract bormi?** **NO** —
  audited for completeness per the brief's own list; this phase's
  TASK 4/5 do not compose it directly (only `ai/trade_journal/` is
  named as the Learning input source), so `ai/learning/` never imports
  `ai.chart_intelligence`.

### `ai/trading_analyst/` (Phase 66.0, LOCKed)

- **Learning model/Runtime/Manager/Registry/contract bormi?** **NO** —
  same conclusion as Chart Intelligence; not composed by this phase.

### `knowledge/`

- **Learning model bormi?** **NO** — `knowledge/models.py`'s
  `KnowledgeCategory` (SMC/WYCKOFF/RISK/PSYCHOLOGY/EXAMPLES/FAQ) is a
  coarse **content-category** taxonomy for static knowledge articles,
  not a per-user skill-topic tracker. `LearningTopic` (TASK 2, 12
  values) is finer-grained and answers a different question ("which
  skill is this user being tracked on," not "which article category
  is this"). Some vocabulary overlap (`RISK`, `PSYCHOLOGY` appear in
  both) is coincidental naming, not duplication — different enums,
  different purposes, no shared identity. Not reused, not imported.

### `ai/memory/`

- **Learning model/Runtime/Manager/Registry bormi?** **NO** —
  `MemoryScope`'s six members (`CONVERSATION`/`MARKET`/`EDUCATION`/
  `USER_PREFERENCE`/`EXPLANATION_HISTORY`/`KNOWLEDGE_REFERENCE`) has
  no member shaped for a learning-topic record, and TASK 5's own
  instruction ("Memory Runtime chaqirilmaydi" — Memory Runtime is
  never called) means this phase does not add one either. Mirrors
  Phase 66.2's own `memory_adapter.py` precedent exactly: a plain
  string-key generator, zero `ai.memory` import.

### `database/`

- **Existing persistence bormi?** **YES** —
  `database_layer/journal_repository/learning_models.py`/`learning_repository.py` (covered
  above under `learning/`). Confirms Rule 3's own premise: real
  persistence already exists for the *other* learning concept; this
  phase must not create a second one or touch the existing one.

### `analytics/`

- **Learning model/Runtime bormi?** **NO** new model, but
  `analytics/strategy_report.py`'s `compute_win_rate()` is reused
  *indirectly* by `ai/learning_context.py` (not by this phase).
  `analytics/performance_metrics.py` (win rate/Sharpe/drawdown/profit
  factor) is explicitly out of scope — Rule 6 forbids performance
  computation of any kind in this phase. Not imported by
  `ai/learning/`.

## Conclusion — genuine gap, TASK 1's package decision

Per Constitution Article 11 step 2 ("can an existing module be
extended without breaking its contract"): `learning/models.py`'s
`LearningRecord` fails this test on two independent grounds — its
field shape answers a different question (trade-outcome statistics,
not per-user topic mastery) and its own package already has real,
wired database persistence, which Rule 3 forbids this phase's
Foundation from acquiring by association. `ai/learning_context.py`'s
`LearningContext` is a read-only aggregation bundle for a future AI
explainer, not a CRUD-able per-user record, and itself transitively
depends on `learning/`/`analytics/` — also unsuitable to extend.

**Decision: `ai/learning/` — a new subpackage inside the
already-existing `ai/` top-level package**, following the exact
precedent `ai/trading_analyst/` (66.0), `ai/chart_intelligence/`
(66.1), and `ai/trade_journal/` (66.2) all already set — per this
phase's own TASK 1 instruction.

**Naming note (documented, not a defect):** `LearningRecord` is used
by two, non-colliding fully-qualified paths in this codebase after
this phase: `learning.models.LearningRecord` (Phase 60.6, trade-outcome
statistics, DB-persisted, untouched by this phase) and
`ai.learning.models.LearningRecord` (this phase, per-user topic
mastery, in-memory only). The two are never imported into the same
file and serve genuinely different purposes — recorded here explicitly
so no future reader mistakes the bare class name for a duplicate, the
same discipline `docs/PHASE66_2_AUDIT.md` already applied to
`TradeJournalEntry`'s own two-namesake situation.

## Related documents

- `docs/PHASE66_2_AUDIT.md` — the immediately preceding phase's own
  audit, whose two-namesake naming-collision discipline this audit
  mirrors for `LearningRecord`.
- `docs/ai/AI_LEARNING.md` — this phase's own full documentation
  (TASK 10).
- `docs/LEARNING_LOOP.md`, `learning/README.md` — the pre-existing,
  unrelated `learning/` package's own documentation.
- `docs/constitution/CONSTITUTION.md` Article 3 — the zero-exception
  `ai/` → `decision/`/`risk/`/`execution/` import rule this phase's
  models are checked against, plus this phase's own Rule 2's wider
  list (`signals/`/`telegram/`/`database/`/`monitoring/`/`strategies/`).
