# Phase 63.5 — AI Conversation Intelligence Foundation: TASK 0 Audit

Per Constitution Article 11 (Foundation Reuse Law): every Worker
Brief's TASK 0 answers, for the capability about to be built —
Foundation / Runtime / Manager / Registry / Model / Contract /
Capability — does it already exist? This audit answers that for
Conversation before any code is written.

## Foundation Reuse Audit

| Component | Exists? | Real file(s) |
|---|---|---|
| Conversation Foundation | ✅ Yes | `ai/conversation/conversation_engine.py` (`ConversationEngine`, Phase 61.3 TASK 5), built on `ai/session/` (`SessionManager`, `ConversationState`, `ConversationTurn`, `ContextWindow`, Phase 61.0 TASK 7) |
| Conversation Manager/Runtime | ✅ Yes — narrower shape than this brief's ask, see finding below | `ConversationEngine`: `start_session()`, `ask()` (the latter a real `AIService.ask()` call — an LLM path) |
| Conversation Registry | ➖ Not applicable | No static catalog concept applies to Conversation the way it does to Knowledge/Memory/Reasoning categories — sessions are runtime state, not a fixed enum of named types. No registry is created this phase. |
| Conversation Contract/Model | ✅ Partial | `ConversationTurn` (`role`, `content`, `at` — matches the brief's `ConversationMessage`), `ConversationState` (`session_id`, `telegram_id`, `created_at`, `turns`, `last_activity` — matches the brief's `ConversationSession`), `ConversationResult` (`session_id`, `response: RuntimeResponse` — **not** primitive-only, see finding below) |
| Conversation Capability | ✅ Yes | `Capability.CHAT` already exists and already has a real `AIService.ask()` mapping (used by `ConversationEngine.ask()`) |
| `ai/reasoning/` (integration source, upstream) | ✅ Yes | `ReasoningResult`/`ReasoningType`/`ReasoningPriority` (Phase 63.4) — type-only reference, untouched |
| `ai/memory/` (integration source, upstream) | ✅ Yes | `MemoryEntry`/`MemoryScope`/`MemoryType` (Phase 63.3) — type-only reference, untouched |
| `knowledge/` (integration source, upstream) | ✅ Yes | `KnowledgeEntry`/`KnowledgeCategory` (Phase 61.3/63.2) — type-only reference, untouched |
| `ai/explanation/` (integration target, downstream) | ✅ Yes | `ExplanationBuilder`/`ExplanationInput` (Phase 63.1) — **not imported**, Intelligence Dependency Principle |

**Rule applied**: unlike Phase 63.4 (where every answer was "no," the
one legitimate case for building fresh), Conversation's Foundation and
Manager both already exist — matching Phase 63.2/63.3's shape. Per
Article 11 and this brief's own Director Notes item 3 ("agar Foundation
mavjud bo'lsa, yangi parallel modul yaratish taqiqlanadi"), no new
top-level package, no new competing Manager/Runtime class. Everything
this phase adds is either a new file inside the existing
`ai/conversation/` package or an additive extension to the existing,
LOCKed `ConversationEngine`/`ConversationState` classes.

## Critical finding — `ConversationEngine` already exists; extend, do
not duplicate

`ConversationEngine.ask()` is a **real, LLM-calling path** (`AIService.ask()`
with `Capability.CHAT`) — a materially different mechanism from this
brief's TASK 3 ask (`start`/`append`/`summarize`/`history`/`context`/
`reset`/`close`, explicitly "Deterministic. Real AI inference yo'q.").
This is the same shape of finding Phase 63.1 made for
`ExplanationEngine` (real `AIService.ask()`) vs. the new, deterministic
`ExplanationBuilder` — but this brief's own Director Notes item 3
explicitly forbids the resolution Phase 63.1 used (a second, sibling
class). Resolution here instead: **extend `ConversationEngine` itself**
with six new, purely deterministic methods, alongside its completely
unchanged `start_session()`/`ask()` (Article 9 — LOCKed since Phase
61.3, additive-only). No second class is created anywhere in
`ai/conversation/`.

Method-by-method mapping against the brief's TASK 3 list:

| Brief's name | Resolution |
|---|---|
| `start()` | Already covered by the existing `start_session(telegram_id) -> ConversationState` — no new method added; using the existing name avoids a needless alias, the same "don't duplicate a name that already means the same thing" resolution `docs/PHASE63_2_AUDIT.md` applied to `KnowledgeItem`/`KnowledgeEntry`. |
| `append()` | **New** — `ConversationEngine.append(session_id, role, content) -> bool`. Calls `ConversationState.add_turn()` (existing, unchanged) directly, never `AIService.ask()` — the deterministic counterpart to `ask()`. |
| `summarize()` | **New** — `ConversationEngine.summarize(session_id) -> Optional[str]`. A string join over stored turns, same posture `ai/reasoning/reasoning_runtime.py`'s `summarize()` already established in Phase 63.4. |
| `history()` | **New** — `ConversationEngine.history(session_id) -> Sequence[ConversationTurn]`. Wraps the existing `ConversationState.history()`. |
| `context()` | **New** — `ConversationEngine.context(session_id, mode, knowledge_keys, memory_keys, reasoning_keys) -> Optional[ConversationContext]`. Assembles the new `ConversationContext` model (TASK 2) from already-stored turns plus caller-supplied upstream-layer key pointers. |
| `reset()` | **New** — `ConversationEngine.reset(session_id) -> bool`. Calls a new, additive `ConversationState.clear_turns()` method (Article 9 — a new method on a LOCKed class, not a signature change) — clears turn history, keeps the session alive. |
| `close()` | **New** — `ConversationEngine.close(session_id) -> bool`. Wraps the existing `SessionManager.end_session()`. |

