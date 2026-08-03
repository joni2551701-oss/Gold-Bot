# Phase 60.10 — v0.4 Foundation Freeze & Final Architecture Audit

Audit-only phase, per the Director's own STRICT RULES: no business
logic in `core/`, `strategies/`, `signals/`, `decision/`, `risk/`,
`execution/`, `ai/`, `context/`, `data/`, or `learning/` was read for
the purpose of changing it — every finding below is report-only.
Nothing was deleted. Method: full-repository AST parsing (import graph,
unused-module detection) cross-checked against `tests/` coverage and
each module's own self-documentation, plus this session's own
accumulated knowledge of every phase (60.0 through 60.9) that built
this codebase.

## TASK 1: Complete Module Inventory

| Package | .py files | Purpose | Depends on | Used by | Foundation status |
|---|---|---|---|---|---|
| `core/` | 16 | Orchestration: `TradingPipeline` (the one real entry point), logger, secrets, error codes, system/emergency state, `PipelineGuard` | `ai`, `context`, `data`, `database`, `decision`, `features`, `risk`, `signals`, `telegram` (delivery only) | `main.py`, every other package's own logger/secrets calls | **Live** — `core/pipeline.py` is the only module that actually runs end-to-end in production |
| `data/` | 23 | Market data fetch/normalization/caching, provider abstraction, historical sync | `core`, `database` | `context`, `core`, `backtesting`, `telegram` | **Live** (TwelveData) + **Foundation** (MT5/Bitget/Binance stubs, normalization layer) |
| `context/` | 20 | SMC market analysis: structure, liquidity, order blocks, FVG, AMD, Wyckoff, session, market regime, market phase, HTF bias, fundamental context | `core`, `data` | `signals`, `decision`, `ai`, `backtesting`, `core/pipeline.py` | **Live** |
| `strategies/` | 9 | Strategy definitions + `StrategyManager`/`StrategyRegistry` (lifecycle metadata) | `context`, `signals` | `signal_layer/signal_engine/signal_engine.py` | **Live** |
| `signals/` | 7 | `SignalCandidate` generation, quality scoring, explainability, schema/adapter for persistence | `context`, `core`, `decision` (type-hints only), `strategies` | `core/pipeline.py`, `ai`, `decision`, `risk`, `backtesting` | **Live** |
| `ai/` | 18 | Advisory analysis: `AIAnalyzer` (heuristic stub), prompt management, journal, memory, learning context adapter | `analytics`, `context`, `core`, `learning`, `signals` | `core/pipeline.py`, `decision`, `platform_layer/telegram/signal_formatter.py` | **Live** (stub) + **Foundation** (prompts/journal/memory not yet real-provider-backed) |
| `decision/` | 3 | `DecisionEngine` — weighted-confidence blend, APPROVE/REJECT/NO_TRADE | `ai`, `context`, `signals` | `core/pipeline.py`, `risk`, `backtesting` | **Live** |
| `risk/` | 2 | `RiskManager` — geometry validation, position sizing, the one hard safety gate | `decision`, `signals` | `core/pipeline.py`, `execution` (type-hints), `backtesting` | **Live** |
| `execution/` | 9 | `ExecutionEngine`/`SignalLifecycle` (both permanently inert, zero real callers — Trading Safety boundary, not an oversight); `execution/simulator/` (real, tested paper-execution simulation) | `lifecycle`, `risk` | `execution/simulator/` used by `platform_layer/telegram/owner/execution_commands.py`; `execution_engine.py`/`signal_lifecycle.py` used by nothing | **Foundation** (deliberately inert core) + **Live** (simulator) |
| `analytics/` | 12 | Performance/report builders: signal, strategy, context, validation, gap, dataset, learning, execution, performance-metrics, equity-curve, benchmark reports | `data`, `database`, `execution`, `learning`, `lifecycle`, `signals` | `platform_layer/telegram/owner/*.py`, `backtesting`, `ai_layer/knowledge_ai/learning_context.py` | **Foundation** (all real, tested, none wired to a live Telegram command) |
| `learning/` | 7 | Observe → analyze → report loop: outcome analysis, pattern detection, confidence scoring, regime memory, the trade→learning bridge | `analytics`, `context`, `database`, `lifecycle` | `ai_layer/knowledge_ai/learning_context.py`, `backtesting_layer/backtest_engine/backtest_engine.py`, `platform_layer/telegram/owner/learning_commands.py` | **Foundation**, wired into `backtesting/` only (Phase 60.8) |
| `telegram/` | 37 | Product layer: user/subscription/signal-access/feedback services, admin panel, 18 owner-command modules, polling entrypoint | `ai`, `analytics`, `backtesting`, `configuration`, `context`, `core`, `data`, `database`, `decision`, `execution`, `learning`, `monitoring`, `risk`, `signals` | `main.py` (formatter/notifier only), `platform_layer.telegram.polling` (systemd unit) | **Live** (user-facing product layer) + **Foundation** (every `platform_layer/telegram/owner/*.py` module — real, tested, not registered in `command_router.py`) |
| `database/` | 29 | Repository layer — SQL only, one file per table/domain | `configuration`, `core`, `data`, `decision`, `risk`, `signals` (types only) | Every other package that persists something | **Live** |
| `configuration/` | 9 | Runtime Feature Registry (Infrastructure only, Phase 60.9), feature flags, dependency validator, runtime API | `core`, `database` | `platform_layer/telegram/owner/control_commands.py`, `platform_layer/telegram/owner/feature_commands.py` | **Foundation**, Infrastructure-only as of Phase 60.9 |
| `backtesting/` | 10 | Replay engine, `IDataFeed` abstraction, `BacktestEngine` (the full real chain, composed not reimplemented) | `ai`, `analytics`, `context`, `core`, `data`, `database`, `decision`, `learning`, `lifecycle`, `risk`, `signals` | `platform_layer/telegram/owner/backtest_commands.py`/`replay_commands.py` | **Foundation**, fully real and tested, not live-scheduled |
| `monitoring/` | 4 | Pre-Phase-59 performance tracking (`performance.py`) and signal monitoring (`signal_monitor.py`) | `core`, `data`, `database` | Nothing (see Dead Code Audit) | **Superseded** — see TASK 3 |
| `lifecycle/` | 5 | `PaperTrade`/`TradeState` simulation model, paper-trade monitor | `data`, `signals` | `analytics`, `learning`, `backtesting`, `execution` | **Foundation**, real and tested, the one `PaperTrade` producer is `backtesting/` |
| `features/` | 3 | `MarketFeatures` standardization layer (turns already-computed results into one ML-ready record) | `context`, `signals` | `core/pipeline.py` | **Live** (computed every cycle, not yet consumed downstream) |
| `docs/` | 77 `.md` files | Documentation — one file per phase/module/topic, cross-referenced from `docs/ARCHITECTURE.md` | n/a | n/a | Current as of this phase (see TASK 5) |

