# AI Personal Assistant (`assistant/`)

Phase 65.3 (Personal AI Assistant Foundation); extended Phase 65.4
(Personal AI Runtime Integration). Genuine new top-level package,
confirmed by `docs/PHASE65_3_AUDIT.md`'s TASK 0 audit. Phase 65.3 let
an Owner pick which Identity (Senior/Seniorita) a conversation/voice
round trip should use and hold that choice in a durable per-user
record, with every integration point structural only. Phase 65.4
connects that Foundation to the real Runtimes: an Owner can now
actually run a personalized "text in → Conversation → Voice out"
round trip through `ai_layer/ai_service/assistant/runtime_adapter.py`.

## AI Identity Model

One AI. A user selects an **Identity**, never a separate AI:

```
Personal AI
        │
 ┌──────┴──────┐
 ▼             ▼
Senior      Seniorita
```

`Narrator`/`Mentor`/`Coach` are named in the brief as possible future
additions; only Senior and Seniorita are built this phase
(`ai_layer/ai_service/assistant/identity_registry.py`).

## Position in the Official Intelligence Pipeline

The brief's own architecture diagram places Assistant **before**
Conversation:

```
User → Identity Manager → Assistant Manager → Conversation → Knowledge
     → Memory → Reasoning → Explanation → Content → Voice → Media → Broadcast
```

Applying the Intelligence Dependency Principle
(`docs/policies/DIRECTOR_POLICY.md`) literally — a layer may depend
only on what comes before it — `assistant/` depends on **nothing**
downstream: not `voice/`, not `ai.conversation/`, not `ai.memory/`,
not `ai.reasoning/`, not `ai.explanation/`, not `ai.persona/`, not
`knowledge/`. The one `ai.*` import anywhere in this package (outside
`runtime_adapter.py`) is `ai_layer.ai_service.access.permissions.AIRole` (an
access-control type, orthogonal to the content chain). See
`docs/PHASE65_3_AUDIT.md`'s "core architectural resolution" for the
full reasoning behind Phase 65.3's structural-only posture.

**Phase 65.4 update:** `ai_layer/ai_service/assistant/runtime_adapter.py` is now the one
deliberate, narrow exception — the single file in `assistant/`
permitted to import `ai.conversation/`, `ai.memory/`, and
`ai_layer.ai_engine.intelligence_runtime` for real integration (never `ai.reasoning/`,
`ai.explanation/`, `ai.persona/`, `knowledge/`, `ai.content/`,
`media/`, or `broadcast/` directly — those are reached only indirectly
through `IntelligenceRuntime.run()`). Every other file in `assistant/`
keeps the original zero-downstream-import posture unchanged. See
`docs/PHASE65_4_AUDIT.md`.

## Model

- `ai_layer/ai_service/assistant/identity.py` — `AssistantIdentity` (`name`, `display_name`,
  `description`, `default_voice`, `default_avatar`,
  `supported_languages`). Pure presentation metadata.
- `ai_layer/ai_service/assistant/models.py` — `AssistantProfile` (`assistant_id`, `user_id`,
  `selected_identity`, `selected_voice`, `selected_language`,
  `timezone`, `created_at`, `updated_at`). Mutable, durable, per-user.
  No `provider` field (TASK 8: "Provider: Hidden").

## Persona vs. Identity vs. Voice Profile (Rule 3 — Persona Protection)

Three distinct, deliberately un-linked concepts now exist in this
codebase:

| Concept | Package | Answers |
|---|---|---|
| `Persona` | `ai/persona/` | How the AI thinks (tone, disclaimer, prompt identity) |
| `AssistantIdentity` | `assistant/` | How the assistant presents itself to a user (display name, description, default voice/avatar) |
| `VoiceProfile` | `voice/` | How the AI sounds (TTS provider, supported modes) |

`SENIOR_IDENTITY.name == "Senior"` coincidentally matches
`ai_layer.voice_ai.profiles.SENIOR_VOICE.name` and, loosely, `ai_layer.personal_ai.persona_manager`'s
`SENIOR_TRADING_AI.name == "Senior Trading AI"` — by convention only.
No code anywhere imports across these three packages to link them;
each is independently constructed. This mirrors the precedent
`ai_layer/voice_ai/profiles.py` already established for `SENIORITA_VOICE` in Phase
65.0.

## Identity Registry

