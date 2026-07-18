# GoldBot — Vision

Governed by `docs/constitution/CONSTITUTION.md` Article 1. This
document answers one question: **what platform is GoldBot becoming?**
`docs/roadmap/VERSIONS.md` answers *when* each piece arrives and what
is actually built today; this document never makes that claim — it is
the destination, not the map.

## GoldBot is not a simple trading bot

Three platforms, one AI Core, one shared Context:

```
              Senior Trading AI
                  AI Core
        ┌───────────────────────┐
        │  Trading Intelligence  │
        │  (Market Data, Context,│
        │   Decision, Risk,      │
        │   Execution)           │
        └───────────────────────┘
        ┌───────────────────────┐
        │  Market Media          │
        │  Intelligence           │
        │  (Weekly Outlook,       │
        │   Education, Market     │
        │   Room, Trade Replay,   │
        │   Voice, Video,         │
        │   Broadcast)            │
        └───────────────────────┘
        ┌───────────────────────┐
        │  User Platform          │
        │  Intelligence            │
        │  (Owner Control,         │
        │   Subscription,          │
        │   Product Surfaces)      │
        └───────────────────────┘
```

## Trading Intelligence

Market Data → Context → Decision → Risk → Execution. Deterministic,
rule-based, fully auditable — Constitution Article 1's Core Principle.
This platform never changes shape based on what the AI or Media
platforms need; it is the one thing every other platform explains,
never influences.

## AI Core

Knowledge → Memory → Reasoning → Conversation → Explanation → Content
→ Translation → Media → Broadcast — the official Intelligence Pipeline
as of Phase 63.3 (see `docs/roadmap/AI_EVOLUTION.md`'s Stage
definitions for the phase-by-phase build order this vision maps to).
The connective layer both other platforms draw on — Trading
Intelligence's decisions become explainable through it; Market Media
Intelligence's content draws on the same Persona, Memory, and
Knowledge. One AI Core, not two competing ones. Explanation is a
*position* in this chain, not a standalone module — it is what
Knowledge + Memory + Reasoning + Conversation produce together, never
a decision-maker of its own (Constitution Article 1).

## Market Media Intelligence

Weekly Outlook, Education, Market Room, Trade Replay — today,
foundation/contract-only (`ai/persona/`, `ai/content/`, `broadcast/`,
`media/`, `translation/`, Phase 63.0). Voice, Video, and live Broadcast
are named here as destination, not as work in progress — see
`docs/roadmap/AI_EVOLUTION.md`'s "AI Media Intelligence Platform"
section for the detailed vision, and `docs/policies/BROADCAST_POLICY.md`
for what explicitly does not exist yet.

## User Platform Intelligence

Owner Control Center, subscription/product surfaces
(`telegram/`, `telegram/owner/`) — where a human, Owner or user,
actually touches any of the above.

## What never changes, regardless of how far this vision goes

Constitution Article 1: **AI yordam beradi. AI qaror bermaydi.** Every
platform above, at every stage of this vision, explains what Trading
Intelligence already decided. None of them ever vote, approve, or
execute. A future proposal to change this is not an evolution of this
vision — it is a Constitutional Amendment, requiring the explicit,
dedicated Director process Article 1 and the Amendment section
describe.

## Related

- `docs/roadmap/VERSIONS.md` — when each piece of this vision actually
  lands, and what version it belongs to.
- `docs/roadmap/AI_EVOLUTION.md` — the AI-specific stage timeline
  within this vision.
- `docs/constitution/CONSTITUTION.md` Article 1 — the permanent
  boundary this entire vision operates inside.
