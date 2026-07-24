# GoldBot — AI Reasoning

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`, established at Phase 63.3's close).
`ai/reasoning/` (Phase 63.4), real code, foundation-only — nothing in
`core/pipeline.py`, `ai/conversation/`, or `ai/explanation/` calls it
yet.

## What's real

```
ai/reasoning/models.py              ReasoningMode/ReasoningType/ReasoningPriority/
                                     ReasoningStep/ReasoningResult
ai/reasoning/reasoning_registry.py  ReasoningTypeDescriptor catalog
ai/reasoning/reasoning_runtime.py    ReasoningRuntime -- deterministic
                                     store/read over ReasoningResult
ai/reasoning/reasoning_adapters.py   Knowledge/Memory (upstream, type-only)
                                     and Explanation (downstream, dict-only)
                                     integration points
```

## Position in the Official Intelligence Pipeline

```
Knowledge → Memory → Reasoning → Conversation → Explanation
   → Content → Media → Broadcast
```

Reasoning is the first Phase 63.x sub-phase that turns "AI Information"
(Knowledge, Memory — what the AI knows/remembers) into "AI Intelligence"
(what the AI concludes from what it knows). It is still bound by
Constitution Article 1: `ReasoningRuntime` never computes a probability,
correlation, or any derived number itself — the caller fully assembles
a `ReasoningResult` before `reason()` ever sees it. This is
deliberately not an inference engine; it is a structured place to
*hold* a conclusion a caller already reached, so `explain()`/
`summarize()`/`compare()`/`chain()`/`history()` can read it back
consistently.

## Model

`ReasoningStep` (`label: str`, `value: str`, `source: Optional[str] =
None`) and `ReasoningResult` (`key: str`, `mode: ReasoningMode`,
`reasoning_type: ReasoningType`, `conclusion: str`, `steps:
Sequence[ReasoningStep]`, `confidence: float` [0.0-1.0], `priority:
ReasoningPriority`) are both 100% primitive/enum fields — no
`DecisionResult`, `RiskResult`, `Trade`, `Position`, `Order`, `MT5`
object, or `Execution` type anywhere, and no `Any`-typed field either
(unlike `ai/memory/models.py`'s deliberately permissive
`MemoryEntry.value`).

## Runtime

```
ReasoningRuntime
  .reason(result: ReasoningResult) -> ReasoningResult
  .explain(key: str) -> Optional[str]
  .summarize(key: str) -> Optional[str]
  .evaluate(key: str) -> Optional[float]
  .compare(key_a: str, key_b: str) -> Optional[float]
  .chain(keys: Sequence[str]) -> Sequence[ReasoningResult]
  .history() -> Sequence[ReasoningResult]
```

`reason()` stores; every other method is a pure, deterministic read
(a string join for `summarize()`, a subtraction for `compare()`).
Zero `AIService`/provider call, zero network call.

## Knowledge/Memory integration (TASK 4/5 — real, type-only)

`reasoning_adapters.py`'s `step_from_knowledge_entry(entry)` and
`step_from_memory_entry(entry)` read a `KnowledgeEntry`'s/`MemoryEntry`'s
own already-public fields (`title`/`summary`/`key`,
`scope`/`value`/`key`) into a `ReasoningStep` — never `KnowledgeManager`'s
or `MemoryRuntime`'s internal state. Both Knowledge and Memory sit
upstream of Reasoning in the pipeline, so this is a sanctioned forward
reference, the same shape Constitution Article 3 already allows for
`decision/` accepting `AIAnalysisResult` from `ai/`.

## Explanation integration (TASK 6 — interface only, no import)

`reasoning_adapters.py`'s `reasoning_result_to_explanation_fields(result)`
returns a plain `dict` (`{"technical_reason": str, "confidence":
float}`, confidence rescaled from this package's 0.0-1.0 convention to
`ExplanationInput`'s own 0-100 scale) — `ai/explanation/` is never
imported anywhere in `ai/reasoning/`, because Explanation sits
**downstream** of Reasoning in the pipeline. A future caller (not this
package) would import both `ai/reasoning/` and `ai/explanation/` and
merge this dict into its own `ExplanationInput` construction.
`ai/explanation/explanation_builder.py` is not modified this phase.

## What it is not

- Not an LLM, not a GPT wrapper, not an inference engine — every
  method is deterministic storage or simple arithmetic over
  caller-supplied data.
- Not a trading decision — `ai/reasoning/` is never imported by
  `core/`, `decision/`, `risk/`, `execution/`, or `strategies/`, and
  never imports any of them either (Constitution Article 3).
- Not wired into `ai/conversation/`'s current live path, or anywhere
  else — extending that wiring is separately-approved future work,
  per the Intelligence Dependency Principle's own "each layer only
  depends on what came before it" rule.

## Related

- `docs/PHASE63_4_AUDIT.md`, `docs/PHASE63_4_FREEZE.md` — TASK 0's
  audit and the phase this package was built in.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline
  Reasoning's position is defined by.
- `docs/ai/AI_KNOWLEDGE.md`, `docs/ai/AI_MEMORY.md` — the two upstream
  packages this package reads from.
