# ai/reasoning/

## Purpose
A structured reasoning foundation for the AI layer — not an LLM, not
an inference engine, not a decision-maker. Turns already-known
Knowledge and already-recalled Memory into a single, deterministic
`ReasoningResult` a caller assembles by hand; this package never
computes a probability, a correlation, or any derived number itself.
Sits between Memory and Reasoning's own downstream consumer,
Conversation, in the Official Intelligence Pipeline
(`docs/roadmap/AI_EVOLUTION.md`):

```
Knowledge → Memory → Reasoning → Conversation → Explanation → Content → Media → Broadcast
```

## Structure
```
ai/reasoning/
  models.py              ReasoningMode/ReasoningType/ReasoningPriority/
                          ReasoningStep/ReasoningResult -- primitive/enum
                          fields only
  reasoning_registry.py  ReasoningTypeDescriptor catalog,
                          build_reasoning_type_registry()/describe()
  reasoning_runtime.py    ReasoningRuntime -- reason/explain/summarize/
                          evaluate/compare/chain/history, all
                          deterministic reads/writes over
                          caller-assembled ReasoningResult objects
  reasoning_adapters.py   step_from_knowledge_entry()/
                          step_from_memory_entry() (type-only,
                          Knowledge/Memory are upstream) and
                          reasoning_result_to_explanation_fields()
                          (returns a plain dict, never imports
                          ai/explanation/ -- Explanation is downstream)
```

## Responsibilities
- `models.py` — the record shape. `ReasoningStep` (`label`, `value`,
  `source`) and `ReasoningResult` (`key`, `mode`, `reasoning_type`,
  `conclusion`, `steps`, `confidence`, `priority`) are 100%
  primitive/enum — no trading-layer object, no `Any`-typed field.
- `reasoning_registry.py` — a static, five-entry catalog describing
  each `ReasoningType` (label, description). Metadata only.
- `reasoning_runtime.py` — `ReasoningRuntime`: stores and reads
  `ReasoningResult` objects the caller already assembled. Zero
  `AIService`/provider call, zero network call.
- `reasoning_adapters.py` — the only place this package touches
  another package's types, and only their already-public dataclass
  fields (`KnowledgeEntry`/`MemoryEntry`), never a Manager/Runtime
  class's internal state.

## Input
A caller-assembled `ReasoningResult` (via `reason()`), or a
`KnowledgeEntry`/`MemoryEntry` (via the two adapter functions).
`ai/reasoning/` never reads live market data, a database, or a trading
layer object directly.

## Output
`Optional[str]`/`Optional[float]` (`explain`/`summarize`/`evaluate`/
`compare`), `Sequence[ReasoningResult]` (`chain`/`history`), a plain
`dict` of primitives (`reasoning_result_to_explanation_fields`).

## Dependencies
`knowledge/` and `ai/memory/` (type-only — `KnowledgeEntry`/
`MemoryEntry`, both upstream in the Intelligence Pipeline), `core/`.
Per the Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`), `ai/reasoning/` never imports
`ai/explanation/`, `ai/content/`, `ai/conversation/`, `broadcast/`,
`media/`, or `translation/` — all downstream. It never imports
`decision/`, `risk/`, `execution/`, `strategies/`, `database/`, or
`telegram/` either (Constitution Article 3) — verified by grep/AST
sweep at the close of every AI-touching phase.

## Future Roadmap
Not wired into `core/pipeline.py`, `ai/conversation/`, or
`ai/explanation/` this phase — foundation only.
`reasoning_result_to_explanation_fields()` is built and tested
standalone; a future caller (not this package) would import both
`ai/reasoning/` and `ai/explanation/` and bridge them.

## Related
- `docs/ai/AI_REASONING.md` — the full, current documentation of this
  package.
- `docs/PHASE63_4_AUDIT.md`, `docs/PHASE63_4_FREEZE.md` — the phase
  that built this package.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
