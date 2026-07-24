# Phase 63.0 — Senior Trading AI Foundation: Audit

**TASK 0.** Mandatory reading completed
(`docs/constitution/CONSTITUTION.md`, `docs/architecture/*`,
`docs/roadmap/*`, `docs/ai/*`, `docs/owner/*`) before any code change,
per this phase's own rule and the Constitution's mandatory reading
order.

## What already exists — real, not assumed

The brief's TASK 1–8 describe several packages as brand new. A direct
`ls` audit of `ai/`, `content/`, `broadcast/`, `knowledge/`,
`telegram/owner/` before writing anything found two areas where the
brief's assumption does not match the real repository:

### `content/` — already exists, as `ai/content/` (Phase 61.5 TASK 5/6)

Not a top-level package — `ai/content/`:
- `content_types.py` — `CONTENT_CAPABILITIES` (a `FrozenSet[Capability]`,
  not a second parallel enum), `is_content_capability()`,
  `content_title()`.
- `content_schema.py` — `ContentRequest`/`ContentResult`, composing
  `Capability`/`AIContext`/`AIRole` (no re-declaration).
- `content_adapter.py` — `ContentEngine.generate()`, wraps
  `AIService.ask()` unmodified.
- `broadcast_output.py` — `BroadcastReadyContent`/`prepare_broadcast()`,
  explicitly documented as "the interface boundary between 'AI
  generated this content' and 'a future layer sends it somewhere'"
  and explicitly deferred broadcast delivery to "a future v0.5 Product
  Media Layer / Phase 62.x Owner Broadcast Foundation" — i.e. this
  exact phase.

**Decision (Module Reuse Principle, step 2 — "can an existing module
be extended?"): yes.** TASK 2 extends `ai/content/content_types.py`'s
`CONTENT_CAPABILITIES` vocabulary in place rather than creating a
second, parallel top-level `content/` package with its own
`models.py`/`content_manager.py`/`content_registry.py`/
`content_types.py`. Creating a duplicate would violate Article 7
("Does this already exist somewhere in the repo?" → yes) and would
give the codebase two competing content-request/result shapes.

### `broadcast/` — does not exist yet, correctly a new top-level package

`ai/content/broadcast_output.py` is a narrow *adapter* (one function,
one dataclass) — not a provider/trigger/delivery manager. Nothing
today manages broadcast providers (YouTube/OBS/RTMP/etc.), delivery
triggers, or Owner enable/disable state. Module Reuse steps 1/2 are
both "no" here: no existing module owns this responsibility, and
`ai/content/broadcast_output.py` cannot be extended into it without
turning a narrow AI-content adapter into a channel-management system
— a different, correctly top-level concern (the same reasoning that
keeps `execution/` a top-level package distinct from `decision/`,
per `docs/architecture/ARCHITECTURE_MASTER.md`). **Decision: TASK 4
creates `broadcast/` as a new top-level package**, and it imports
`ai.content.broadcast_output.BroadcastReadyContent` as its input type
rather than re-declaring a content shape.

### Everything else the brief names — confirmed genuinely absent

- `ai/persona/` — does not exist. TASK 1 is genuine new work.
- `media/` (top-level) — does not exist. TASK 5 is genuine new work.
- `translation/` (top-level) — does not exist. TASK 6 is genuine new
  work.
- `telegram/owner/broadcast_commands.py` — does not exist. TASK 7 is
  genuine new work.
- `Capability.AI_CONTENT`/`AI_MEDIA`/`AI_TRANSLATION`/`AI_BROADCAST` —
  none of the four exist on the enum yet (current members: `CHAT`,
  `ANALYSIS`, `EXPLANATION`, `SUMMARY`, `MEMORY`, `EDUCATION`,
  `TOOL_CALLING`, `VISION`, `IMAGE`, `VIDEO`, `VOICE`, `DOCUMENT`,
  `AI_MARKET_REPORT`, `AI_WEEKLY_OUTLOOK`, `AI_NEWS_ANALYSIS`,
  `AI_SCRIPT_GENERATION`). TASK 8 is genuine new work — additive only,
  same pattern the four `AI_*` content members already used in Phase
  61.5 (OWNER/ADMIN gain access automatically via
  `frozenset(Capability)`; VIP/PREMIUM/FREE do not until explicitly
  opted in).
- `ai/explanation/` currently has only `explanation_engine.py` — no
  `ExplanationOutput` model. TASK 3 is genuine new work, additive to
  the existing package (no new file needed beyond one new model file
  or an addition to the existing module — see TASK 3 for the exact
  placement decision).
- `knowledge/` (top-level, sibling of `ai/`, confirmed in Phase 62.0's
  own audit) has `examples.py`/`faq.py`/`models.py`/`psychology.py`/
  `registry.py`/`risk.py`/`smc.py`/`wyckoff.py` — pure trading-education
  content, unrelated to this phase's persona/content/broadcast/media/
  translation scope. No overlap, nothing to reuse from or extend here.

## Constitution compliance

- Article 1 (Core Principle): every new module this phase is
  contract-only or foundation-only — no module calls `AIService.ask()`
  to actually produce content, no module writes to Telegram, no module
  touches `decision/`/`risk/`/`execution/`. Verified per-task below.
- Article 2/3 (Dependency Law / Import Rules): `broadcast/`, `media/`,
  `translation/` (new top-level packages) may depend on `ai/`'s already
  public types (`ContentResult`, `BroadcastReadyContent`) and `core/`;
  they must never be imported by `decision/`/`risk/`/`execution/`, and
  `ai/persona/` must never import `decision/`/`risk/`/`execution/`.
  Re-verified via grep sweep at the close of this phase (Final
  Constitution Audit).
- Article 7 (Reuse Principle): applied above for `content/`/`broadcast/`;
  every other new package passed both "does this exist?" (no) and
  "can an existing module be extended?" (no — each is a genuinely new
  responsibility) before being created.

## Plan for this phase

TASK 1 (`ai/persona/`), TASK 3 (extend `ai/explanation/`), TASK 4
(`broadcast/`), TASK 5 (`media/`), TASK 6 (`translation/`), TASK 7
(`telegram/owner/broadcast_commands.py`), TASK 8 (4 new `Capability`
members) proceed as new work. TASK 2 extends `ai/content/content_types.py`
in place instead of creating a duplicate top-level `content/` package.
