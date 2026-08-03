# Phase 65.3 Audit — Personal AI Assistant Foundation

TASK 0's Foundation Reuse Audit (Constitution Article 11), run before
any Phase 65.3 code was written. Governed by
`docs/constitution/CONSTITUTION.md` and the Phase 65.3 Worker Brief's
own Rule 1 (LOCK: `voice/`, `ai/persona/`, `ai/conversation/`,
`ai/memory/`, `ai/reasoning/`, `knowledge/`).

## Scope of this audit

The brief asks for five things: an Identity system (Senior/Seniorita
metadata, not Persona), a per-user Assistant Profile, an Identity
Registry, an Assistant Manager, and Conversation/Voice/Memory
"integration" — all Owner-only, all foundation (no avatar/video/
hologram work, per Director Note 4).

## Question 1 — Does Identity already exist?

**No**, not in the shape this brief needs. `ai/persona/persona.py`'s
`Persona` is the closest existing concept, but Rule 3 (Persona
Protection) is explicit: *"Persona: AI qanday fikrlaydi. Voice
Profile: AI qanday gapiradi. Ular aralashtirilmaydi."* (Persona is how
the AI thinks; Voice Profile is how it speaks; they are not mixed.)
`ai_layer/voice_ai/profiles.py` already established the precedent this phase
follows: `SENIORITA_VOICE.name == "Seniorita"` is a free-text
identifier that coincidentally matches nothing in `ai/persona/`'s
one-entry registry (`SENIOR_TRADING_AI`) — no import, no linkage. This
phase's `AssistantIdentity` (Senior/Seniorita as *presentation*
metadata: display name, description, default voice, default avatar,
language support) extends that same precedent one layer further: it
is deliberately **not** `ai_layer.personal_ai.persona_manager.Persona` and never imports
`ai/persona/` at all. This keeps Rule 3's separation airtight by
construction rather than by convention alone.

## Question 2 — Does an Assistant Manager already exist?

**No.** `ai/persona/persona_manager.py`'s `PersonaManager` is a
read-only lookup over one static persona; `voice/session/manager.py`'s
`VoiceSessionManager` manages ephemeral per-call `VoiceSession`
objects (profile name + language + a pointer). Neither owns a
persistent, per-user, multi-field settings record
(`assistant_id`/`selected_identity`/`selected_voice`/
`selected_language`/`timezone`) with `switch`/`update` semantics. This
is a genuine gap — a new `AssistantManager` is required, and it is
structurally distinct from both existing managers (durable per-user
profile vs. read-only static lookup vs. ephemeral per-call session).

## Question 3 — Does a User Profile already exist?

**No.** `database_layer/user_repository/user_repository.py`'s user model is checked (read
only, not imported) — it carries account/subscription fields, nothing
about AI identity/voice/language selection. No existing dataclass in
`ai/`, `voice/`, or `database/` matches TASK 2's `AssistantProfile`
shape. Genuine gap.

## Question 4 — Does Session already exist (relevant, but distinct)?

**Yes, twice, and neither is what this phase needs.**
`ai/session/session_manager.py`'s `SessionManager` (per-conversation
turn history, TTL-based) and `voice/session/manager.py`'s
`VoiceSessionManager` (per-voice-call profile/language pointer) are
both genuinely different from what TASK 2 asks for: a **durable**
per-user settings record that outlives any single conversation or
voice call. `AssistantProfile` is not a third session type — it has no
TTL, no turn history, no per-call audio state. It is closer in shape
to `ai/persona/persona.py`'s static metadata than to either session
class, except it is per-user and mutable (selections change over
time). No duplicate Manager is created for Conversation or Voice
session concerns; `AssistantManager` owns exactly one new resource
type.

## Question 5 — Is a duplicate Manager needed anywhere?

**No**, confirmed by the four answers above — one genuinely new
resource (`AssistantProfile`), one genuinely new read-only registry
(`AssistantIdentity` catalog), one genuinely new Manager
(`AssistantManager`). No existing class is duplicated.

## The core architectural resolution: where does `assistant/` sit?

The brief's own architecture diagram is:

```
User → Identity Manager → Assistant Manager → Conversation → Knowledge
     → Memory → Reasoning → Explanation → Content → Voice → Media → Broadcast
```

This places Assistant **before** Conversation — one step earlier than
anything the existing Intelligence Dependency Principle
(`docs/policies/DIRECTOR_POLICY.md`) already governs
(`Knowledge → Memory → Reasoning → Conversation → Explanation → Content
→ Media → Broadcast`, extended informally to `→ Voice` by Phase 65.0's
own pipeline diagram). Applying the Principle's own rule literally —
"may depend only on the layer(s) that come before it, never one that
comes after" — since nothing in the chain comes before Identity/
Assistant, **`assistant/` may depend on nothing downstream of it: not
`voice/`, not `ai.conversation/`, not `ai.memory/`, not `ai.persona/`,
not `knowledge/`.**

