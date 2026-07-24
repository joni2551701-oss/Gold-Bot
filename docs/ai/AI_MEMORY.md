# GoldBot — AI Memory

Governed by `docs/constitution/CONSTITUTION.md` Article 1. `ai/memory/`
(Phase 61.3 TASK 6, extended Phase 63.3), real code, foundation-only in
the sense that nothing in `core/pipeline.py` calls it — it is
available to any Product-layer surface that wants conversational
continuity, but no live Telegram handler wires it up yet.

## What's real

```
ai/memory/context_memory.py    ContextMemory — the underlying raw store
ai/memory/memory_runtime.py    MemoryRuntime — a 5-layer facade over it,
                                extended Phase 63.3 with a structured
                                MemoryEntry surface
ai/memory/models.py            MemoryType/MemoryPriority/MemoryScope/
                                MemoryEntry (Phase 63.3)
ai/memory/memory_registry.py   MemoryScopeDescriptor catalog (Phase 63.3)
```

`MemoryRuntime` does not reimplement storage — it composes
`ContextMemory` (unmodified since before Phase 61.3) behind a
narrower, purpose-shaped interface for the five things a
conversational AI surface actually needs: short-term recall, session
continuity, and long-term pattern reference, without every caller
needing to know `ContextMemory`'s own full internal shape.

## Structured Memory (Phase 63.3)

`MemoryRuntime`'s original `save`/`load`/`clear`/`clear_all` surface
(over the five fixed `MemoryLayer` values) is unchanged and LOCKed.
Phase 63.3 added a second, additive surface on the same class, over a
new `MemoryEntry` contract instead of raw values:

```
MemoryRuntime
  .store(entry: MemoryEntry) -> None
  .recall(key: str) -> Optional[MemoryEntry]
  .search(query: str) -> Sequence[MemoryEntry]
  .filter(predicate) -> Sequence[MemoryEntry]
  .list_all() -> List[MemoryEntry]
  .short_term() -> Sequence[MemoryEntry]
  .long_term() -> Sequence[MemoryEntry]
  .forget(key: str) -> None
```

`MemoryEntry` (`key`, `scope: MemoryScope`, `memory_type: MemoryType`,
`value: Any`, `priority: MemoryPriority = NORMAL`) is primitive/enum
only in every field except `value`, which stays permissive (same
posture `ContextMemory` already uses) — the real, mechanically-checked
guarantee is that `ai/memory/` itself never imports a trading-layer
type, not a runtime check on stored values.

`ai/memory/memory_registry.py`'s `build_memory_scope_registry()`
returns a static, six-entry `MemoryScopeDescriptor` catalog — one per
`MemoryScope` (`CONVERSATION`/`MARKET`/`EDUCATION`/`USER_PREFERENCE`/
`EXPLANATION_HISTORY`/`KNOWLEDGE_REFERENCE`) — metadata only, no AI
reasoning.

Two integration points are documented, not implemented:
`MemoryScope.KNOWLEDGE_REFERENCE` as a future pointer back to a
`knowledge/` entry key, and a future caller populating
`ai/explanation/explanation_input.py`'s `ExplanationInput` fields from
a `recall()`/`short_term()` result. `ai/memory/` does not import
`knowledge/` or `ai/explanation/` — see `docs/PHASE63_3_AUDIT.md`.

## What it is not

- Not a trading memory — it never stores or replays a `decision/`
  output as if it were a fact the AI could act on (Constitution
  Article 1).
- Not wired into `ai/conversation/conversation_engine.py`'s current
  live path beyond what Phase 61.3 already tested — extending that
  wiring is separately-approved future work.

## Related

- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — TASK 6, where this was
  built.
- `docs/ai/AI_ARCHITECTURE.md` — this package's place in the full `ai/`
  tree.
- `docs/architecture/AI_FLOW.md` — Memory's position in the
  Intelligence-layer composition order.
