# ai_layer / ai_service / assistant

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `access.py` -- Assistant Layer — Owner Mode Gate (Phase 65.3: Personal AI Assistant
- `assistant_manager.py` -- Assistant Layer — Assistant Manager (Phase 65.3: Personal AI Assistant
- `conversation_adapter.py` -- Assistant Layer — Conversation/Voice/Memory Integration Adapters
- `identity.py` -- Assistant Layer — Assistant Identity Model (Phase 65.3: Personal AI
- `identity_manager.py` -- Assistant Layer — Identity Manager (Phase 65.3: Personal AI Assistant
- `identity_registry.py` -- Assistant Layer — Identity Registry (Phase 65.3: Personal AI Assistant
- `models.py` -- Assistant Layer — Assistant Profile Model (Phase 65.3: Personal AI
- `runtime_adapter.py` -- Assistant Layer — Runtime Adapter (Phase 65.4: Personal AI Runtime

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `access.py`: function `is_personal_ai_enabled_for()`
- `assistant_manager.py`: class `AssistantManager`
- `conversation_adapter.py`: function `assistant_to_voice_session_params()`
- `conversation_adapter.py`: function `assistant_to_conversation_params()`
- `conversation_adapter.py`: function `assistant_memory_scope_key()`
- `identity.py`: class `AssistantIdentity`
- `identity_manager.py`: class `IdentityManager`
- `identity_registry.py`: function `build_identity_registry()`
- `models.py`: class `AssistantProfile`
- `models.py`: class `AssistantRuntime`
- `runtime_adapter.py`: function `advance_conversation()`
- `runtime_adapter.py`: function `synthesize_voice()`
- `runtime_adapter.py`: function `remember_turn()`
- `runtime_adapter.py`: function `recall_turn()`
- `runtime_adapter.py`: function `run_intelligence_pipeline()`
- `runtime_adapter.py`: function `run_personal_ai_turn()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
