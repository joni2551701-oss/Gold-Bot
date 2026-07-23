# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002C — Navigation Registry

**Status: DELIVERED, AWAITING DIRECTOR REVIEW.** Type: Real
implementation, first code since PLATFORM-001 — Director-authorized
under a specific rule list: no hardcoded screens, no `telegram/`
dependency, no platform-specific code, Universal Screen ID (ADR-002),
a dynamic Registry (extending TASK-001's `platforms/menu_registry.py`,
not replacing it), a Navigation Event Bus interface only (ADR-004, no
dispatch), and extensibility for future modules (AI, Education,
Marketplace, Trading) without a Registry code change. Populates
GoldBot's real, currently-live 25 Telegram screens only — no
fictitious future-module entries. Zero change to
`telegram/reply_keyboard_manager.py`'s live behavior. 15 new tests
(39 total in `tests/platforms/`), full suite 4648 passing.

## Frozen / closed phases

- **PLATFORM-001** — ✅ **FROZEN**, never reopened.
- **TASK-002A (Navigation Analysis)** — ✅ **CLOSED**.
- **TASK-002B (Navigation Architecture)** — ✅ **APPROVED**, following
  Director resolution of its 6 open questions
  (`docs/NAVIGATION_ARCHITECTURE.md`'s "Director Decisions" section)
  and three new ADRs (`communication/decisions/ADR-002.md` Universal
  Screen Identity, `ADR-003.md` Platform never creates a Screen,
  `ADR-004.md` Navigation Event Bus).

## Governance added this round

- **Constitution-level decisions ADR-002/003/004** (not promoted to
  Constitution Articles — Director-issued Architecture Decision
  Records, permanent per `docs/changelog/DECISION_LOG.md`, but scoped
  to Navigation specifically rather than a codebase-wide law like
  Article 13).
- **"Future Expansion" section**, mandatory in every Architecture
  document from now on (AI/Education/Marketplace/Enterprise Impact,
  Scalability, Migration Risk) — `docs/PLATFORM_WORKFLOW.md`.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched. **Platform** (Product
Experience & Platform Foundation) is where all activity happens.

## Next

TASK-002C's own deliverable (Registry code + tests + documentation +
CI), then Director review before TASK-002D (Navigation Implementation)
starts. See `communication/task_queue/QUEUE.md` for the full chain.

## Related

- `docs/NAVIGATION_ARCHITECTURE.md` — the approved architecture this
  Registry implements.
- `communication/decisions/ADR-001.md` through `ADR-004.md`.
- `docs/PLATFORM_WORKFLOW.md` — "Architecture First," Universal UI
  Abstraction, Future Expansion, Director Questions.
- `communication/task_queue/QUEUE.md` — the live task chain.
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the one open item from an earlier phase,
  still unresolved (out of scope for this one too).
