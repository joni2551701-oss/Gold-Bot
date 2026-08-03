# ai_layer / ai_service / content

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `broadcast_output.py` -- AI Layer — Broadcast Preparation Interface (Phase 61.5: AI Production
- `content_adapter.py` -- AI Layer — AI Content Adapter (Phase 61.5: AI Production Integration
- `content_adapters.py` -- AI Layer — Content Integration Adapters (Phase 63.6, TASK 4/5).
- `content_schema.py` -- AI Layer — AI Content Schema (Phase 61.5: AI Production Integration
- `content_type_vocabulary.py` -- AI Layer — Content Type Vocabulary (shared pipeline vocabulary).
- `content_types.py` -- AI Layer — AI Content Types (Phase 61.5: AI Production Integration
- `explanation_content_adapter.py` -- AI Layer — Explanation-to-Content Adapter (Phase 63.1, TASK 6).
- `models.py` -- AI Layer — Content Model (Phase 63.6, TASK 2).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `broadcast_output.py`: class `BroadcastReadyContent`
- `broadcast_output.py`: function `prepare_broadcast()`
- `content_adapter.py`: class `ContentEngine`
- `content_adapters.py`: function `content_context_from_explanation()`
- `content_adapters.py`: function `content_context_from_conversation()`
- `content_schema.py`: class `ContentRequest`
- `content_schema.py`: class `ContentResult`
- `content_type_vocabulary.py`: class `ContentType`
- `content_types.py`: function `is_content_capability()`
- `content_types.py`: function `content_title()`
- `explanation_content_adapter.py`: function `explanation_to_broadcast_ready()`
- `models.py`: class `ContentMode`
- `models.py`: class `ContentMetadata`
- `models.py`: class `ContentContext`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
