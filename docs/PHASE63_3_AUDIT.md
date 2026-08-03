# Phase 63.3 — AI Memory Intelligence Foundation: TASK 0 Audit

Per Constitution Article 11 (Foundation Reuse Law): every Worker
Brief's TASK 0 answers, for the capability about to be built —
Foundation / Manager / Contract / Model / Capability / Registry — does
it already exist? This audit answers that for Memory before any code
is written.

## Foundation Reuse Audit

| Component | Exists? | Real file(s) |
|---|---|---|
| Memory Foundation | ✅ Yes — **not** top-level `memory/`, see finding below | `ai/memory/` (subpackage of `ai/`, Phase 55 + Phase 61.3) |
| Memory Manager | ✅ Yes — narrower shape than this brief's ask, see finding below | `ai/memory/memory_runtime.py`'s `MemoryRuntime` (Phase 61.3 TASK 6) |
| Memory Registry | ❌ No | none — no static catalog of memory categories exists |
| Memory Contract/Model | ❌ No | none — `MemoryEntry`/`MemoryType`/`MemoryPriority`/`MemoryScope` do not exist; storage today is raw `Any` |
| Memory Capability | ➖ Not applicable | `ai/capabilities/capability.py`'s `Capability.MEMORY` already exists (Phase 61.0) — no change needed, see TASK 8 |
| `knowledge/` (referenced for integration) | ✅ Yes | `KnowledgeManager` (Phase 63.2) — untouched this phase, TASK 5 documents only |
| `ai/persona/` (referenced for pattern) | ✅ Yes | `Persona`/`PersonaManager`/`persona_registry.py` (Phase 63.0) — pattern reference only |
| `ai/explanation/` (referenced for integration) | ✅ Yes | `ExplanationBuilder`/`ExplanationInput`/`ExplanationOutput` (Phase 63.1) — untouched this phase, TASK 6 documents only |
| `ai/runtime/` (referenced for pattern) | ✅ Yes | `AIService`, `RuntimeManager` — not touched; Memory Foundation has no runtime/provider dependency at this phase |
| `broadcast/`, `translation/`, `media/` | ✅ Yes | Phase 63.0 foundations (`*_manager.py`/`*_registry.py`/`models.py` each) — not part of this phase's scope, listed by the brief for completeness only |

**Rule applied**: Foundation and Manager already exist. Per Article 11,
a new top-level package and a new competing Manager class are both
forbidden — the existing `ai/memory/` package and its existing
`MemoryRuntime` are extended, never duplicated. Registry and
Contract/Model are genuine gaps — these two are the real, permitted
new-file additions this phase makes, both landing inside the existing
`ai/memory/` package.

## Critical finding 1 — factual correction, not a Constitution conflict

**The brief's top-level `memory/` package does not exist.** Verified
by directory listing: no `memory/` at repository root. The real,
current Memory Foundation is `ai/memory/` — a **subpackage of `ai/`**,
built Phase 55 (`context_memory.py`) and extended Phase 61.3 TASK 6
(`memory_runtime.py`). This is the third time in three consecutive
phases this exact category of correction has been necessary
(`docs/PHASE63_1_AUDIT.md`'s `TradeContext`, `docs/PHASE63_2_AUDIT.md`'s
`ai/knowledge/`, now this phase's top-level `memory/`) — each one a
factual sketch discrepancy, not an Article 3 boundary violation, so no
Director Decision pause is required; the Worker proceeds inside the
real package and documents the correction, the same resolution applied
twice before.

Note the direction of this correction is the *opposite* of Phase
63.2's: Knowledge's real package sits *outside* `ai/` (`knowledge/`,
sibling of `ai/`); Memory's real package sits *inside* `ai/`
(`ai/memory/`, not a sibling). Both are real, both are documented
(`docs/architecture/NAMING_CONVENTIONS.md`, `docs/ai/AI_MEMORY.md`),
and this phase does not change either package's location.

## Critical finding 2 — a Manager already exists; extend, do not duplicate

**`MemoryRuntime` is a real, tested Manager already covering "AI
memory" as a concern**, so Article 11 check #2 answers "yes" and
forbids a second, competing Manager class for the same concern —
unlike Phase 63.2's Knowledge Manager, which filled a genuine "no
Manager exists" gap.

`MemoryRuntime`'s current shape (Phase 61.3, LOCKed per
`docs/PHASE61_3_INTELLIGENCE_FREEZE.md`):

```
MemoryRuntime
  .save(layer: MemoryLayer, key: str, value: Any) -> None
  .load(layer: MemoryLayer, key: str) -> Optional[Any]
  .clear(layer: MemoryLayer, key: Optional[str] = None) -> None
  .clear_all() -> None
```

