# GoldBot — AI Broadcast

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `broadcast/` (Phase 63.0, extended
Phase 63.8), real code, foundation-only — no live Telegram handler,
YouTube API, RTMP, or any real delivery wires this up yet.

`broadcast/` is a top-level package, a sibling of `ai/` — not
`ai/broadcast/`. See `docs/PHASE63_0_FOUNDATION_AUDIT.md` (original
decision) and `docs/PHASE63_8_AUDIT.md` (this phase's confirmation).

## Two surfaces on the same `BroadcastManager`

```
broadcast/broadcast_manager.py
  would_broadcast()     Phase 63.0 -- unchanged
  prepare()              Phase 63.0 -- unchanged (BroadcastRequest, never sent)
  create_broadcast()   Phase 63.8 -- deterministic, no external call
  validate_broadcast()   Phase 63.8 -- deterministic, no external call
  prepare_broadcast()      Phase 63.8 -- deterministic, no external call
  get_broadcast()             Phase 63.8 -- deterministic, no external call
  list_broadcasts()              Phase 63.8 -- deterministic, no external call
```

Per `docs/PHASE63_8_AUDIT.md`'s own finding, `BroadcastManager` already
existed as the one real Manager for Broadcast before this phase —
Constitution Article 11 forbade a second, competing class for the same
concern, so Phase 63.8's asset surface was added as new methods on the
same, LOCKed (since Phase 63.0) class, rather than a sibling class.
`would_broadcast()`/`prepare()` are byte-for-byte unchanged.

## Position in the Official Intelligence Pipeline

```
Knowledge → Memory → Reasoning → Conversation → Explanation → Content → Media → Broadcast
```

Broadcast is the pipeline's terminal layer this phase — nothing in
this codebase reads from `broadcast/` yet; a future, separately-
approved delivery phase would be the first caller.

## Model

`broadcast/models.py` (Phase 63.8): `BroadcastStatus`
(`DRAFT`/`READY`/`PUBLISHED`/`FAILED`/`ARCHIVED`) and `BroadcastAsset`
(`id`, `content_id`, `media_id`, `broadcast_type`, `status`,
`persona_name`, `metadata`, `created_at`) are the two genuine gaps this
phase's Foundation Reuse Audit found — `BroadcastProviderType`/
`BroadcastProviderStatus`/`BroadcastProviderDescriptor`/
`BroadcastTrigger`/`BroadcastRequest` (Phase 63.0) already existed and
are reused as-is. No `BroadcastType` enum was created — `broadcast_type`
reuses `ai.content.content_types.ContentType`, the same type
`BroadcastTrigger.content_type` already referenced; the one genuine
gap in that vocabulary, `LIVE_ANALYSIS`, was added as an additive
`ContentType` member (not a new, parallel enum).

`BroadcastProviderType` gained two additive members this phase:
`TELEGRAM`/`MINI_APP` (Phase 63.8 TASK 3) — GoldBot's own real
delivery channel and its Mini App surface, both explicitly named by
the Director this phase. `BroadcastTrigger` gained one additive
optional field, `trigger_type: BroadcastTriggerType` (defaulting to
`MANUAL`), backed by the new `BroadcastTriggerType` enum
(`MANUAL`/`SCHEDULED`/`EVENT`/`MARKET`).

## Content/Media integration (TASK 6 — real, type-only)

`broadcast/broadcast_adapter.py`'s
`broadcast_asset_from_content_and_media(content, media, manager)`
reads an upstream `ContentResult`'s and `MediaAsset`'s own
already-public fields into a `BroadcastAsset` via
`BroadcastManager.create_broadcast()` — never touches `ContentEngine`/
`MediaManager`'s internal state. An optional `persona` parameter
(type-only `ai.persona.persona.Persona` reference) populates
`BroadcastAsset.persona_name` as a free-text string — never an
embedded `Persona` object.

## Persona (Senior / Seniorita) — metadata only, no new Persona

Per this phase's own TASK 5 instruction ("Yangi persona yaratish yo'q"),
no new `Persona` object was created. `ai/persona/persona_registry.py`
still registers exactly one identity, `SENIOR_TRADING_AI`.
`BroadcastAsset.persona_name` is a free-text field — today only
`"Senior Trading AI"` maps to a real registered `Persona`; `"Seniorita"`
is a documented future label (`MARKET_UPDATE`/`WEEKLY_REPORT`/
`TRADE_REPLAY` for Senior's "Professional Analyst" style, `EDUCATION`/
`TRAINING`/`BEGINNER_GUIDE` for Seniorita's "Mentor" style) with no
backing `Persona` object — creating one is out of this phase's scope,
per the brief's own instruction.

## What it is not

- Not a second `BroadcastRequest`-producing path — the five new
  methods never build a `BroadcastRequest`; `would_broadcast()`/
  `prepare()` remain the only path that does.
- Not real delivery — no YouTube API, Telegram API, RTMP, stream
  server, voice provider, or video hosting call anywhere in this
  package (Rule 4). `BroadcastManager` has no `send()`/`publish()`/
  `deliver()` method at all.
- Not a trading decision — `broadcast/` is never imported by `core/`,
  `decision/`, `risk/`, `execution/`, `strategies/`, or `signals/`,
  and never imports any of them either (Constitution Article 3 / Rule 1).
- Not wired into `telegram/owner/broadcast_commands.py` this phase —
  those commands still report `NOT IMPLEMENTED` (Phase 63.0 TASK 7).
- Not a second "BroadcastReady" contract — `broadcast_adapter.py`'s
  output *is* `BroadcastAsset`; `ai.content.broadcast_output.BroadcastReadyContent`/
  `prepare_broadcast()` (Phase 61.5) remain untouched, a separate,
  narrower Content-only path.

## Related

- `docs/PHASE63_8_AUDIT.md`, `docs/PHASE63_8_FREEZE.md` — TASK 0's
  audit and the phase this extension was built in.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline
  Broadcast's position is defined by.
- `docs/ai/AI_MEDIA.md`, `docs/ai/AI_CONTENT.md` — the two most
  immediately upstream packages this package reads from.
