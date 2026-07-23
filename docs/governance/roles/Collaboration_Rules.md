# Collaboration Rules

The authoritative, binding standard for how the **Director**, **Core
Worker**, and **Platform Worker** collaborate on GoldBot Engineering
Governance: how work is requested, ordered, executed, reviewed,
approved, handed off, and — when things go wrong — escalated and
recovered. It is governed by `docs/constitution/CONSTITUTION.md`, sits
beside the three role documents (`docs/governance/roles/Director.md`,
`Core_Worker.md`, `Platform_Worker.md`), and is the fourth of the nine
Governance v1.1 documents planned in
`docs/GOVERNANCE_V1_1_MASTER_PLAN.md` (issued as GOV-004 / ORDER-018).

This document defines **how the roles work together**. It does not
redefine any role, restate the Constitution, or restate
`docs/policies/DIRECTOR_POLICY.md` — those are referenced, not copied
(§25). Where this document sits above the existing `communication/`
folder infrastructure (`requests/`, `responses/`, `notifications/`,
`issues/`, `contracts/`, `reviews/`, `decisions/`, `technical_debt/`,
`task_queue/`), it is the **role-level narrative** for how those
channels are used together; each folder's own README remains the
authoritative format/index for that channel and is not replaced here.

## 1. Purpose

To make collaboration on this repository predictable, traceable, and
role-bounded — so that every task has a clear beginning (a Director
Order), a clear middle (Worker execution under an executable brief),
and a clear end (a Director verdict and, where required, a Freeze), and
so that no participant ever has to guess who decides, who executes, or
what happens when work is blocked, rejected, or urgent.

## 2. Collaboration Principles

These twelve principles are mandatory and bind every participant:

- **Single Director Authority** — one Director holds final governance
  authority; approvals, rejections, ADRs, freezes, and repository-
  strategy decisions are the Director's alone
  (`docs/governance/roles/Director.md`).
- **No Silent Decisions** — a Worker never self-authorizes a decision
  reserved for the Director (folder-structure change, new public API,
  broken contract, DB schema change, Core↔Platform interface change);
  it opens a `PROPOSED-DECISION-XXXX.md` and waits
  (`communication/decisions/README.md`).
- **Order Before Execution** — no code or file is created until an
  executable Director Order exists (Constitution Article 8).
- **Review Before Approval** — no work is approved without a Director
  review against the brief and the standards.
- **Approval Before Continuation** — a task is not complete, and
  dependent work does not begin, until the Director returns APPROVED.
- **Documentation First** — the documents above a change agree before
  the change is written (`docs/policies/DEVELOPMENT_POLICY.md`).
- **Architecture First** — Platform implementation follows the 10-step
  workflow (`docs/PLATFORM_WORKFLOW.md`); design and Approval Check
  precede code.
- **Fail Closed** — any unknown/invalid/missing/malformed permission or
  state denies rather than allows (ADR-010).
- **Traceability** — every standing decision is recorded (ADR / ORDER /
  amendment); a decision that cannot be traced to a written record is
  not binding.
- **Accountability** — every deliverable ends with an explicit
  changed-files list and the Pre-Commit Verification checklist; the
  author of a change is identifiable from the commit record.
- **Separation of Responsibilities** — the Director governs; the Core
  Worker owns the Trading Core layers; the Platform Worker owns the
  Platform layers; none enters another's authority (§3, §14).
- **Single Source of Truth** — for any fact, exactly one document is
  authoritative; others cross-reference it rather than restating it
  (`docs/policies/DOCUMENTATION_POLICY.md`).

## 3. Engineering Governance Chain

Intent flows down; execution and reporting flow back up:

```
Founder  (human vision / high-level intent)
   ↓
Director (governance authority — turns intent into Orders, reviews, approves)
   ↓
Core Worker  ┆  Platform Worker  (execution, on disjoint layers)
   ↓
Repository (the single source of truth for all work product)
```

**Note on "Founder"**: the Founder is the human vision-holder whose
intent the Director serves and translates into executable Orders. The
Founder is **not** one of the three governed *engineering* roles
defined in Governance v1.1 (Director / Core Worker / Platform Worker) —
it is the principal above the governance chain. If the Founder is ever
to be a formally-governed role with its own authority document, that is
a separate future document, not defined or assumed here (flagged per
the No Silent Decisions principle rather than silently invented).

