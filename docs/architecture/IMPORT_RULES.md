# GoldBot — Import Rules

Governed by `docs/constitution/CONSTITUTION.md` Article 3. This
document makes Article 3 checkable line-by-line: every import
pattern in this codebase is either explicitly allowed or explicitly
forbidden below. There is no third category.

## Allowed imports

| From | To | Example |
|---|---|---|
| `telegram/handlers.py` | `telegram/*_service.py` | `telegram/handlers.py` → `telegram/signal_service.py` |
| `telegram/*_service.py` | `database/*_repository.py` | `telegram/user_service.py` → `database/user_repository.py` |
| `telegram/owner/*.py` | corresponding service/repository | `telegram/owner/runtime_commands.py` → `ai/runtime/ai_service.py` |
| `ai/*` | `ai/*` | `ai/runtime/ai_service.py` → `ai/router/router.py` |
| `ai/*` | `core/*` | any `ai/` module → `core/secrets.py` |
| `ai/ai_analyzer.py`, `ai/ai_prompt.py`, `ai/confidence_model.py`, `ai/journal/trade_journal.py`, `ai/explanation/explanation_engine.py`, `ai/context/context_snapshot.py`, `ai/context/context_builder.py` | `signals/*` or `context/*` — **type definitions only** (`SignalCandidate`, `SignalSchema`, `MarketContext`) | `ai/context/context_snapshot.py` → `signals.schema.SignalCandidate` (type import, no decision/risk call) |
| `decision/models.py`, `decision/decision_engine.py` | `ai.ai_analyzer` — **`AIAnalysisResult` type only** | `decision/models.py` → `from ai.ai_analyzer import AIAnalysisResult`, used as a `TradeDecision`/`DecisionResult` field (`decision_engine.py`'s own import is `TYPE_CHECKING`-guarded); `decision/` never imports `ai/router/`, `ai/providers/`, or `ai/runtime/`, and never calls `AIService.ask()` itself — `core/pipeline.py` is the only caller of `AIAnalyzer.analyze()` |
| `core/pipeline.py` | `ai.ai_analyzer` (`AIAnalyzer`, `AIAnalysisResult`) | the pipeline orchestrator is the one place that actually invokes the AI analyzer, per `CLAUDE.md`'s `signals/ -> ai/ -> decision/` order |
| `decision/`, `risk/`, `signals/`, `strategies/`, `context/` | the layer immediately before it in `CLAUDE.md`'s pipeline order | `risk/risk_manager.py` → `decision/decision_engine.py` output types |
| any module | `core/*` | `core/` is the shared foundation every layer may depend on |

## Forbidden imports

| From | To | Why |
|---|---|---|
| `ai/*` (any file, no exceptions) | `decision/*` | Constitution Article 1/3 — AI never participates in the trade decision |
| `ai/*` (any file, no exceptions) | `risk/*` | AI must never call or influence Risk Manager |
| `ai/*` (any file, no exceptions) | `execution/*` | AI must never trigger an execution action |
| `ai/*` | `signals/*` / `context/*` for anything beyond the seven named type-only sites above | a new such import requires the same audit discipline as any new cross-layer import (Article 7) — it is not automatically exempt |
| `decision/*` | `ai/router/*`, `ai/providers/*`, `ai/runtime/*`, or any call into `AIService.ask()` | Decision Engine may accept an `AIAnalysisResult` *value* (see Allowed table) but never calls into the AI layer's own machinery — that would make AI participate in the decision, forbidden by Article 1 |
| `risk/*` | `ai/*` | Risk Manager operates entirely on the Decision Engine's own output; it imports nothing from `ai/` today and has no sanctioned reason to |
| `strategies/*` | `telegram/*` | upward dependency, forbidden by Article 2 |
| `signals/*` | `telegram/*` | upward dependency, forbidden by Article 2 |
| `telegram/handlers.py` | `database/*` (directly) | must go through a `telegram/*_service.py` — Constitution Article 4 |
| `telegram/handlers.py` | `core.pipeline` (directly) | must go through a service — already stated in `telegram/handlers.py`'s own module docstring |
| `database/*_repository.py` | anything above it (`telegram/`, `ai/`, `decision/`) | repositories own SQL only, never a caller's business logic |
| any module | `core/*` importing back up | `core/` depends on nothing else in the diagram — a `core/` → any-other-layer import is always forbidden |

## Mechanical verification

The Forbidden table's `ai/` rows are checked, not just documented —
a grep sweep at the close of every AI-touching phase:

```
grep -rn "^from decision\|^from risk\|^from execution\|^import decision\|^import risk\|^import execution" ai/
```

must return zero results. This has held since Phase 61.0's own
isolation audit and was re-verified at the close of Phase 61.7.

## Related documents

- `docs/constitution/CONSTITUTION.md` — Article 3, the rule this
  document operationalizes.
- `docs/architecture/MODULE_DEPENDENCIES.md` — the real dependency
  map these rules are checked against.
- `docs/architecture/EXTENSION_GUIDE.md` — how to add a new import
  without violating this table.