`ai_layer/ai_service/assistant/identity_registry.py`: `SENIOR_IDENTITY`, `SENIORITA_IDENTITY`,
`build_identity_registry()`. Each entry: display name, description,
default voice (a `voice/` profile *name* string, never an object),
default avatar (a stable identifier string only — no image/video/
render exists this phase, Director Note 4), supported languages.

## Identity Manager

`ai_layer/ai_service/assistant/identity_manager.py`'s `IdentityManager` — read-only lookup
over the registry, mirrors `ai/persona/persona_manager.py`'s
`PersonaManager` shape exactly (`get()`/`exists()`/`default()`/`all()`).

## Assistant Manager (TASK 4)

`ai_layer/ai_service/assistant/assistant_manager.py`'s `AssistantManager` owns
`AssistantProfile` CRUD:

- `create_assistant(user_id, role, identity_name="Senior", language, timezone_name)`
- `get_assistant(assistant_id)` / `get_assistant_for_user(user_id)`
- `switch_identity(assistant_id, identity_name, role)`
- `update_settings(assistant_id, role, selected_voice, selected_language, timezone_name)`

Every mutator is Owner-gated (see below) and never raises — a denied
role, an unknown assistant, or an unknown identity all return
`None`/`False`. In-memory only, no persistence, no background job —
same posture `ai/session/` and `voice/session/` both already commit
to.

## Owner Mode (TASK 7)

`ai_layer/ai_service/assistant/access.py`'s `is_personal_ai_enabled_for(role, flags)`
requires **both** `configuration.feature_flags.FeatureFlags.enable_personal_ai`
(default `False`) **and** `role == AIRole.OWNER`. Admin, VIP, Premium,
and Free all BLOCK unconditionally, even when the flag is on — this is
deliberately *not* `ai/access/access_control.py`'s `AccessControl`
matrix, which grants `OWNER` and `ADMIN` the same
`frozenset(Capability)`. No `Capability` member was added for Personal
AI Assistant, precisely to avoid that auto-grant. See
`docs/PHASE65_3_AUDIT.md`'s "Owner Mode" section.

## Settings (TASK 8)

- **Identity**: `switch_identity()` — Senior or Seniorita.
- **Voice**: `Optional[selected_voice]` on `AssistantProfile`; `None`
  means "Auto" — `ai_layer/ai_service/assistant/conversation_adapter.py`'s
  `assistant_to_voice_session_params()` falls back to the selected
  identity's own `default_voice`.
- **Provider**: never a field anywhere in this package — "hidden" by
  never existing, not by UI concealment.

## Conversation/Voice/Memory integration (TASK 5/6 — structural, not live)

Three pure functions in `ai_layer/ai_service/assistant/conversation_adapter.py`, each
producing a primitive-shaped value matching an existing, unmodified
public API — without importing it:

- `assistant_to_voice_session_params(profile, identity)` → `dict`
  matching `ai_layer.voice_ai.session.manager.VoiceSessionManager.create_session()`'s
  `(user_id, voice_profile_name, language)`.
- `assistant_to_conversation_params(profile)` → `dict` matching
  `ai_layer.personal_ai.interaction_manager.conversation_engine.ConversationEngine.start_session()`'s
  `(telegram_id)`.
- `assistant_memory_scope_key(profile, sub_key=None)` → a
  `"USER_PREFERENCE:{user_id}"`-shaped string, matching
  `ai_layer.personal_ai.interaction_manager.conversation_adapters.memory_key_from_entry()`'s own
  `"scope:key"` convention, without importing
  `ai_layer.knowledge_ai.memory_manager.models.MemoryScope`. Always keyed by `profile.user_id`,
  never `profile.assistant_id` — TASK 6's "Assistant Memory egasi
  emas. Memory Userniki." (Assistant is not the memory owner; memory
  belongs to the user), enforced by construction.

Phase 65.3 deferred the actual call to "a future, separately-approved
live-wiring phase" — Phase 65.4 is that phase.

## Assistant Runtime + Real Integration (Phase 65.4)

`ai_layer/ai_service/assistant/models.py`'s `AssistantRuntime` (`session_id`,
`assistant_id`, `started_at`, `updated_at`, `active`,
`conversation_id`) is a live session record, managed by
`AssistantManager`'s new methods:

- `create_runtime(assistant_id, role)` — Owner-gated, validates
  `assistant_id` exists.
- `load_runtime(session_id)` / `runtime_status(session_id)` — getters.
- `restore_runtime(session_id, role)` / `close_runtime(session_id, role)`
  — Owner-gated, toggle `active`.

