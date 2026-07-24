# Phase 65.1 — AI Voice Provider Integration: Audit

TASK 0. Mandatory reading completed (`docs/constitution/CONSTITUTION.md`,
`docs/policies/DIRECTOR_POLICY.md`, `docs/PHASE65_0_AUDIT.md`,
`docs/PHASE65_0_FREEZE.md`, `docs/ai/AI_VOICE.md`) before any code
change, per this phase's own Rule 1.

## Foundation Reuse Audit (Rule 1's own required table)

| Component | Brief's assumed location | Real state | Decision |
|---|---|---|---|
| Voice Manager | `voice/manager.py` | ✅ `VoiceManager` already exists (Phase 65.0), LOCKed | Extend — add adapter registry + per-profile provider selection methods; existing methods untouched |
| Voice Registry | `voice/registry.py` | ✅ `VoiceProfileRegistry` already exists (Phase 65.0), LOCKed | Reused as-is, no change |
| Voice Runtime | `voice/runtime.py` | ✅ `VoiceRuntime` already exists (Phase 65.0), LOCKed | Extend — add `resolve_provider_for_profile()`/`generate_audio()`/`generate_with_fallback()`; existing methods untouched |
| Voice Provider Contract | `voice/provider_contract.py` | ❌ Does not exist — `voice/models.py`'s `VoiceProvider` (Phase 65.0) is a metadata *descriptor* (`supports_stream`/`supports_clone`/...), not a callable contract | Genuine new work (TASK 1) |
| Provider Adapter Layer | `voice/providers/` (brief's literal path) | ❌ Does not exist as a directory — **collides with `voice/providers.py`, a LOCKed file** (Phase 65.0's static descriptor catalog, `build_voice_provider_registry()`) | Resolved below — new directory named `voice/provider_adapters/` instead |
| Real LLM Provider Contract | `ai/providers/base_provider.py`'s `BaseAIProvider` | ✅ Exists — real precedent for `name`/abstract-methods/`health_check()` shape, `session`/`secrets` injectable constructor, typed runtime errors (`ai/providers/runtime_errors.py`), raw `requests` REST calls (no SDK) | Pattern reused (Rule 8-style), concept not — `BaseAIProvider` is LLM-chat-shaped (`analyze`/`chat`/`explain`/`vision`/`image`/`voice` all returning `ProviderResult`), a different domain from TTS synthesis; `voice/provider_contract.py` is its own, smaller contract (`generate_audio`/`validate`/`health_check`) rather than an extension of `BaseAIProvider` |
| Provider Selection / Fallback | `ai/providers/provider_manager.py`'s `ProviderManager` (PREFERRED/FALLBACK/DISABLED) | ✅ Exists — real precedent, but scoped to a single global provider selection for the whole `ai/` runtime, not per-profile | Pattern reused for fallback-ordering *shape*; per-profile selection is a genuinely new concern folded into `VoiceManager` (extension, not a new `VoiceProviderManager` class — Rule 1 explicitly forbids a duplicate Manager) |
| Secrets | `core/secrets.py` | ✅ `OPENAI_API_KEY` already exists (Phase 61.2, optional) — reused as-is; `ELEVENLABS_API_KEY` does not exist | Extend `core/secrets.py` with one new optional property; no other secret needed (`local`/`custom` providers take no API key this phase) |
| Media/Broadcast/Conversation → Voice adapters | `voice/adapter.py` | ➖ Partial — `content_result_to_voice_request()` already exists (Phase 65.0), reading `ai.content` only; Phase 65.0's own audit explicitly deferred `media`/`broadcast` imports to "a future phase" | This phase is that future phase (TASK 9) — extend `voice/adapter.py` with three new pure functions; requires updating `voice/`'s isolation regression test and the Intelligence Dependency Principle diagram (both documented below, not a violation) |

## Why `voice/provider_adapters/` (not the brief's literal `voice/providers/`)

