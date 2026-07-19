# GoldBot — AI Conversation

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `ai/conversation/` (Phase 61.3,
extended Phase 63.5), real code, foundation-only — no live Telegram
handler wires either surface up yet.

## Two surfaces on the same `ConversationEngine`

```
ai/conversation/conversation_engine.py
  start_session()   Phase 61.0/61.3 -- unchanged
  ask()             Phase 61.3 -- real AIService.ask() (LLM) call, unchanged
  append()          Phase 63.5 -- deterministic, no AI call
  summarize()       Phase 63.5 -- deterministic, no AI call
  history()         Phase 63.5 -- deterministic, no AI call
  context()         Phase 63.5 -- deterministic, no AI call
  reset()           Phase 63.5 -- deterministic, no AI call
  close()           Phase 63.5 -- deterministic, no AI call
```

Per `docs/PHASE63_5_AUDIT.md`'s own finding, `ConversationEngine`
already existed as the one real Manager for Conversation before this
phase — Constitution Article 11 forbids a second, competing class for
the same concern, so Phase 63.5's deterministic surface was added as
new methods on the same, LOCKed (since Phase 61.3) class, rather than
a sibling class. `start_session()`/`ask()` are byte-for-byte
unchanged.

## Position in the Official Intelligence Pipeline

```
Knowledge → Memory → Reasoning → Conversation → Explanation → Content → Media → Broadcast
```

## Model

`ai/conversation/models.py` (Phase 63.5): `ConversationMode`
(`GENERAL`/`MARKET`/`EDUCATION`) and `ConversationContext`
(`session_id`, `telegram_id`, `mode`, `recent_messages:
Sequence[ConversationTurn]`, `knowledge_keys`, `memory_keys`,
`reasoning_keys`). No parallel `ConversationMessage`/
`ConversationSession`/`ConversationResult` class exists —
`ConversationTurn`/`ConversationState` (Phase 61.0) already cover the
first two concepts, and a primitive-only "result" wrapper was judged
unnecessary once `append()`/`reset()`/`close()` return `bool`,
`summarize()` returns `Optional[str]`, and `history()`/`context()`
return their own natural types — see `docs/PHASE63_5_AUDIT.md` for the
full naming resolution (the existing `ConversationResult` in
`conversation_engine.py`, tied to the `ask()`/LLM path, is untouched).

## Knowledge/Memory/Reasoning integration (TASK 4/5/6 — real,
type-only)

`ai/conversation/conversation_adapters.py`'s
`knowledge_key_from_entry()`, `memory_key_from_entry()`, and
`reasoning_key_from_result()` each read one upstream entry's own
already-public metadata field (`category`, `scope`, `reasoning_type`)
into a single pointer string (e.g. `"SMC:smc.bos"`) — never
`KnowledgeManager`/`MemoryRuntime`/`ReasoningRuntime`'s internal
state. These populate `ConversationContext.knowledge_keys`/
`memory_keys`/`reasoning_keys` via `ConversationEngine.context()`.

## Explanation integration (TASK 7 — interface only, no import)

`conversation_adapters.py`'s
`conversation_context_to_explanation_fields(context)` returns a plain
`dict` (`{"technical_reason": str}`, a join of `context.recent_messages`)
shaped like a subset of `ExplanationInput`'s own fields —
`ai/explanation/` is never imported anywhere in `ai/conversation/`,
because Explanation sits downstream of Conversation in the pipeline. A
future caller (not this package) would import both `ai/conversation/`
and `ai/explanation/` and bridge them.

## Real callers of `ask()` (updated Phase 65.2)

`ConversationEngine.ask()` itself is unmodified, unmoved, and its
signature unchanged (Phase 65.2's own Rule 1: no rename/move/breaking
API) — but as of Phase 65.2 it has a second real caller:
`voice/conversation_bridge.py`'s `handle_voice_turn()`, which passes
an STT-transcribed message through it as the one real, LLM-backed step
of a voice round trip. `ai/conversation/` itself required zero code
change for this — `voice/` simply calls the same public method a
future `telegram/command_router.py` text-chat caller would.

## What it is not

- Not a second LLM-calling path — the six new methods never call
  `AIService.ask()`; only the pre-existing `ask()` does.
- Not a trading decision — `ai/conversation/` is never imported by
  `core/`, `decision/`, `risk/`, `execution/`, or `strategies/`, and
  never imports any of them either (Constitution Article 3).
- Not wired into `telegram/command_router.py` or `ai/explanation/`
  this phase — foundation only.

## Related

- `docs/PHASE63_5_AUDIT.md`, `docs/PHASE63_5_FREEZE.md` — TASK 0's
  audit and the phase this extension was built in.
- `docs/PHASE65_2_AUDIT.md`, `docs/PHASE65_2_FREEZE.md`,
  `docs/ai/AI_VOICE.md` — `voice/conversation_bridge.py`'s own
  real-call integration, this package's second real caller.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline
  Conversation's position is defined by.
- `docs/ai/AI_KNOWLEDGE.md`, `docs/ai/AI_MEMORY.md`,
  `docs/ai/AI_REASONING.md` — the three upstream packages this package
  reads from.