`ai_layer/ai_service/assistant/runtime_adapter.py` — the third composition-root-shaped
file in this codebase (after `ai_layer/ai_engine/intelligence_runtime.py` and
`ai_layer/voice_ai/conversation_bridge.py`) — composes the real calls:

- `advance_conversation()` — real `ConversationEngine.ask()`, creating
  a session via `start_session()` the first time and storing the
  pointer onto `AssistantRuntime.conversation_id`.
- `synthesize_voice()` — real `VoiceRuntime.generate_audio()`/
  `generate_with_fallback()`, using `assistant_to_voice_session_params()`
  (Phase 65.3, unchanged) to resolve profile/language.
- `remember_turn()` / `recall_turn()` — real `MemoryRuntime.store()`/
  `recall()`, keyed via `assistant_memory_scope_key()` (Phase 65.3,
  unchanged) — always by `user_id`, never `assistant_id`.
- `run_intelligence_pipeline()` — reuses `IntelligenceRuntime.run()`
  exactly as-is (Phase 64.0, unmodified); Reasoning/Explanation/
  Content/Media/Broadcast are all reached only through this one call,
  never directly.
- `run_personal_ai_turn()` — the full round trip: Owner-gate → run the
  deterministic Intelligence pipeline for grounding → real
  Conversation → remember the response → real Voice synthesis.
  Returns a `REJECTED` `VoiceResult` at any failure point, the same
  "never fabricate" convention `ai_layer/voice_ai/conversation_bridge.py`'s
  `handle_voice_turn()` already established.

Every function re-checks `is_personal_ai_enabled_for()` itself —
Owner Mode holds even if a caller reaches `runtime_adapter.py`
directly, not only through `AssistantManager`.

## Future Compatibility (TASK 9)

Every public method takes a plain `user_id: str` — never a
Telegram-specific chat ID type, never a platform enum. Nothing in
`assistant/` imports `telegram/`. This keeps the package usable from a
future Mini App, Web, Desktop, or Mobile caller without a rewrite.

## What it is not

- No avatar, animation, video, hologram, or 3D render of any kind
  (Director Note 4) — `default_avatar` is a stable identifier string
  only.
- No persistence — every `AssistantProfile`/`AssistantRuntime` lives
  in-process only.
- No new Manager, Engine, or Runtime class for Conversation, Voice,
  Memory, Reasoning, or the Intelligence Pipeline — `runtime_adapter.py`
  calls each real, unmodified, existing class's public methods only
  (Phase 65.4 Director Note 2).
- Not a new `ai_layer.personal_ai.persona_manager.Persona`, and never imports `ai/persona/` at
  all (Rule 3: Persona Protection) — not even from `runtime_adapter.py`.
- Outside `runtime_adapter.py`, never imports `voice/`,
  `ai.conversation/`, `ai.memory/`, `ai.reasoning/`, `ai.explanation/`,
  `knowledge/`, `ai.content/`, `media/`, `broadcast/`, `translation/`,
  `decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
  `database/`, or `telegram/` — zero exceptions, permanently enforced
  by `tests/assistant/test_assistant_isolation.py` and
  `tests/assistant/runtime/test_runtime_isolation.py`. Even
  `runtime_adapter.py` never imports `ai.reasoning/`,
  `ai.explanation/`, `ai.persona/`, `knowledge/`, `ai.content/`,
  `media/`, or `broadcast/` directly.
- Not wired into any Telegram command or dashboard — foundation only,
  same "not yet live-wired" posture every prior Owner-facing
  foundation in this codebase has followed since Phase 59.x; Phase
  65.4 makes the composition real and callable, not the Telegram
  surface.

## Related

- `docs/PHASE65_3_AUDIT.md`, `docs/PHASE65_3_FREEZE.md`,
  `docs/PHASE65_4_AUDIT.md`, `docs/PHASE65_4_FREEZE.md` — full
  documentation of both phases.
- `assistant/README.md` — the package's own top-level README.
- `docs/ai/AI_VOICE.md`, `docs/ai/AI_CONVERSATION.md`,
  `docs/ai/AI_INTELLIGENCE_PIPELINE.md` — the packages
  `runtime_adapter.py` now calls for real (Phase 65.4), after Phase
  65.3's own adapters first produced their structurally-compatible
  params.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against, applied one layer earlier than any prior phase.
