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
GOVERNANCE-REVIEW-001   Engineering Governance Layer Review          ✅ DELIVERED — awaiting Director Governance Freeze decision
    ↓
GOV-PLAN-001            Governance v1.1 Master Plan (ORDER-013)      ✅ DELIVERED — awaiting Director review before GOV-001..GOV-009 are issued
    ↓  (each issued separately, reviewed separately, Frozen separately)
GOV-001  Director.md                     ✅ APPROVED (ORDER-015)
GOV-002  Core_Worker.md                  ✅ APPROVED (ORDER-016)
GOV-003  Platform_Worker.md              ✅ APPROVED (ORDER-017)
GOV-004  Collaboration_Rules.md          ✅ APPROVED (ORDER-018)
GOV-005  Repository_Policy.md            ✅ APPROVED (ORDER-019, GOV-PACKAGE-001)
GOV-006  Branch_Policy.md                ✅ APPROVED (ORDER-019, GOV-PACKAGE-001)
GOV-007  Branch_Protection_Policy.md     ✅ APPROVED (ORDER-019, GOV-PACKAGE-001)
GOV-008  Engineering_Language_Policy.md  ✅ APPROVED (ORDER-019, GOV-PACKAGE-001)
GOV-009  Git_Workflow_Standard.md        ✅ APPROVED (ORDER-019, GOV-PACKAGE-001)
    ↓
Engineering Governance v1.1            ✅ FROZEN (all 9 GOV documents approved — Director declaration)
```

| Task | Title | Status |
|---|---|---|
| GOVERNANCE-REVIEW-001 | Engineering Governance Layer Review | ✅ DELIVERED — see `communication/task_queue/GOVERNANCE-REVIEW-001.md` and `docs/GOVERNANCE_REVIEW_001.md`. Final Recommendation: READY WITH MINOR IMPROVEMENTS. |
| GOV-PLAN-001 | Governance v1.1 Master Plan | ✅ DELIVERED — see `communication/task_queue/GOV-PLAN-001.md` and `docs/GOVERNANCE_V1_1_MASTER_PLAN.md`. Planning only; each of GOV-001–GOV-009 remains Pending until individually issued by the Director. |
| GOV-001 | Director.md — Director Role Definition | ✅ APPROVED (ORDER-015) — `docs/governance/roles/Director.md`. Naming convention `GOV-001`..`GOV-009` confirmed final by Director (TASK-XXX reserved for Platform Tasks). |
| GOV-002 | Core_Worker.md — Core Worker Role Definition | ✅ APPROVED (ORDER-016) — `docs/governance/roles/Core_Worker.md`. |
| GOV-003 | Platform_Worker.md — Platform Worker Role Definition | ✅ APPROVED (ORDER-017) — `docs/governance/roles/Platform_Worker.md`. |
| GOV-004 | Collaboration_Rules.md — Collaboration Standard | ✅ APPROVED (ORDER-018) — `docs/governance/roles/Collaboration_Rules.md`. Founder = informal principal above the chain (Director-confirmed via Freeze). |
| GOV-005 | Repository_Policy.md | ✅ APPROVED (ORDER-019 / GOV-PACKAGE-001) — `docs/governance/policies/Repository_Policy.md`. |
| GOV-006 | Branch_Policy.md | ✅ APPROVED (ORDER-019 / GOV-PACKAGE-001) — `docs/governance/policies/Branch_Policy.md`. |
| GOV-007 | Branch_Protection_Policy.md | ✅ APPROVED (ORDER-019 / GOV-PACKAGE-001) — `docs/governance/policies/Branch_Protection_Policy.md`. |
| GOV-008 | Engineering_Language_Policy.md | ✅ APPROVED (ORDER-019 / GOV-PACKAGE-001) — `docs/governance/policies/Engineering_Language_Policy.md`. English confirmed as the engineering language (Uzbek-internal option not taken). |
| GOV-009 | Git_Workflow_Standard.md | ✅ APPROVED (ORDER-019 / GOV-PACKAGE-001) — `docs/governance/standards/Git_Workflow_Standard.md`. |
| — | **Engineering Governance v1.1** | ✅ **FROZEN** — all 9 GOV documents approved (Director declaration). |

## Repository Engineering (separate track — `REPO-XXX`, never a `TASK-XXX`, `DEVOPS-XXX`, or `GOVERNANCE-REVIEW-XXX`)

A fourth independent track for whole-repository engineering work
(branch strategy, migration, CI/branch-protection structure) — the
first task on this track is explicitly the first Engineering task
after Governance v1.0 is frozen, per Director order.

```
REPO-001              Repository Engineering Migration (Audit + Plan)   ✅ Audit/Plan delivered — Migration unpaused (Governance v1.1 FROZEN)
    ↓
