# Platform Task Queue

Live chain. Update this file and the corresponding `TASK-XXX.md`/
`DEVOPS-XXX.md` together whenever a status changes. Seeded from the
Director's own GoldBot Master Progress table (Phase 2 — Platform);
TASK-002 (Navigation) split into sub-tasks per Director decision —
Navigation is treated as the highest-risk Platform module, so it is
staged through the full "Architecture First" workflow
(`docs/PLATFORM_WORKFLOW.md`) one step at a time.

**Two independent tracks, per Director decision (this update):
Platform Tasks and Engineering never interrupt each other.** A future
Engineering/DevOps item is never inserted into the Platform Tasks
numbering (e.g. it does not take the reserved TASK-003 slot) — it gets
its own `DEVOPS-XXX` sequence instead.

## Platform Tasks

```
TASK-001   Platform Foundation & Collaboration Infrastructure   ✅ Frozen
    ↓
TASK-002   Navigation                                           In Progress
    ├── TASK-002A  Navigation Analysis                          ✅ CLOSED
    ├── TASK-002B  Navigation Architecture                      ✅ APPROVED
    ├── TASK-002C  Navigation Registry                          ✅ FROZEN
    ├── TASK-002D  Navigation Implementation                    ✅ FROZEN
    ├── TASK-002E  Navigation Tests (Validation)                 ✅ FROZEN
    └── TASK-002F  Navigation Foundation Final Audit               🟢 AUTHORIZED
    ↓  ("Navigation Foundation Complete")
TASK-003   Dashboard                                             Pending
    ↓
TASK-004   Settings                                               Pending
    ↓
TASK-005   Notification Center                                     Pending
```

| Task | Title | Status |
|---|---|---|
| TASK-001 | Platform Foundation & Collaboration Infrastructure | ✅ Frozen — never reopened |
| TASK-002 | Navigation (parent) | In Progress |
| TASK-002A | Navigation Analysis | ✅ CLOSED |
| TASK-002B | Navigation Architecture | ✅ APPROVED |
| TASK-002C | Navigation Registry | ✅ FROZEN (Freeze Checklist complete) |
| TASK-002D | Navigation Implementation | ✅ FROZEN — CI #158's cancellation resolved by ADR-009 (CI Supersession Rule); #159 success is the official validation |
| TASK-002E | Navigation Tests (Validation) | ✅ FROZEN — 80 tests passing, CI #163 success; surfaced Security Backlog item (`has_sufficient_permission()`), see ADR-010/011 |
| TASK-002F | Navigation Foundation Final Audit | 🟢 AUTHORIZED — expanded scope: Architecture/Code/Documentation/Test/Future/Security Audit |
| TASK-003 | Dashboard | Pending |
| TASK-004 | Settings | Pending |
| TASK-005 | Notification Center | Pending |

## Engineering (separate track — `DEVOPS-XXX`, never a `TASK-XXX`)

Per Director decision: DevOps/CI-infrastructure work is its own
roadmap, sequenced independently of Platform Tasks so neither
interrupts the other's context.

```
DEVOPS-001   Smart CI Routing         ⏳ Blocked until Navigation Foundation Complete (TASK-002E + TASK-002F)
DEVOPS-002   Release Pipeline         ⏳ Not yet scoped
DEVOPS-003   Branch Protection        ⏳ Not yet scoped
DEVOPS-004   Build Optimization       ⏳ Not yet scoped
```

| Task | Title | Status |
|---|---|---|
| DEVOPS-001 | Smart CI Routing | ⏳ Blocked — starts only after TASK-002E and TASK-002F are both fully complete. See `communication/task_queue/DEVOPS-001.md` for the full scope and mandatory pre-start deliverables. |
| DEVOPS-002 | Release Pipeline | ⏳ Not yet scoped |
| DEVOPS-003 | Branch Protection | ⏳ Not yet scoped |
| DEVOPS-004 | Build Optimization | ⏳ Not yet scoped |

## Governance (separate track — `GOVERNANCE-REVIEW-XXX`, never a `TASK-XXX` or `DEVOPS-XXX`)

A third independent track for whole-governance-layer review work (as
opposed to Platform feature work or CI/Engineering infrastructure work)
— never interrupts, and is never interrupted by, either of the other
two tracks.

```
GOVERNANCE-REVIEW-001   Engineering Governance Layer Review   ✅ DELIVERED — awaiting Director Governance Freeze decision
```

| Task | Title | Status |
|---|---|---|
| GOVERNANCE-REVIEW-001 | Engineering Governance Layer Review | ✅ DELIVERED — see `communication/task_queue/GOVERNANCE-REVIEW-001.md` and `docs/GOVERNANCE_REVIEW_001.md`. Final Recommendation: READY WITH MINOR IMPROVEMENTS. |

## Repository Engineering (separate track — `REPO-XXX`, never a `TASK-XXX`, `DEVOPS-XXX`, or `GOVERNANCE-REVIEW-XXX`)

A fourth independent track for whole-repository engineering work
(branch strategy, migration, CI/branch-protection structure) — the
first task on this track is explicitly the first Engineering task
after Governance v1.0 is frozen, per Director order.

```
REPO-001   Repository Engineering Migration (Audit + Plan)   ✅ DELIVERED — awaiting Director approval before REPO-002 (Implementation)
```

| Task | Title | Status |
|---|---|---|
| REPO-001 | Repository Engineering Migration | ✅ DELIVERED — see `communication/task_queue/REPO-001.md` and `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`. Audit + Proposal + Plan only, no branch/PR/protection/settings action taken. Recommend approving the plan and authorizing REPO-002 (Implementation). |

## Rule change (Engineering track, this update)

Per Director decision: a separate Engineering/DevOps roadmap
(`DEVOPS-XXX`) exists alongside Platform Tasks (`TASK-XXX`), never
replacing a reserved Platform Tasks slot. DEVOPS-001 (Smart CI
Routing — routing CI into Documentation/Platform/Trading/Full-Regression
pipelines by changed path) is recorded now but does not start until
Navigation Foundation (TASK-002E + TASK-002F) is complete. No
`.github/workflows/*.yml` file is touched before then, and not even
then without the five mandatory pre-start deliverables (current
Actions map, per-pipeline trigger conditions, path→pipeline table,
measured time savings, regression risk) reviewed and approved first.

## Rule change (ADR-001, this update)

Per `communication/decisions/ADR-001.md` and Constitution Article 13
(Future First Principle): GoldBot Platform is architected around a
Shared Platform Layer serving five equal clients (Telegram Bot,
Telegram Mini App, Android, iOS, Desktop), not Telegram Bot with
others added later. Every Architecture document from TASK-002B onward
states each component's compatibility across all five, and no
component is ever written as `Telegram Callback → Business Logic`
directly (`docs/PLATFORM_WORKFLOW.md`'s Universal UI Abstraction rule).

## Rule change (prior update)

Per Director decision: every future task (not just Navigation) follows
the mandatory 10-step "Architecture First" workflow
(`docs/PLATFORM_WORKFLOW.md`) — Analysis → Architecture →
Implementation Plan → Approval Check → Implementation → Tests →
Documentation → CI → Freeze → Next Task. A task that touches a new
public API, a folder-structure change, a broken contract, a database
schema change, or the Core↔Platform interface additionally requires a
`communication/decisions/PROPOSED-DECISION-XXXX.md` ticket and Director
approval before Implementation starts (`communication/decisions/README.md`'s
"No Silent Decisions Policy"). Internal refactoring, bug fixes, and
documentation are exempt from that specific ticket requirement.
