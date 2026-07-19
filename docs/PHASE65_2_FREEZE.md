# Phase 65.2 Freeze — AI Voice Conversation Intelligence

Governed by `docs/constitution/CONSTITUTION.md` Article 12 (Architecture
Evolution Law). This freeze closes Phase 65.2, the third phase in the
`65.x` Voice sub-sequence (Phase 65.0 built the Foundation, Phase 65.1
added real provider integration; this phase adds the first real,
LLM-backed voice round trip). It records what was actually built, what
remains explicitly out of scope, and the Constitution/Dependency
compliance checks run at close.

## Audit Summary

TASK 0's audit (`docs/PHASE65_2_AUDIT.md`) confirmed every LOCKed
surface named in this phase's Rule 1 (`voice/*.py` from Phase
65.0/65.1, `ai/conversation/conversation_engine.py`,
`ai/session/session_manager.py`, `ai/memory/`, `ai/reasoning/`,
`ai/knowledge/`/top-level `knowledge/`, `ai/explanation/`) already
existed and stayed byte-for-byte unchanged — this phase's real work
landed as extensions to `VoiceManager`/`VoiceRuntime`/`voice/adapter.py`
(already extended Phase 65.1) plus five genuinely new files/packages.
One deliberate architectural decision required explicit justification:
`voice/conversation_bridge.py` is the second composition-root exception
in this codebase (the first is `ai/intelligence_runtime.py`, Phase
64.0) — the one file permitted to *call* (not merely read the type of)
`ConversationEngine.ask()`, because Phase 65.2's entire purpose is the
real "user speaks → AI understands → AI replies by voice" round trip
that a type-only read cannot produce. See the audit's own "the one new
composition-root file" section. No Director Decision pause was
required — no Constitution Article conflict.

## Built this phase

- `voice/stt/` (new package, 8 files) — `models.py` (`STTRequest`/
  `STTResult`/`STTResultStatus`), `contract.py` (`STTProviderContract`
  + `STTProviderError` hierarchy), `manager.py` (`STTManager`: adapter
  registry + single active-provider selection, unlike `VoiceManager`'s
  per-profile selection), `providers/openai.py` (real HTTP call to
  OpenAI's `/v1/audio/transcriptions` Whisper endpoint, reusing the
  existing `OPENAI_API_KEY` secret), `providers/local.py`/`custom.py`
  (skeletons).
- `voice/intents/` (new package, 3 files) — `models.py` (`VoiceIntent`:
  `MARKET_ANALYSIS`/`TRADE_EXPLANATION`/`EDUCATION`/`ACCOUNT_HELP`/
  `GENERAL_CHAT`), `detector.py` (`detect_intent()`, deterministic
  keyword classifier, metadata only, no branching logic reads it yet).
- `voice/session/` (new package, 3 files) — `models.py` (`VoiceSession`:
  `session_id`/`user_id`/`voice_profile_name`/`language`/
  `conversation_session_id`/`created_at`, mutable), `manager.py`
  (`VoiceSessionManager`: create/get/end + `set_voice_profile()` +
  `link_conversation_session()`, validated against the existing
  `VoiceProfileRegistry`).
- `voice/conversation_bridge.py` (new file) — `handle_voice_turn()`,
  the second composition-root exception: composes
  `STTManager.transcribe()` → `detect_intent()` (metadata) → the
  *existing* `ConversationEngine.ask()` (real call, unmodified) → the
  *existing* `VoiceRuntime.generate_audio()`/`generate_with_fallback()`
  (unmodified). Zero new business logic in any of the four systems it
  composes.
