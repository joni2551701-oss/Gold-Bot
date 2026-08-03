# Phase 65.2 — AI Voice Conversation Intelligence: Audit

TASK 0. Mandatory reading completed (`docs/constitution/CONSTITUTION.md`,
`docs/policies/DIRECTOR_POLICY.md`, `docs/PHASE65_0_AUDIT.md`,
`docs/PHASE65_1_AUDIT.md`, `docs/ai/AI_VOICE.md`,
`docs/ai/AI_CONVERSATION.md`) before any code change, per this phase's
own Rule 1.

## Foundation Reuse Audit (Rule 1's own required table)

| Component | Brief's assumed location | Real state | Decision |
|---|---|---|---|
| STT component | `voice/stt/` | ❌ Does not exist anywhere. `voice/provider_adapters/` (Phase 65.1) is TTS (text→audio), the opposite direction | Genuine new work (TASK 1/2) |
| Conversation Engine | `ai/conversation/conversation_engine.py` | ✅ `ConversationEngine` already exists (Phase 61.3, extended 63.5), LOCKed. `ask()` performs a real `AIService.ask()` call; `start_session()`/`append()`/`history()`/`context()`/`reset()`/`close()` are deterministic | Reused as-is via its own public API — not extended, not duplicated |
| Session Manager | `ai/session/session_manager.py` | ✅ `SessionManager`/`ConversationState` already exist (Phase 61.0), LOCKed — but model a *conversation* session (`telegram_id`, turn history), not a *voice* session (`voice_profile_name`, `language`, provider selection) | Reused by reference (a `VoiceSession` stores a `conversation_session_id` pointer into it) — not extended, not duplicated; a new `VoiceSessionManager` is a genuinely different concern (Module Reuse Principle step 2: extending `SessionManager` to also carry voice-profile/language fields would conflate two independent lifecycles) |
| Voice Runtime | `ai_layer/voice_ai/runtime.py` | ✅ `VoiceRuntime` already exists (Phase 65.0, extended 65.1), LOCKed — `generate_audio()`/`generate_with_fallback()` already do exactly the TTS half of this phase's TASK 6 flow | Reused as-is, called (not duplicated) from the new composition-root function this phase adds |
| Intent Detection | `voice/intents/` | ❌ Does not exist. No keyword/intent classifier exists anywhere in `ai/`, `voice/`, or `knowledge/` | Genuine new work (TASK 3) |
| Duplicate class risk | — | `ai/conversation/conversation_engine.py`'s own Phase 63.5 docstring already establishes the precedent: "`ConversationEngine` already existed as the one real Manager for Conversation, Constitution Article 11 forbids a second, competing class" | This phase adds **zero** new Manager for Conversation itself — `ConversationEngine` is called via its existing `ask()`, never reimplemented |

## Why `voice/stt/` mirrors `voice/provider_adapters/`'s shape exactly

