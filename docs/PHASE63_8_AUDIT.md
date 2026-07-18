# Phase 63.8 — AI Broadcast Intelligence Foundation: Audit

TASK 0. Mandatory reading completed (`docs/constitution/CONSTITUTION.md`,
`docs/policies/DIRECTOR_POLICY.md`, `docs/architecture/*`,
`docs/roadmap/*`, `docs/ai/*`) before any code change, per this
phase's own Rule 2.

## Foundation Reuse Audit (Rule 2's own required table)

`broadcast/` already exists — a real, non-trivial Foundation built in
Phase 63.0 TASK 4, not the empty package this brief's phrasing ("Agar
mavjud bo'lmasa yaratish") anticipates as the likely case:

| Component | Real state | Decision |
|---|---|---|
| Foundation | ✅ `broadcast/` (Phase 63.0 TASK 4) | Extend in place — Rule 5 itself already names this as the priority check |
| Manager | ✅ `BroadcastManager` (`would_broadcast()`/`prepare()`, composes `BroadcastProviderManager`+`BroadcastTriggerManager`) | Extend with `create_broadcast()`/`validate_broadcast()`/`prepare_broadcast()`/`get_broadcast()`/`list_broadcasts()` (TASK 2) — no second Manager |
| Model | ➖ Partial — `BroadcastProviderType`/`BroadcastProviderStatus`/`BroadcastProviderDescriptor`/`BroadcastTrigger`/`BroadcastRequest` exist. ❌ No lifecycle status, no per-item tracked object | `BroadcastStatus` and `BroadcastAsset` are the two genuine gaps (TASK 1) |
| Contract | ✅ `BroadcastRequest` (the shape a future delivery layer consumes) | Reused as-is — `BroadcastAsset` (new) is a distinct, lifecycle-tracked contract, not a duplicate |
| Registry | ✅ `build_broadcast_provider_registry()` (six `BroadcastProviderType` entries: YOUTUBE/OBS/RTMP/TWITCH/KICK/CUSTOM) | Extend the enum with two genuine gaps (`TELEGRAM`, `MINI_APP`); see naming resolution below |
| Capability | ✅ `Capability.AI_BROADCAST` (Phase 63.0 TASK 8), already in `ai/router/routing_rules.py`'s provider-preference table | Reused as-is, no new capability |
| Provider | ✅ `BroadcastProviderManager` (`list_providers()`/`descriptor_of()`/`status_of()`/`set_status()`/`is_enabled()`) — this **is** TASK 3's "Provider Layer," already built | No second provider manager; TASK 3 satisfied by the registry extension above |

## TASK 1's `BroadcastType` naming resolution

The brief's `BroadcastType` (`MARKET_UPDATE`/`WEEKLY_REPORT`/
`TRADE_REPLAY`/`EDUCATION`/`LIVE_ANALYSIS`) is not a new, parallel
enum — `BroadcastTrigger.content_type: ContentType` (Phase 63.0) has
already tied broadcast triggers to `ai.content.content_types.ContentType`
directly, and a second "BroadcastType" enum covering the same
vocabulary would violate Article 11 the moment it is compared against
`ContentType`, exactly like Phase 63.6's own `ContentType`-vs-brief's-
`ContentType` mapping exercise:

| Brief's `BroadcastType` | Real `ContentType` member |
|---|---|
| `MARKET_UPDATE` | `MARKET_UPDATE` (exact) |
| `WEEKLY_REPORT` | `WEEKLY_OUTLOOK` |
| `TRADE_REPLAY` | `TRADE_REPLAY` (exact, added Phase 63.6) |
| `EDUCATION` | `EDUCATION` (exact) |
| `LIVE_ANALYSIS` | genuine gap — no existing member covers a live/real-time analysis session |

`LIVE_ANALYSIS` is added as one new, additive `ContentType` member
(Article 9 — LOCKed since Phase 63.0, extended 63.6, additive-only),
the same resolution shape Phase 63.6 used for `TRADE_REPLAY`. No new
`BroadcastType` enum is created.

## TASK 3's provider naming resolution

The brief's example provider types (`TELEGRAM`/`YOUTUBE`/`MINI_APP`/
`LIVE`) partially overlap the existing `BroadcastProviderType`
(`YOUTUBE`/`OBS`/`RTMP`/`TWITCH`/`KICK`/`CUSTOM`):

- `YOUTUBE` — exact match, reused.
- `LIVE` — overlaps conceptually with the existing `OBS`/`RTMP`/
  `TWITCH`/`KICK` members, all of which are already real-time/live
  streaming channel types; no new member added (naming difference,
  not a functional gap).
- `TELEGRAM` — genuine gap. GoldBot is itself a Telegram bot
  (`docs/telegram/TELEGRAM_ARCHITECTURE.md`) and the Director's own
  message this phase named Telegram first among future delivery
  channels — added as a new, additive `BroadcastProviderType` member.
