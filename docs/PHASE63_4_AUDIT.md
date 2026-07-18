# Phase 63.4 — AI Reasoning Intelligence Foundation: TASK 0 Audit

Per Constitution Article 11 (Foundation Reuse Law): every Worker
Brief's TASK 0 answers, for the capability about to be built —
Foundation / Manager / Contract / Model / Capability / Registry — does
it already exist? This audit answers that for Reasoning before any
code is written.

## Foundation Reuse Audit

| Component | Exists? | Real file(s) |
|---|---|---|
| Reasoning Foundation | ❌ No | no `ai/reasoning/` directory anywhere in the repository — verified by directory listing |
| Reasoning Manager/Runtime | ❌ No | no `ReasoningRuntime`/`ReasoningManager`/`ReasoningEngine` class anywhere |
| Reasoning Registry | ❌ No | none |
| Reasoning Contract/Model | ❌ No | no `ReasoningResult`/`ReasoningStep`/`ReasoningMode`/`ReasoningType`/`ReasoningPriority` anywhere |
| Reasoning Capability | ➖ Not applicable | `ai/capabilities/capability.py`'s `Capability.ANALYSIS` is the closest existing member; no dedicated `REASONING` capability exists — see TASK 8 |
| `ai/memory/` (integration source, upstream) | ✅ Yes | `MemoryEntry`/`MemoryScope`/`MemoryType`/`MemoryPriority` (Phase 63.3) — type-only reference, untouched |
| `knowledge/` (integration source, upstream) | ✅ Yes | `KnowledgeEntry`/`KnowledgeCategory` (Phase 61.3/63.2) — type-only reference, untouched |
| `ai/explanation/` (integration target, downstream) | ✅ Yes | `ExplanationBuilder`/`ExplanationInput`/`ExplanationOutput` (Phase 63.1) — **not imported**, see Intelligence Dependency Principle finding below |
| `ai/persona/` (referenced for pattern) | ✅ Yes | `Persona`/`PersonaManager`/`persona_registry.py` (Phase 63.0) — pattern reference only, not imported |
| `ai/runtime/` (referenced for pattern) | ✅ Yes | `AIService`, `RuntimeManager` — not touched; Reasoning has no runtime/provider dependency at this phase |

**Rule applied**: unlike the three prior Phase 63.x sub-phases (each of
which found an existing Foundation and/or Manager to extend), every
answer for Reasoning itself is "no." Per Article 11, this is the one
case where a genuinely new module set is permitted — `ai/reasoning/`
is created fresh this phase, as a subpackage of `ai/` (not a new
top-level package; `ai/persona/`, `ai/explanation/`, `ai/memory/` are
the direct precedent for "AI-internal concept → subpackage of `ai/`,"
per `docs/architecture/NAMING_CONVENTIONS.md`).

## No naming correction needed this phase

The first three Phase 63.x sub-phases each found a factual sketch
discrepancy in the brief's own package name (`docs/PHASE63_1_AUDIT.md`'s
`TradeContext`, `docs/PHASE63_2_AUDIT.md`'s `ai/knowledge/` vs. the
real top-level `knowledge/`, `docs/PHASE63_3_AUDIT.md`'s top-level
`memory/` vs. the real `ai/memory/`). This brief's own TASK 0 audit
list and TASK 1 both correctly name `ai/reasoning/` — matching where
the package actually belongs (a subpackage of `ai/`, alongside
`ai/persona/`, `ai/explanation/`, `ai/memory/`). No correction is
needed this time.

## Intelligence Dependency Principle compliance (Director Policy,
established at Phase 63.3's close)

```
Knowledge → Memory → Reasoning → Conversation → Explanation
   → Content → Media → Broadcast
```

Reasoning sits **between** Memory and Conversation in this chain.
Applied to this phase's own TASK 4/5/6:

- **TASK 4/5 (Knowledge, Memory — upstream, allowed)**: `ai/reasoning/`
  may reference `knowledge.models.KnowledgeEntry`/`KnowledgeCategory`
  and `ai.memory.models.MemoryEntry`/`MemoryScope`/`MemoryType` as
  **types only** — the same "reference a data shape from an earlier
  stage" pattern already sanctioned for `decision/` accepting
  `AIAnalysisResult` from `ai/` (Constitution Article 3). It never
  imports `KnowledgeManager` or `MemoryRuntime` themselves, and never
  reaches into either class's internal state — only their already-public
  dataclass fields, via two pure adapter functions
  (`ai/reasoning/reasoning_adapters.py`).
