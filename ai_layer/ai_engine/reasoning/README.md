# ai_layer / ai_engine / reasoning

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `models.py` -- AI Layer — Reasoning Model (Phase 63.4, TASK 2).
- `reasoning_adapters.py` -- AI Layer — Reasoning Integration Adapters (Phase 63.4, TASK 4/5/6).
- `reasoning_registry.py` -- AI Layer — Reasoning Type Registry (Phase 63.4, TASK 1/3).
- `reasoning_runtime.py` -- AI Layer — Reasoning Runtime (Phase 63.4, TASK 3).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `models.py`: class `ReasoningMode`
- `models.py`: class `ReasoningType`
- `models.py`: class `ReasoningPriority`
- `models.py`: class `ReasoningStep`
- `models.py`: class `ReasoningResult`
- `reasoning_adapters.py`: function `step_from_knowledge_entry()`
- `reasoning_adapters.py`: function `step_from_memory_entry()`
- `reasoning_adapters.py`: function `reasoning_result_to_explanation_fields()`
- `reasoning_registry.py`: class `ReasoningTypeDescriptor`
- `reasoning_registry.py`: function `build_reasoning_type_registry()`
- `reasoning_registry.py`: function `describe()`
- `reasoning_runtime.py`: class `ReasoningRuntime`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
