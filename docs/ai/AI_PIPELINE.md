# GoldBot — AI Pipeline

Governed by `docs/constitution/CONSTITUTION.md` Article 1. The full
Intelligence-layer composition order already lives in
`docs/architecture/AI_FLOW.md` (Phase 62.1b) — this document does not
repeat it. What it adds: where a request's *market* context actually
enters that chain, a detail `AI_FLOW.md` names but doesn't trace.

## Entry point

```
Market Context (context_layer/context_engine/context_orchestrator.py, Layer 1)
      │
      ▼
AI Context Adapter        ai/context/context_adapter.py
                           market_context_from_snapshot() (Phase 61.3 TASK 2)
                           TYPE_CHECKING-only — no runtime context/ dependency
      │
      ▼
ai/context/context_snapshot.py / context_builder.py
      │
      ▼
(continues into docs/architecture/AI_FLOW.md's own chain:
 Knowledge → Tools → Conversation → Memory → Explanation → Content → Media)
```

`market_context_from_snapshot()` is the one place a `ContextSnapshotSchema`
(the real, already-decided pipeline context) becomes a `MarketContext`
shape the AI layer's own types can consume — without `ai/context/`
importing `context/` at runtime, only for type-checking. This is the
same "type-only, not a runtime dependency" pattern Constitution
Article 3 already sanctions for the seven pre-existing
`signals/`/`context/` import sites.

## Related

- `docs/architecture/AI_FLOW.md` — the full composition chain this
  document's entry point feeds into.
- `docs/architecture/DATA_FLOW.md` — where the `ai` pipeline stage
  sits relative to `context`/`decision`/`risk` in `core/pipeline.py`'s
  real 16-stage order.
- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — TASK 2, where the adapter
  was built.
