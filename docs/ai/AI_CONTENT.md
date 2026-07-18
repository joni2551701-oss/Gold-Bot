# GoldBot — AI Content

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `ai/content/` (Phase 61.5,
extended Phase 63.0 and Phase 63.6), real code, foundation-only — no
live Telegram handler, `translation/`, `media/`, or `broadcast/` wires
either surface up yet.

## Two surfaces on the same `ContentEngine`

```
ai/content/content_adapter.py
  generate()   Phase 61.5 -- real AIService.ask() (LLM) call, unchanged
  create()     Phase 63.6 -- deterministic, no AI call
  format()     Phase 63.6 -- deterministic, no AI call
  preview()    Phase 63.6 -- deterministic, no AI call
  validate()   Phase 63.6 -- deterministic, no AI call
  history()    Phase 63.6 -- deterministic, no AI call
```

Per `docs/PHASE63_6_AUDIT.md`'s own finding, `ContentEngine` already
existed as the one real Manager for Content before this phase —
Constitution Article 11 forbids a second, competing class for the same
concern, so Phase 63.6's deterministic surface was added as new
methods on the same, LOCKed (since Phase 61.5) class, rather than a
sibling class. `generate()`'s signature and return value are
unchanged; it gained one additive internal side-effect (recording its
own result to the new `self._history`, the same list `create()` also
appends to).

## Position in the Official Intelligence Pipeline

```
Knowledge → Memory → Reasoning → Conversation → Explanation → Content → Translation → Media → Broadcast
```

## Model

`ai/content/models.py` (Phase 63.6): `ContentMode`
(`GENERAL`/`MARKET`/`EDUCATION`) and `ContentContext` (`content_type`,
`mode`, `audience`, `tone`, `purpose`, `metadata: ContentMetadata`).
`ContentMetadata` (`category`, `language`, `priority`, `tags`) is the
one new supporting dataclass `ContentContext` embeds — not
`ContentRequest`/`ContentResult` (`content_schema.py`, Phase 61.5) or
`ContentType` (`content_types.py`, Phase 61.5/63.0), which already
existed and are reused as-is. Every field is primitive, enum, or
`ContentMetadata` itself — no `DecisionResult`, `RiskResult`, `Trade`,
`Order`, or `Position` anywhere. See `docs/PHASE63_6_AUDIT.md` for the
full Foundation Reuse Audit this model set was built from.

`ContentType` gained one additive member this phase: `TRADE_REPLAY`
(Phase 63.6 TASK 6) — the Director brief's other five named types
(`TRADE_EXPLANATION`, `MARKET_REPORT`, `EDUCATION`, `WEEKLY_OUTLOOK`,
`NEWS_SUMMARY`) each map onto a pre-existing member (`EXPLANATION`,
`MARKET_UPDATE`, `EDUCATION`, `WEEKLY_OUTLOOK`, `NEWS_ANALYSIS`
respectively) rather than being duplicated as new members.

## Explanation integration (TASK 4 — real, type-only)

`ai/content/content_adapters.py`'s
`content_context_from_explanation(output)` reads an upstream
`ExplanationOutput`'s own already-public fields (`summary`,
`language`) into a `ContentContext` — never calls `ExplanationBuilder`
or `ExplanationEngine`. `ExplanationOutput`/`ExplanationBuilder` are
unchanged.

## Conversation integration (TASK 5 — real, type-only)

`content_adapters.py`'s `content_context_from_conversation(context)`
reads an upstream `ConversationContext`'s own fields (`mode`,
`recent_messages`) into a `ContentContext` — never touches
`ConversationEngine`'s internal session state. Content may use
Conversation's context (audience/tone/purpose, expressed here as a
joined `purpose` string) but never manages Conversation's own session
lifecycle.

## What it is not

- Not a second LLM-calling path — the five new methods never call
  `AIService.ask()`; only the pre-existing `generate()` does.
- Not real AI content generation — `create()` builds a `ContentResult`
  directly from caller-supplied primitive values, never a fabricated
  or provider-generated body (Phase 63.6 TASK 7 explicitly forbids any
  GPT/Gemini/external API or image/video generation this phase).
- Not a trading decision — `ai/content/` is never imported by `core/`,
  `decision/`, `risk/`, `execution/`, or `strategies/`, and never
  imports any of them either (Constitution Article 3).
- Not Media, Translation, or Broadcast — `ai/content/` never imports
  `translation/`, `media/`, or `broadcast/` (all downstream in the
  Intelligence Dependency Principle); `ai/content/broadcast_output.py`'s
  `BroadcastReadyContent` is a locally-defined type, not an import of
  the top-level `broadcast/` package.
- Not wired into `telegram/command_router.py`, `translation/`,
  `media/`, or `broadcast/` this phase — foundation only.

## Related

- `docs/PHASE63_6_AUDIT.md`, `docs/PHASE63_6_FREEZE.md` — TASK 0's
  audit and the phase this extension was built in.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline
  Content's position is defined by.
- `docs/ai/AI_REASONING.md`, `docs/ai/AI_CONVERSATION.md` — the two
  most immediately upstream packages this package reads from.