BRANCH-FORENSICS-001  Repository History Forensics (ORDER-003)          ✅ APPROVED — root cause confirmed (F-008–F-013)
    ↓
MIGRATION_PLAN.md     Recovery + Migration control document              ✅ DELIVERED — awaiting Director approval + branch-op authority
    ↓
ORDER-020/021 Repository Recovery   Unicode fix + rollback tags          🟢 Runbook APPROVED, scope confirmed (fix only strategy_manager.py); awaiting Authorized Operator execution, then Worker verifies + writes Recovery Report
    ↓
REPO-002              Repository Migration Implementation               ⏳ Blocked — starts only after Repository Recovery is APPROVED
```

| Task | Title | Status |
|---|---|---|
| REPO-001 | Repository Engineering Migration | ⏸ PAUSED — Director ORDER-009: stays paused until Engineering Governance v1.1 is frozen. Audit + Plan themselves remain delivered and unchanged (`communication/task_queue/REPO-001.md`, `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`). |
| BRANCH-FORENSICS-001 | Repository History Forensics | ✅ APPROVED — see `communication/task_queue/BRANCH-FORENSICS-001.md` and `docs/BRANCH_FORENSICS_001.md`. Director findings F-008 through F-013 confirmed: root cause is a single invisible Unicode character (U+2060) in one filename (`strategy_layer/strategy_manager/strategy_manager.py`), zero code difference; the `strategie/` typo was a separate, already self-corrected historical event, not the conflict cause. |
| MIGRATION_PLAN.md | Recovery + Migration control document | ✅ DELIVERED — `docs/governance/MIGRATION_PLAN.md`. Single control document (Recovery phases, Migration phases, Rollback plan, Risk Analysis, Success/Exit Criteria, Recovery + Migration Checklists). Awaiting Director approval and branch-operation authority confirmation before any mutating step. |
| ORDER-020/021 Repository Recovery | Unicode filename fix + rollback tags | 🟢 READY FOR AUTHORIZED OPERATOR — Director confirmed the one-file scope, updated the Exit Criteria, and APPROVED `docs/governance/RECOVERY_OPERATOR_RUNBOOK.md`. HTTP-trace-confirmed (ORDER-022): the Claude Code git-proxy blocks this session from pushing **tags** (any ref outside `refs/heads/*`); a `main` push from this session was **not tested**. GitHub itself accepted the receive-pack advertisement — the 403 is from the git-proxy, not GitHub permissions. So Option 2 (a differently-scoped Authorized Operator) executes the approved runbook; the Worker then verifies and writes the Recovery Report. See `communication/task_queue/REPO-RECOVERY-001.md`. |
| REPO-002 | Repository Migration Implementation | ⏳ Blocked — starts only after Repository Recovery is APPROVED. |

## Governance v1.1 (upcoming, not yet an executable brief)

Per Director's Next Priority ordering (this update): (1) Governance
v1.1 — 9 new documents, not yet individually named/scoped by an
executable Director Brief; (2) Governance v1.1 Freeze; (3) Repository
Recovery (Unicode fix + rollback tags); (4) Repository Migration;
(5) Core/Platform parallel workflow. Per Constitution Article 8 /
`docs/policies/DIRECTOR_POLICY.md`'s "what makes a brief executable"
rule, a priority ordering naming a document count but not each
document's scope, TASK 0 audit, Strict Rules, and Acceptance Criteria
is roadmap guidance, not yet an executable brief — the Worker
acknowledges this priority and awaits the explicit Governance v1.1
brief before creating any of the 9 documents.

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
