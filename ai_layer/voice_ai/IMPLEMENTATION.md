# voice/

Phase 65.0 (AI Voice Intelligence Foundation); extended Phase 65.1 (AI
Voice Provider Integration — real OpenAI/ElevenLabs TTS calls) and
Phase 65.2 (AI Voice Conversation Intelligence — real OpenAI STT plus
the first real, LLM-backed voice round trip). Genuine new top-level
package, confirmed by `docs/PHASE65_0_AUDIT.md`'s TASK 0 audit
(neither `voice/` nor `ai/voice/` existed before Phase 65.0).

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
  (real HTTP TTS calls via `requests`, gated on `core_layer/secrets/secrets.py`'s
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
- `stt/` (Phase 65.2) — `models.py` (`STTRequest`/`STTResult`/
  `STTResultStatus`), `contract.py` (`STTProviderContract` +
  `STTProviderError` hierarchy), `manager.py` (`STTManager`: adapter
  registry + single active-provider selection), `providers/openai.py`
  (real HTTP call to OpenAI Whisper), `providers/local.py`/`custom.py`
  (skeletons). Mirrors `provider_contract.py`/`provider_adapters/`'s
  shape for the opposite direction (audio → text).
- `intents/` (Phase 65.2) — `models.py` (`VoiceIntent`), `detector.py`
  (`detect_intent()`, deterministic keyword classifier, no LLM).
- `session/` (Phase 65.2) — `models.py` (`VoiceSession`), `manager.py`
  (`VoiceSessionManager`: create/get/end + `set_voice_profile()`
  validated against `VoiceProfileRegistry`). A genuinely different
  session concept from `ai/session/`'s `ConversationState` — linked by
  a `conversation_session_id` pointer, never an embedded object.
- `conversation_bridge.py` (Phase 65.2) — `handle_voice_turn()`, the
  second composition-root exception in this codebase (after
  `ai_layer/ai_engine/intelligence_runtime.py`). Composes STT → intent detection → the
  *existing* `ConversationEngine.ask()` (real call) → the *existing*
  `VoiceRuntime.generate_audio()`/`generate_with_fallback()`. The one
  file in this package permitted to import
  `ai_layer.personal_ai.interaction_manager.conversation_engine`.

## What this package is not

No Speech/Microphone SDK import, no permanent synthesized-audio or
transcribed-audio storage anywhere — real STT/TTS HTTP calls exist
(Phase 65.1/65.2), but no audio bytes or synthesized output is ever
written to disk or a database in this package. No real Telegram/Mini
App/YouTube integration (Rule 4). No LLM call anywhere in this package
*except* the one real, intentional round trip `conversation_bridge.py`
composes — every other file stays fully deterministic besides the real
TTS/STT HTTP calls their own adapters make. Never imports `ai_layer.knowledge_ai.memory_manager`,
`ai_layer.ai_engine.reasoning`, `ai_layer.explanation_ai`, or top-level `knowledge` — anywhere,
zero exemptions (Phase 65.2 Rule 2). `SENIORITA_VOICE` is a free-text
voice-profile identifier only; it does not create, and is not, an
`ai_layer.personal_ai.persona_manager.persona.Persona` — see `docs/PHASE65_0_AUDIT.md`'s own
Persona relationship section and `voice/session/`'s TASK 8 resolution.
`VoiceProviderType.OPENAI`'s descriptor/adapter here is unrelated to
`ai/providers/openai_provider.py`'s real, `AIService`-calling
`OpenAIProvider` — different package, different concern, no shared
code. No provider is ever hardcoded per-call — always resolved through
`VoiceManager`'s registry/selection methods (Phase 65.1 Rule 3).

## Related

- `ai/content/`, `media/`, `broadcast/`, `ai_layer.ai_service.session`/`ai_layer.personal_ai.interaction_manager`
  — the upstream packages `adapter.py`'s four functions read from
  (type-only), and `conversation_bridge.py`'s one real
  `ConversationEngine.ask()` call. Per Phase 65.1's own pipeline
  diagram, `voice/` is the terminal narrating stage: `... → Content →
  Media → Broadcast → Voice`.
- `media_layer/content_manager/media_types.py`'s `MediaType.VOICE` — an adjacent-but-different
  vocabulary member flagging a media asset as voice-shaped; this
  package models *who speaks, via which backend, with what settings*
  instead.
- `docs/ai/AI_VOICE.md`, `docs/PHASE65_0_AUDIT.md`,
  `docs/PHASE65_0_FREEZE.md`, `docs/PHASE65_1_AUDIT.md`,
  `docs/PHASE65_1_FREEZE.md`, `docs/PHASE65_2_AUDIT.md`,
  `docs/PHASE65_2_FREEZE.md` — full documentation of all three phases.