**Owner** (in the sense of "which phase/module governs this concern," not a person): every package above traces to a specific phase already named in `docs/ARCHITECTURE.md`'s per-phase sections — no package in this inventory was built without a corresponding phase doc.

## TASK 2: Dependency Audit

Built via full-repository `ast` parsing (every `import`/`from...import` statement, package-level). Package-to-package edges:

```
ai          -> analytics, context, core, learning, signals
analytics   -> data, database, execution, learning, lifecycle, signals
backtesting -> ai, analytics, context, core, data, database, decision, learning, lifecycle, risk, signals
configuration -> core, database
context     -> core, data
core        -> ai, context, data, database, decision, features, risk, signals, telegram
data        -> core, database
database    -> configuration, core, data, decision, risk, signals
decision    -> ai, context, signals
execution   -> lifecycle, risk
features    -> context, signals
learning    -> analytics, context, database, lifecycle
lifecycle   -> data, signals
monitoring  -> core, data, database
risk        -> decision, signals
signals     -> context, core, decision (TYPE_CHECKING only), strategies
strategies  -> context, signals
telegram    -> ai, analytics, backtesting, configuration, context, core, data, database,
               decision, execution, learning, monitoring, risk, signals
```

### Findings

| # | Finding | Expected? | Reason | Decision |
|---|---|---|---|---|
| 1 | `core -> telegram` (`core/pipeline.py` imports `platform_layer.telegram.signal_formatter`/`platform_layer.telegram.notifier`) **and** `telegram -> core` (`platform_layer/telegram/owner/emergency_commands.py` imports `core_layer.emergency.*`; `platform_layer/telegram/owner/status_commands.py` imports `core_layer.system_state.system_state`) | **Expected, not a real cycle** | Package-name-level cycle only — no two individual files import each other. `core/pipeline.py`'s own role is orchestrator: it legitimately calls down into `telegram/` for the final delivery stage (documented in its own module docstring since Phase 33). `platform_layer/telegram/owner/*.py` reading `core/emergency`/`core/system_state` is a *different* subpackage reading read-only status for reporting, not the orchestrator being called back into. The full test suite (1519+ tests) already imports every package combination and passes, proving no fatal circular import exists at the interpreter level. | **Leave unchanged** — matches the architecture's own documented shape (`core/pipeline.py`'s docstring), not a violation. |
| 2 | `database -> decision`, `database -> risk`, `database -> signals` | Expected | `database_layer/trade_repository/signal_record.py` imports `SignalCandidate`/`TradeDecision`/`RiskResult` **types only**, to build a `SignalRecord` DTO from already-computed upstream objects (`create_signal_record(candidate, decision, risk_result, ...)`) — the same "adapter reads upstream types to build its own persistence record" posture as `signal_layer/signal_builder/adapter.py`/`context_layer/context_engine/snapshot.py`. No business logic is imported or executed. | **Leave unchanged.** |
| 3 | `signals -> decision` | Expected, and weaker than it looks | The only occurrence is a `TYPE_CHECKING`-only import in `signal_layer/signal_builder/adapter.py` (`from decision.models import TradeDecision`, for a type hint on `from_signal_candidate()`'s `decision:` parameter) — no runtime dependency. Same disclosed-exception pattern used throughout this codebase (e.g. `ai_layer/knowledge_ai/learning_loop/trade_event_bridge.py`). | **Leave unchanged.** |
| 4 | `execution -> lifecycle, risk` but `execution_layer/execution_engine/execution_engine.py` and `execution_layer/execution_monitor/signal_lifecycle.py` (the package's own two named files) have **zero callers anywhere** | Expected (see TASK 1: Foundation status) | Deliberate Trading Safety boundary — CLAUDE.md: "execution/ is intentionally inert... wiring it up is itself a change requiring explicit approval." Confirmed unchanged since Phase 60.8's own audit. | **Leave unchanged**, by design. |
| 5 | No package under `decision/`, `risk/`, `strategies/`, `signals/`, `context/`, `ai/` imports `telegram/`, `database/` (except the disclosed type-only cases above), or `configuration/` | Expected | Matches CLAUDE.md's own stated layer order (`data/ -> context/ -> strategies/ -> signals/ -> ai/ -> decision/ -> risk/ -> telegram/ -> database/`) exactly — no backward or skip-layer import found anywhere in the trading-decision chain. | **No action — this is the healthy state.** |

**No illegal dependency, no fatal circular import, no layer violation found.**

## TASK 3: Dead Code Audit (report only — nothing removed)

Method: any `.py` file under a package directory that (a) is never the target of an `import`/`from...import` statement anywhere else in the repository (source or tests, `ast`-verified) and (b) is not invoked as a script entry point (`python -m package.module`, checked against `deploy/`). Two categories, per the Director's own request to distinguish real dead code from disclosed artifacts:

### Category A — already self-disclosed historical artifacts (not a new finding)

| File | Status |
|---|---|
| `ai/analyzer/ai_analyzer.py` | Phase 55 compatibility shim, explicitly documented in its own docstring as a deliberate re-export with zero current importers by design. |
| `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` | Phase 55 compatibility shim, explicitly documented as "zero importers... at the time of the move... a defensive, zero-cost safety net." |
| `configuration/settings.py` | Phase A13, explicitly documented as "could, in the future, replace ad-hoc `config.Config.*` reads" — an intentionally-unused foundation model. |
| `ai_layer/ai_engine/ai_prompt.py` | Superseded in spirit by `ai/prompts/prompt_manager.py` (Phase 60.5), which explicitly documents `ai_prompt.py` as "left [as is]" rather than merged. |

**Decision for all four: leave unchanged.** Each already carries its own disclosure; re-disclosing here, not deleting.

### Category B — genuine findings, not previously disclosed

| File | Evidence | Assessment |
|---|---|---|
| `core_layer/health_monitor/performance.py` (169 lines) | Zero importers, zero test file. Reads `SignalRepository` directly to compute performance stats. | Very likely superseded by `backtesting_layer/statistics/performance_metrics.py`/`backtesting_layer/statistics/signal_performance.py`/`backtesting_layer/statistics/strategy_report.py` (Phase 60.4 and earlier), which cover the same ground with real test coverage and real `platform_layer/telegram/owner/performance_commands.py` callers. **Recommend**: future consolidation — either delete in a dedicated, separately-approved cleanup phase, or add the same "why kept" disclosure `ai_prompt.py`/`trade_journal.py` already have. Not removed in this phase (report only). |
| `core_layer/health_monitor/signal_monitor.py` (42 lines) | Zero importers, zero test file. Only two frozen dataclasses (`MonitorConfig`, `MonitorResult`), no logic. | Looks like an abandoned foundation stub predating `trade_monitoring_layer/paper_trading/paper_trade_monitor.py` (Phase 59.4), which is the real, tested, wired monitor today. **Recommend**: same as above — future consolidation candidate. |
| `platform_layer/telegram/result_handler.py` (93 lines) | Zero importers, zero test file. Reads `SignalRepository` directly. | Likely superseded by `database_layer/trade_repository/signal_repository.py`'s own result-tracking methods plus `backtesting_layer/statistics/signal_performance.py` (Phase 59.4's own "Signal Result Tracking" task explicitly re-verified and fixed the CANCELLED-result path in the repository, not here). **Recommend**: future consolidation candidate. |
| `data_layer/live_data/session_filter.py` (32 lines) | Zero importers, zero test file. `is_trading_time()`/`get_tashkent_time()`. | **Not a duplicate** of `context_layer/session/session.py` (verified directly, not just trusting the old docstring: `session.py` classifies *which session a candle's own UTC timestamp falls in*, five-way; `session_filter.py` answers *is it trading time right now*, wall-clock Tashkent binary — genuinely different questions). But it has no caller anywhere — nothing in `core/pipeline.py` gates the schedule by `is_trading_time()`, so the function it defines is presently inert. **Recommend**: either wire it into a future scheduling gate, or fold its disclosure-worthy status into a comment matching the other three Category-A files. |

**Nothing was deleted or modified in this audit.** All four Category B findings are flagged for a **future, separately-approved cleanup phase** — consistent with STRICT RULE ("HECH NARSA O'CHIRILMAYDI").

## TASK 4: Duplicate Audit

| Area | Real duplicate? | Assessment | Decision |
|---|---|---|---|
| Owner commands (`platform_layer/telegram/owner/*.py`, 18 files) | No | Each wraps a distinct underlying service (`feature_commands.py`'s `list_features()` reads static `Config`/`FeatureFlags`; `control_commands.py`'s `get_feature_states()` reads live `RuntimeFeatureManager` state — already disclosed in `control_commands.py`'s own docstring as "a different function for a different question, not a same-named competing implementation"). Consistent `ProviderCommandResult` return shape across all 18 is convention, not duplication. | Leave unchanged. |
| Analytics report builders (`analytics/*_report.py`, `*_metrics.py`) | No | Each covers a genuinely distinct domain: signal, strategy, context, validation, gap, dataset, learning, execution, equity-curve, benchmark. No two compute the same statistic from the same input. | Leave unchanged. |
| Learning (`ai_layer/knowledge_ai/learning_loop/models.py`'s `LearningRecord` vs `backtesting_layer/statistics/signal_performance.py`'s `SignalPerformance`) | Partial/disclosed | `learning/README.md` already discloses this as "a disclosed near-duplicate of `backtesting_layer.statistics.signal_performance.SignalPerformance`'s shared fields... a different lifecycle (meant to be persisted append-only, not computed on demand)." | Leave unchanged — already the correct, disclosed shape. |
| Configuration (`feature_flags.py` vs `feature_registry.py` vs `runtime_feature_manager.py`) | No | Three distinct layers, already audited and confirmed non-duplicate in Phase 60.0's own "Duplicate Logic audit" task: static reserved flags (Phase A13) -> structured catalog (Phase 59.6) -> runtime-toggleable state (Phase 59.7), each building on the one below it, none reimplementing it. | Leave unchanged. |
| Formatters (`platform_layer/telegram/signal_formatter.py`, `ai_layer/knowledge_ai/learning_loop/pattern_detector.py`'s `format_pattern_insight()`, every `analytics/*_report.py`'s own `format_*()`) | No | Each formats a distinct domain object for a distinct audience (a Telegram signal message vs a pattern-insight summary vs an owner report) — no shared logic to extract. | Leave unchanged. |
| Prompt systems (`ai_layer/ai_engine/ai_prompt.py` vs `ai/prompts/prompt_manager.py`) | Yes, disclosed, unresolved | Two real, separately-maintained system-prompt string sets. `prompt_manager.py`'s own docstring already discloses this ("distinct from the existing `ai_layer/ai_engine/ai_prompt.py`... left [as is]") rather than merging them. | **Future consolidation candidate** — flagged again here since it's a real duplicate of *concept* (both are "system prompt for AI validation"), even though not of *code*. Not resolved in this phase. |
| Session/time logic (`data_layer/live_data/session_filter.py` vs `context_layer/session/session.py`) | No (verified in TASK 3) | Different questions (wall-clock gate vs per-candle classification). | Leave unchanged; `session_filter.py`'s dead-code status is the real issue (TASK 3), not duplication. |

**No real, unaddressed code duplication found.** The one open item (prompt systems) is a conceptual overlap already disclosed by its own authors, not a fresh discovery, and is left for a future, explicitly-approved consolidation phase.
