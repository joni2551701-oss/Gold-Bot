# Phase 61.3 — AI Intelligence Layer: Reuse Audit

TASK 1 of the Phase 61.3 Worker Brief. Audits `context/`, `learning/`,
`analytics/`, `ai/`, `database/`, `telegram/`, `education/` before any
code is written. Per the brief's own rule: "Agar reuse qilsa bo'ladigan
modul topilsa, yangi kod yozilmaydi" (if a reusable module is found,
no new code is written) — every TASK 2-9 decision below traces back to
a specific finding here.

## `context/`

`context_layer/context_engine/context_orchestrator.py`'s `ContextSnapshot` (12 required
fields: candles, structure, bos_events, choch_events, liquidity_zones,
liquidity_sweeps, order_blocks, fair_value_gaps, amd_events,
wyckoff_events, session_events, market_regime) is the full internal
detection output — `ai.interfaces.MarketContext`'s own docstring
already states it is "deliberately narrower... so a future provider's
input contract doesn't leak internal Context Layer types into `ai/`."

**Gap confirmed**: no adapter from `ContextSnapshot` to `MarketContext`
exists. **Reuse found**: `context_layer/context_engine/snapshot.py`'s
`from_context_snapshot(context_snapshot, symbol, timeframe, engine_version=None) -> ContextSnapshotSchema`
already converts `ContextSnapshot` into a flat, JSON-serializable
summary shape — its own docstring names "a future AI provider... or
Education consumer" as an intended reader. TASK 2 builds the
`ContextSnapshot -> MarketContext` adapter by calling
`from_context_snapshot()` and formatting `MarketContext.summary` from
its already-computed fields, not by re-deriving structure/liquidity/
regime logic a second time.

## `learning/`

Every module already produces read-only, already-computed
intelligence: `learning/pattern_detector.py` (`PatternInsight`,
`detect_patterns()`), `learning/confidence.py`
(`compute_pattern_confidence()`), `learning/regime_memory.py`
(`RegimeMemory`, `format_regime_summary()`), `learning/outcome_analyzer.py`
(`TradeAnalysis`, `analyze_trade_result()`). `ai/learning_context.py`
(Phase 60.6/60.7) already composes these into `LearningContext` for
`ai/context/context_builder.py`'s `build_ai_context()` — **TASK 2's
"Learning Context" step is already fully built and wired**, nothing
new needed there.

## `analytics/`

Twelve report-building modules exist (`performance_metrics.py`,
`strategy_report.py`, `learning_report.py`, `context_report.py`,
etc.), each already following the "build result + format to text"
pattern a future Explanation/Education tool needs. No module named
`explain*` exists here — the only "explain" logic in the repo is
`signal_layer/signal_scoring/explainability.py`'s `explain_signal()` (why a *signal*
fired, not a trade outcome or a conversational answer). **TASK 7's
Explanation Engine reuses `signal_layer/signal_scoring/explainability.py`'s already-built
`SignalExplanation` as one optional input rather than re-deriving
signal reasoning**, and reuses `analytics/learning_report.py`/
`analytics/strategy_report.py`'s formatted text for summary-shaped
answers rather than re-aggregating raw records.

## `ai/`

- `ai/session/` (`SessionManager`, `ConversationState`, `ContextWindow`)
  — **complete, tested, and confirmed unused anywhere in production
  code** (only referenced from its own test file). TASK 5's
  Conversation Engine is built directly on top of this package, not a
  new session mechanism.
- `ai/memory/context_memory.py`'s `ContextMemory` (save/load/clear,
  string key) — **complete and confirmed unused in production code**.
  TASK 6's five memory "layers" are five namespaced `ContextMemory`
  instances behind one facade, not five new storage implementations.
- `ai/tools/*.py` — every one of the four existing tools
  (`market_tool.py`, `news_tool.py`, `analytics_tool.py`,
  `education_tool.py`) is an explicit, self-disclosed placeholder
  (`run()` returns a fixed stub string). TASK 4 replaces their bodies
  with real, read-only logic — the `BaseAITool` interface and
  `ToolRegistry` (Phase 61.0) are reused unchanged.
- `ai/runtime/ai_service.py`'s `AIService.ask()` (Phase 61.2) is the
  one call path every new module this phase routes through — TASK 5/7
  build on top of it, never bypass it or duplicate its Access ->
  Capability -> Router -> Provider -> Validator -> Cache -> Audit
  chain.
- `ai/audit/provider_stats.py`'s `ProviderStats` already carries
  every field TASK 9's benchmark needs (`avg_latency_ms`,
  `success_rate`, `total_cost`, `failure_count`) — TASK 9 adds a
  ranking function over this existing data, no new metric.

