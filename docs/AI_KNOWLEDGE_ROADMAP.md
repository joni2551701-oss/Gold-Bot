# GoldBot — AI Knowledge Roadmap

Phase 63.1 (AI Explanation Intelligence Layer), TASK 5. Vision only —
`docs/ai/AI_KNOWLEDGE.md` (Phase 62.1c) already documents the real,
current `knowledge/` package (6 categories, 26 entries, static
`registry.py` lookup); this document does not repeat that and adds no
code.

## What real Knowledge looks like today

A static, hand-authored catalog. `explanation_engine.py`'s
`explain_topic()` already reads it by key
(`ai_layer.knowledge_ai.knowledge_base.registry.get_entry()`); `explanation_builder.py`'s
templates (Phase 63.1 TASK 3) reference the same underlying concepts
via `ExplanationInput.concept`/`example`/`lesson`, but as caller-supplied
text, not a live lookup into `knowledge/` — no wiring between the two
exists yet.

## What is explicitly not built

- ❌ A database-backed knowledge store.
- ❌ Vector search or embeddings of any kind.
- ❌ A real-time knowledge update/ingestion pipeline.

None of these are scoped to this phase or any phase before it. Adding
any of them is real infrastructure work requiring its own dedicated,
Director-approved phase and its own Foundation Reuse Audit — this
document names the direction, not a commitment to build it.

## Related

- `docs/ai/AI_KNOWLEDGE.md` — the real, current `knowledge/` package.
- `docs/roadmap/AI_EVOLUTION.md` Stage 3 (AI Market Analyst) — the
  stage a real knowledge-search capability would most likely belong to.
