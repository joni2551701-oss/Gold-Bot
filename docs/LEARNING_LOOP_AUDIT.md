# Learning Loop Foundation — Reuse Audit (Phase 60.6, TASK 1)

Read before any new code was written, per the Director's own
`exists? -> extend -> new module` rule (`CLAUDE.md`'s Module Reuse
Principle). Six directories audited: `analytics/`, `ai/` (incl.
`ai/journal/`), `lifecycle/`, `database/`, `context/`.

## What already exists

| Module | Shape | Verdict |
|---|---|---|
| `ai/journal/failure_analysis.py` — `FailureAnalysisEntry` | `signal_id`, `reason` (single free-text string), `context` (free-text), `result`, `created_at`. In-memory only. | **Not extended.** Loss-specific by name and contract (its own docstring: "narrower and failure-specific"); TASK 3 needs a shape covering wins *and* losses, with a list of structured reasons plus a `lesson`, not one free-text `reason`. Broadening `FailureAnalysisEntry` to cover wins would break its own stated purpose. `learning/outcome_analyzer.py` is a new, adjacent, disclosed-duplicate type — same "small documented duplication" precedent this codebase already accepted for Wyckoff-vs-AMD and Data Quality-vs-market_data.py. |
| `ai/journal/trade_journal.py` — `TradeJournalEntry` | A general completed-trade record (`pnl`, `rr`, `exit_price`, `ai_confidence`, `technical_score`, `decision`, `outcome`). No pattern detection, no failure/success classification, no repository — pure in-memory dataclass + factory, nothing else. | **Not extended or reused.** Different question (a full trade receipt vs. a learning-shaped record keyed to `market_phase`/`session`/`timeframe`, none of which `TradeJournalEntry` carries). |
| `analytics/signal_performance.py` — `SignalPerformance` | `performance_id`, `signal_id`, `strategy_id`, `context_id`, `result`, `profit_loss`, `r_multiple`, `duration`, `session`, `market_phase`, `timeframe`, `created_at`. **Largest overlap found** — 7 of `LearningRecord`'s 11 named fields already exist here under the same or an equivalent name. | **Not extended, not reused directly.** `SignalPerformance` is an in-memory, computed-on-demand analytics type with no repository and no persistence story (its own README: "Does not read or write the database"). `LearningRecord` (TASK 2) needs to be persisted append-only (TASK 5) — a different lifecycle. Reusing `SignalPerformance` as the persisted row shape would conflate an ephemeral analytics view with a permanent memory store. `learning/models.py`'s `LearningRecord` is a new, disclosed near-duplicate of `SignalPerformance`'s shared fields, adding the two genuinely new fields neither `SignalPerformance` nor any other module has anywhere in this codebase: `failure_type`, `success_pattern`. |
| `analytics/strategy_report.py` / `context_report.py` | Aggregate `SignalPerformance` records by strategy / (session, strategy, market_phase). Both already do "which condition wins more" grouping. | **Not extended.** TASK 4 (Pattern Detector) needs a *failure/success probability per condition combination* framed around `LearningRecord.failure_type`/`success_pattern` — a different question than a plain win-rate grouping, and its output (`PatternInsight`) is intentionally learning-specific, not another `*PerformanceReport`. `pattern_detector.py` is new; it does not import or duplicate the win/loss counting arithmetic (`compute_win_rate()` is reused directly where relevant — see TASK 4). |
| `analytics/validation_report.py` | Weekly signals/BUY/SELL + best session/market_phase report, built from `SignalPerformance`. | Confirmed no overlap — a period summary, not a pattern/failure classifier. |
| `lifecycle/paper_trade.py` — `PaperTrade` | The real, only source of a trade's `result`/`opened_at`/`closed_at`/`entry`/`stop_loss`/`take_profit`. No analysis, no learning concept. | Read-only input to `learning/outcome_analyzer.py` (TASK 3), `TYPE_CHECKING`-only — same convention `analytics/signal_performance.py` already uses for the same type. |
| `database/audit_log_models.py` + `audit_log_repository.py` | The exact "append-only, no update/delete, `init_X_schema()` in `database/models.py`, called from the repository's own `__init__`" pattern TASK 5 asks for verbatim ("append only, tarix o'chirilmaydi, auditga mos"). | **Reused as the structural template**, not imported — `database/learning_repository.py` (TASK 5) mirrors `AuditLogRepository`'s shape (`log_action()` → `record()`, `get_recent()`, `get_by_actor()` → `get_by_strategy()`) rather than inventing a new repository shape. |
| `database/raw_candle_repository.py` / `raw_candle_models.py` | A second real precedent for a database-layer model kept deliberately separate from its domain-layer counterpart (`RawCandle` vs. `data.twelve_data_client.Candle`) despite overlapping fields — the same "different name, same layer-separation reasoning" this audit applies to `LearningRecord` vs. a new `LearningRecordRow`. | Confirms the convention, not reused directly. |
| `context/` (all detectors) | No failure/pattern/learning concept anywhere — confirmed via full module list read in Phase 60.5's own audit, unchanged since. | No overlap. |