- `MINI_APP` — genuine gap, also explicitly named by the Director this
  phase — added as a new, additive member.

## TASK 4's Trigger naming resolution

`BroadcastTriggerManager`/`BroadcastTrigger` (Phase 63.0) already
model *armed/disarmed* intent per `ContentType`, but carry no
`MANUAL`/`SCHEDULED`/`EVENT`/`MARKET` categorization — a genuine gap.
`BroadcastTriggerType` is added as a new enum in `broadcast/models.py`,
and `BroadcastTrigger` gains one new optional field,
`trigger_type: BroadcastTriggerType = BroadcastTriggerType.MANUAL`
(Article 9 — LOCKed since Phase 63.0, additive-only: a new optional
field with a safe default, the same shape `ExplanationOutput` used in
Phase 63.1). `register()`/`get()`/`is_armed()`/`all()` are unchanged.

## TASK 5's Persona resolution — no new Persona created

`ai/persona/persona_registry.py`'s `build_persona_registry()` returns
exactly one entry: `SENIOR_TRADING_AI`. **No "Seniorita" `Persona`
object exists anywhere in the codebase.** The brief's own TASK 5 is
explicit: "Yangi persona yaratish yo'q" (no new persona is created) —
so this phase does not add one. Resolution: `broadcast/`'s new model
(`BroadcastAsset`) carries persona identity as a free-text
`persona_name: Optional[str]` field — never an embedded `Persona`
object, the same "never carry another package's object graph"
convention `ai/conversation/models.py`'s `ConversationContext` and
`ai/content/models.py`'s `ContentContext` already established.
`broadcast/broadcast_adapter.py` (TASK 6) reads an optional, upstream
`ai.persona.persona.Persona`'s own already-public `.name` field
type-only (never `PersonaManager`'s internal state) to populate it.
Today only `"Senior Trading AI"` maps to a real registered `Persona`;
`"Seniorita"` remains a documented future label with no backing
object — creating it is explicitly out of this phase's scope per the
brief's own instruction, and would require a separate, dedicated
`ai/persona/` Worker Brief.

## TASK 6's "BroadcastReady" resolution — reuses `BroadcastAsset`, does not duplicate `BroadcastReadyContent`

`ai/content/broadcast_output.py`'s `BroadcastReadyContent`/
`prepare_broadcast()` (Phase 61.5, LOCKed, flagged again in
`docs/PHASE63_6_AUDIT.md`/`docs/PHASE63_7_AUDIT.md`) already produces
"the one shape a future broadcast layer would receive" — but only from
a `ContentResult`, with no `MediaAsset` or persona reference. The
brief's TASK 6 wants a combined `ContentResult + MediaAsset + Persona
→ BroadcastReady` adapter. Rather than declare a second, competing
"BroadcastReady" dataclass, `broadcast/broadcast_adapter.py`'s new
function builds a `BroadcastAsset` (TASK 1's own model) directly — the
tracked, lifecycle-aware object this phase's `BroadcastManager`
extension already operates on. `BroadcastReadyContent`/
`prepare_broadcast()` are not modified and continue to exist as the
narrower Content-only path; a future Broadcast delivery phase decides
which of the two paths (or both) it reads from — not resolved here,
out of this phase's scope, exactly as `docs/PHASE63_7_AUDIT.md`
already flagged for its own future audit's attention.

## Dependency Compliance (Rule 3)

`broadcast/*.py` today imports only `ai.content.broadcast_output`,
`ai.content.content_types`, other `broadcast.*` modules, and
`core.logger` — zero dependency on `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, or `database/`. This phase adds one new,
type-only import: `media.models.MediaAsset` (media sits immediately
upstream of broadcast in the Official Intelligence Pipeline) and
`ai.persona.persona.Persona` (type-only, per Rule 3's explicit "Broadcast
o'qishi mumkin: media, content, ai" allowance). `broadcast/` continues
to never import `decision/`, `risk/`, `execution/`, `strategies/`,
`signals/`, or `database/` — TASK 7's isolation test enforces this
permanently.

## Trading Core Isolation

`git diff --stat -- core/ decision/ risk/ execution/ strategies/
signals/` — zero output before any change this phase.

## Conclusion

No Constitution Article conflict. TASK 1 (`BroadcastStatus`/
`BroadcastAsset` model, `LIVE_ANALYSIS` `ContentType` member), TASK 2
(`BroadcastManager` extended with the five deterministic asset
methods), TASK 3 (`TELEGRAM`/`MINI_APP` added to the existing
`BroadcastProviderType`), TASK 4 (`BroadcastTriggerType` +
`BroadcastTrigger.trigger_type`), and TASK 6
(`broadcast/broadcast_adapter.py`) are the genuine pieces of new/
extended work this phase does — all inside the real, existing
`broadcast/` package. Requesting no Director Decision.
