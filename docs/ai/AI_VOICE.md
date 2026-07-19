# GoldBot — AI Voice

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `voice/` (Phase 65.0 Foundation;
Phase 65.1 real Provider Integration; Phase 65.2 real Conversation
Intelligence), real code — Phase 65.1 added real OpenAI/ElevenLabs TTS
HTTP calls; Phase 65.2 adds a real OpenAI STT (Whisper) HTTP call plus
the first real, LLM-backed "user speaks → AI understands → AI replies
by voice" round trip via `voice/conversation_bridge.py`. Still no real
Telegram/Mini App/YouTube wiring, no Local/Custom backend, no
persistent Personal AI Assistant (Phase 65.3, not yet briefed).

**`voice/` is a top-level package, a sibling of `ai/` — not
`ai/voice/`.** Unlike `knowledge/`/`media/`/`broadcast/`'s naming
corrections, this is a genuine ground-up new package: neither `voice/`
nor `ai/voice/` existed before Phase 65.0 — see
`docs/PHASE65_0_AUDIT.md`'s TASK 0 finding.

## Position in the Official Intelligence Pipeline

`voice/` is the terminal narrating stage of the Official Intelligence
Pipeline (`docs/roadmap/AI_EVOLUTION.md`): `Knowledge → Memory →
Reasoning → Conversation → Explanation → Content → Media → Broadcast →
Voice`. `voice/adapter.py` reads from `ai/content/`, `media/`,
`broadcast/`, and `ai.conversation`/`ai.session` (all upstream,
type-only) — Phase 65.0 deferred the `media`/`broadcast` reads "to a
future phase"; Phase 65.1 was that phase (TASK 9). Phase 65.2 adds a
second, narrower exception: `voice/conversation_bridge.py` is
permitted to *call* (not merely read the type of)
`ai.conversation.conversation_engine.ConversationEngine.ask()` — the
one real LLM-backed round trip this whole subsystem exists for. Rule 2
of Phase 65.2's own brief draws the boundary precisely: "Voice faqat
yuqori qatlam natijasini qabul qiladi" (Voice only receives the upper
layer's *result*) — `voice/` still never imports `ai.memory`,
`ai.reasoning`, `ai.explanation`, or top-level `knowledge` directly,
anywhere, with zero exemptions (not even `conversation_bridge.py`,
which only calls `ConversationEngine.ask()` and never reaches those
four layers itself). Nothing downstream imports `voice/` back — the
dependency still flows one direction only.

## Model

