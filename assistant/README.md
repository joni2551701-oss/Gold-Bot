# assistant/

Phase 65.3 (Personal AI Assistant Foundation). Genuine new top-level
package, confirmed by `docs/PHASE65_3_AUDIT.md`'s TASK 0 audit (no
existing package owns a durable per-user AI-identity settings record).

## What this package is

- `identity.py` — `AssistantIdentity` (name, display_name, description,
  default_voice, default_avatar, supported_languages). Pure
  presentation metadata — deliberately **not**
  `ai.persona.persona.Persona` (Rule 3: Persona Protection). Never
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
  gate, deliberately distinct from `ai.access.access_control.AccessControl`
  (which grants OWNER and ADMIN equally — TASK 7 requires ADMIN BLOCK).
- `assistant_manager.py` — `AssistantManager`: `create_assistant()`/
  `get_assistant()`/`get_assistant_for_user()`/`switch_identity()`/
  `update_settings()`. Every mutator is Owner-gated. In-memory only, no
  persistence.
- `conversation_adapter.py` — three pure functions producing
  primitive-shaped params matching `VoiceSessionManager.create_session()`/
  `ConversationEngine.start_session()`'s existing signatures, plus a
  Memory scope-key helper — structural integration, zero imports of
  `voice/`, `ai.conversation/`, `ai.memory/`.

## What this package is not

No avatar/animation/video/hologram/3D render of any kind (Director
Note 4 — `default_avatar` is a stable identifier string only). No
persistence — every profile lives in-process only, the same posture
`ai/session/` and `voice/session/` both already commit to. No real
call into `ConversationEngine`/`VoiceRuntime`/`MemoryRuntime` — every
integration point this phase provides is a plain-value adapter a
future, separately-approved live-wiring phase consumes; see
`docs/PHASE65_3_AUDIT.md`'s "core architectural resolution" for why.
Never imports `voice/`, `ai.conversation/`, `ai.memory/`,
`ai.reasoning/`, `ai.explanation/`, `ai.persona/`, `knowledge/`,
`ai.content/`, `media/`, `broadcast/`, `translation/`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `database/`, or
`telegram/` — zero exceptions, permanently enforced by
`tests/assistant/test_assistant_isolation.py`. Not tied to Telegram or
any other channel (TASK 9: Mini App/Web/Desktop/Mobile compatibility —
every public method takes a plain `user_id: str`, never a
platform-specific identifier type).

## Related

- `docs/PHASE65_3_AUDIT.md`, `docs/PHASE65_3_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_PERSONAL_ASSISTANT.md` — the user-facing architecture
  doc for this package.
- `ai/persona/`, `voice/`, `ai/conversation/` — the LOCKed packages
  this phase reads *nothing* from (by design), and whose existing
  public APIs this package's `conversation_adapter.py` output is
  shaped to match.
