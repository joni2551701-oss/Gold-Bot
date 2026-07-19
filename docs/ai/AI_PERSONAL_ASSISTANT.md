# AI Personal Assistant (`assistant/`)

Phase 65.3 (Personal AI Assistant Foundation). Genuine new top-level
package, confirmed by `docs/PHASE65_3_AUDIT.md`'s TASK 0 audit. Owns
one job: let an Owner pick which Identity (Senior/Seniorita) a future
conversation/voice round trip should use, and hold that choice in a
durable per-user record. Nothing else.

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
(`assistant/identity_registry.py`).

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
`knowledge/`. The one `ai.*` import anywhere in this package is
`ai.access.permissions.AIRole` (an access-control type, orthogonal to
the content chain). See `docs/PHASE65_3_AUDIT.md`'s "core
architectural resolution" for the full reasoning, including why TASK
5/6's "integration" requirement is satisfied structurally (compatible
output shapes) rather than by a real cross-package call this phase.

## Model

- `assistant/identity.py` — `AssistantIdentity` (`name`, `display_name`,
  `description`, `default_voice`, `default_avatar`,
  `supported_languages`). Pure presentation metadata.
- `assistant/models.py` — `AssistantProfile` (`assistant_id`, `user_id`,
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
`voice.profiles.SENIOR_VOICE.name` and, loosely, `ai.persona`'s
`SENIOR_TRADING_AI.name == "Senior Trading AI"` — by convention only.
No code anywhere imports across these three packages to link them;
each is independently constructed. This mirrors the precedent
`voice/profiles.py` already established for `SENIORITA_VOICE` in Phase
65.0.

## Identity Registry

`assistant/identity_registry.py`: `SENIOR_IDENTITY`, `SENIORITA_IDENTITY`,
`build_identity_registry()`. Each entry: display name, description,
default voice (a `voice/` profile *name* string, never an object),
default avatar (a stable identifier string only — no image/video/
render exists this phase, Director Note 4), supported languages.

## Identity Manager

`assistant/identity_manager.py`'s `IdentityManager` — read-only lookup
over the registry, mirrors `ai/persona/persona_manager.py`'s
`PersonaManager` shape exactly (`get()`/`exists()`/`default()`/`all()`).

## Assistant Manager (TASK 4)

`assistant/assistant_manager.py`'s `AssistantManager` owns
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

`assistant/access.py`'s `is_personal_ai_enabled_for(role, flags)`
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
  means "Auto" — `assistant/conversation_adapter.py`'s
  `assistant_to_voice_session_params()` falls back to the selected
  identity's own `default_voice`.
- **Provider**: never a field anywhere in this package — "hidden" by
  never existing, not by UI concealment.

## Conversation/Voice/Memory integration (TASK 5/6 — structural, not live)

Three pure functions in `assistant/conversation_adapter.py`, each
producing a primitive-shaped value matching an existing, unmodified
public API — without importing it:

- `assistant_to_voice_session_params(profile, identity)` → `dict`
  matching `voice.session.manager.VoiceSessionManager.create_session()`'s
  `(user_id, voice_profile_name, language)`.
- `assistant_to_conversation_params(profile)` → `dict` matching
  `ai.conversation.conversation_engine.ConversationEngine.start_session()`'s
  `(telegram_id)`.
- `assistant_memory_scope_key(profile, sub_key=None)` → a
  `"USER_PREFERENCE:{user_id}"`-shaped string, matching
  `ai.conversation.conversation_adapters.memory_key_from_entry()`'s own
  `"scope:key"` convention, without importing
  `ai.memory.models.MemoryScope`. Always keyed by `profile.user_id`,
  never `profile.assistant_id` — TASK 6's "Assistant Memory egasi
  emas. Memory Userniki." (Assistant is not the memory owner; memory
  belongs to the user), enforced by construction.

A future, separately-approved live-wiring phase is the one that
actually calls `VoiceSessionManager.create_session(**assistant_to_voice_session_params(...))`
or `ConversationEngine.start_session(**assistant_to_conversation_params(...))`.

## Future Compatibility (TASK 9)

Every public method takes a plain `user_id: str` — never a
Telegram-specific chat ID type, never a platform enum. Nothing in
`assistant/` imports `telegram/`. This keeps the package usable from a
future Mini App, Web, Desktop, or Mobile caller without a rewrite.

## What it is not

- No avatar, animation, video, hologram, or 3D render of any kind
  (Director Note 4) — `default_avatar` is a stable identifier string
  only.
- No persistence — every `AssistantProfile` lives in-process only.
- No real call into `ConversationEngine`/`VoiceRuntime`/`MemoryRuntime`
  — every integration point is a plain-value adapter (see above).
- Not a new `ai.persona.Persona`, and never imports `ai/persona/` at
  all (Rule 3: Persona Protection).
- Never imports `voice/`, `ai.conversation/`, `ai.memory/`,
  `ai.reasoning/`, `ai.explanation/`, `knowledge/`, `ai.content/`,
  `media/`, `broadcast/`, `translation/`, `decision/`, `risk/`,
  `execution/`, `strategies/`, `signals/`, `database/`, or
  `telegram/` — zero exceptions, permanently enforced by
  `tests/assistant/test_assistant_isolation.py`.
- Not wired into any Telegram command or dashboard this phase —
  foundation only, same "not yet live-wired" posture every prior
  Owner-facing foundation in this codebase has followed since Phase
  59.x.

## Related

- `docs/PHASE65_3_AUDIT.md`, `docs/PHASE65_3_FREEZE.md` — full
  documentation of this phase.
- `assistant/README.md` — the package's own top-level README.
- `docs/ai/AI_VOICE.md`, `docs/ai/AI_CONVERSATION.md` — the two
  packages this package's adapters produce structurally-compatible
  (not literally imported) params for.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against, applied one layer earlier than any prior phase.
