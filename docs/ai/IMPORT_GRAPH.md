# IMPORT_GRAPH.md — TASK-AI-000A: Post-Cleanup Internal Import Graph

Status: **POST-IMPLEMENTATION, machine-generated**. Flat edge list of
every internal `ai.X → ai.Y` dependency, produced by AST-parsing every
`.py` under `ai/` (module-level imports only; `if TYPE_CHECKING:`
blocks excluded). Cycle detection over this exact graph reports
**0 cycles**.

## Neutral foundation nodes (no outgoing `ai.` edges)

`ai.event_bus`, `ai.content_types`, `ai.capabilities`, `ai.memory`,
`ai.interfaces`, `ai.persona`, `ai.session`, `ai.profiles`,
`ai.ai_analyzer`, `ai.confidence_model`, `ai.validation` (→providers
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

- **`ai.explanation`** now points at `ai.content_types` (neutral) and
  **no longer at `ai.content`** → the `explanation ↔ content` cycle is
  broken and the Intelligence Dependency Principle (Content downstream
  of Explanation) holds: `ai.content → ai.explanation` exists, the
  reverse does not.
- **`ai.providers`/`ai.audit`/`ai.runtime`** all point at
  `ai.event_bus` (neutral) → no subpackage imports *up* into
  `ai.runtime`; runtime orchestrates providers/router/audit
  one-directionally. The three runtime-cluster cycles are broken.
- No edge from any `ai/` module targets `decision`/`risk`/`execution`/
  `database`/`telegram`/`strategies` (Constitution Article 3 — checked
  separately, still zero).
