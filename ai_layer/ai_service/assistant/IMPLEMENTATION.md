# assistant/

Phase 65.3 (Personal AI Assistant Foundation); extended Phase 65.4
(Personal AI Runtime Integration — real composition with
Conversation/Voice/Memory/Intelligence Pipeline). Genuine new
top-level package, confirmed by `docs/PHASE65_3_AUDIT.md`'s TASK 0
audit (no existing package owns a durable per-user AI-identity
settings record).

## What this package is

- `identity.py` — `AssistantIdentity` (name, display_name, description,
  default_voice, default_avatar, supported_languages). Pure
  presentation metadata — deliberately **not**
  `ai_layer.personal_ai.persona_manager.persona.Persona` (Rule 3: Persona Protection). Never
  imports `ai/persona/`.
- `identity_registry.py` — static catalog: `SENIOR_IDENTITY`,
  `SENIORITA_IDENTITY`, `build_identity_registry()`.
- `identity_manager.py` — `IdentityManager`, read-only lookup over the
  registry, mirrors `ai/persona/persona_manager.py`'s shape exactly.
- `models.py` — `AssistantProfile` (assistant_id, user_id,
  selected_identity, selected_voice, selected_language, timezone,
  created_at, updated_at). A genuinely new, durable per-user resource
  — not a third session type alongside `ConversationState`/
  `VoiceSession`. Has no `provider` field (TASK 8: "Provider: Hidden").
- `access.py` — `is_personal_ai_enabled_for(role, flags)`: Owner-only
  gate, deliberately distinct from `ai_layer.ai_service.access.access_control.AccessControl`
  (which grants OWNER and ADMIN equally — TASK 7 requires ADMIN BLOCK).
- `assistant_manager.py` — `AssistantManager`: `create_assistant()`/
  `get_assistant()`/`get_assistant_for_user()`/`switch_identity()`/
  `update_settings()` (Phase 65.3), plus `create_runtime()`/
  `load_runtime()`/`restore_runtime()`/`close_runtime()`/
  `runtime_status()` (Phase 65.4). Every mutator is Owner-gated.
  In-memory only, no persistence. Still imports nothing from `voice/`,
  `ai.conversation/`, `ai.memory/` — stays business-logic-free, only
  manages the `AssistantRuntime` lifecycle record.
- `conversation_adapter.py` — three pure functions producing
  primitive-shaped params matching `VoiceSessionManager.create_session()`/
  `ConversationEngine.start_session()`'s existing signatures, plus a
  Memory scope-key helper — structural integration, zero imports of
  `voice/`, `ai.conversation/`, `ai.memory/`.
- `runtime_adapter.py` (Phase 65.4) — the third composition-root-shaped
  file in this codebase (after `ai_layer/ai_engine/intelligence_runtime.py` and
  `ai_layer/voice_ai/conversation_bridge.py`). The one file in this package
  permitted to import `ai_layer.personal_ai.interaction_manager.conversation_engine`,
  `ai_layer.ai_engine.intelligence_runtime`, `ai_layer.knowledge_ai.memory_manager.memory_runtime`/`models`, and
  `ai_layer.voice_ai.runtime`/`models`. `advance_conversation()` (real
  `ConversationEngine.ask()`), `synthesize_voice()` (real
  `VoiceRuntime.generate_audio()`/`generate_with_fallback()`),
  `remember_turn()`/`recall_turn()` (real `MemoryRuntime.store()`/
  `recall()`), `run_intelligence_pipeline()` (real
  `IntelligenceRuntime.run()`, which already composes Reasoning/
  Explanation/Content/Media/Broadcast), and `run_personal_ai_turn()`
  — the full round trip composing all of the above. Every function
  re-checks Owner Mode itself.

## AssistantRuntime (Phase 65.4)

`models.py`'s `AssistantRuntime` (`session_id`, `assistant_id`,
`started_at`, `updated_at`, `active`, `conversation_id`) is a live
session record, distinct from `AssistantProfile`'s durable per-user
settings — not a third session class alongside `ConversationState`/
`VoiceSession` either; see `docs/PHASE65_4_AUDIT.md` Question 1.
`conversation_id` is a pointer into `ai_layer.ai_service.session.SessionManager`'s own
store, never an embedded object.

## What this package is not

No avatar/animation/video/hologram/3D render of any kind (Director
Note 4 — `default_avatar` is a stable identifier string only). No
persistence — every profile/runtime lives in-process only, the same
posture `ai/session/` and `voice/session/` both already commit to.
Outside `runtime_adapter.py`, never imports `voice/`,
`ai.conversation/`, `ai.memory/`, `ai.reasoning/`, `ai.explanation/`,
`ai.persona/`, `knowledge/`, `ai.content/`, `media/`, `broadcast/`,
`translation/`, `decision/`, `risk/`, `execution/`, `strategies/`,
`signals/`, `database/`, or `telegram/` — zero exceptions, permanently
enforced by `tests/assistant/test_assistant_isolation.py` and
`tests/assistant/runtime/test_runtime_isolation.py`. Even
`runtime_adapter.py` never imports `ai.reasoning/`, `ai.explanation/`,
`ai.persona/`, `knowledge/`, `ai.content/`, `media/`, or `broadcast/`
directly — it reaches Reasoning/Explanation/Content/Media/Broadcast
only indirectly through `IntelligenceRuntime.run()`. Not tied to
Telegram or any other channel (TASK 9: Mini App/Web/Desktop/Mobile
compatibility — every public method takes a plain `user_id: str`,
never a platform-specific identifier type).

## Related

- `docs/PHASE65_3_AUDIT.md`, `docs/PHASE65_3_FREEZE.md`,
  `docs/PHASE65_4_AUDIT.md`, `docs/PHASE65_4_FREEZE.md` — full
  documentation of both phases.
- `docs/ai/AI_PERSONAL_ASSISTANT.md` — the user-facing architecture
  doc for this package.
- `ai/persona/` — the one LOCKed package this phase still reads
  nothing from (by design), even in `runtime_adapter.py`.
- `voice/`, `ai/conversation/`, `ai/memory/`,
  `ai_layer/ai_engine/intelligence_runtime.py` — the LOCKed packages
  `runtime_adapter.py` now calls via their existing, unmodified public
  APIs (Phase 65.4).
