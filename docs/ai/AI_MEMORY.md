# GoldBot — AI Memory

Governed by `docs/constitution/CONSTITUTION.md` Article 1. `ai/memory/`
(Phase 61.3 TASK 6), real code, foundation-only in the sense that
nothing in `core/pipeline.py` calls it — it is available to any
Product-layer surface that wants conversational continuity, but no
live Telegram handler wires it up yet.

## What's real

```
ai/memory/context_memory.py    ContextMemory — the underlying store
ai/memory/memory_runtime.py    MemoryRuntime — a 5-layer facade over it
```

`MemoryRuntime` does not reimplement storage — it composes
`ContextMemory` (unmodified since before Phase 61.3) behind a
narrower, purpose-shaped interface for the five things a
conversational AI surface actually needs: short-term recall, session
continuity, and long-term pattern reference, without every caller
needing to know `ContextMemory`'s own full internal shape.

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