- **TASK 6 (Explanation — downstream, forbidden as an import)**:
  Explanation comes **after** Reasoning in the chain, so
  `ai/reasoning/` must never import `ai/explanation/` at all — not
  even the frozen `ExplanationInput` contract. The brief's own TASK 6
  language ("Real ulanish yo'q. Faqat interface.") is honored exactly
  this way: `reasoning_result_to_explanation_fields()` returns a plain
  `dict` of primitive values shaped like `ExplanationInput`'s own
  fields, without importing `ai.explanation` at all. A future caller
  (e.g. `core/pipeline.py`, or a future `ai/conversation/`) is the one
  that would import both packages and bridge them — `ai/reasoning/`
  itself stays one-directional.

This is a stronger constraint than Constitution Article 3 alone would
require (Article 3 only forbids `ai/* → decision/risk/execution`); the
Intelligence Dependency Principle additionally forbids `ai/reasoning/`
from importing any *downstream* AI-layer package
(`ai/explanation/`, `ai/content/`, `ai/conversation/`, `broadcast/`,
`media/`, `translation/`). TASK 8 adds a permanent regression test for
this specific check, beyond the standard trading-layer import sweep.

## TASK 2's model — primitive-only, no trading objects

`ReasoningMode` (`MARKET`/`EDUCATION`/`GENERAL`), `ReasoningType`
(`CORRELATION`/`COMPARISON`/`TREND_CONTINUITY`/
`PROBABILITY_ESTIMATE`/`SUMMARY`), `ReasoningPriority`
(`LOW`/`NORMAL`/`HIGH`) are plain enums. `ReasoningStep` (`label: str`,
`value: str`, `source: Optional[str] = None`) and `ReasoningResult`
(`key: str`, `mode: ReasoningMode`, `reasoning_type: ReasoningType`,
`conclusion: str`, `steps: Sequence[ReasoningStep]`, `confidence:
float`, `priority: ReasoningPriority`) are both 100% primitive/enum
fields — no `Any`-typed field anywhere (unlike `ai/memory/models.py`'s
`MemoryEntry.value`, which Phase 63.3 deliberately kept permissive).
`source` on `ReasoningStep` is a free-text pointer (e.g.
`"knowledge:smc.bos"`, `"memory:market.cpi_last"`) rather than an
embedded `KnowledgeEntry`/`MemoryEntry` object, so `ReasoningResult`
itself never carries another package's object graph — only the two
adapter functions (TASK 4/5) read a `KnowledgeEntry`/`MemoryEntry`'s
fields to *produce* a `ReasoningStep`.

## TASK 3's runtime — deterministic only, no inference

`ReasoningRuntime.reason()` stores a caller-fully-assembled
`ReasoningResult` (the caller decides `conclusion`/`confidence`/
`steps` — this module never computes a probability, a correlation
score, or any derived number itself). `explain()`/`summarize()`/
`evaluate()`/`compare()`/`chain()`/`history()` are all pure reads or
simple arithmetic (a confidence subtraction for `compare()`, a string
join for `summarize()`) over already-stored data — zero `AIService`/
provider call, zero network call, the same deterministic posture
`ai/explanation/explanation_builder.py` already established in Phase
63.1.

## Requesting no Director Decision

No Constitution Article conflict was found. This is the first Phase
63.x sub-phase where the Foundation Reuse Audit's answer is "build
fresh" rather than "extend" — a legitimate outcome under Article 11,
not an exception to it. TASK 1 through TASK 10 proceed without a
pause.

## Related

- `docs/constitution/CONSTITUTION.md` Article 3, 7, 11, 12.
- `docs/PHASE63_1_AUDIT.md`, `docs/PHASE63_2_AUDIT.md`,
  `docs/PHASE63_3_AUDIT.md` — the three prior audits in this
  sub-sequence, and the naming-correction pattern this phase did not
  need to repeat.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline
  this audit's dependency-direction finding is checked against.
