# Phase 65.0 Freeze — AI Voice Intelligence Foundation

Governed by `docs/constitution/CONSTITUTION.md` Article 12 (Architecture
Evolution Law). This freeze closes Phase 65.0, the first phase in a new
`65.x` Voice sub-sequence following the `63.0`–`63.8` AI Intelligence
Layer sequence and Phase 64.0's Integration Layer. It records what was
actually built, what remains explicitly out of scope, and the
Constitution/Dependency compliance checks run at close.

## Audit Summary

TASK 0's audit (`docs/PHASE65_0_AUDIT.md`) confirmed the critical
question this phase turns on: **neither `voice/` nor `ai/voice/`
existed anywhere in the codebase before this phase.** Unlike the
naming-discrepancy pattern established for `knowledge/` (Phase 63.2),
`media/` (Phase 63.7), and `broadcast/` (Phase 63.8) — where a brief's
assumed path was wrong but a real Foundation existed elsewhere under a
different name — this is a genuine ground-up new top-level package
case, matching the original reasoning `docs/PHASE63_0_FOUNDATION_AUDIT.md`
used to justify `broadcast/`. `Capability.VOICE` and `MediaType.VOICE`
already existed as vocabulary members and were reused as-is, unchanged;
`ai/persona/`'s `Persona.tone` field was confirmed adjacent-but-different
(a docstring mention only, no actual Voice model). Resolution: one new
top-level package, `voice/`, with the brief's literal one-file-per-item
`profiles/`/`providers/` subfolder layout consolidated into single
files (`profiles.py`/`providers.py`) per Rule 8 — no existing static
catalog module in this codebase (`persona_registry.py`,
`media_registry.py`, `media_layer/telegram_broadcast/provider_manager.py`) uses a
one-file-per-item shape. No Director Decision pause was required — no
Constitution Article conflict.

## Built this phase

- `voice/models.py` — `VoiceProviderType` (`OPENAI`/`ELEVENLABS`/
  `LOCAL`/`CUSTOM`), `VoiceProviderStatus` (`ENABLED`/`DISABLED`),
  `VoiceResultStatus` (`PENDING`/`READY`/`REJECTED`), and five frozen
  dataclasses: `VoiceProvider`, `VoiceProfile`, `VoiceSettings`,
  `VoiceRequest`, `VoiceResult`. Primitive/enum/same-file-dataclass
  fields only.
- `voice/profiles.py` — `SENIOR_VOICE`/`SENIORITA_VOICE`/
  `NARRATOR_VOICE` static constants, `build_voice_profile_registry()`.
- `voice/providers.py` — `build_voice_provider_registry()`, four
  static descriptors (OpenAI/ElevenLabs/Local/Custom).
- `voice/registry.py` — `VoiceProfileRegistry`, a real runtime-mutable
  registry (`register()`/`get()`/`exists()`/`list_all()`/`default()`),
  pre-seeded from `profiles.py`, modeled on
  `media_layer/telegram_broadcast/trigger_manager.py`'s `BroadcastTriggerManager`.
- `voice/manager.py` — `VoiceManager`; delegates profile storage to
  the injected `VoiceProfileRegistry` (no duplicate storage), owns its
  own provider ENABLED/DISABLED intent tracking (every provider starts
  `DISABLED`), deterministic `validate()`/`prepare()` request
  lifecycle.
- `voice/adapter.py` — `content_result_to_voice_request(result,
  manager, profile_name, provider_type, settings=None)`, a type-only
  read of an upstream `ai.content.content_schema.ContentResult`,
  mirroring `media_layer/content_manager/media_adapter.py`'s
  `content_result_to_media_asset()` shape exactly. Returns `None` for
  a rejected/empty-body `ContentResult` or an unknown profile/provider.
- `voice/runtime.py` — `VoiceRuntime`, a thin façade over
  `VoiceManager` (`resolve_profile()`/`resolve_provider()`/
  `validate()`/`build_request()`/`build_result()`/`prepare_voice()`);
  computes nothing `VoiceManager` doesn't already compute.
- `voice/README.md`, `docs/ai/AI_VOICE.md` — new. `docs/ai/AI_ARCHITECTURE.md`,
  `docs/architecture/MODULE_DEPENDENCIES.md` extended.
- `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md` — status
  update only (`65.0` marked DONE, new `65.x` sub-sequence recorded) —
  no roadmap restructure.
- 61 new tests across 8 files in `tests/voice/`: `test_voice_models.py`
  (dataclass defaults/frozen checks, enum value sets),
  `test_voice_profiles.py` (static catalog shape + the permanent
  Persona-non-relationship regression guard),
  `test_voice_providers.py` (static catalog shape),
  `test_voice_registry.py` (register/get/exists/list_all/default),
  `test_voice_manager.py` (delegation to Registry, provider status
  tracking, validate/prepare true/false paths),
  `test_voice_adapter.py` (accepted/rejected/empty-body/unknown-profile
  paths), `test_voice_runtime.py` (façade delegation, not
  reimplementation), `test_voice_isolation.py` (permanent AST
  regression guards: no trading/downstream-Intelligence imports, no
  Speech/Whisper/ElevenLabs SDK import). All passing — exceeds the
  brief's own 25-test minimum.