## TASK 2's models — reuse mapping and one genuine naming collision

- **`ConversationMessage`** — conceptually identical to the existing
  `ConversationTurn` (`role`, `content`, `at`). No parallel class
  created; `ConversationContext.recent_messages` (below) is typed
  `Sequence[ConversationTurn]` directly.
- **`ConversationSession`** — conceptually identical to the existing
  `ConversationState`. No parallel class created.
- **`ConversationContext`** — genuine gap, created new
  (`ai/conversation/models.py`): `session_id: str`, `telegram_id: str`,
  `mode: ConversationMode`, `recent_messages: Sequence[ConversationTurn]`,
  `knowledge_keys: Sequence[str]`, `memory_keys: Sequence[str]`,
  `reasoning_keys: Sequence[str]`. Every field is primitive, enum, or
  the already-existing, already-primitive `ConversationTurn` — no
  `DecisionResult`/`RiskResult`/`Trade`/`Position`/`Order` anywhere.
- **`ConversationMode`** — genuine gap, created new (`GENERAL`/
  `MARKET`/`EDUCATION`, mirroring `ai/reasoning/models.py`'s
  `ReasoningMode` shape exactly).
- **`ConversationResult`** — **name collision, not a functional gap.**
  `ai/conversation/conversation_engine.py` already defines a
  `ConversationResult` (`session_id`, `response: RuntimeResponse`),
  LOCKed since Phase 61.3, and it is **not** primitive-only (it carries
  a `RuntimeResponse`). This brief's TASK 2 wants a primitive-only
  result shape. Resolution: no second `ConversationResult` class is
  created under any name — `append()`/`reset()`/`close()` return a
  plain `bool`, `summarize()` returns `Optional[str]`, `history()`
  returns `Sequence[ConversationTurn]`, `context()` returns
  `Optional[ConversationContext]`. Each already-natural return type
  fully covers what a wrapping "result" object would have, without
  reusing a name that already means something different in the same
  package (the same discipline `docs/PHASE63_3_AUDIT.md` applied when
  it chose `forget()` over reusing the already-taken `clear()` name).

## TASK 4/5/6 integration — type-only, metadata only

`ai/conversation/conversation_adapters.py` (new file, mirroring Phase
63.4's `ai/reasoning/reasoning_adapters.py` exactly) adds three pure
functions reading an upstream entry's own metadata field into a single
pointer string, never touching that package's Manager/Runtime
internals:

- `knowledge_key_from_entry(entry: KnowledgeEntry) -> str` — reads
  `category`/`key`.
- `memory_key_from_entry(entry: MemoryEntry) -> str` — reads
  `scope`/`key`.
- `reasoning_key_from_result(result: ReasoningResult) -> str` — reads
  `reasoning_type`/`key`.

These populate `ConversationContext.knowledge_keys`/`memory_keys`/
`reasoning_keys`. `KnowledgeManager`, `MemoryRuntime`, and
`ReasoningRuntime` are never imported by `ai/conversation/` — only
their already-public dataclass types.

## TASK 7 — Explanation interface (downstream, no import)

`conversation_adapters.py`'s
`conversation_context_to_explanation_fields(context)` returns a plain
`dict` (`{"technical_reason": str}`, a join of `recent_messages`) shaped
like a subset of `ExplanationInput`'s own fields — `ai/explanation/` is
never imported anywhere in `ai/conversation/`, since Explanation sits
downstream of Conversation in the Official Intelligence Pipeline. Same
resolution Phase 63.4 already used for its own TASK 6.

## Requesting no Director Decision

No Constitution Article conflict was found. This phase's own Director
Notes item 3 pre-empted the one design question that would otherwise
have needed a pause (whether a second Conversation class is
permitted) — it explicitly is not, so `ConversationEngine` is extended
in place. TASK 1 through TASK 11 proceed without a pause.

## Related

- `docs/constitution/CONSTITUTION.md` Article 3, 9, 11, 12.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this audit's TASK 7 finding is checked against.
- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — where `ConversationEngine`
  was LOCKed.
- `docs/PHASE63_3_AUDIT.md`, `docs/PHASE63_4_AUDIT.md` — the two prior
  audits whose naming-collision and extend-vs-duplicate resolutions
  this document's own findings follow.
