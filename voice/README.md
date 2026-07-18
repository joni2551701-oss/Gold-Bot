# voice/

Phase 65.0 (AI Voice Intelligence Foundation); extended Phase 65.1 (AI
Voice Provider Integration — real OpenAI/ElevenLabs TTS calls). Genuine
new top-level package, confirmed by `docs/PHASE65_0_AUDIT.md`'s TASK 0
audit (neither `voice/` nor `ai/voice/` existed before Phase 65.0).

## What this package is

- `models.py` — `VoiceProvider`/`VoiceProfile`/`VoiceSettings`/
  `VoiceRequest`/`VoiceResult` (`metadata` field added Phase 65.1),
  `VoiceProviderType` (OPENAI/ELEVENLABS/LOCAL/CUSTOM),
  `VoiceProviderStatus` (ENABLED/DISABLED), `VoiceResultStatus`
  (PENDING/READY/REJECTED). Pure dataclasses, primitive/enum fields
  only.
- `profiles.py` — static catalog: `SENIOR_VOICE`, `SENIORITA_VOICE`,
  `NARRATOR_VOICE`, `build_voice_profile_registry()`.
- `providers.py` — static catalog: `build_voice_provider_registry()`,
  one descriptor per `VoiceProviderType`. LOCKed since Phase 65.0 —
  not to be confused with `provider_adapters/` below.
- `registry.py` — `VoiceProfileRegistry`, a real runtime-mutable
  registry (`register()`/`get()`/`exists()`/`list_all()`/`default()`),
  pre-seeded from `profiles.py`.
- `manager.py` — `VoiceManager`; delegates profile storage to the
  injected `VoiceProfileRegistry` (no duplicate storage), owns its own
  provider ENABLED/DISABLED tracking, and exposes a deterministic
  `validate()`/`prepare()` request lifecycle. Phase 65.1 additions:
  a real adapter registry (`register_adapter()`/`get_adapter()`/
  `list_adapters()`) and per-profile provider selection
  (`set_provider_for_profile()`/`provider_for_profile()`).
- `provider_contract.py` (Phase 65.1) — `VoiceProviderContract` (ABC:
  `generate_audio()`/`validate()`/`health_check()`) and the
  `VoiceProviderError` exception hierarchy every real adapter raises.
- `provider_adapters/` (Phase 65.1) — `openai.py`/`elevenlabs.py`
  (real HTTP TTS calls via `requests`, gated on `core/secrets.py`'s
  `OPENAI_API_KEY`/`ELEVENLABS_API_KEY`), `local.py`/`custom.py`
  (skeletons, no real backend).
- `adapter.py` — four pure functions reading one upstream type each
  into a `VoiceRequest`: `content_result_to_voice_request()` (Phase
  65.0), `media_asset_to_voice_request()`/
  `broadcast_asset_to_voice_request()`/
  `conversation_turn_to_voice_request()` (Phase 65.1).
- `runtime.py` — `VoiceRuntime`, a thin façade over `VoiceManager`
  (`resolve_profile()`/`resolve_provider()`/`validate()`/
  `build_request()`/`build_result()`/`prepare_voice()`, plus Phase
  65.1's `resolve_provider_for_profile()`/`generate_audio()`/
  `generate_with_fallback()`); computes nothing `VoiceManager` doesn't
  already compute.

## What this package is not

No STT, no Speech/Microphone/Whisper SDK import, no synthesized audio
storage or playback anywhere (Rule 3, Phase 65.0 — still in force for
everything except the two real TTS HTTP calls Phase 65.1 adds). No
real Telegram/Mini App/YouTube integration (Rule 4). No LLM call
anywhere in this package (Rule 5) — the two real adapters' HTTP calls
are TTS synthesis, not chat/completion calls. `SENIORITA_VOICE` is a
free-text voice-profile identifier only; it does not create, and is
not, an `ai.persona.persona.Persona` — see
`docs/PHASE65_0_AUDIT.md`'s own Persona relationship section.
`VoiceProviderType.OPENAI`'s descriptor/adapter here is unrelated to
`ai/providers/openai_provider.py`'s real, `AIService`-calling
`OpenAIProvider` — different package, different concern, no shared
code. No provider is ever hardcoded per-call — always resolved through
`VoiceManager`'s registry/selection methods (Phase 65.1 Rule 3).

## Related

- `ai/content/`, `media/`, `broadcast/`, `ai.session`/`ai.conversation`
  — the upstream packages `adapter.py`'s four functions read from
  (type-only). Per Phase 65.1's own pipeline diagram, `voice/` is now
  the terminal narrating stage: `... → Content → Media → Broadcast →
  Voice`.
- `media/media_types.py`'s `MediaType.VOICE` — an adjacent-but-different
  vocabulary member flagging a media asset as voice-shaped; this
  package models *who speaks, via which backend, with what settings*
  instead.
- `docs/ai/AI_VOICE.md`, `docs/PHASE65_0_AUDIT.md`,
  `docs/PHASE65_0_FREEZE.md`, `docs/PHASE65_1_AUDIT.md`,
  `docs/PHASE65_1_FREEZE.md` — full documentation of both phases.
