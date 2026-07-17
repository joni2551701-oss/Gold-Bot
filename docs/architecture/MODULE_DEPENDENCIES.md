# GoldBot — Module Dependencies

Governed by `docs/constitution/CONSTITUTION.md` Article 2 (Dependency
Law) and Article 3 (Import Rules). This document is the living proof
those Articles hold today — it lists the real, current per-module
dependency structure, not an aspirational one.

## Dependency diagram

```
        Telegram
           |
     Command Layer          (telegram/command_router.py, commands.py, permissions.py)
           |
     Service Layer           (telegram/*_service.py, telegram/owner/*.py)
           |
      AI / Product Layer      (ai/session, ai/conversation, ai/prompts)
           |
        AI Core               (ai/runtime, ai/router, ai/providers, ai/analyzer, ...)
           |
      Data Context            (context/, signals/ [type-only], data/)
           |
        Database               (database/*_repository.py)
```

`core/` sits beneath everything and is depended on by every layer
above; it depends on nothing in this diagram.

## Real per-module dependencies

### Trading pipeline (unchanged this phase — documentation only)

| Module | Depends on |
|---|---|
| `data/` | external market data sources, `core/` |
| `context/context_orchestrator.py` | `data/`, `core/` |
| `strategies/strategy_manager.py` | `context/`, `data/`, `core/` |
| `signals/signal_engine.py` | `strategies/`, `context/`, `core/` |
| `decision/decision_engine.py`, `decision/models.py` | `signals/`, `context/`, `core/`, plus `ai.ai_analyzer.AIAnalysisResult` (**type only** — the one sanctioned `decision/ → ai/` import, see Constitution Article 1/3) |
| `risk/risk_manager.py` | `decision/`, `core/` |
| `execution/execution_engine.py` | `risk/`, `core/` (inert — no live order calls) |
| `lifecycle/paper_trade_monitor.py` | `decision/`, `risk/`, `core/` |
| `core/pipeline.py` | orchestrates all of the above, top to bottom |

### Telegram layer

| Module | Depends on |
|---|---|
| `telegram/handlers.py` | `telegram/*_service.py` only — never `database.*` or `core.pipeline` directly |
| `telegram/command_router.py` | `telegram/commands.py`, `telegram/permissions.py`, `telegram/handlers.py` |
| `telegram/*_service.py` (admin/feedback/notification/signal/subscription/user) | `database/*_repository.py` |
| `telegram/owner/*.py` (19 files: ai/backtest/control/dashboard/dataset/emergency/execution/feature/fundamental/learning/performance/provider/replay/report/runtime/security/status/system/validation) | corresponding service/repository layer for their domain; `runtime_commands.py` additionally depends on `ai/runtime/` (`AIService`, `RuntimeManager`, `self_check`) |

### Database layer

| Module | Depends on |
|---|---|
| `database/*_repository.py` (19 repositories) | `database/*_models.py`, `database/database.py` — SQL only, no business logic |

### AI layer — 19 real subpackages under `ai/`

| Subpackage | Real responsibility | Depends on |
|---|---|---|
| `ai/access/` | capability/permission gating for AI requests | `core/` |
| `ai/analyzer/` | Phase 55 compat entry point → re-exports canonical `ai/ai_analyzer.py` | `ai/ai_analyzer.py` |
| `ai/audit/` | provider stats / call auditing (`provider_stats.py`) | `core/` |
| `ai/cache/` | response caching | `core/` |
| `ai/capabilities/` | capability enum + permission matrix | `core/` |
| `ai/content/` | content assembly helpers | `core/` |
| `ai/context/` | `context_snapshot.py`/`context_builder.py` — reads `signals/`/`context/` types only | `signals/` (type-only), `context/` (type-only), `core/` |
| `ai/conversation/` | multi-turn conversation state | `ai/session/`, `core/` |
| `ai/explanation/` | `explanation_engine.py` — reads `signals/` types only | `signals/` (type-only), `core/` |
| `ai/journal/` | `trade_journal.py` (canonical) — reads `signals/` types only | `signals/` (type-only), `core/` |
| `ai/memory/` | long-term AI memory storage | `core/` |
| `ai/profiles/` | `RuntimeProfile` definitions | `core/` |
| `ai/prompts/` | prompt templates | `core/` |
| `ai/providers/` | `BaseAIProvider`, vendor implementations, `circuit_breaker.py` | `core/` only — no vendor name leaks above this package |
| `ai/router/` | `AIRouter`, `routing_rules.py` | `ai/providers/`, `ai/capabilities/`, `core/` |
| `ai/runtime/` | `AIService`, `RuntimeManager`, `EventBus`, `self_check.py` — the orchestration point | `ai/router/`, `ai/providers/`, `ai/cache/`, `ai/audit/`, `ai/profiles/`, `core/` |
| `ai/session/` | session/user context for AI product surfaces | `core/` |
| `ai/tools/` | AI-callable tool definitions (advisory only) | `core/` |
| `ai/validation/` | response validation, `safety.py` | `core/` |

Two top-level compat shims, documented so they are not mistaken for
new modules: `ai/ai_analyzer.py` and `ai/trade_journal.py` are the
canonical files; `ai/analyzer/ai_analyzer.py` and
`ai/journal/trade_journal.py` are the Phase 55-restructure entry
points that re-export them.

**Note on the brief's assumption**: `knowledge/` is a separate
**top-level** package (`knowledge/`, a sibling of `ai/`, not
`ai/knowledge/`), and there is no dedicated `ai/security/` folder —
AI-relevant safety logic lives in `ai/validation/safety.py`, and
Telegram-side security lives in `telegram/owner/security.py`. This
document records the real structure rather than the assumed one, per
Constitution Article 7 (Reuse Principle — audit before asserting).

## Related documents

- `docs/architecture/ARCHITECTURE_MASTER.md` — the layer diagram and
  per-layer CAN/CANNOT this document's dependencies serve.
- `docs/architecture/IMPORT_RULES.md` — the allowed/forbidden import
  table this document's dependencies are checked against.
