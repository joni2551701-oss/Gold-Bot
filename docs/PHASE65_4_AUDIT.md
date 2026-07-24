# Phase 65.4 Audit — Personal AI Runtime Integration

TASK 0's Foundation Reuse Audit (Constitution Article 11), run before
any Phase 65.4 code was written. Governed by
`docs/constitution/CONSTITUTION.md` and the Phase 65.4 Worker Brief's
own Rule 1 (LOCK: `assistant/`, `voice/`, `knowledge/`, `ai/memory/`,
`ai/reasoning/`, `ai/conversation/`, `ai/explanation/`, `ai/content/`,
`media/`, `broadcast/`) and Rule 3 (no new Foundation package).

## Scope of this audit

Phase 65.3 built `assistant/` as a Foundation that deliberately imports
nothing downstream (Knowledge/Memory/Reasoning/Conversation/Voice all
excluded by design — see `docs/PHASE65_3_AUDIT.md`'s own resolution).
This phase's entire purpose is the opposite: connect that Foundation
to the real, already-existing Runtimes via their public APIs. TASK 0
checks four things named in the brief: does a Runtime already exist
for Assistant? Does a composition already exist? Does an adapter
already exist? Is a duplicate needed anywhere?

## Question 1 — Does an Assistant Runtime already exist?

**No.** `assistant/assistant_manager.py`'s `AssistantManager` (Phase
65.3) owns `AssistantProfile` (durable per-user settings) but has no
concept of a live session — no `session_id`, no `started_at`/
`updated_at`, no `active` flag, no `conversation_id` pointer. This is
a genuine gap, matching the brief's own TASK 8 (`AssistantRuntime`)
almost field-for-field. `ai/session/session_manager.py`'s
`SessionManager`/`ConversationState` and `voice/session/manager.py`'s
`VoiceSessionManager`/`VoiceSession` are both structurally close
precedents (in-memory create/get/end, no persistence) but track
different resources (a conversation's turn history; a voice call's
profile/language selection) — reusing either by import would collapse
two different concerns into one, the same distinction Phase 65.2's own
audit already drew between `VoiceSession` and `ConversationState`. The
correct move, per Article 11 step 2 ("can an existing module be
extended"), is answered by TASK 1 itself: extend the existing
`AssistantManager` with runtime-lifecycle methods rather than creating
a new `AssistantRuntimeManager` class. `AssistantRuntime` itself is a
new dataclass in the already-existing `assistant/models.py` (extension
of a file, not a new module).

## Question 2 — Does a composition (real cross-layer call) already exist?

**Yes, twice, and neither is Assistant-scoped.** `ai/intelligence_runtime.py`'s
`IntelligenceRuntime.run(topic, telegram_id)` is the first composition
root (Phase 64.0) — deterministic only, walks Knowledge → Memory →
Reasoning → Conversation (via `append()`, never `ask()`) → Explanation
→ Content → Media → Broadcast, and is directly reusable as-is for
TASK 5/6 (Reasoning + Pipeline Integration) with zero modification.
`voice/conversation_bridge.py`'s `handle_voice_turn()` is the second
(Phase 65.2) — the real, LLM-backed round trip, but its own entry
point requires raw audio bytes (STT input) and a `VoiceSession`; this
phase's brief names only text-based `ConversationEngine.ask()` and
`VoiceRuntime.generate_audio()`/`generate_with_fallback()` as the
methods to use (TASK 2/3), never STT. Reusing
`handle_voice_turn()` by importing it would require fabricating a
`VoiceSession` and dummy audio bytes to satisfy a signature this phase
doesn't need — a worse fit than composing `ConversationEngine.ask()`
and `VoiceRuntime.generate_audio()` directly, which is exactly what
TASK 2/3's own brief text specifies. No third composition-root
*duplicate* is created — `assistant/runtime_adapter.py` (TASK 9) is a
new, Assistant-scoped composition, structurally parallel to (not a
copy of) the existing two, calling each real Runtime's already-public
methods and adding no new business logic of its own (same "zero new
business logic in any of the systems it composes" posture
`voice/conversation_bridge.py` already established).

## Question 3 — Does an adapter already exist?

**Yes, one, and it is now extended one file further.**
`assistant/conversation_adapter.py` (Phase 65.3) already produces
primitive-shaped params matching `VoiceSessionManager.create_session()`/
`ConversationEngine.start_session()`'s signatures, plus a Memory
scope-key helper. This phase's `assistant/runtime_adapter.py` is a
**new file**, not a modification of `conversation_adapter.py` — Rule 1
LOCKs `assistant/` itself (no rename/move/breaking API), and
`conversation_adapter.py`'s three existing pure functions keep their
exact signatures, unchanged. `runtime_adapter.py` *calls*
`conversation_adapter.py`'s functions internally (to build the params)
and then performs the real cross-package calls Phase 65.3 deliberately
never did. This is the same "extend by adding a new file inside the
existing package, not a new top-level package" resolution the brief's
own Rule 3 requires.

## Question 4 — Is any duplicate needed?

**No.** No second `AssistantManager`, no second `ConversationEngine`,
no second `VoiceRuntime`, no second `MemoryRuntime`, no second
`ReasoningRuntime`, no second `IntelligenceRuntime`. Every one of these
six classes is called via its existing, unmodified public API only:

| Class | Method(s) called | Unmodified? |
|---|---|---|
| `ConversationEngine` | `start_session()`, `ask()` | Yes |
| `VoiceRuntime` | `generate_audio()`, `generate_with_fallback()` | Yes |
| `MemoryRuntime` | `store()`, `recall()` | Yes |
| `ReasoningRuntime` | *(none directly — reached only via `IntelligenceRuntime.run()`, which already composes it)* | Yes |
| `IntelligenceRuntime` | `run()` | Yes |
| `AssistantManager` | extended in place with 5 new methods | Extended, not duplicated |

## The one deliberate widening: `assistant/runtime_adapter.py`'s imports

Phase 65.3's own isolation test
(`test_assistant_package_never_imports_downstream_intelligence_layers`)
forbade `voice/`, `ai.conversation/`, `ai.memory/`, `ai.reasoning/`,
`ai.explanation/`, `ai.persona/`, `knowledge/`, `ai.content/`,
`media/`, `broadcast/`, `translation/` anywhere in `assistant/`, with
zero exemptions. This phase's own brief explicitly authorizes crossing
that boundary for real integration (TASK 2/3/4/6's own named method
calls cannot be satisfied any other way). The resolution mirrors
`voice/conversation_bridge.py`'s own precedent exactly:
`assistant/runtime_adapter.py` becomes the **one** file in `assistant/`
permitted to import `ai.conversation.conversation_engine`,
`ai.intelligence_runtime`, `ai.memory.memory_runtime`/`ai.memory.models`,
and `voice.runtime`/`voice.models` — every other file in `assistant/`
(`identity.py`, `identity_registry.py`, `identity_manager.py`,
`models.py`, `access.py`, `assistant_manager.py`,
`conversation_adapter.py`) keeps the exact zero-downstream-import
posture Phase 65.3 established, unchanged. The updated isolation test
(`tests/assistant/runtime/test_runtime_isolation.py`) enforces this
confinement mechanically, the same AST-sweep pattern
`tests/voice/test_voice_isolation.py`'s own
`test_conversation_engine_real_call_confined_to_conversation_bridge`
already uses.

## Conclusion

One genuine gap confirmed (`AssistantRuntime`, a session-lifecycle
model with no existing counterpart); one existing class extended in
place (`AssistantManager`, +5 methods); one new file added inside the
existing `assistant/` package (`runtime_adapter.py`, the third
composition-root-shaped file in this codebase, after
`ai/intelligence_runtime.py` and `voice/conversation_bridge.py`); zero
duplicate Managers/Runtimes/Engines; zero new top-level packages; zero
changes to any of the ten Rule-1-LOCKed packages' own files (they are
called, never edited).

## Related documents

- `docs/PHASE65_3_AUDIT.md`, `docs/PHASE65_3_FREEZE.md` — the prior
  phase's own Foundation this phase connects.
- `docs/PHASE64_0_AUDIT.md` — `IntelligenceRuntime`'s own composition-
  root precedent, reused as-is via TASK 6.
- `docs/PHASE65_2_AUDIT.md` — `voice/conversation_bridge.py`'s own
  composition-root precedent, the structural pattern this phase's
  `runtime_adapter.py` follows without importing or calling it.
- `docs/ai/AI_PERSONAL_ASSISTANT.md` — updated with this phase's real
  integration surface.
