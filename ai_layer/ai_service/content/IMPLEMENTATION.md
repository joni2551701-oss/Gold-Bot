# IMPLEMENTATION.md -- ai_layer/ai_service/content

## `broadcast_output.py`

AI Layer — Broadcast Preparation Interface (Phase 61.5: AI Production

Classes: `BroadcastReadyContent`

Top-level functions: `prepare_broadcast()`

## `content_adapter.py`

AI Layer — AI Content Adapter (Phase 61.5: AI Production Integration

Classes: `ContentEngine`

## `content_adapters.py`

AI Layer — Content Integration Adapters (Phase 63.6, TASK 4/5).

Top-level functions: `content_context_from_explanation()`, `content_context_from_conversation()`

## `content_schema.py`

AI Layer — AI Content Schema (Phase 61.5: AI Production Integration

Classes: `ContentRequest`, `ContentResult`

## `content_type_vocabulary.py`

AI Layer — Content Type Vocabulary (shared pipeline vocabulary).

Classes: `ContentType`

## `content_types.py`

AI Layer — AI Content Types (Phase 61.5: AI Production Integration

Top-level functions: `is_content_capability()`, `content_title()`

## `explanation_content_adapter.py`

AI Layer — Explanation-to-Content Adapter (Phase 63.1, TASK 6).

Top-level functions: `explanation_to_broadcast_ready()`

## `models.py`

AI Layer — Content Model (Phase 63.6, TASK 2).

Classes: `ContentMode`, `ContentMetadata`, `ContentContext`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