- `tests/voice/test_voice_isolation.py` restructured (not a new file)
  — the trading/translation forbidden list now also permanently
  forbids `ai.memory`/`ai.reasoning`/`ai.explanation`/top-level
  `knowledge`, with zero exemptions (Rule 2's explicit "Voice →
  Knowledge ❌, Voice → Reasoning ❌"); a new test confines the real
  `ai.conversation.conversation_engine` import to
  `voice/conversation_bridge.py` alone.
- Documentation: `docs/PHASE65_2_AUDIT.md`, `docs/PHASE65_2_FREEZE.md`
  (new); `docs/ai/AI_VOICE.md`, `docs/ai/AI_CONVERSATION.md`,
  `docs/ai/AI_ARCHITECTURE.md`, `docs/architecture/MODULE_DEPENDENCIES.md`,
  `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md`,
  `voice/README.md` (extended).
- 65 new tests across 7 new files (`tests/voice/stt/test_stt_models.py`,
  `test_stt_contract.py`, `test_stt_manager.py`, `test_stt_providers.py`,
  `tests/voice/conversation/test_voice_intents.py`,
  `test_voice_session.py`, `test_conversation_bridge.py`) plus one
  extension (`test_voice_isolation.py`, +1 test, 3 → 4) — 66 new tests
  total, bringing `tests/voice/` from 117 to 183. All passing —
  exceeds the brief's own 40-test minimum.

## Not Built this phase

- No STT/TTS storage of any kind — `STTRequest.audio` (raw bytes)
  exists only as a function-call parameter, never a persisted field
  (Rule 9: no permanent audio storage by default).
- No real Local/Custom STT backend — both remain interface-ready
  skeletons.
- No branching logic on detected intent — `VoiceIntent` is attached to
  results for observability only this phase.
- No Personal AI Assistant, no persistent per-user AI profile — Phase
  65.2's own brief explicitly scopes this out ("Bu bosqichda Personal
  AI Assistant hali to'liq ochilmaydi"), deferred to Phase 65.3.
- No new Persona — `VoiceSession.set_voice_profile()` selects an
  existing `VoiceProfile` by name; no `ai.persona.Persona` is created
  or referenced (TASK 8).
- No `ConversationEngine`/`SessionManager`/`VoiceManager`/`VoiceRuntime`
  code change beyond what Phase 65.0/65.1 already made — all four are
  called via their existing public APIs, never modified, never
  duplicated (Rule 1).
- No trading pipeline changes — zero diff in `core/`, `decision/`,
  `risk/`, `execution/`, `strategies/`, `signals/` this phase (Rule 3).

## Constitution Compliance (checks run at close)

- **Article 3 (Import Rules) / Rule 2** — AST sweep for `decision`/
  `risk`/`execution`/`strategies`/`signals`/`database`/`telegram`/
  `translation`/`ai.memory`/`ai.reasoning`/`ai.explanation`/`knowledge`
  imports across `voice/**/*.py`: zero matches, zero exemptions
  (`tests/voice/test_voice_isolation.py`).
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`: no changes in any of those directories this phase.
- **Article 9 (Version Compatibility)** — every Phase 65.0/65.1 public
  method/field signature is unchanged; `ConversationEngine`,
  `SessionManager`, `VoiceManager`, `VoiceRuntime` all keep their exact
  existing public APIs.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  `ConversationEngine`, `SessionManager`, `VoiceManager`, `VoiceRuntime`
  all already existed before being called/extended; no duplicate
  Manager was created for Conversation, Session, or Voice provider
  selection. See `docs/PHASE65_2_AUDIT.md`.

## Dependency Compliance (the strictest checks yet)

`voice/stt/*.py`, `voice/intents/*.py`, `voice/session/*.py` import
only their own package plus `core.logger`/`core.secrets`/`requests` —
no upstream Intelligence layer at all. `voice/conversation_bridge.py`
is the one file in the whole `voice/` package permitted to import
`ai.conversation.conversation_engine.ConversationEngine` (real call);
it also imports `ai.access.permissions.AIRole` and
`ai.context.context_snapshot.AIContext` (pass-through types the
caller-supplied `ConversationEngine.ask()` call already required, not
new coupling). Nothing in `voice/` imports `ai.memory`, `ai.reasoning`,
`ai.explanation`, or top-level `knowledge` — anywhere, with zero
exemptions, permanently enforced by
`test_voice_package_never_imports_trading_translation_or_upstream_intelligence_layers`.
Nothing downstream imports `voice/` back.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | `voice/stt/` (8 files), `voice/intents/` (3 files), `voice/session/` (3 files) (3 packages) | — | — |
| Modules | `voice/conversation_bridge.py` (1) | `tests/voice/test_voice_isolation.py` (restructured) | `voice/manager.py`, `voice/runtime.py`, `voice/adapter.py`, `voice/models.py` (unchanged this phase) |
| Classes | `STTProviderContract`, `OpenAISTTProvider`, `LocalSTTProvider`, `CustomSTTProvider`, `STTManager`, `VoiceSessionManager` (6) | — | `ConversationEngine`, `SessionManager`, `VoiceManager`, `VoiceRuntime` (called, not modified) |
| Models | `STTRequest`, `STTResult`, `STTResultStatus`, `STTProviderError` + 3 subclasses, `VoiceIntent`, `VoiceSession` (9) | — | `VoiceRequest`, `VoiceResult`, `VoiceProfile`, `AIContext`, `AIRole`, `ConversationState`, `RuntimeResponse` |
| Functions | `detect_intent()`, `handle_voice_turn()` (2) | — | `ConversationEngine.ask()`/`start_session()`, `VoiceRuntime.generate_audio()`/`generate_with_fallback()` |
| Secrets | — | — | `OPENAI_API_KEY` (STT and TTS share one account) |
| Tests | 7 new files, 65 new tests | `test_voice_isolation.py` (+1 test, 3 → 4) | — |
| Docs | `docs/PHASE65_2_AUDIT.md`, `docs/PHASE65_2_FREEZE.md` (2) | `docs/ai/AI_VOICE.md`, `docs/ai/AI_CONVERSATION.md`, `docs/ai/AI_ARCHITECTURE.md`, `docs/architecture/MODULE_DEPENDENCIES.md`, `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md`, `voice/README.md` (7) | — |

Totals: **3 new subpackages + 1 new composition-root file inside the
existing `voice/` package** (no new top-level package), **1 test file
restructured**, **0 changes to any pre-existing LOCKed class's public
API**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/` returns no output.

## Next phase recommendation

Per the Director's own roadmap on this brief: Phase 65.3 (Personal AI
Assistant — a persistent per-user AI profile unifying memory, voice,
and character selection) is the named next step, not yet briefed.
Requires its own dedicated Worker Brief per this session's Director
Policy.

## Related documents

- `docs/PHASE65_2_AUDIT.md` — TASK 0's Foundation Reuse Audit.
- `docs/ai/AI_VOICE.md` — the full, current documentation of
  `voice/`'s STT/Intent/Session/Conversation-Bridge surfaces.
- `docs/ai/AI_CONVERSATION.md` — `ConversationEngine`'s own
  documentation, now noting its second real caller.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this freeze's Dependency Compliance section is checked
  against.