## Not Built this phase

- No STT, no TTS, no Whisper/OpenAI-TTS/ElevenLabs API code, no
  Speech/Microphone SDK import anywhere (Rule 3).
- No real Telegram/Mini App/YouTube integration (Rule 4).
- No LLM call anywhere — every method in `voice/` is deterministic
  (Rule 5); `test_voice_isolation.py`'s own structural test enforces
  this permanently.
- No new `ai.persona.persona.Persona` — `SENIORITA_VOICE` is a
  self-contained `VoiceProfile`, not a `Persona`; only
  `SENIOR_TRADING_AI` remains the one registered real `Persona`
  (Phase 63.8's own finding, carried forward unchanged).
- No `media/` or `broadcast/` import — `voice/` reads only
  `ai/content/` (type-only) and `core/` this phase; composing Voice
  with Media/Broadcast is explicitly deferred (per the Director's own
  closing note: Phase 65.1 real STT/TTS, Phase 65.2 live Voice
  Conversation).
- No trading pipeline changes — zero diff in `core/`, `decision/`,
  `risk/`, `execution/`, `strategies/`, `signals/` this phase (Rule 2).

## Constitution Compliance (checks run at close)

- **Article 3 (Import Rules) / Rule 2** — `grep`/AST sweep for
  `decision`/`risk`/`execution`/`strategies`/`signals`/`database`/
  `telegram` imports across `voice/*.py`: zero matches
  (`tests/voice/test_voice_isolation.py`).
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`: no changes in any of those directories this phase.
- **Article 9 (Version Compatibility)** — no existing module's public
  API changed this phase; every `voice/*.py` file is entirely new
  content, so there is no LOCKed surface to preserve here.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed no
  Foundation/Manager/Registry/Runtime/Model/Capability/Provider
  concept for Voice existed anywhere before creating `voice/`; the two
  adjacent-but-different existing vocabulary members
  (`Capability.VOICE`, `MediaType.VOICE`) were confirmed reused as-is,
  not duplicated. See `docs/PHASE65_0_AUDIT.md`.

## Dependency Compliance

`voice/*.py` imports only `ai.content.content_schema` (type-only,
`adapter.py` only) and `core_layer.logger.logger` (`manager.py` only) outside its
own package. It never imports `media/`, `broadcast/`, `translation/`,
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`database/`, or `telegram/` — the permanent AST regression test in
`tests/voice/test_voice_isolation.py` enforces this. `voice/providers.py`'s
`VoiceProviderType.OPENAI` descriptor is unrelated to
`ai/providers/openai_provider.py`'s real, `AIService`-calling
`OpenAIProvider` — different package, different concern, no shared
code, confirmed by name-collision check in the audit.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Modules | `voice/__init__.py`, `models.py`, `profiles.py`, `providers.py`, `registry.py`, `manager.py`, `adapter.py`, `runtime.py` (8) | — | none — genuine new top-level package, no existing module extended |
| Managers | `VoiceManager` (1) | — | — |
| Models | `VoiceProviderType`, `VoiceProviderStatus`, `VoiceResultStatus`, `VoiceProvider`, `VoiceProfile`, `VoiceSettings`, `VoiceRequest`, `VoiceResult` (8) | — | `ContentResult` (type-only read in `adapter.py`, unmodified) |
| Registries | `VoiceProfileRegistry` (1) | — | — |
| Capabilities | — | — | `Capability.VOICE` (unchanged, already existed) |
| Runtime | `VoiceRuntime` (1) | — | — |
| Tests | 8 new files, 61 tests (`tests/voice/`) | — | — |
| Docs | `docs/PHASE65_0_AUDIT.md`, `docs/PHASE65_0_FREEZE.md`, `docs/ai/AI_VOICE.md`, `voice/README.md` (4) | `docs/ai/AI_ARCHITECTURE.md`, `docs/architecture/MODULE_DEPENDENCIES.md`, `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md` (4) | — |

Totals: **1 new top-level package (8 files)**, **0 extended code
modules**, **2 reused existing vocabulary members**
(`Capability.VOICE`, `MediaType.VOICE`, the latter documented as
adjacent-but-different, not consumed as a field type). This is the
first genuinely new top-level package since `broadcast/`/`media/`/
`translation/` in Phase 63.0.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/` returns no output.

## Next phase recommendation

Per the Director's own closing note on the Phase 65.0 brief: Phase
65.1 will add real STT/TTS providers (wiring `voice/providers.py`'s
descriptors to actual OpenAI/ElevenLabs/local backends), and Phase
65.2 will add live Voice Conversation. Both are deliberately kept
separate from this Foundation phase and require their own dedicated
Worker Briefs — no work has begun on either.

## Related documents

- `docs/PHASE65_0_AUDIT.md` — TASK 0's Foundation Reuse Audit.
- `docs/ai/AI_VOICE.md` — the full, current documentation of
  `voice/`'s Model/Registry/Manager/Adapter/Runtime surfaces.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this freeze's Dependency Compliance section is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the `65.x` Voice sub-sequence this
  phase opens.