**Collaboration boundaries** (no role enters another's authority):

| Role | Owns |
|---|---|
| **Director** | Orders, Reviews, Approvals, Governance (scope, priority, ADRs, Freeze, repository strategy). |
| **Core Worker** | Core Layer, Trading Logic, AI Core, Risk, Decision (`context/`, `strategies/`, `signals/`, `decision/`, `risk/`, `execution/`, `ai/`, `core/pipeline.py`). |
| **Platform Worker** | Telegram, Users, Subscription, Admin, Platform Services (`telegram/`, `platforms/`, `communication/`, the four platform DB tables, `translation/`). |

## 4. Communication Rules

- The Director communicates intent through **executable Orders/briefs**
  (Objective, `TASK 0`, `TASK 1…N`, Strict Rules, Acceptance Criteria).
  A message lacking that shape is guidance, not a brief; the Worker
  acknowledges it and does not create code or files until an executable
  brief arrives (`docs/policies/DIRECTOR_POLICY.md`; Constitution
  Article 8).
- Structured cross-role exchange uses the `communication/` channels:
  `requests/` → `responses/` for "I need X to finish Y," `notifications/`
  for one-way heads-up, `issues/` for a bug found during work,
  `contracts/` for an agreed cross-boundary data/API shape,
  `reviews/` for a completed review instance, `decisions/` for ADR/DEC/
  PROPOSED-DECISION tickets. Each channel's README is authoritative for
  its own format.
- The conversational language between Founder/Director and Worker is
  unrestricted; every artifact committed to the repository is English
  (GOV-008 / `Engineering_Language_Policy.md` will formalize this).
- Reporting language is disciplined: no "Complete"/"Validated"/
  "Production Ready"/"All checks passed" before GitHub Actions returns
  `success` for the exact commit (`CLAUDE.md`).

## 5. Task Lifecycle

Every task moves through the same lifecycle, tracked in
`communication/task_queue/QUEUE.md` and its per-task ticket:

```
(Founder intent) → Director Review → Director Order → Worker Assignment
   → Execution → Report → Director Review → APPROVED → (Freeze, where required)
```

Status values: `Pending → In Progress → Delivered → APPROVED`
(or `CHANGES REQUIRED` → revise, or `REJECTED` → closed). Exactly one
task per track is `In Progress` at a time
(`communication/task_queue/README.md`); the four tracks (Platform
`TASK-XXX`, Engineering `DEVOPS-XXX`, Governance `GOVERNANCE-REVIEW-XXX`/
`GOV-XXX`, Repository `REPO-XXX`) never interrupt one another.

## 6. Director Order Workflow

1. The Director converts Founder intent (or the Director's own
   priority) into an **executable Order**: a unique Order ID, a Task
   ID, an Objective, a `TASK 0` reuse/compliance audit instruction,
   deliverables, Strict Rules, Acceptance Criteria, and an Exit
   Criteria.
2. The Order is delivered to the assigned Worker (Core or Platform,
   per the task's layer).
3. The Order is recorded — the Task ID appears in the queue and gets
   its own ticket.

An Order is the **only** valid trigger for execution. No Worker begins
implementation from guidance, a roadmap, or praise.

## 7. Worker Execution Workflow

1. **TASK 0 first** — audit what already exists against the Order's
   assumptions (Foundation Reuse Audit, Article 11); implement only the
   genuine gap.
2. **Architecture First** (Platform implementation) — Analysis →
   Architecture → Implementation Plan → **Approval Check** →
   Implementation → Tests → Documentation → CI → Freeze → Next Task
   (`docs/PLATFORM_WORKFLOW.md`). A Core task follows the same
   universal disciplines (Commit Protocol, Article 6 tests, Article 8).
3. **No Silent Decisions gate** — if TASK 0/Architecture surfaces a
   reserved-decision trigger, stop and file `PROPOSED-DECISION-XXXX.md`
   before implementing.
4. **Validate** — the full Commit Protocol in order (`git add -A` →
   pyflakes → compileall → pytest → smoke run → clean status →
   reviewed diff → commit → push → CI).
5. **Report** — end every commit-producing response with the Pre-Commit
   Verification checklist and the changed-files list; use no
   completion language before CI confirms.

## 8. Review Workflow

1. The Worker submits the completed deliverable (delivered status +
   report + CI result).
2. The Director reviews it against: the Order's scope, the Constitution
   and applicable Standards/Policies/ADRs, the absence of unauthorized
   change (no cross-layer edit, no branch/CI/governance change unless
   the Order named it), and the honesty of the reported validation —
   applying (not restating) `docs/standards/REVIEW_STANDARD.md`.
3. The Director issues exactly one verdict (§9–§11).

## 9. Approval Workflow

```
Worker delivers → Director Review → APPROVED → (Freeze, where required) → task complete
```

- **APPROVED** means the deliverable is accepted as-is; the task may
  proceed to Freeze (if the workflow requires one) and dependent tasks
  may begin.
- The Worker never treats CI success alone as approval, and never
  self-approves or self-freezes.

## 10. Change Request Workflow

```
Director → CHANGES REQUIRED → Worker → Revision → Review → APPROVED
```

- **CHANGES REQUIRED** means the deliverable is not accepted as-is; the
  Director states exactly what must change.
- The Worker revises against those stated changes only (no
  uninstructed scope creep), re-runs the full Commit Protocol, and
  resubmits for review. The loop repeats until APPROVED.

## 11. Rejection Workflow

```
Director → REJECTED → Task Closed → New Order Required
```

- **REJECTED** means the deliverable's current line is not to be
  revised into acceptance; the Director states why.
- The task is closed. Any further work on the underlying goal requires
  a **new** Director Order — the rejected task is not silently reopened
  or continued.

## 12. Escalation Rules

- When an Order's instruction conflicts with the Constitution, a
  LOCKed/Frozen module, or an existing ADR, the Worker executes
  **STOP → AUDIT → Director Decision**: stop, document the specific
  rule and the specific conflicting instruction, return it to the
  Director, and wait (Constitution Article 8;
  `docs/governance/roles/Director.md` §11).
- When a Worker discovers something that is a Director decision to make
  (an ambiguity, a security weakness, a naming collision, an
  unauthorized-but-tempting shortcut), it surfaces the finding and
  waits — it never self-authorizes (No Silent Decisions).
- The Director is the sole resolving authority for every escalation.

## 13. Conflict Resolution

- **Constitution supremacy** — if any document, Order, or proposal
  conflicts with the Constitution, the Constitution wins; the
  conflicting item is corrected or withdrawn.
- **Document hierarchy** — Constitution → Architecture → Roadmap →
  Policy → Standard → Role/Collaboration → Code (Article 8's order); a
  lower-tier document never overrides a higher-tier one.
- **Cross-role conflict** — if the Core Worker and Platform Worker
  disagree on a boundary (e.g. who owns a change touching the
  Core↔Platform interface), neither decides it; it goes to the
  Director as an escalation, and the interface change follows the No
  Silent Decisions `PROPOSED-DECISION-XXXX.md` gate.

## 14. Cross-Team Collaboration

- The Core Worker and Platform Worker own **disjoint** layers (§3) and
  never edit each other's layers without an Order that explicitly says
  so — proven on every commit by a `git diff --cached --stat` against
  the other role's paths.
- When one role needs something only the other (or Core) can provide, it
  files a `requests/REQ-XXXX.md`; the other answers in
  `responses/RESP-XXXX.md`. A cross-boundary data/API shape both sides
  will build against is fixed in a `contracts/CONTRACT-XXXX.md` before
  either side implements it.
- A change to the Core↔Platform interface itself is a reserved decision
  (No Silent Decisions) and requires a `PROPOSED-DECISION-XXXX.md`
  approved before implementation.

## 15. Handoff Procedure

- Work product is handed off through the **repository itself** (the
  Single Source of Truth), never through undocumented conversation:
  committed code, the task ticket, and the phase/handoff documents
  (`docs/HANDOFF.md`, `docs/CURRENT_PHASE.md`) carry everything a next
  session or a different role needs to continue.
- A handoff between roles (Core → Platform or vice versa) is
  accompanied by a `notifications/NOTE-XXXX.md` (one-way heads-up) or a
  `requests/REQ-XXXX.md` (if action is needed), plus any
  `contracts/CONTRACT-XXXX.md` the receiving role must build against.
- No handoff is "complete" until the receiving side can continue from
  the written record alone, without re-deriving lost context.

## 16. Repository Collaboration Rules

- All work product lives in the repository; the repository is the
  single source of truth for code and governance alike.
- The concrete branch model (`main` / `develop` / `feature/core` /
  `feature/platform`), branch protection, and the git mechanics of
  collaboration are **proposed** in
  `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` and will be
  **ratified** by GOV-006 (`Branch_Policy.md`), GOV-007
  (`Branch_Protection_Policy.md`), and GOV-009 (`Git_Workflow_Standard.md`)
  — this document does not pre-empt them. Until those are approved and
  Repository Migration executes (paused under ORDER-009), collaboration
  continues on the current branch structure.
- No participant performs a repository-strategy action (branch create/
  delete, merge, protection, default-branch change) except under a
  Director Order authorizing that specific action.

## 17. Documentation Rules

- **Documentation First** — the governing documents agree before a
  change is written; every new module carries its documentation in the
  same deliverable (`docs/policies/DOCUMENTATION_POLICY.md`).
- **Single Source of Truth** — one authoritative document per fact;
  everything else cross-references it. This document, for instance,
  references the role documents and the `communication/` READMEs rather
  than restating them.
- **Honesty over completeness** — a document states foundation-only or
  not-yet-wired status plainly; overstating capability is a policy
  violation of the same severity as a missing test.

## 18. Emergency Procedures

```
Critical Issue → Immediate Report → Director Decision → Recovery Plan → Execution
```

- A critical issue (a production-affecting failure, a security finding,
  a repository-integrity problem such as the `BRANCH-FORENSICS-001`
  conflict investigation) is reported to the Director **immediately**,
  without waiting for the current task's normal cycle to finish.
- The Director decides the response and issues a recovery Order. The
  Worker does not self-authorize an emergency fix to a Frozen module,
  a branch operation, or a Trading-Safety-critical change — even under
  time pressure, the Director's decision precedes execution.
- Recovery is executed under that Order, validated through the normal
  Commit Protocol, and reported like any other task. (Precedent: the
  `has_sufficient_permission()` finding was surfaced and queued as a
  Security Backlog item under Director decision, never self-fixed.)

## 19. Temporary Role Reassignment

```
Platform Worker → (Director ORDER) → Repository Migration → Temporary Core Assignment
   → Migration Complete → (Director ORDER) → Return to Platform
```

- A Worker may temporarily take on work outside its normal layer —
  for example, the Platform Worker executing Repository Recovery /
  Migration (a cross-cutting, non-Platform task) — **only under an
  explicit Director Order** that names the reassignment, its scope, and
  its end condition.
- During a temporary reassignment, the Worker is still bound by every
  constraint of the layer it is temporarily touching (e.g. Trading
  Safety still applies if a reassignment ever touched Core), and by the
  same Commit Protocol and reporting discipline.
- The reassignment ends when its stated end condition is met; the
  Worker returns to its normal role, and the return is recorded. A
  temporary reassignment never becomes permanent by default and never
  transfers any Director authority to the Worker.

## 20. Governance Freeze Rules

- A single task Freezes only when its full Freeze Checklist is
  satisfied and the Director has approved it (`docs/PLATFORM_WORKFLOW.md`).
- A **governance version** (e.g. Governance v1.1) is declared Frozen by
  the Director **only once every constituent document is individually
  approved and frozen** — for v1.1, all nine GOV documents
  (GOV-001…GOV-009). No governance version is Frozen while any
  constituent remains Pending or in CHANGES REQUIRED.
- A Frozen artifact is reopened only for a critical bug, a security
  issue, a Director-approved ADR, or a future authorized Migration Task
  (ADR-005 precedent).

## 21. Constraints

This document, and any Worker acting under it, does **not**:

- Create a new policy (that is a separate Director-authorized task).
- Modify the Constitution.
- Rewrite or restate any existing document (Constitution, the three
  role documents, `DIRECTOR_POLICY.md`, the `communication/` READMEs) —
  it references them.
- Change any role's authority or the boundaries between roles.
- Contain implementation detail.

## 22. Out of Scope

This document does **not**:

- Redefine the Director, Core Worker, or Platform Worker roles
  (GOV-001/002/003) — it governs their *interaction* only.
- Define the Founder as a governed engineering role (§3 note).
- Ratify the branch model, branch protection, or git mechanics
  (GOV-005/006/007/009) — it references them as forthcoming.
- Define the `communication/` channel formats (each folder's own README
  is authoritative) — it describes how the channels are used together.

## 23. Compliance Requirements

- **Constitution** — consistent with all 13 Articles, in particular
  Article 8 (the Change Management order and STOP → AUDIT → Director
  Decision this document operationalizes at the collaboration level).
  Constitution supremacy applies.
- **`Director.md`, `Core_Worker.md`, `Platform_Worker.md`** — no
  contradiction and no authority overlap; this document composes the
  three into a collaboration model without redefining any of them.
- **`docs/policies/DIRECTOR_POLICY.md`** — consistent with its
  executable-brief, STOP → AUDIT, and reporting-discipline content, which
  it references rather than restates.
- **`communication/` READMEs and `docs/PLATFORM_WORKFLOW.md`** —
  consistent with the channel definitions and the Architecture First
  workflow; both referenced, neither restated.
- **Existing ADRs** — breaks none; builds the collaboration model atop
  ADR-001 (roles/UI abstraction), ADR-005 (Freeze/Migration), ADR-010/011
  (fail-closed/security-review) rather than altering them.

## 24. Success Criteria

This document succeeds if:

- All twelve mandatory Collaboration Principles are stated (§2).
- All five mandatory workflows are fully described — Task Creation (§5,
  §6, §7), Change Request (§10), Rejection (§11), Emergency (§18),
  Temporary Role Reassignment (§19).
- Every question the Order named is answered: how Director/Worker
  communicate (§4); how a task starts (§5, §6) and ends (§8–§11); how
  review (§8), APPROVED (§9), CHANGES REQUIRED (§10), and REJECTED (§11)
  work; how handoff happens (§15); how Core and Platform hand off to
  each other (§14, §15); who decides in emergencies (§18); whether roles
  may temporarily swap and how (§19).
- Role authorities do not overlap (§3, §14).
- Temporary role reassignment is formally defined as Director-Order-only
  (§19).
- Review and Approval processes are fully documented (§8, §9).
- No existing document is restated or altered; no implementation detail
  is included.

## 25. References

- `docs/constitution/CONSTITUTION.md` — the supreme document; Article 8
  in particular.
- `docs/governance/roles/Director.md`, `Core_Worker.md`,
  `Platform_Worker.md` — the three roles this document composes.
- `docs/policies/DIRECTOR_POLICY.md` — the executable-brief and
  reporting process referenced throughout.
- `docs/PLATFORM_WORKFLOW.md` — the Architecture First workflow, Freeze
  Checklist, and No Silent Decisions / Fail Closed / Security Review
  rules.
- `communication/README.md` and the nine subfolder READMEs
  (`requests/`, `responses/`, `notifications/`, `issues/`, `contracts/`,
  `reviews/`, `decisions/`, `technical_debt/`, `task_queue/`) — the
  channels this document narrates the combined use of.
- `communication/decisions/README.md` — the No Silent Decisions Policy
  and ADR/DEC/PROPOSED-DECISION ticket types.
- `docs/HANDOFF.md`, `docs/CURRENT_PHASE.md` — the handoff/phase records
  §15 relies on.
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` — the
  repository-collaboration proposals §16 defers to GOV-005/006/007/009.
- `docs/GOVERNANCE_V1_1_MASTER_PLAN.md` — the Master Plan this document
  (GOV-004) is the fourth deliverable of.
- `communication/task_queue/GOV-004.md` — this task's own ticket record.