This reads, at first glance, as tension with TASK 5/6's explicit ask
for "Conversation bilan integratsiya" / "Voice bilan integratsiya" /
"Memory bilan integratsiya." The resolution, consistent with every
prior Phase 6x.x's "foundation, not yet live-wired" posture (no phase
before this one has ever had a brand-new top-level package make a real
call into another LOCKed package's Manager on its first phase — even
`ai_layer/voice_ai/conversation_bridge.py`, Phase 65.2's real round trip, only
called *existing, unmodified* `ConversationEngine`/`VoiceRuntime`
methods, never reached into `ai/memory/` directly): **the integration
this phase provides is structural, not a Python import.**
`ai_layer/ai_service/assistant/conversation_adapter.py`'s pure functions produce plain
primitive values (`user_id`, `voice_profile_name`, `language`,
`telegram_id`) shaped to exactly match the existing, public,
already-LOCKed constructor signatures of
`ai_layer.voice_ai.session.manager.VoiceSessionManager.create_session()` and
`ai_layer.personal_ai.interaction_manager.conversation_engine.ConversationEngine.start_session()`
— without importing either class. A future, separately-approved
live-wiring phase (the same pattern every dashboard/report/command
foundation in this codebase has followed since Phase 59.x) is the one
that actually calls `AssistantManager` → builds those params → passes
them into the real `VoiceSessionManager`/`ConversationEngine`. This
phase proves the shapes are compatible; it does not perform the call.

This also resolves TASK 6 cleanly: `assistant_memory_scope_key()`
returns a formatted string (`"USER_PREFERENCE:{user_id}"`) matching
the exact convention `ai/conversation/conversation_adapters.py`'s
`memory_key_from_entry()` already establishes, **without importing
`ai_layer.knowledge_ai.memory_manager.models.MemoryScope`** — the string literal `"USER_PREFERENCE"`
mirrors that enum's existing value by convention, the same
coincidental-name-not-code-link pattern already used for
`SENIORITA_VOICE.name`/persona names. The key point TASK 6 asks for —
"Assistant: Memory egasi emas. Memory: Userniki." (Assistant is not
the memory owner; memory belongs to the user) — is enforced by
construction: every key this function produces is scoped by
`profile.user_id`, never by `profile.assistant_id`.

## Owner Mode (TASK 7) — why this is not the existing `AccessControl` matrix

`ai/access/access_control.py`'s `AccessControl` grants `AIRole.OWNER`
and `AIRole.ADMIN` the same `frozenset(Capability)` — every capability,
automatically, evaluated at import time. TASK 7 requires something
stricter: **only** `AIRole.OWNER` passes; `ADMIN`, `VIP`, `PREMIUM`,
and `FREE` all BLOCK. Reusing `AccessControl` (or adding a new
`Capability.AI_PERSONAL_ASSISTANT` member to route through it) would
silently grant `ADMIN` access too, contradicting the brief's explicit
"Admin: BLOCK" line. This phase does not add a `Capability` member for
Personal AI Assistant, and does not route through `AccessControl` —
`ai_layer/ai_service/assistant/access.py` implements a narrower, dedicated
`is_personal_ai_enabled_for(role)` check (`role == AIRole.OWNER` AND
`FeatureFlags.enable_personal_ai` both true) instead. `AIRole` itself
(the enum, not `AccessControl`) is read from `ai_layer.ai_service.access.permissions` —
an access-control *type*, orthogonal to the Knowledge→...→Broadcast
content chain, the same class every `platform_layer/telegram/owner/ai_commands.py`
function already imports without violating any pipeline direction.

`configuration/feature_flags.py`'s `FeatureFlags` dataclass is
extended (Module Reuse Principle step 2 — extend, don't duplicate)
with one new field, `enable_personal_ai: bool = False`, following the
exact pattern its own six existing `enable_*` fields already use.

## Conclusion

Five genuine gaps confirmed (Identity, Identity Registry, Assistant
Profile, Assistant Manager, Owner-only gate); zero duplicate Managers;
zero new `Capability` members; zero new imports into any LOCKed
package (`voice/`, `ai/persona/`, `ai/conversation/`, `ai/memory/`,
`ai/reasoning/`, `knowledge/` all stay byte-for-byte unchanged this
phase). One new top-level package, `assistant/`, following the same
justification precedent `voice/`, `media/`, `broadcast/`, and
`translation/` each already established in Phase 63.0/65.0 (a genuinely
new resource type with no existing package to extend into).

## Related documents

- `docs/PHASE65_2_AUDIT.md` — the prior phase's own composition-root
  precedent this audit builds on.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this audit applies one layer earlier than it has been
  applied before.
- `docs/ai/AI_PERSONAL_ASSISTANT.md` — the full documentation of what
  this phase actually builds.