`voice/models.py`: `VoiceProviderType` (`OPENAI`/`ELEVENLABS`/`LOCAL`/
`CUSTOM`), `VoiceProviderStatus` (`ENABLED`/`DISABLED`),
`VoiceResultStatus` (`PENDING`/`READY`/`REJECTED`), and five frozen
dataclasses: `VoiceProvider` (capability descriptor —
`supports_stream`/`supports_clone`/`supports_emotion`/
`supports_ssml`/`status`), `VoiceProfile` (`name`/`display_name`/
`description`/`supported_languages`/`supported_modes`/
`default_provider`), `VoiceSettings` (`language`/`speed`/`pitch`),
`VoiceRequest` (`id`/`profile_name`/`provider_type`/`text`/`settings`/
`requested_at`), `VoiceResult` (`request_id`/`status`/`reason`/
`generated_at`/`metadata` — the last one added Phase 65.1 TASK 3/4,
additive per Article 9: a real provider adapter's own reference info,
e.g. `content_type`/`byte_length`/`provider`, never raw audio bytes,
the same "reference only, never the payload itself" posture
`media/models.py`'s `MediaAsset` already established). Every field is
a primitive, an enum defined in the same file, or another dataclass in
the same file — no `ContentResult`, `MediaAsset`, `BroadcastAsset`,
`Persona`, `DecisionResult`, `RiskResult`, or MT5/trading object is a
valid field type.

## Registry

`voice/registry.py`'s `VoiceProfileRegistry` is a real,
runtime-mutable registry (`register()`/`get()`/`exists()`/
`list_all()`/`default()`), pre-seeded from `voice/profiles.py`'s
static catalog — the same "class wrapping a dict, genuine `register()`"
shape `broadcast/trigger_manager.py`'s `BroadcastTriggerManager`
established, as opposed to `media/media_registry.py`'s deliberately
fixed catalog.

## Profiles

`voice/profiles.py`'s `build_voice_profile_registry()` returns three
static profiles this phase: `SENIOR_VOICE` (professional analyst —
market updates, weekly reports, trade replays), `SENIORITA_VOICE`
(mentor — education, training, beginner guides), `NARRATOR_VOICE`
(neutral narration — general content, no persona attached). Every
profile is metadata only — no audio, no synthesis.

**`SENIORITA_VOICE.name == "Seniorita"` is not, and does not create, an
`ai.persona.persona.Persona`.** Phase 63.8 established that only
`SENIOR_TRADING_AI` is a registered real `Persona`, and explicitly
deferred creating a Seniorita `Persona` to a future dedicated
`ai/persona/` brief. This phase's `VoiceProfile("Seniorita", ...)` is
a self-contained voice-delivery metadata record with no relationship
to `Persona` — `tests/voice/test_voice_profiles.py`'s
`test_seniorita_voice_profile_is_not_an_ai_persona` is the permanent
regression guard for this.

## Providers

`voice/providers.py`'s `build_voice_provider_registry()` returns four
static descriptors — `OPENAI` (stream + SSML), `ELEVENLABS` (stream +
clone + emotion + SSML), `LOCAL` (none), `CUSTOM` (none). Descriptors
only — no network client, no SDK import. `VoiceProviderType.OPENAI`'s
descriptor here is unrelated to `ai/providers/openai_provider.py`'s
real, `AIService`-calling `OpenAIProvider` — different package,
different concern, no shared code.

## Manager

`voice/manager.py`'s `VoiceManager` delegates profile storage to its
injected `VoiceProfileRegistry` (`register_profile()`/`get_profile()`)
rather than re-implementing it, and owns its own provider
ENABLED/DISABLED intent tracking (`register_provider()`/
`get_provider()`/`set_provider_status()`/`is_provider_enabled()`/
`list_providers()`) — every provider starts `DISABLED`, mirroring
`media/media_manager.py` and `broadcast/provider_manager.py` exactly.
`validate(request)` is deterministic: `True` only when the profile
exists, the provider is registered and enabled, and `text` is
non-empty. `prepare(request)` returns `validate()`'s own result.

Phase 65.1 TASK 6/7 additions (both additive, folded into this same
class rather than a new `VoiceProviderManager` — Rule 1's own "no
duplicate Manager"):
- **Adapter registry**: `register_adapter(provider_type, adapter)`/
  `get_adapter(provider_type)`/`list_adapters()` — holds the real
  `VoiceProviderContract` implementation backing each provider type,
  separate from the Phase 65.0 descriptor/status tracking.
- **Per-profile provider selection**: `set_provider_for_profile(name,
  provider_type)`/`provider_for_profile(name)` — an explicit override,
  falling back to the profile's own `default_provider` (Phase 65.0,
  LOCKed) when unset. An override never mutates the static
  `VoiceProfile` itself.

## Provider Contract (Phase 65.1 TASK 1)

`voice/provider_contract.py`'s `VoiceProviderContract` (ABC) is the
interface every real synthesis adapter implements:
`generate_audio(request) -> VoiceResult` (abstract), `validate() ->
bool`/`health_check() -> bool` (concrete, overridable defaults). Not
an extension of `ai/providers/base_provider.py`'s `BaseAIProvider` —
that contract is LLM-chat-shaped, a different domain; see
`docs/PHASE65_1_AUDIT.md`'s own resolution. `VoiceProviderError` (and
its `VoiceProviderTimeoutError`/`VoiceProviderUnavailableError`/
`VoiceProviderInvalidResponseError` subclasses) mirrors `ai/providers/
runtime_errors.py`'s shape without importing it — `voice/` stays
self-contained.

## Provider Adapters (Phase 65.1 TASK 2-5)