## `database/`

`database_layer/journal_repository/learning_repository.py`'s `LearningRepository.get_recent()`/
`get_by_strategy()` and `database_layer/trade_repository/signal_repository.py`'s
`SignalRepository.get_closed_signals()` are the two existing read
paths to historical trade data — TASK 4's Learning Tool and TASK 6's
Trade Memory read through these repositories directly (read-only,
matching every existing repository's own contract) rather than adding
a new persistence layer.

## `telegram/`

**Confirmed: no free-text/conversational handling exists anywhere.**
`platform_layer/telegram/command_router.py`'s `_parse_command()` requires a leading
`/`; anything else resolves to a fixed "unknown command" response.
Every handler in `platform_layer/telegram/handlers.py` and all 18
`platform_layer/telegram/owner/*.py` modules are fixed-command handlers. This
confirms TASK 5's Conversation Engine is genuinely new logic (no
existing chat flow to extend) — and, per this phase's own scope, it
is **not wired into `platform_layer/telegram/command_router.py`** this phase, same
"foundation, not yet live-wired" posture as every prior phase's new
module.

## `education/` / `knowledge/`

Neither exists as a package anywhere in the repo. Several `docs/*.md`
files (`docs/WYCKOFF.md`, `docs/MARKET_REGIME.md`,
`docs/EXPLAINABILITY.md`, `docs/SESSION_INTELLIGENCE.md`) already
contain the underlying domain concepts in prose form — TASK 3's
`knowledge/` entries are derived from this existing documentation
(the same facts this codebase already committed to, restated in a
queryable data shape), not newly invented trading theory.

**Structural adaptation**: the brief's own literal paths
(`knowledge/smc/`, `knowledge/wyckoff/`, etc., as subdirectories) are
implemented as flat files (`knowledge/smc.py`, `knowledge/wyckoff.py`,
...) instead — each category is a handful of `KnowledgeEntry` constants,
not enough content to justify a subpackage with its own `__init__.py`.
Same precedent this codebase has used before (e.g. Phase 59 Val TASK 7
placed `failure_analysis.py` inside the existing `ai/journal/` instead
of a new top-level `journal/` directory the brief's own path implied,
because "a second, disconnected top-level journal/ package would just
be a confusingly-parallel duplicate").

## AI → Trading connection risk

Every new TASK 2-9 module was designed against the same isolation
boundary Phase 61.2's TASK 1 already established and verified: no new
module imports `decision/`, `risk/`, `execution/`, or `strategies/`.
TASK 4's real tools are explicitly read-only (repository `get_*`
methods only, never a `save`/`create`/`update` call). This is
re-verified by AST sweep at the end of this phase (TASK 10), matching
Phase 61.2's own closing verification step.

## Summary of what's built new vs. reused

| TASK | New | Reused |
|---|---|---|
| 2 (Context Intelligence) | `ContextSnapshot -> MarketContext` adapter (one function) | `context_layer/context_engine/snapshot.py`'s `from_context_snapshot()`; `ai/learning_context.py`; `ai/journal/trade_journal.py`; `ai/profiles/user_profile.py`; `ai/context/context_builder.py` (unmodified) |
| 3 (Knowledge Foundation) | `knowledge/` package (new, flat structure) | Content sourced from existing `docs/*.md` |
| 4 (Real Tool Calling) | Real logic inside existing tool classes | `ai/tools/tool_registry.py`'s `BaseAITool`/`ToolRegistry` (unchanged); `database_layer/journal_repository/learning_repository.py`, `database_layer/trade_repository/signal_repository.py`, `database_layer/market_repository/market_snapshot_repository.py`; `context_layer/fundamental/fundamental_context.py`; `analytics/*` |
| 5 (Conversation Engine) | `ConversationEngine` (new, thin) | `ai/session/` (entirely, unmodified); `ai/runtime/ai_service.py` (unmodified) |
| 6 (Memory Runtime) | `MemoryRuntime` facade (new, thin) | `ai/memory/context_memory.py`'s `ContextMemory` (5 instances, unmodified) |
| 7 (Explanation Engine) | `ExplanationEngine` (new, thin) | `ai/runtime/ai_service.py`; `signal_layer/signal_scoring/explainability.py`'s `SignalExplanation`; `analytics/learning_report.py`/`strategy_report.py` |
| 8 (Runtime Trace) | `request_id` field + trace lookup function | `ai/audit/request_log.py`/`response_log.py`'s existing UUID `request_id` (no new ID generator) |
| 9 (Provider Benchmark) | One ranking function | `ai/audit/provider_stats.py`'s `ProviderStats` (unmodified fields) |
