# GoldBot — AI Voice

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `voice/` (Phase 65.0), real code,
foundation-only — no STT, no TTS, no real Telegram/Mini App/YouTube
wiring yet.

**`voice/` is a top-level package, a sibling of `ai/` — not
`ai/voice/`.** Unlike `knowledge/`/`media/`/`broadcast/`'s naming
corrections, this is a genuine ground-up new package: neither `voice/`
nor `ai/voice/` existed before this phase — see
`docs/PHASE65_0_AUDIT.md`'s TASK 0 finding.

## Position in the Official Intelligence Pipeline

`voice/` reads from `ai/content/` (upstream, type-only, via
`adapter.py`) the same way `media/` does, but is not itself a stage in
the `Knowledge → Memory → Reasoning → Conversation → Explanation →
Content → Media → Broadcast` chain — it is a parallel, content-adjacent
package (same relationship `translation/` has to that chain), intended
to eventually serve AI Assistant, AI Conversation, Weekly Report,
Market Brief, Trade Replay, Education, Broadcast, Mini App, and YouTube
delivery surfaces.

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
`generated_at`). Every field is a primitive, an enum defined in the
same file, or another dataclass in the same file — no `ContentResult`,
`MediaAsset`, `BroadcastAsset`, `Persona`, `DecisionResult`,
`RiskResult`, or MT5/trading object is a valid field type.

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

## Content integration (TASK 7 — real, type-only)

`voice/adapter.py`'s `content_result_to_voice_request(result, manager,
profile_name, provider_type, settings=None)` reads an upstream
`ContentResult`'s own already-public fields (`body`, `content_type`,
`generated_at`) into a new `VoiceRequest`, mirroring
`media/media_adapter.py`'s `content_result_to_media_asset()` shape
exactly — never touches `ContentEngine`'s internal state. Returns
`None` for a rejected or empty-body `ContentResult`, and also for an
unknown `profile_name`/`provider_type` (checked via `manager`).

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

## Relationship to `media/media_types.py`'s `MediaType.VOICE`

`MediaType.VOICE` is a single existing enum member flagging "this
media asset is voice-shaped" — it stays untouched by this phase. This
package's models answer a materially different question: *who speaks*
(`VoiceProfile`), *via which backend* (`VoiceProvider`), and *with
what settings* (`VoiceSettings`). The two vocabularies are
complementary, never embedded objects either direction, and `voice/`
does not import `media/` this phase (see Dependency Compliance below).

## What it is not

- No Speech/Microphone/Whisper/OpenAI-TTS/ElevenLabs API code, no STT,
  no TTS, no synthesized audio anywhere (Rule 3).
- No real Telegram/Mini App/YouTube integration (Rule 4).
- No LLM call anywhere — every method is deterministic (Rule 5).
- Not a trading decision — `voice/` is never imported by `core/`,
  `decision/`, `risk/`, `execution/`, `signals/`, or `strategies/`,
  and never imports any of them either (Constitution Article 3).
- Not Media or Broadcast — `voice/` does not import `media/` or
  `broadcast/` this phase (per `docs/PHASE65_0_AUDIT.md`'s own
  dependency-compliance decision); a future phase may compose them.
- Not a new `ai.persona.Persona` — see the Profiles section above.

## Related

- `docs/PHASE65_0_AUDIT.md`, `docs/PHASE65_0_FREEZE.md` — TASK 0's
  audit and the phase this Foundation was built in.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/ai/AI_CONTENT.md` — the immediately upstream package this
  package reads from.
- `docs/ai/AI_MEDIA.md`, `docs/ai/AI_BROADCAST.md` — the sibling
  top-level Intelligence packages this package is modeled after and
  will eventually compose with (Phase 65.1/65.2, not this phase).