Same "Contract + Manager + per-vendor adapters" pattern Phase 65.1
established for TTS, applied to the opposite direction (audio→text
instead of text→audio): `voice/stt/contract.py`'s `STTProviderContract`
(`transcribe()`/`validate()`/`health_check()`), `voice/stt/manager.py`'s
`STTManager` (adapter registry + single active-provider selection —
unlike `VoiceManager`'s *per-profile* selection, STT has no "profile"
concept, so one active provider is the correct shape, mirroring
`ai/providers/provider_manager.py`'s single-selection `ProviderManager`
more closely than `VoiceManager`'s per-profile selection),
`voice/stt/providers/openai.py` (real HTTP call to OpenAI's
`/v1/audio/transcriptions` Whisper endpoint, reusing the existing
`OPENAI_API_KEY` secret — no new secret needed, STT and TTS share one
OpenAI account), `local.py`/`custom.py` (skeletons, same posture as
`voice/provider_adapters/local.py`/`custom.py`).

## The one new composition-root file: `ai_layer/voice_ai/conversation_bridge.py`

Rule 2 draws the Intelligence Dependency Principle boundary precisely:
"Voice faqat yuqori qatlam natijasini qabul qiladi" (Voice only
receives the upper layer's *result*) — the exact same boundary
`ai_layer/voice_ai/adapter.py`'s existing four functions already respect (each
reads one upstream type's already-public fields, never calls into that
layer's engine). That boundary is correct for `ai_layer/voice_ai/adapter.py`
itself and stays unchanged this phase.

But TASK 4/6's actual ask — a real "user speaks → AI understands →
AI replies by voice" round trip — requires something to *call*
`ConversationEngine.ask()` (a real, LLM-backed call), not merely read
its output type. No existing file is allowed to do that: `voice/*.py`
(Phase 65.0/65.1) never imports `ai_layer.personal_ai.interaction_manager.conversation_engine`,
only `ai_layer.personal_ai.interaction_manager.models`/`ai_layer.ai_service.session.conversation_state`
(type-only). `ai_layer/ai_engine/intelligence_runtime.py` (Phase 64.0) *does* import
`ConversationEngine`, but deliberately calls only `.append()`, never
`.ask()`, to stay permanently LLM-free — extending it to call `.ask()`
would break that file's own permanent structural test
(`test_intelligence_runtime.py`'s "never calls AIService" guard) and
conflate two different composition roots (deterministic 8-layer
pipeline vs. real live voice conversation).

**Resolution**: one new file, `ai_layer/voice_ai/conversation_bridge.py`, is the
second, narrowly-scoped composition-root exception in this codebase —
the same justification `ai_layer/ai_engine/intelligence_runtime.py`'s own docstring
already uses for itself ("the one file allowed to import every layer
it composes... the same role `core/pipeline.py` plays for the Trading
layer"). `ai_layer/voice_ai/conversation_bridge.py`'s one function,
`handle_voice_turn()`, composes (in order): `voice/stt/`'s
`STTManager.transcribe()`, `voice/intents/`'s `detect_intent()`
(metadata/logging only, no branching this phase), the *existing*
`ConversationEngine.ask()` (real call, unmodified), and the *existing*
`VoiceRuntime.generate_audio()`/`generate_with_fallback()` (unmodified).
Zero new business logic in any of the four systems it composes — pure
orchestration, matching Phase 64.0's own "zero new business logic
added to any of the layers themselves" precedent.

## `voice/session/` (TASK 7) — a genuinely different session concept

`ai/session/session_manager.py`'s `SessionManager`/`ConversationState`
already exist and are reused, unmodified, as the thing a
`VoiceSession.conversation_session_id` points *into* — never
reimplemented. `VoiceSession` (new) carries what `ConversationState`
structurally cannot without conflating concerns: `voice_profile_name`
(which `ai_layer/voice_ai/profiles.py` catalog entry — Senior/Seniorita/Narrator),
`language`, and the `conversation_session_id` pointer. `VoiceSessionManager`
(new) is a real, second `create`/`get`/`end` manager — but for a
different resource (`VoiceSession`, not `ConversationState`), the same
"two managers for two different resources is not a duplicate" reasoning
`VoiceProfileRegistry` (Phase 65.0) vs. `SessionManager` (Phase 61.0)
already established implicitly by existing side-by-side.

## TASK 8 — Senior/Seniorita "configuration," not a new Persona

Confirmed: `ai_layer.personal_ai.persona_manager.persona_registry.SENIOR_TRADING_AI.name ==
"Senior Trading AI"`, while `ai_layer.voice_ai.profiles.SENIOR_VOICE.name ==
"Senior"` — the two names do **not** coincidentally match, so this
phase cannot rely on string equality. Per the brief's own "Bu yangi
Persona emas. Faqat configuration" instruction, and per Phase 63.8's
standing rule (only `SENIOR_TRADING_AI` is a registered real `Persona`;
no `Persona` named "Seniorita" exists or is created here), TASK 8 is
satisfied entirely by `voice/session/`'s own `set_voice_profile()`
validating a chosen profile name against the already-existing
`VoiceProfileRegistry` (Phase 65.0) — no new Persona-linkage file,
no new Persona. A user "choosing Senior or Seniorita" is choosing an
existing `VoiceProfile` by name; nothing about `ai_layer.personal_ai.persona_manager.Persona`
changes or is referenced.

## Security (TASK 9)

No field anywhere in `voice/stt/models.py`/`voice/session/models.py`
persists raw audio to disk or a database — `STTRequest.audio` (raw
bytes) exists only as a function-call parameter, never a dataclass
field stored beyond the single `transcribe()` call's lifetime; no
`voice/*.py` file imports `database/` or writes a file. This matches
the brief's own Rule: "audio default permanent storage emas... faqat
session davomida" (audio is not permanently stored by default — only
for the duration of the session, in memory).

## Dependency Compliance

- `voice/stt/*.py`: imports only its own package, `core_layer.logger.logger`,
  `core.secrets`, `requests` — same posture as
  `voice/provider_adapters/*.py`.
- `voice/intents/*.py`: pure functions, no imports beyond its own
  package.
- `voice/session/*.py`: imports its own package, `core_layer.logger.logger`; may
  reference `ai_layer.ai_service.session.conversation_state`/`ai_layer.voice_ai.registry` type-only
  for validation.
- `ai_layer/voice_ai/conversation_bridge.py`: the one new file permitted to import
  `ai_layer.personal_ai.interaction_manager.conversation_engine.ConversationEngine`,
  `ai_layer.voice_ai.stt.manager.STTManager`, `ai_layer.voice_ai.intents.detector`,
  `ai_layer.voice_ai.runtime.VoiceRuntime`, `ai_layer.voice_ai.session.models.VoiceSession` —
  documented and permanently tested (mirrors
  `test_intelligence_runtime_isolation.py`'s own pattern).
- Every other `voice/*.py` file's existing isolation (no `decision`/
  `risk`/`execution`/`strategies`/`signals`/`database`/`telegram`/
  `translation`) is unchanged and re-verified this phase.

## Trading Core Isolation

Confirmed zero diff planned: no change to `core/`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`.

## Conclusion

No Constitution conflict. `ai_layer/voice_ai/conversation_bridge.py` is
consciously modeled on `ai_layer/ai_engine/intelligence_runtime.py`'s own precedent
and documented as such — not a new, undisciplined cross-layer import,
but the same disciplined "one composition root per real orchestration
need" pattern this codebase already uses twice (`core/pipeline.py` for
Trading, `ai_layer/ai_engine/intelligence_runtime.py` for the deterministic 8-layer
Intelligence Pipeline). Every other new file lands inside `voice/`
(existing package, new subpackages `stt/`/`intents/`/`session/`); no
new top-level package is created this phase.