Python cannot have a package directory and a module file share one
name in the same parent package. `voice/providers.py` (Phase 65.0,
LOCKed) already owns that name — it holds the static
`VoiceProvider` descriptor catalog (`build_voice_provider_registry()`),
which stays completely untouched this phase (Rule 1: no rename, no
move, no breaking API). The real per-vendor adapter implementations
this phase adds (TASK 2-5) go in a differently-named directory,
`voice/provider_adapters/` — the exact same resolution shape Phase
65.0 itself used for TASK 5/6's brief-vs-codebase naming mismatch
(`docs/PHASE65_0_AUDIT.md`'s "file-layout resolution" section), now
applied one level down.

## Why a new `voice/provider_contract.py` (not extending `ai/providers/base_provider.py`)

`ai/providers/base_provider.py`'s `BaseAIProvider` is the contract
every LLM-chat vendor (Gemini/OpenAI/Claude/Grok) implements —
`analyze()`/`chat()`/`explain()`/`vision()`/`image()`/`voice()`, all
returning one `ProviderResult(content: str, metadata: dict)` shape.
Its `voice()` method itself is a stub every real subclass raises
`NotImplementedError` from (see `ai/providers/openai_provider.py`
line 104-105, `ai/providers/gemini_provider.py` line 137-138) — it was
never meant to carry real TTS traffic, and forcing a
`VoiceProfile`/`VoiceRequest`/`VoiceResult`-shaped call through a
`str -> ProviderResult` interface would either fabricate fields or
require breaking `BaseAIProvider`'s own LOCKed signature (Article 9
violation). `voice/provider_contract.py`'s `VoiceProviderContract` is
therefore a new, small, TTS-shaped contract — `generate_audio(request:
VoiceRequest) -> VoiceResult`, `validate() -> bool`, `health_check() ->
bool` — matching the brief's own TASK 1 interface literally. It
reuses `BaseAIProvider`'s *pattern* (injectable `session`/`secrets`,
`health_check()` as a concrete overridable default, typed runtime
errors, raw `requests` REST calls) without importing `ai/providers/`
at all — `voice/` stays a self-contained package, importing nothing
from `ai/` except `ai.content.content_schema` (type-only, unchanged
from Phase 65.0) and now `ai.conversation`/`media`/`broadcast` (type-only,
this phase's TASK 9).

## Why provider selection/fallback extends `VoiceManager` (no new `VoiceProviderManager`)

`ai/providers/provider_manager.py`'s `ProviderManager` establishes the
real PREFERRED/FALLBACK/DISABLED selection shape this phase's TASK 6/8
need — but it is scoped to a single global "which LLM provider does
`ai/runtime/` call right now" question. Voice's actual need is
per-profile ("Senior uses OpenAI, Seniorita uses ElevenLabs") with a
simple ordered-fallback list, a related but distinct shape. Per Rule 1
("duplicate Manager taqiqlanadi"), this phase does not create a
`VoiceProviderManager` sibling to `VoiceManager` — the selection
methods (`set_provider_for_profile()`/`provider_for_profile()`) and
adapter registry (`register_adapter()`/`get_adapter()`) are added as
new methods on the existing, LOCKed `VoiceManager` class instead.
`VoiceManager`'s existing provider-descriptor/status tracking (Phase
65.0: `register_provider()`/`get_provider()`/`set_provider_status()`/
`is_provider_enabled()`/`list_providers()`/`validate()`/`prepare()`)
is untouched — the new methods are additive, operating on a separate
internal dict (`_adapters`, `_profile_provider_overrides`), never
replacing or duplicating the Phase 65.0 surface.

## Why Media/Broadcast/Conversation adapters land in `voice/adapter.py` (extension, not a new file)

`voice/adapter.py` already holds exactly one function,
`content_result_to_voice_request()` (Phase 65.0), whose entire job is
"read one upstream type, produce one `VoiceRequest`, never raise."
TASK 9's three new integration points (`media_asset_to_voice_request()`,
`broadcast_asset_to_voice_request()`, `conversation_turn_to_voice_request()`)
are the exact same shape applied to three more upstream types — adding
them to the existing file is the correct extension (Module Reuse
Principle step 2), not a new module.

`broadcast.models.BroadcastAsset` carries no narration text of its own
(only `content_id`/`media_id` free-text references, per its own
docstring's "never carry another package's object graph" posture) —
`broadcast_asset_to_voice_request()` therefore takes the narration
`text` as an explicit parameter rather than fabricating it from a
field that does not exist, the same "never fabricate" convention every
other adapter in this codebase already follows.

## Dependency Compliance change (documented, not a violation)

Phase 65.0's own audit deferred `media`/`broadcast` imports "to a
future phase." TASK 9 of this brief is explicitly that phase — the
Director's own pipeline diagram in this brief
(`Content → Media → Broadcast → Voice Narration`) places Voice as the
terminal narrating layer, downstream of all three. This phase
therefore:
- Extends the Official Intelligence Pipeline
  (`docs/roadmap/AI_EVOLUTION.md`) to append `→ Voice` after
  `Broadcast`.
- Updates `voice/`'s permanent isolation regression test
  (`tests/voice/test_voice_isolation.py`) to allow `media`/`broadcast`/
  `ai.conversation`/`ai.session` imports (type-only, read-only, mirroring
  the exact posture `voice/adapter.py` already uses for `ai.content`),
  while continuing to forbid `decision`/`risk`/`execution`/`strategies`/
  `signals`/`database`/`telegram`/`translation` permanently.
- Nothing in `media/`, `broadcast/`, or `ai/conversation/` imports
  `voice/` — the dependency still flows one direction only (Rule 2's
  own "Faqat pastga oqadi").

## Relationship to `ai.persona.persona.Persona` (unchanged)

Not touched this phase. No new `Persona` is created; `voice/`'s
Profile/Provider selection stays exactly as separate from `Persona` as
Phase 65.0 established.

## Trading Core Isolation

Confirmed zero diff planned: no change to `core/`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `database/`,
`telegram/`.

## Conclusion

No Constitution conflict. Every new file lands inside `voice/`
(existing package) or as a small, justified extension to
`core/secrets.py`; no new top-level package is created this phase.
