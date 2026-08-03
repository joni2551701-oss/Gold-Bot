# Phase 65.1 Freeze — AI Voice Provider Integration

Governed by `docs/constitution/CONSTITUTION.md` Article 12 (Architecture
Evolution Law). This freeze closes Phase 65.1, the second phase in the
`65.x` Voice sub-sequence (Phase 65.0 built the Foundation; this phase
adds real provider integration on top of it). It records what was
actually built, what remains explicitly out of scope, and the
Constitution/Dependency compliance checks run at close.

## Audit Summary

TASK 0's audit (`docs/PHASE65_1_AUDIT.md`) confirmed every LOCKed
Phase 65.0 surface (`VoiceManager`, `VoiceProfileRegistry`,
`VoiceRuntime`, `voice/models.py`, `voice/profiles.py`,
`voice/providers.py`) already existed and stayed untouched in shape —
this phase's real work landed as extensions to `VoiceManager`/
`VoiceRuntime`/`voice/adapter.py` plus four genuinely new files. Two
naming resolutions were required: (1) the brief's literal
`voice/providers/` directory collides with `voice/providers.py`, a
LOCKed file since Phase 65.0 — resolved as `voice/provider_adapters/`
instead, the same "consolidate to the codebase's real shape" move
Phase 65.0 itself used for TASK 5/6; (2) `voice/provider_contract.py`
is a new, TTS-shaped contract rather than an extension of
`ai/providers/base_provider.py`'s `BaseAIProvider` (LLM-chat-shaped, a
different domain) — see the audit's own resolution section. No
Director Decision pause was required — no Constitution Article
conflict.

## Built this phase

- `voice/provider_contract.py` — `VoiceProviderContract` (ABC:
  `generate_audio()` abstract, `validate()`/`health_check()` concrete
  overridable defaults) and the `VoiceProviderError`/
  `VoiceProviderTimeoutError`/`VoiceProviderUnavailableError`/
  `VoiceProviderInvalidResponseError` exception hierarchy.
- `voice/provider_adapters/` (new directory, 4 files) —
  `openai.py`'s `OpenAIVoiceProvider` and `elevenlabs.py`'s
  `ElevenLabsVoiceProvider`: real HTTP TTS calls via `requests` (no
  SDK dependency added), injectable `session`/`secrets`, API key
  travels only in the request header, never logged, never in a raised
  exception's message. `local.py`'s `LocalVoiceProvider` and
  `custom.py`'s `CustomVoiceProvider`: skeletons, `validate()` always
  `False`, `generate_audio()` always raises
  `VoiceProviderUnavailableError`.
- `core/secrets.py` — one new optional property, `ELEVENLABS_API_KEY`
  (additive; `OPENAI_API_KEY`, Phase 61.2, reused as-is).
- `voice/models.py` — `VoiceResult` gained one new optional field,
  `metadata: Dict[str, Any] = field(default_factory=dict)` (additive
  per Article 9; carries reference info like
  `content_type`/`byte_length`/`provider`, never raw audio bytes).
- `voice/manager.py` extension — adapter registry
  (`register_adapter()`/`get_adapter()`/`list_adapters()`) and
  per-profile provider selection (`set_provider_for_profile()`/
  `provider_for_profile()`, falling back to the LOCKed
  `VoiceProfile.default_provider` when unset). Every Phase 65.0 method
  on `VoiceManager` is unchanged.
- `voice/runtime.py` extension — `resolve_provider_for_profile()`,
  `generate_audio()` (validates then delegates to the registered real
  adapter, never fabricates a `READY` result), `generate_with_fallback()`
  (tries the primary provider then each fallback in order, returns the
  first `READY` result or the last `REJECTED` one). Every Phase 65.0
  method on `VoiceRuntime` is unchanged.
- `voice/adapter.py` extension — three new pure functions:
  `media_asset_to_voice_request()`, `broadcast_asset_to_voice_request()`
  (narration `text` is an explicit parameter — `BroadcastAsset` carries
  no text of its own), `conversation_turn_to_voice_request()` (only
  narrates `role == "assistant"` turns). `content_result_to_voice_request()`
  (Phase 65.0) is unchanged.
- `tests/voice/test_voice_isolation.py` updated (not a new file) —
  permanently allows `media`/`broadcast`/`ai.session`/`ai.conversation`
  imports (type-only, confined to `adapter.py` — enforced by a new
  test), while `translation` and every trading-layer prefix remain
  permanently forbidden.
- Documentation: `docs/PHASE65_1_AUDIT.md`, `docs/PHASE65_1_FREEZE.md`
  (new); `docs/ai/AI_VOICE.md`, `voice/README.md`,
  `docs/ai/AI_ARCHITECTURE.md`, `docs/architecture/MODULE_DEPENDENCIES.md`,
  `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md` (extended).
  `docs/roadmap/AI_EVOLUTION.md`'s Official Intelligence Pipeline now
  ends `... → Broadcast → Voice`.
- 56 new tests across 2 new files (`test_voice_provider_contract.py`,
  `test_voice_provider_adapters.py`) and extensions to
  `test_voice_manager.py`, `test_voice_runtime.py`,
  `test_voice_adapter.py`, `test_voice_isolation.py` — bringing
  `tests/voice/` to 117 total. All passing — exceeds the brief's own
  30-test minimum.

## Not Built this phase

