# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002B — Navigation Architecture

**Status: IN PROGRESS.** Type: Architecture only, per Director
authorization — no implementation, code, or API is written. Designs
Universal Navigation, Screen Model, Navigation Graph, Route Registry,
Back Stack, Deep Link System, Permission Layer, Platform Adapter,
Navigation State, Session Navigation, Navigation Events, Screen
Lifecycle, and Platform Capability Mapping, each stating its
compatibility across all five target platforms (Constitution Article
13). Governed by ADR-001 (`communication/decisions/ADR-001.md`) and
the Universal UI Abstraction rule (`docs/PLATFORM_WORKFLOW.md`).
Deliverable: `docs/NAVIGATION_ARCHITECTURE.md`, ending with a
"Director Questions" section. TASK-002C (Registry) does not start
until this Architecture is approved.

## Previous phases (frozen, never reopened)

- **PLATFORM-001 (Platform Foundation & Collaboration Infrastructure)**
  — ✅ **APPROVED, FROZEN**. CI `success` (`ci.yml` runs #150/#151).
  Record: `docs/changelog/CHANGELOG.md`, `docs/PLATFORM_FOUNDATION.md`,
  `communication/task_queue/TASK-001.md`.
- **TASK-002A (Navigation Analysis)** — ✅ **APPROVED**. Record:
  `docs/NAVIGATION_ANALYSIS.md`, its six open questions answered in
  `communication/decisions/ADR-001.md`.

## Governance added this round

- **ADR-001** (`communication/decisions/ADR-001.md`) — GoldBot
  Platform is a Shared Platform Layer serving five equal clients
  (Telegram Bot, Telegram Mini App, Android, iOS, Desktop), not
  Telegram Bot with others bolted on later.
- **Constitution Article 13 — Future First Principle** — every
  Architecture document states its compatibility across all five
  platforms, even the four with no code today.
- **Universal UI Abstraction rule** (`docs/PLATFORM_WORKFLOW.md`) — no
  Platform component is ever `Telegram Callback → Business Logic`
  directly; always `Platform UI → Navigation Layer → Application Layer
  → Business Logic`.
- **Director Questions section** — every Architecture document now
  ends with one (or `None.`), per `docs/PLATFORM_WORKFLOW.md`.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched. **Platform** (Product
Experience & Platform Foundation) is where all activity in this and
the prior two phases happens.

## Next

`docs/NAVIGATION_ARCHITECTURE.md` (this phase's deliverable), then
Director review before TASK-002C (Navigation Registry) starts. See
`communication/task_queue/QUEUE.md` for the full chain.

## Related

- `docs/PLATFORM_WORKFLOW.md` — the "Architecture First" process,
  Universal UI Abstraction rule, and Director Questions requirement.
- `communication/decisions/ADR-001.md`, `docs/constitution/CONSTITUTION.md`
  Article 13 — this round's governance additions.
- `communication/task_queue/QUEUE.md` — the live task chain.
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the one open item from an earlier phase,
  still unresolved (out of scope for this one too).
