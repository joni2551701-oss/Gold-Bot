# UPDATED_DEPENDENCY_GRAPH.md — TASK-AI-000A: Post-Cleanup Dependency Graph

Status: **POST-IMPLEMENTATION**. This supersedes the "before" state
captured in `AI_DEPENDENCY_GRAPH.md` (TASK-AI-000). Result:
**0 circular dependencies** (was 4), verified by an AST-based
white/gray/black cycle detector over every `.py` under `ai/`, with
`if TYPE_CHECKING:` blocks excluded (39 subpackage/module nodes,
88 edges).

## Before → After

| Cycle (before) | Status now | How removed |
|---|---|---|
| `ai_layer.ai_engine.runtime ↔ ai.providers` | **gone** | `event_bus` extracted to neutral `ai_layer.ai_service.event_bus` |
| `ai_layer.ai_service.audit ↔ ai.runtime` | **gone** | same (event_bus extraction) |
| `ai_layer.ai_service.audit → ai.runtime → ai.router → ai.audit` | **gone** | same (event_bus extraction) |
| `ai_layer.explanation_ai ↔ ai.content` | **gone** | adapter moved to `ai/content/`; `ContentType` extracted to neutral `ai_layer.ai_service.content.content_types` |

## The two new neutral foundation modules

Both sit at the bottom of the graph — nothing in `ai/` is imported by
them, so every consumer depends on them strictly downward:

- **`ai_layer.ai_service.event_bus`** (`EventBus`, `EventType`, `RuntimeEvent`) —
  depends only on `core_layer.logger.logger` + stdlib. Consumers: `ai_layer.ai_engine.runtime`,
  `ai_layer.ai_engine.providers`, `ai_layer.ai_service.audit`, `platform_layer.telegram.owner`.
- **`ai_layer.ai_service.content.content_types`** (`ContentType` enum) — depends only on stdlib
  `enum`. Consumers: `ai_layer.explanation_ai`, `ai_layer.ai_service.content`,
  `ai_layer.ai_engine.trading_analyst`, `ai_layer.vision_ai`, `ai_layer.ai_engine.intelligence_runtime`,
  `broadcast`.

## Corrected key edges (formerly bidirectional)

Runtime/provider/router/audit cluster — now one-directional:
```
ai.event_bus                (neutral foundation, no ai/ deps)
   ▲        ▲        ▲
   │        │        │            (all import DOWN into event_bus)
ai.providers  ai.audit  ai.runtime ── ai.router ── ai.audit
   ▲                        │  (runtime orchestrates providers/router/audit,
   └────────────────────────┘   none of them import back up into runtime)
```

Content/explanation cluster — Intelligence Dependency Principle restored:
```
ai.content_types           (neutral vocabulary, no ai/ deps)
   ▲            ▲
   │            │
ai.explanation  ────────►  ai.content   (content is DOWNSTREAM of
   (upstream)                            explanation; explanation no longer
                                         imports anything from content)
```

## Confirmed unchanged (still holds after cleanup)

- The `ai/` → `decision/`/`risk/`/`execution/`/`database/`/`telegram/`/
  `strategies/` absolute no-import rule (Constitution Article 3) — still
  zero real import statements; the cleanup touched none of these edges.
- The `ai_layer.ai_engine.context ↔ ai.cache` relationship remains one-directional at
  runtime (`ai_layer.ai_engine.cache`'s reference to `ai_layer.ai_engine.context` is `TYPE_CHECKING`-only,
  never executed) — untouched by this task, and the cycle detector
  (which excludes TYPE_CHECKING) confirms it is not a cycle.
- The 66.x-family subpackages (`coaching`…`research`) remain a clean
  forward-only DAG.

See `IMPORT_GRAPH.md` for the flat edge list.
