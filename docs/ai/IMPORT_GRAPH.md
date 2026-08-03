# IMPORT_GRAPH.md — TASK-AI-000A: Post-Cleanup Internal Import Graph

Status: **POST-IMPLEMENTATION, machine-generated**. Flat edge list of
every internal `ai.X → ai.Y` dependency, produced by AST-parsing every
`.py` under `ai/` (module-level imports only; `if TYPE_CHECKING:`
blocks excluded). Cycle detection over this exact graph reports
**0 cycles**.

## Neutral foundation nodes (no outgoing `ai.` edges)

`ai_layer.ai_service.event_bus`, `ai_layer.ai_service.content.content_types`, `ai_layer.ai_engine.capabilities`, `ai_layer.knowledge_ai.memory_manager`,
`ai_layer.ai_service.interfaces`, `ai_layer.personal_ai.persona_manager`, `ai_layer.ai_service.session`, `ai_layer.personal_ai.user_profile`,
`ai_layer.ai_engine.ai_analyzer`, `ai_layer.confidence_ai.confidence_model`, `ai_layer.confidence_ai` (→providers
only), etc. These are imported by others but import nothing else in
`ai/` — the base of the DAG.

## Full edge list (source → target)

```
ai.access            -> ai.capabilities
ai.audit             -> ai.capabilities
ai.audit             -> ai.event_bus
ai.cache             -> ai.capabilities
ai.chart_intelligence-> ai.access, ai.content, ai.content_types, ai.explanation, ai.trading_analyst
ai.coaching          -> ai.access, ai.learning, ai.trade_journal
ai.content           -> ai.access, ai.capabilities, ai.content_types, ai.context, ai.conversation, ai.explanation, ai.runtime
ai.context           -> ai.cache, ai.interfaces, ai.journal, ai.learning_context, ai.profiles
ai.conversation      -> ai.access, ai.capabilities, ai.context, ai.memory, ai.reasoning, ai.runtime, ai.session
ai.explanation       -> ai.access, ai.capabilities, ai.content_types, ai.context, ai.persona, ai.runtime
ai.intelligence_runtime -> ai.content, ai.content_types, ai.conversation, ai.explanation, ai.memory, ai.reasoning
ai.learning          -> ai.access, ai.trade_journal
ai.performance       -> ai.access, ai.trade_journal
ai.portfolio         -> ai.access, ai.performance, ai.strategy
ai.prompts           -> ai.interfaces
ai.providers         -> ai.capabilities, ai.event_bus
ai.reasoning         -> ai.memory
ai.research          -> ai.access, ai.performance, ai.portfolio, ai.strategy
ai.router            -> ai.audit, ai.capabilities, ai.providers
ai.runtime           -> ai.access, ai.audit, ai.cache, ai.capabilities, ai.context, ai.event_bus, ai.prompts, ai.providers, ai.router, ai.validation
ai.strategy          -> ai.access, ai.performance, ai.trade_journal
ai.tools             -> ai.interfaces, ai.learning_context
ai.trade_journal     -> ai.access, ai.chart_intelligence, ai.journal, ai.trading_analyst
ai.trading_analyst   -> ai.access, ai.content, ai.content_types, ai.explanation, ai.intelligence_runtime
ai.validation        -> ai.providers
(top-level shims, unchanged: ai.analyzer -> ai.ai_analyzer; ai.ai_prompt -> ai.confidence_model)
```

## Key verification points

- **`ai_layer.explanation_ai`** now points at `ai_layer.ai_service.content.content_types` (neutral) and
  **no longer at `ai_layer.ai_service.content`** → the `explanation ↔ content` cycle is
  broken and the Intelligence Dependency Principle (Content downstream
  of Explanation) holds: `ai_layer.ai_service.content → ai.explanation` exists, the
  reverse does not.
- **`ai_layer.ai_engine.providers`/`ai_layer.ai_service.audit`/`ai_layer.ai_engine.runtime`** all point at
  `ai_layer.ai_service.event_bus` (neutral) → no subpackage imports *up* into
  `ai_layer.ai_engine.runtime`; runtime orchestrates providers/router/audit
  one-directionally. The three runtime-cluster cycles are broken.
- No edge from any `ai/` module targets `decision`/`risk`/`execution`/
  `database`/`telegram`/`strategies` (Constitution Article 3 — checked
  separately, still zero).