`voice/provider_adapters/` (not the brief's literal `voice/providers/`
— that name is a LOCKed file, `voice/providers.py`, since Phase 65.0;
see `docs/PHASE65_1_AUDIT.md`'s naming resolution):
- `openai.py`'s `OpenAIVoiceProvider` — real HTTP call to OpenAI's
  `/v1/audio/speech` TTS endpoint via `requests` (no SDK), gated on
  `core/secrets.py`'s existing `OPENAI_API_KEY`.
- `elevenlabs.py`'s `ElevenLabsVoiceProvider` — real HTTP call to
  ElevenLabs' `/v1/text-to-speech/{voice_id}` endpoint, gated on the
  new `ELEVENLABS_API_KEY` secret (Phase 65.1 TASK 2).
- `local.py`'s `LocalVoiceProvider`, `custom.py`'s
  `CustomVoiceProvider` — skeletons only, `validate()` always `False`,
  `generate_audio()` always raises `VoiceProviderUnavailableError`; a
  future phase wires a real backend into either without changing its
  public shape (Article 9).

Both real adapters: injectable `session`/`secrets` (never a real
network call or environment variable needed in a test), API key
travels only in the request header, never in a raised exception's
message, never logged. `VoiceResult.metadata` carries reference info
(`content_type`/`byte_length`/`provider`) on success — never the raw
audio bytes.

## Content/Media/Broadcast/Conversation integration (TASK 7, extended TASK 9)

`voice/adapter.py` holds four pure functions, each reading one
upstream type's own already-public fields into a `VoiceRequest` via
`VoiceManager` — never touching any upstream engine's internal state:
- `content_result_to_voice_request(result, manager, profile_name,
  provider_type, settings=None)` (Phase 65.0) — reads `ContentResult`.
- `media_asset_to_voice_request(asset, manager, profile_name,
  provider_type, settings=None)` (Phase 65.1) — reads `MediaAsset`,
  requires `status == READY` and a non-empty `description`.
- `broadcast_asset_to_voice_request(asset, text, manager, profile_name,
  provider_type, settings=None)` (Phase 65.1) — reads `BroadcastAsset`;
  `text` is an explicit parameter since `BroadcastAsset` carries no
  narration text of its own (only free-text `content_id`/`media_id`
  references).
- `conversation_turn_to_voice_request(turn, manager, profile_name,
  provider_type, settings=None)` (Phase 65.1) — reads
  `ai.session.conversation_state.ConversationTurn`; only narrates
  `role == "assistant"` turns, never the user's own message.

Every function returns `None` rather than fabricating a request for a
non-ready/empty/unknown input — same "never fabricate" convention
every adapter in this codebase already uses.

## Runtime

`voice/runtime.py`'s `VoiceRuntime` is a thin façade over
`VoiceManager` — `resolve_profile()`/`resolve_provider()`/`validate()`
delegate directly; `build_request()`/`build_result()` are pure
dataclass construction; `prepare_voice()` composes `validate()` +
`build_result()` into the one full-lifecycle call. It computes nothing
`VoiceManager` doesn't already compute — the three-tier
Registry → Manager → Runtime design exists specifically to satisfy
CLAUDE.md's "No duplicate logic" restriction while still giving each
of TASK 3/4/8's three files its own differently-named method set.

Phase 65.1 TASK 7/8 additions:
- `resolve_provider_for_profile(profile_name)` — delegates to
  `VoiceManager.provider_for_profile()`.
- `generate_audio(request)` — the one full real-generation call:
  `validate()` first, then delegates to whichever `VoiceProviderContract`
  adapter `VoiceManager.get_adapter()` returns. A `VoiceProviderError`
  (or no adapter registered at all) becomes a `REJECTED` `VoiceResult`
  — never raises, never fabricates a `READY` result.
- `generate_with_fallback(request, fallback_providers=None)` — tries
  `request.provider_type` first, then each provider in
  `fallback_providers` in order (same id/profile/text/settings, only
  `provider_type` changes), returning the first `READY` result or the
  last `REJECTED` one if every attempt fails.

## Speech-To-Text (Phase 65.2 TASK 1/2)

`voice/stt/` mirrors `voice/provider_contract.py`/`voice/provider_adapters/`'s
shape exactly, applied to the opposite direction (audio → text):
- `models.py` — `STTResultStatus` (`PENDING`/`READY`/`REJECTED`),
  `STTRequest` (`id`/`audio: bytes`/`language`/`requested_at`),
  `STTResult` (`request_id`/`status`/`text`/`reason`/`generated_at`/
  `metadata`). `STTRequest.audio` is the one field in this whole
  package that ever carries raw bytes — never persisted to disk or a
  database, held only for the duration of one `transcribe()` call
  (Rule 9 — no permanent audio storage by default).
- `contract.py` — `STTProviderContract` (`transcribe()` abstract,
  `validate()`/`health_check()` concrete defaults) and an
  `STTProviderError` hierarchy, self-contained (not importing
  `ai/providers/runtime_errors.py`, same posture Phase 65.1 chose for
  `VoiceProviderError`). Not a shared ABC with `VoiceProviderContract`
  — the two contracts are opposite-direction shapes; forcing one ABC
  across both would leave one direction's method irrelevant.
- `manager.py` — `STTManager`: adapter registry
  (`register_adapter()`/`get_adapter()`/`list_adapters()`) plus a
  *single* active-provider selection (`set_active_provider()`/
  `active_provider()`) — unlike `VoiceManager`'s *per-profile*
  selection (correct for TTS, where different Voice Profiles may want
  different vendors), STT has no "profile" concept, mirroring
  `ai/providers/provider_manager.py`'s single-selection shape more
  closely. `transcribe(request)` delegates to the active adapter,
  never fabricating a `READY` result on failure.
- `providers/openai.py`'s `OpenAISTTProvider` — real HTTP call to
  OpenAI's `/v1/audio/transcriptions` (Whisper) endpoint via
  `requests`, reusing the existing `OPENAI_API_KEY` secret (no new
  secret — STT and TTS share one OpenAI account).
  `providers/local.py`/`custom.py` — skeletons, same posture as
  `voice/provider_adapters/local.py`/`custom.py`.

## Intent Detection (Phase 65.2 TASK 3)

`voice/intents/models.py`'s `VoiceIntent` (`MARKET_ANALYSIS`/
`TRADE_EXPLANATION`/`EDUCATION`/`ACCOUNT_HELP`/`GENERAL_CHAT`) and
`detector.py`'s `detect_intent(text) -> VoiceIntent` — a pure,
deterministic keyword classifier, no LLM call. This phase attaches the
detected intent to `conversation_bridge.py`'s own result metadata for
observability only; no branching logic anywhere reads it yet.