- No STT anywhere (Rule 1's own TASK list never named it this phase —
  Phase 65.2 per the Director's own roadmap).
- No real Telegram/Mini App/YouTube wiring (unchanged from Phase
  65.0).
- No real Local/Custom backend — both remain interface-ready
  skeletons, per the brief's own TASK 5 instruction ("Real model shart
  emas... Kelajak uchun").
- No hardcoded provider selection anywhere — every real call resolves
  through `VoiceManager`'s registry/selection methods (Rule 3).
- No new `VoiceProviderManager`/duplicate Registry — TASK 6/7's
  selection and adapter-registry surfaces are extensions of the
  existing, LOCKed `VoiceManager` (Rule 1).
- No trading pipeline changes — zero diff in `core/`, `decision/`,
  `risk/`, `execution/`, `strategies/`, `signals/`, `database/` this
  phase (Rule 2).

## Constitution Compliance (checks run at close)

- **Article 3 (Import Rules) / Rule 2** — AST sweep for `decision`/
  `risk`/`execution`/`strategies`/`signals`/`database`/`telegram`/
  `translation` imports across `voice/**/*.py`: zero matches
  (`tests/voice/test_voice_isolation.py`, now recursive over
  `voice/provider_adapters/` too).
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `database/`: no changes in any of those directories this
  phase.
- **Article 9 (Version Compatibility)** — every Phase 65.0 public
  method/field signature is unchanged; the one field addition
  (`VoiceResult.metadata`) has a default value, so every existing
  caller/test continues to construct and compare `VoiceResult`
  instances exactly as before.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  `VoiceManager`/`VoiceProfileRegistry`/`VoiceRuntime` already existed
  before extending them; no duplicate Manager/Registry was created for
  provider selection or the adapter registry. See
  `docs/PHASE65_1_AUDIT.md`.

## Dependency Compliance (extended this phase, documented not a violation)

`voice/*.py` (excluding `adapter.py`) still imports only its own
package plus `core_layer.logger.logger`/`core.secrets`/`requests` — no trading
layer, no `media`/`broadcast`/`ai.conversation` import anywhere except
`voice/adapter.py`, which now also imports `media.models`,
`broadcast.models`, and `ai.session.conversation_state` (all
type-only, read-only, mirroring the exact posture `adapter.py` already
used for `ai.content` since Phase 65.0). This is Phase 65.0's own
explicit deferral ("a future phase may compose them") being exercised,
per the Director's own Phase 65.1 pipeline diagram
(`Content → Media → Broadcast → Voice Narration`). Nothing in
`media/`, `broadcast/`, or `ai/conversation/` imports `voice/` back —
the dependency still flows one direction only. Two new permanent
regression tests enforce both halves of this:
`test_voice_package_never_imports_trading_or_translation_layers` (the
permanent forbidden list) and
`test_voice_package_media_broadcast_conversation_imports_are_type_only_adapter_reads`
(confines the new imports to `adapter.py` alone).

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Modules | `voice/provider_contract.py`, `voice/provider_adapters/__init__.py`/`openai.py`/`elevenlabs.py`/`local.py`/`custom.py` (6) | `voice/manager.py`, `voice/runtime.py`, `voice/adapter.py`, `voice/models.py`, `core/secrets.py` (5) | `voice/registry.py`, `voice/profiles.py`, `voice/providers.py` (unchanged) |
| Classes | `VoiceProviderContract`, `OpenAIVoiceProvider`, `ElevenLabsVoiceProvider`, `LocalVoiceProvider`, `CustomVoiceProvider` (5) | `VoiceManager`, `VoiceRuntime` (2) | `VoiceProfileRegistry` |
| Models | `VoiceProviderError` + 3 subclasses (4) | `VoiceResult` (+`metadata` field) (1) | `VoiceProviderType`, `VoiceProviderStatus`, `VoiceResultStatus`, `VoiceProvider`, `VoiceProfile`, `VoiceSettings`, `VoiceRequest` |
| Secrets | `ELEVENLABS_API_KEY` (1) | — | `OPENAI_API_KEY` |
| Adapter functions | `media_asset_to_voice_request`, `broadcast_asset_to_voice_request`, `conversation_turn_to_voice_request` (3) | — | `content_result_to_voice_request` |
| Tests | `test_voice_provider_contract.py`, `test_voice_provider_adapters.py` (2 files, 27 tests) | `test_voice_manager.py`, `test_voice_runtime.py`, `test_voice_adapter.py`, `test_voice_isolation.py` (4 files, 29 new tests) | — |
| Docs | `docs/PHASE65_1_AUDIT.md`, `docs/PHASE65_1_FREEZE.md` (2) | `docs/ai/AI_VOICE.md`, `voice/README.md`, `docs/ai/AI_ARCHITECTURE.md`, `docs/architecture/MODULE_DEPENDENCIES.md`, `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md` (6) | — |

Totals: **6 new modules inside the existing `voice/` package** (no new
top-level package), **5 extended modules**, **0 new capability**
(`Capability.VOICE`, Phase 61.0, still unchanged and unused this
phase).

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/ database/` returns no output.

## Next phase recommendation

Per the Director's own roadmap on the Phase 65.1 brief: Phase 65.2
(Voice Conversation — STT, live dialogue), Phase 65.3 (Personal AI
Assistant — Senior/Seniorita user-facing selection), Phase 65.4 (Voice
Avatar/Media — video, broadcast). All future, not yet briefed; each
requires its own dedicated Worker Brief per this session's Director
Policy.

## Related documents

- `docs/PHASE65_1_AUDIT.md` — TASK 0's Foundation Reuse Audit.
- `docs/ai/AI_VOICE.md` — the full, current documentation of
  `voice/`'s Model/Registry/Manager/Contract/Adapters/Runtime
  surfaces.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this freeze's Dependency Compliance section is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline,
  now ending `... → Broadcast → Voice`.
