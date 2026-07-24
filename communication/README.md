# GoldBot — Communication Infrastructure

Cross-role collaboration between **Core** (Trading Engine & AI) and
**Platform** (Product Experience & Platform Foundation) — the role
split the Director established in `docs/CURRENT_PHASE.md`. Introduced
by PLATFORM-001 (Platform Foundation & Collaboration Infrastructure).

Before this phase, handoff between roles was a single prose document
per phase (`docs/HANDOFF.md`). This folder tree adds structured,
per-item tickets for the recurring exchanges that don't warrant a
whole phase document: a Platform Worker needing something from Core, a
bug found during Platform work, a review, a decision, a piece of
technical debt.

## Folders

| Folder | Purpose | Ticket prefix |
|---|---|---|
| `requests/` | Platform → Core: "I need X to finish Y" | `REQ-XXXX.md` |
| `responses/` | Core's answer to a specific `REQ-XXXX` | `RESP-XXXX.md` |
| `notifications/` | One-way heads-up, no response expected | `NOTE-XXXX.md` |
| `issues/` | A bug found during Platform (or Core) work | `ISSUE-XXXX.md` |
| `contracts/` | An agreed data/API shape crossing the Core↔Platform boundary | `CONTRACT-XXXX.md` |
| `reviews/` | A completed review of a specific piece of work | `RVW-XXXX.md` |
| `decisions/` | A cross-role decision ticket (see note below) | `DEC-XXXX.md` |
| `technical_debt/` | A debt ticket (see note below) | `TD-XXXX.md` |
| `task_queue/` | The Platform Worker's own task chain (see its own README) | `TASK-XXXX.md` |

Every folder has its own `README.md` (this file only indexes them) and
a `TEMPLATE.md` to copy for a new ticket. IDs are sequential per
prefix, zero-padded to 4 digits, never reused.

## Reused, not duplicated (Constitution Article 7/11)

Two folders are deliberately **tickets that feed an existing,
permanent record** rather than a competing system:

- `decisions/` tickets are working documents for a specific Core↔Platform
  question; once a decision is made and load-bearing, it is also
  recorded in `docs/changelog/DECISION_LOG.md` (the permanent ledger,
  Constitution Article 8) — the ticket is not a replacement for that
  ledger.
- `technical_debt/` tickets are the same relationship to
  `docs/TECHNICAL_DEBT.md` (the permanent ledger, established the
  prior phase): a ticket here is raised during handoff; once accepted
  as a known, deliberately-unfixed item it is folded into that file.

`reviews/` tickets apply the existing `docs/standards/REVIEW_STANDARD.md`
checklist to one specific piece of work — the standard itself is not
restated here.

## The request/response loop

1. Platform (or Core) writes `requests/REQ-XXXX.md` (see its README's
   template — Need / Reason / Priority, per the Director's own
   example).
2. The other role answers in `responses/RESP-XXXX.md`, referencing the
   same `XXXX` number.
3. If the request surfaced a bug, an `issues/ISSUE-XXXX.md` is opened
   instead (or in addition), using `docs/PLATFORM_BUG_REPORT_STANDARD.md`'s
   format.

## Related

- `docs/CURRENT_PHASE.md` — the Core/Platform role split this
  infrastructure serves.
- `docs/HANDOFF.md` — the phase-level handoff document this
  ticket-level infrastructure complements, not replaces.
- `docs/TECHNICAL_DEBT.md`, `docs/changelog/DECISION_LOG.md`,
  `docs/standards/REVIEW_STANDARD.md` — the permanent records the
  `technical_debt/`/`decisions/`/`reviews/` tickets feed.
- `docs/PLATFORM_BUG_REPORT_STANDARD.md` — the format `issues/` tickets use.