## Voice Session (Phase 65.2 TASK 7/8)

`voice/session/models.py`'s `VoiceSession` (`session_id`/`user_id`/
`voice_profile_name`/`language`/`conversation_session_id`/
`created_at`) is a genuinely different session concept from
`ai/session/session_manager.py`'s `ConversationState` — it carries
voice-specific state plus a `conversation_session_id` *pointer* into
`ai.session.SessionManager`'s own store, never an embedded
`ConversationState` object. `manager.py`'s `VoiceSessionManager`
mirrors `SessionManager`'s create/get/end shape for this different
resource; `set_voice_profile()` (TASK 8 — "Senior/Seniorita
configuration, not a new Persona") validates a chosen name against the
existing `VoiceProfileRegistry` — a user "choosing Senior or
Seniorita" is choosing an existing `VoiceProfile` by name, nothing
about `ai.persona.Persona` is read or referenced anywhere in this
file. Confirmed: `ai.persona.persona_registry.SENIOR_TRADING_AI.name
== "Senior Trading AI"` while `voice.profiles.SENIOR_VOICE.name ==
"Senior"` — the two names do not coincidentally match, so no code here
relies on string equality between them.

## Voice Conversation Bridge (Phase 65.2 TASK 4/6) — the real round trip

`voice/conversation_bridge.py`'s `handle_voice_turn()` is the second
composition-root exception in this codebase (the first is
`ai/intelligence_runtime.py`, Phase 64.0, which stays deliberately
deterministic and never calls `.ask()`). Unlike that file, this one's
entire purpose is the real round trip: `STTManager.transcribe()` →
`detect_intent()` (metadata only) → the *existing*
`ConversationEngine.ask()` (real, LLM-backed, unmodified) →
`VoiceRuntime.generate_audio()`/`generate_with_fallback()` (existing,
unmodified). Zero new business logic in any of the four systems it
composes. Never raises: every failure mode (STT failure, conversation
rejection, TTS failure) returns a `REJECTED` `VoiceResult` explaining
which step failed. If `voice_session.conversation_session_id` is
unset, it calls `ConversationEngine.start_session()` once and stores
the returned pointer on the `VoiceSession` — a real session-linking
side effect, not a fabricated one.

`tests/voice/test_voice_isolation.py`'s
`test_conversation_engine_real_call_confined_to_conversation_bridge`
is the permanent regression guard: `ai.conversation.conversation_engine`
(the real, LLM-backed module) is imported by exactly this one file in
the whole `voice/` package.

## Relationship to `media/media_types.py`'s `MediaType.VOICE`

`MediaType.VOICE` is a single existing enum member flagging "this
media asset is voice-shaped" — it stays untouched. This package's
models answer a materially different question: *who speaks*
(`VoiceProfile`), *via which backend* (`VoiceProvider`), and *with
what settings* (`VoiceSettings`). The two vocabularies are
complementary, never embedded objects either direction.

## What it is not

- No Speech/Microphone SDK, no permanent synthesized-audio or
  transcribed-audio storage anywhere — real STT/TTS HTTP calls exist
  (Phase 65.1/65.2), but neither audio bytes nor synthesized output is
  ever written to disk or a database in this package.
- No real Telegram/Mini App/YouTube integration (Rule 4, Phase 65.0,
  unchanged).
- No LLM call anywhere in `voice/` itself *except* the one real,
  intentional round trip `voice/conversation_bridge.py` composes —
  every other file (including `voice/stt/`, `voice/intents/`,
  `voice/session/`) stays fully deterministic, no network call beyond
  the real TTS/STT HTTP calls those specific adapters make.
- Not a trading decision — `voice/` is never imported by `core/`,
  `decision/`, `risk/`, `execution/`, `signals/`, or `strategies/`,
  and never imports any of them either (Constitution Article 3).
- Not `translation/` — `voice/` never imports it, and it never
  imports `voice/` (Intelligence Dependency Principle).
- Never imports `ai.memory`, `ai.reasoning`, `ai.explanation`, or
  top-level `knowledge` — anywhere, with zero exemptions (Phase 65.2
  Rule 2: "Voice → Knowledge ❌, Voice → Reasoning ❌"). Only
  `voice/conversation_bridge.py` may reach one layer up, into
  `ai.conversation.conversation_engine`, and only via its already
  public `ask()` method — never those four layers directly.
- Not a new `ai.persona.Persona` — see the Profiles and Voice Session
  sections above.
- Not Personal AI Assistant — Phase 65.2 builds the real voice
  round-trip Foundation only; a persistent per-user AI profile is
  Phase 65.3, not yet briefed.
- Provider selection is never hardcoded per-call — always resolved
  through `VoiceManager`'s registry/selection methods (Rule 3 of
  Phase 65.1: "Hech qaysi provider hardcode qilinmaydi").

## Related

- `docs/PHASE65_0_AUDIT.md`, `docs/PHASE65_0_FREEZE.md` — the
  Foundation phase.
- `docs/PHASE65_1_AUDIT.md`, `docs/PHASE65_1_FREEZE.md` — the real
  Provider Integration phase.
- `docs/PHASE65_2_AUDIT.md`, `docs/PHASE65_2_FREEZE.md` — this real
  Voice Conversation Intelligence phase.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/ai/AI_CONTENT.md`, `docs/ai/AI_MEDIA.md`,
  `docs/ai/AI_BROADCAST.md` — the upstream packages this package now
  reads from.
- `docs/ai/AI_CONVERSATION.md` — `ai/conversation/`'s own
  documentation; `voice/conversation_bridge.py` calls
  `ConversationEngine.ask()` exactly as documented there, without
  extending or modifying it.