**No existing pattern-detection module, no existing `learning/` package, no Gemini/AI training-data exporter anywhere in this codebase.**

## Decisions carried into TASK 2–8

1. **`learning/models.py`'s `LearningRecord`** is a new, disclosed
   near-duplicate of `SignalPerformance`'s shared fields (`trade_id`
   replaces `SignalPerformance.duration`/`profit_loss`/`context_id`,
   which `LearningRecord` doesn't need; `failure_type`/`success_pattern`
   are the two genuinely new fields). `id` is **excluded** from the
   dataclass — same convention `AuditLogEntry`'s own docstring
   establishes ("repository-internal detail... same convention as
   every other Phase 59.x model"); a `LearningRecord` built by
   `outcome_analyzer.py` has no database id yet.
2. **`database/learning_models.py`** defines its own `LearningRecordRow`
   (not a second `LearningRecord`) — same disambiguation-by-naming
   discipline as `ExecutionSimulationResult`/`FundamentalContextSnapshot`
   before it, avoiding a same-name collision between the domain type
   (`learning/models.py`, in-memory, used by `outcome_analyzer.py`/
   `pattern_detector.py`) and the persistence type (`database/`,
   matches the `learning_records` table's own columns, including `id`).
3. **`database/learning_repository.py`** mirrors `AuditLogRepository`
   exactly: append-only (`record()` only — no `update()`/`delete()`
   method exists), `init_learning_schema()` added to
   `database/models.py` (same file every other schema lives in),
   called from the repository's own `__init__`, same as every other
   repository in this codebase.
4. **`learning/outcome_analyzer.py`** and **`learning/pattern_detector.py`**
   are genuinely new — nothing in `analytics/`/`ai/` computes a
   structured multi-reason win/loss explanation with a `lesson`, or a
   cross-record condition-combination failure/success probability.
   Neither imports `decision/`, `risk/`, `execution/`, `strategies/`,
   or `signals/` — both read only already-computed `PaperTrade`
   (`TYPE_CHECKING`), `LearningRecord`, and `context.fundamental_context`/
   `context.context_orchestrator` types (`TYPE_CHECKING`) where a
   caller supplies market context.
5. **`ai/learning_context.py`** — placed at the top level of `ai/`
   (not inside `ai/journal/`), matching `ai/prompts/`'s own placement
   (a sibling concern to journal, not a journal entry type itself).
   Advisory-only, same `AIAnalyzerInterface` boundary every `ai/`
   module already respects: explanation/summary/recommendation text
   only, never a decision, never itself calling `risk/`, `decision/`,
   or Telegram.
6. **`telegram/owner/learning_commands.py`** follows the exact
   established "real function, not live-wired" posture — thin
   wrappers over `analytics.learning_report`/`learning.pattern_detector`,
   same as `performance_commands.py`/`fundamental_commands.py` before
   it.
