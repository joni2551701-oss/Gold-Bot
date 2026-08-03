# AI_DEPENDENCY_GRAPH.md — TASK-AI-000 Phase 2: Dependency Audit

Status: **AUDIT ONLY**. No code changed. Method: `grep -rn` over
`ai/**/*.py` for every `import`/`from` statement, cross-checked
against direct file reads. Comment/docstring mentions of a package
name were explicitly excluded from edges — only real, executing
import statements count. `TYPE_CHECKING`-only imports are called out
separately since they never execute at runtime.

## Why not the Director's example chain

The Director's task description sketched an idealized chain:

```
AI Manager
  ↓
Registry
  ↓
Factory
  ↓
Session
  ↓
Context
  ↓
Services
```

The actual codebase does not have a single `AIManager`, a single
unified `Registry`, or a `Factory` class at all (see
`AI_FOUNDATION_READINESS.md`) — so this chain does not describe `ai/`
as it exists today. What follows is the graph as it actually is, not
as idealized.

---

## 1. Internal edge list (`ai.X → ai.Y`, subpackage-level)

| Source | Depends on | Evidence |
|---|---|---|
| ai.access | ai.capabilities | ai/access/tool_permissions.py |
| ai.audit | ai.capabilities, ai.runtime | ai/audit/*.py |
| ai.cache | ai.capabilities, ai.context* | ai/cache/cache_policy.py:44, :47 (*TYPE_CHECKING only) |
| ai.chart_intelligence | ai.access, ai.content, ai.explanation, ai.trading_analyst | ai/chart_intelligence/*.py |
| ai.coaching | ai.access, ai.learning, ai.trade_journal | ai/coaching/*.py |
| ai.content | ai.access, ai.capabilities, ai.context, ai.conversation, ai.explanation, ai.runtime | ai/content/*.py |
| ai.context | ai.cache, ai.interfaces (top-level), ai.journal, ai.learning_context (top-level), ai.profiles | ai/context/*.py |
| ai.conversation | ai.access, ai.capabilities, ai.context, ai.memory, ai.reasoning, ai.runtime, ai.session | ai/conversation/*.py |
| ai.explanation | ai.access, ai.capabilities, ai.content, ai.context, ai.persona, ai.runtime | ai/explanation/*.py |
| ai.learning | ai.access, ai.trade_journal | ai/learning/*.py |
| ai.performance | ai.access, ai.trade_journal | ai/performance/*.py |
| ai.portfolio | ai.access, ai.performance, ai.strategy | ai/portfolio/*.py |
| ai.prompts | ai.interfaces (top-level) | ai/prompts/prompt_manager.py |
| ai.providers | ai.capabilities, ai.runtime | ai/providers/circuit_breaker.py:51 |
| ai.reasoning | ai.memory | ai/reasoning/reasoning_adapters.py |
| ai.research | ai.access, ai.performance, ai.portfolio, ai.strategy | ai/research/*.py |
| ai.router | ai.audit, ai.capabilities, ai.providers | ai/router/router.py |
| ai.runtime | ai.access, ai.audit, ai.cache, ai.capabilities, ai.context, ai.prompts, ai.providers, ai.router, ai.validation | ai/runtime/ai_service.py:158-179 |
| ai.strategy | ai.access, ai.performance, ai.trade_journal | ai/strategy/*.py |
| ai.tools | ai.interfaces (top-level), ai.learning_context (top-level) | ai/tools/*.py |
| ai.trade_journal | ai.access, ai.chart_intelligence, ai.trading_analyst | ai/trade_journal/*.py |
| ai.trading_analyst | ai.access, ai.content, ai.explanation, ai.intelligence_runtime (top-level) | ai/trading_analyst/*.py |
| ai.validation | ai.providers | ai/validation/response_validator.py |
| ai.analyzer (top-level) | ai.ai_analyzer (top-level shim) | ai/analyzer/ai_analyzer.py:16 |
| ai.ai_prompt (top-level) | ai.confidence_model (top-level) | ai/ai_prompt.py:4 |
| ai.trade_journal.py (shim) | ai.journal | ai/trade_journal.py:9-15 |
| ai.intelligence_runtime (top-level) | ai.content, ai.conversation, ai.explanation, ai.memory, ai.reasoning | ai/intelligence_runtime.py |

## 2. External edges (`ai.X → non-ai top-level package`)

| Source | Depends on | Evidence |
|---|---|---|
| Most subpackages | `dataclasses` (stdlib) | ubiquitous |
| ai.ai_analyzer.py | context, core, signals | ai/ai_analyzer.py:1-4 |
| ai.ai_prompt.py, ai.confidence_model.py | context, signals | ai/ai_prompt.py:2-3, ai/confidence_model.py:3-4 |
| ai.capabilities, ai.prompts, ai.providers, ai.runtime, ai.session | core (`core_layer.logger.logger`) | e.g. ai/providers/openai_provider.py:30 |
| ai.chart_intelligence | broadcast, configuration, media | ai/chart_intelligence/content_adapter.py:34,37 |
| ai.coaching, ai.learning, ai.portfolio, ai.research, ai.strategy, ai.trade_journal | configuration | e.g. ai/coaching/access.py:10 |
| ai.context | context (top-level), signals | ai/context/context_adapter.py:35, ai/context/context_snapshot.py:37 |
| ai.conversation, ai.explanation, ai.reasoning, ai.intelligence_runtime.py | knowledge | ai/conversation/conversation_adapters.py:27 |
| ai.explanation | signals | ai/explanation/explanation_engine.py:35 |
| ai.intelligence_runtime.py, ai.trading_analyst | broadcast, media | ai/intelligence_runtime.py:53,56 |
| ai.journal | signals | ai/journal/trade_journal.py:4 |
| ai.learning_context.py (top-level) | analytics, learning (top-level) | ai/learning_context.py:66-67 |
| ai.performance, ai.tools | analytics | ai/performance/analytics_adapter.py:26 |

**Confirmed absent**: no file under `ai/` imports `decision`, `risk`,
`execution`, `database`, `telegram`, or `strategies` — anchored greps
returned zero real import statements for all six. Every unanchored
match on these strings inside `ai/` is prose in a docstring/comment
restating the forbidden-import rule itself (e.g. `ai/interfaces.py:74-76`).
This confirms Article 3 / Constitution's AI-never-imports-Trading-Core
rule holds with no exceptions anywhere in `ai/`.

---

## 3. Cycle detection

Method: directed graph built from Section 1's edges, DFS-based cycle
detection (white/gray/black coloring), then every reported edge
manually verified by reading the source line to confirm it's a real,
unguarded, module-level import.

**Result: 4 real circular dependencies, 1 false positive.**

### Cycle 1 (real) — `ai.runtime ↔ ai.providers`
- `ai/runtime/ai_service.py:167` — `from ai.providers.circuit_breaker import ProviderCircuitBreaker`
- `ai/providers/circuit_breaker.py:51` — `from ai.runtime.event_bus import EventBus, EventType, RuntimeEvent`

Both unguarded, module-level. No `ImportError` occurs in practice only
because neither file imports the other's *importer* module directly —
but the subpackage-level dependency is genuinely bidirectional.

### Cycle 2 (real) — `ai.audit ↔ ai.runtime`
- `ai/audit/provider_stats.py:61` — `from ai.runtime.event_bus import ...`
- `ai/runtime/ai_service.py:159` — `from ai.audit.provider_stats import compute_daily_usage, evaluate_cost_protection`

### Cycle 3 (real, 3-node) — `ai.audit → ai.runtime → ai.router → ai.audit`
- `ai/audit/provider_stats.py:61` — audit → runtime (same edge as Cycle 2)
- `ai/runtime/ai_service.py:178` — `from ai.router.router import AIRouter`
- `ai/router/router.py:34` — `from ai.audit.provider_stats import ProviderStats, compute_provider_stats`

### Cycle 4 (real) — `ai.explanation ↔ ai.content`
- `ai/explanation/explanation_output.py:29` — `from ai.content.content_types import ContentType`
- `ai/explanation/explanation_content_adapter.py:15` — `from ai.content.broadcast_output import BroadcastReadyContent`
- `ai/content/content_adapters.py:17` — `from ai.explanation.explanation_output import ExplanationOutput`

`ai/content/content_adapters.py:6-9`'s own docstring asserts an
"Intelligence Dependency Principle" that `ai/explanation/` sits
**upstream** of `ai/content/` — content should depend on explanation,
never the reverse. `explanation_output.py:29` and
`explanation_content_adapter.py:15` both import from `ai/content/`,
directly contradicting that stated one-directional policy.

### Not a real cycle — `ai.context ↔ ai.cache`
- `ai/context/context_builder.py:34` — `from ai.cache.cache_policy import compute_context_hash` (real, unguarded, context → cache)
- `ai/cache/cache_policy.py:47` — `from ai.context.context_snapshot import AIContext` — inside `if TYPE_CHECKING:` (lines 46-47), never executes at runtime.

Confirmed no other file under `ai/cache/` references `ai.context`
outside comments — this relationship is one-directional at runtime.

---

## 4. Cluster summary

Grouping the 4 real cycles by the runtime relationships they sit in:

- **Runtime/Provider/Router/Audit cluster**: `ai.runtime`, `ai.providers`,
  `ai.router`, `ai.audit` form a tightly bidirectionally-coupled group
  (Cycles 1-3). This is the AI Service orchestration core.
- **Content/Explanation cluster**: `ai.content` and `ai.explanation`
  are bidirectionally coupled (Cycle 4), despite a documented
  one-directional design intent.
- **Everything else is acyclic**: the 66.x-family subpackages
  (`coaching`, `learning`, `performance`, `portfolio`, `research`,
  `strategy`, `trade_journal`, `trading_analyst`, `chart_intelligence`)
  form a forward-only DAG rooted at `ai.access` + earlier
  foundational subpackages (`ai.memory`, `ai.reasoning`, `ai.context`,
  `ai.persona`, `ai.session`) — no cycles found among any of them.

See `AI_ARCHITECTURE_REVIEW.md` for the Clean Architecture / Dependency
Direction assessment of these cycles, and
`AI_REFACTOR_RECOMMENDATIONS.md` for break-the-cycle recommendations.
