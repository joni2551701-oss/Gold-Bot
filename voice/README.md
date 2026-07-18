# voice/

Phase 65.0 (AI Voice Intelligence Foundation). Foundation only — genuine
new top-level package, confirmed by `docs/PHASE65_0_AUDIT.md`'s TASK 0
audit (neither `voice/` nor `ai/voice/` existed before this phase).

## What this package is

- `models.py` — `VoiceProvider`/`VoiceProfile`/`VoiceSettings`/
  `VoiceRequest`/`VoiceResult`, `VoiceProviderType`
  (OPENAI/ELEVENLABS/LOCAL/CUSTOM), `VoiceProviderStatus`
  (ENABLED/DISABLED), `VoiceResultStatus` (PENDING/READY/REJECTED).
  Pure dataclasses, primitive/enum fields only.
- `profiles.py` — static catalog: `SENIOR_VOICE`, `SENIORITA_VOICE`,
  `NARRATOR_VOICE`, `build_voice_profile_registry()`.
- `providers.py` — static catalog: `build_voice_provider_registry()`,
  one descriptor per `VoiceProviderType`.
- `registry.py` — `VoiceProfileRegistry`, a real runtime-mutable
  registry (`register()`/`get()`/`exists()`/`list_all()`/`default()`),
  pre-seeded from `profiles.py`.
- `manager.py` — `VoiceManager`; delegates profile storage to the
  injected `VoiceProfileRegistry` (no duplicate storage), owns its own
  provider ENABLED/DISABLED tracking (every provider starts
  DISABLED), and exposes a deterministic `validate()`/`prepare()`
  request lifecycle.
- `adapter.py` — `content_result_to_voice_request()`, a type-only read
  of an upstream `ai.content.content_schema.ContentResult`, mirroring
  `media/media_adapter.py`'s shape exactly.
- `runtime.py` — `VoiceRuntime`, a thin façade over `VoiceManager`
  (`resolve_profile()`/`resolve_provider()`/`validate()`/
  `build_request()`/`build_result()`/`prepare_voice()`); computes
  nothing `VoiceManager` doesn't already compute.

## What this package is not

No Speech/Microphone/Whisper/OpenAI-TTS/ElevenLabs API code, no STT,
no TTS, no synthesized audio anywhere (Rule 3). No real Telegram/Mini
App/YouTube integration (Rule 4). No LLM call anywhere — every method
in this package is deterministic (Rule 5). `SENIORITA_VOICE` is a
free-text voice-profile identifier only; it does not create, and is
not, an `ai.persona.persona.Persona` — see
`docs/PHASE65_0_AUDIT.md`'s own Persona relationship section.
`VoiceProviderType.OPENAI`'s descriptor here is unrelated to
`ai/providers/openai_provider.py`'s real, `AIService`-calling
`OpenAIProvider`.

## Related

- `ai/content/` — the immediately upstream package this package reads
  from (type-only, `adapter.py`).
- `media/media_types.py`'s `MediaType.VOICE` — an adjacent-but-different
  vocabulary member flagging a media asset as voice-shaped; this
  package models *who speaks, via which backend, with what settings*
  instead. Not extended into or by this phase.
- `docs/ai/AI_VOICE.md`, `docs/PHASE65_0_AUDIT.md`,
  `docs/PHASE65_0_FREEZE.md` — full documentation of this phase.