Five fixed `MemoryLayer` values (`CONVERSATION`/`USER`/`TRADE`/
`LEARNING`/`MARKET`), each a separate raw `Any`-valued
`ContextMemory` dict. This brief's TASK 2–4 ask for something
materially different in shape: structured `MemoryEntry` records
(`key`, `scope`, `memory_type`, `priority`, `value`) plus `store()`/
`recall()`/`search()`/`filter()`/`list()`/`short_term()`/`long_term()`
over them — a catalog-and-query surface `MemoryRuntime` does not
provide today.

**Resolution**: extend `MemoryRuntime` itself (Article 9's allowed
shape — new methods added, no existing method's signature changed) to
also hold and query structured `MemoryEntry` records, alongside its
existing, completely unchanged `save`/`load`/`clear`/`clear_all`/
`MemoryLayer` surface. No second Manager class is created anywhere.

**One naming substitution, made explicit here**: the brief's own TASK
4 example API names a `clear()` method. `MemoryRuntime.clear(layer,
key)` already exists with a different signature (LOCKed — Article 9
forbids changing its shape). The new entry-clearing method is named
`forget(key)` instead, to add the capability without colliding with
or reshaping the existing, LOCKed `clear()`. Every other name in the
brief's TASK 4 list (`store`, `recall`, `search`, `filter`,
`short_term`, `long_term`) is used as given; `list()` is implemented
as `list_all()` to avoid shadowing the Python builtin, the same
convention `ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py`'s `KnowledgeManager`
already used in Phase 63.2.

## TASK 2's model — primitive-only, no trading objects

`MemoryType` (`SHORT_TERM`/`LONG_TERM`), `MemoryPriority`
(`LOW`/`NORMAL`/`HIGH`), `MemoryScope` (`CONVERSATION`/`MARKET`/
`EDUCATION`/`USER_PREFERENCE`/`EXPLANATION_HISTORY`/
`KNOWLEDGE_REFERENCE` — the six categories TASK 3 itself names) are
all plain enums. `MemoryEntry`'s own fields (`key: str`, `scope:
MemoryScope`, `memory_type: MemoryType`, `priority: MemoryPriority`)
are primitives/enums only, matching the brief's own constraint. Its
`value: Any` field (matching `ContextMemory`'s own existing, permissive
shape) cannot be restricted to a primitive at the type-checker level
without breaking the "store whatever the caller has" contract every
memory store in this codebase already uses — instead, the constraint
the brief actually cares about ("no `DecisionResult`/`RiskResult`/
`Trade`/`Execution`/`Position`/MT5 object") is enforced the same way
Phase 63.1's `ExplanationInput` enforced its own no-trading-object
rule: a permanent regression test that inspects `ai/memory/*.py`'s own
AST for any `decision`/`risk`/`execution` import (TASK 8), not a
runtime type check on every `store()` call — `ai/memory/` itself never
imports those types, which is the actual, mechanically-checkable
guarantee Constitution Article 3 requires.

## TASK 5/6 integration points (documented, not wired)

- **Knowledge** — a future caller could `store()` a `MemoryEntry` with
  `scope=MemoryScope.KNOWLEDGE_REFERENCE` and `value` holding a
  `ai_layer.knowledge_ai.knowledge_base.models.KnowledgeEntry.key` string, letting a later
  `recall()` resolve back through `KnowledgeManager.lookup()`.
  `ai/memory/` does not import `knowledge/`; the caller performs the
  join, the same "caller assembles, module doesn't reach into another
  package" shape already used twice (Phase 63.1 `core/pipeline.py` →
  `ExplanationInput`; Phase 63.2's own TASK 5).
- **Explanation** — a future caller could populate
  `ExplanationInput.technical_reason`/`concept`/etc. from a
  `MemoryRuntime.recall()`/`.short_term()` result before calling
  `ExplanationBuilder.build()`. `ai/explanation/` is not modified this
  phase; `ai/memory/` does not import it either.

## Requesting no Director Decision

No Constitution Article conflict was found — only the naming
correction (Critical finding 1) and the extend-not-duplicate
resolution (Critical finding 2), both self-resolvable under the same
precedent already established in `docs/PHASE63_1_AUDIT.md` and
`docs/PHASE63_2_AUDIT.md`. TASK 1 through TASK 10 proceed without a
pause.

## Related

- `docs/constitution/CONSTITUTION.md` Article 7, 9, 11, 12.
- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — where `MemoryRuntime` was
  LOCKed.
- `docs/ai/AI_MEMORY.md` — the existing, real documentation of
  `ai/memory/` this phase extends rather than replaces.
- `docs/PHASE63_1_AUDIT.md`, `docs/PHASE63_2_AUDIT.md` — the two prior
  audits this document's resolution pattern follows.
