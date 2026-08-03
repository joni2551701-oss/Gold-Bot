# Director — Role Definition

The authoritative definition of the **Director** role in GoldBot
Engineering Governance. This is a **Role-tier** document: it defines
who the Director is, what authority the Director holds, and where that
authority stops. It is governed by `docs/constitution/CONSTITUTION.md`
(Articles 8 and 10 in particular) and is the first of the nine
Governance v1.1 documents planned in
`docs/GOVERNANCE_V1_1_MASTER_PLAN.md` (issued as GOV-001 / ORDER-015).

It is **not** a substitute for `docs/policies/DIRECTOR_POLICY.md`. That
document is Policy-tier and describes the operating *process* between
Director and Worker (what makes a brief executable, STOP → AUDIT →
Director Decision, reporting discipline, and the separate Intelligence
Dependency Principle). This document describes the *role* — its
authority and boundaries. The two coexist at different tiers and are
cross-referenced here rather than merged or restated. Where they touch
the same subject, `DIRECTOR_POLICY.md`'s process detail governs the
process, and this document governs the role.

## 1. Purpose

To state, in one authoritative place, the Director's authority,
responsibilities, and hard boundaries — so that every task, review,
approval, and freeze decision in this repository can be traced to a
clearly-defined role rather than to informal precedent. Before this
document, the Director role existed only as the sum of its exercised
decisions (ORDER-numbered rulings, ADR issuance, Freeze declarations)
and a Policy-tier process description; this document makes the role
itself explicit.

## 2. Role Definition

The **Director** is the principal authority for GoldBot Engineering
Governance. The Director sets mission and priority, issues executable
briefs, reviews and approves the Worker's deliverables, issues binding
decisions (ORDER-numbered rulings and Architecture Decision Records),
and holds final sign-off on every Freeze.

The Director is a **governance** role, not an **implementation** role.
The Director decides *what* is built, *in what order*, and *whether the
result is accepted* — never *how* it is built at the level of writing,
testing, or committing code. That execution belongs to the Worker
roles (`docs/governance/roles/Core_Worker.md` and
`docs/governance/roles/Platform_Worker.md`, issued separately as
GOV-002 and GOV-003).

### Director is not the Owner

The **Director** (this role) and the **Owner** (Constitution Article
10's "Owner Override Law") are distinct roles and must not be
conflated, even where one person holds both:

- The **Owner** is the runtime-control principal of the *running
  product*. The Owner acts through the Telegram Owner Panel
  (`platform_layer/telegram/owner/*_commands.py`, gated by `platform_layer/telegram/owner/security.py`)
  to control safety- and control-critical modules of the live bot
  (emergency state, runtime lifecycle, feature toggles, broadcast
  intent). The Owner's authority is over the *deployed system's
  behavior*.
- The **Director** is the governance principal of the *engineering
  process*. The Director's authority is over *what work is done to the
  repository and whether it is accepted* — briefs, reviews, approvals,
  freezes, and repository-strategy decisions.

The two authorities never substitute for each other: a Director
approval is not an Owner Panel command, and an Owner Panel action is
not a governance decision. This document governs only the Director
role.

## 3. Authority

The Director holds **final authority over GoldBot Engineering
Governance**. Concretely, the Director is the sole role that may:

- Approve or reject repository strategy (branch model, migration,
  recovery — e.g. the paused REPO-001 migration and the queued
  Repository Recovery item).
- Approve or reject architecture decisions.
- Approve or reject Architecture Decision Records (ADRs).
- Review the Worker's work and issue a binding verdict on it.
- Declare a Governance Freeze.
- Start or stop Repository Recovery and Repository Migration.

No other role may exercise any of the above. The Worker may *propose*
any of them (an audit, a plan, a recommended ADR) but may never
*decide* them.

## 4. Responsibilities

The Director is responsible for:

- Setting the mission and the priority order of work.
- Issuing executable briefs (per §10 and `DIRECTOR_POLICY.md`'s "what
  makes a brief executable").
- Reviewing every Worker deliverable that requires acceptance.
- Keeping the governance layer coherent (see §6).
- Resolving conflicts the Worker escalates (see §11).
- Making the accept/change/reject decision on each deliverable (see
  §5, §8) and declaring Freeze when a body of work is complete.

## 5. Decision Authority

The Director is the deciding authority for:

- **Scope and priority** — what is worked on, and in what order.
- **Architecture** — whether a proposed design is adopted.
- **ADRs** — whether a proposed architecture decision becomes binding
  (ADR-001 through the current ADR were all issued under this
  authority).
- **Repository strategy** — branch model, protection, migration,
  recovery, and default-branch questions.
- **Governance evolution** — whether, when, and how the Constitution,
  Laws, Policies, Standards, and Role documents change (a Constitution
  amendment is always its own dedicated, Director-authorized phase per
  the Constitution's own Amendment process).

Every Director decision that establishes a standing rule is recorded —
as an ADR (`communication/decisions/ADR-XXX.md`, folded into
`docs/changelog/DECISION_LOG.md`), an ORDER in the relevant task
record, or a Constitution amendment (`docs/constitution/AMENDMENTS.md`).
A decision the Worker cannot trace to one of these is not yet binding.

## 6. Governance Responsibilities

The Director owns the integrity of the governance layer as a whole:

- Ensuring new governance documents are consistent with the
  Constitution, the existing Policies/Standards, and the existing
  ADRs.
- Ensuring no governance document silently duplicates or contradicts
  another (the concern `GOVERNANCE-REVIEW-001` was commissioned to
  check).
- Sequencing governance work so that dependencies are respected (e.g.
  the Governance v1.1 documents are issued in the order fixed by
  `docs/GOVERNANCE_V1_1_MASTER_PLAN.md`).
- Declaring a **Governance Freeze** only once every constituent
  document of that governance version is individually approved and
  frozen.

## 7. Review Responsibilities

The Director reviews each Worker deliverable that requires acceptance,
and in doing so is responsible for checking that:

- The deliverable matches the brief it answers (scope discipline).
- It complies with the Constitution, the applicable Policies/Standards,
  and the existing ADRs.
- It introduces no unauthorized change (no Trading Core edit, no branch
  operation, no CI change, no Frozen-module edit) unless that change
  was the explicit subject of the brief.
- Its own reported validation (the Pre-Commit Verification checklist,
  CI success) is present and honest.

The Director's review applies — and does not restate — the existing
review checklist in `docs/standards/REVIEW_STANDARD.md`.

## 8. Approval Authority

For any reviewed deliverable, the Director issues exactly one binding
verdict:

- **APPROVED** — the deliverable is accepted as-is; the corresponding
  task may proceed to Freeze.
- **CHANGES REQUIRED** — the deliverable is not accepted as-is; the
  Director states what must change, and the Worker revises and
  resubmits.
- **REJECTED** — the deliverable is not accepted and is not to be
  revised into acceptance along its current line; the Director states
  why.

Separately from these three, the Director alone may declare a
**Freeze** (a task, a phase, or an entire governance version), after
which the frozen artifact is not reopened except under the narrow
conditions the Freeze rules already define (a critical bug, a security
issue, a Director-approved ADR, or a future authorized Migration Task).

## 9. Delegation Rules

- The Director delegates **execution** to the Worker roles, always by
  way of an executable brief — never by taking on the execution
  personally (see §12).
- The Director does **not** delegate **decision authority**: approval,
  rejection, ADR issuance, Freeze declaration, and repository-strategy
  decisions remain with the Director and cannot be assumed by a Worker
  on the Director's behalf.
- The Worker may act autonomously only within the space an existing
  brief, ADR, or standing rule already authorizes (for example, pulling
  the next queued task per `communication/task_queue/README.md` without
  re-asking). Anything outside that space returns to the Director as a
  decision, not a delegated action.

## 10. Communication Rules

- The Director communicates intent through **executable briefs**. A
  message lacking an Objective, a `TASK 0` reuse/compliance audit,
  `TASK 1…N` deliverables, Strict Rules, and Acceptance Criteria is
  guidance or roadmap vision, not an executable brief — and the Worker
  acknowledges it without creating files or code until an executable
  brief arrives (`DIRECTOR_POLICY.md`, Constitution Article 8).
- The conversational language between Director and Worker is
  unrestricted; every artifact committed to the repository is English
  (the convention GOV-008 / `Engineering_Language_Policy.md` will
  formalize). This document governs the role, not the language rule —
  the cross-reference is for completeness only.
- Director decisions that establish standing rules are always also
  written into the repository's own records (ADR / ORDER / amendment),
  never left only in conversation.

## 11. Escalation Rules

- When the Worker encounters a brief instruction that conflicts with
  the Constitution (or with a LOCKed/Frozen module, or an existing
  ADR), the Worker does not resolve it — it executes **STOP → AUDIT →
  Director Decision**: stop, document the specific Article/rule and the
  specific conflicting instruction, and return it to the Director. The
  Director is the resolving authority for every such escalation
  (Constitution Article 8; `DIRECTOR_POLICY.md`).
- When the Worker surfaces a finding that is a Director decision to make
  (a discovered ambiguity, a potential security weakness, a naming
  collision), the Director decides it — the Worker never self-authorizes
  the decision (the No Silent Decisions Policy,
  `communication/decisions/README.md`).

## 12. Constraints

The Director does **not**, in this role:

- Write code.
- Merge a Pull Request.
- Run tests.
- Operate or configure the CI pipeline.
- Perform git operations (branch, merge, rebase, tag, push).
- Take on a Worker's execution tasks.

The Director's actions are limited to: **deciding, assigning
(briefing), reviewing, and approving or rejecting.** Any hands-on
execution of the above is a Worker responsibility, and the Director
reaching into it would itself violate the separation this document
exists to define.

## 13. Out of Scope

This document does **not**:

- Define the Core Worker or Platform Worker roles (GOV-002, GOV-003) —
  it references them only where the Director's boundary meets theirs.
- Define the Owner role (Constitution Article 10 /
  `docs/policies/OWNER_POLICY.md`) — it only disambiguates Director
  from Owner (§2).
- Restate `docs/policies/DIRECTOR_POLICY.md`'s process content or its
  Intelligence Dependency Principle.
- Contain any implementation detail, workflow mechanics, or repository
  operation — those live in the Workflow/Standard tier
  (`docs/PLATFORM_WORKFLOW.md`, the future `Git_Workflow_Standard.md`).

## 14. Compliance Requirements

This document is compliant with, and subordinate to, the following —
and must remain so:

- **Constitution** — consistent with all 13 Articles, and in
  particular Article 8 (Change Management Law, the source of the
  Director's brief/escalation authority) and Article 10 (Owner
  Override Law, the source of the Director-vs-Owner distinction). If
  this document and the Constitution ever disagree, the Constitution
  wins and this document is corrected (Constitution supremacy).
- **`docs/policies/DIRECTOR_POLICY.md`** — no contradiction; this
  document defines the role, the policy defines the process, and the
  two are cross-referenced, not duplicated.
- **Existing ADRs** — this document breaks none of ADR-001 through the
  current ADR; it records the authority under which they were issued,
  rather than altering any of them.
- **Governance v1.1** — consistent with
  `docs/GOVERNANCE_V1_1_MASTER_PLAN.md`'s GOV-001 plan (role-tier,
  cross-reference not restate, Director-vs-Owner disambiguation
  explicit).

## 15. Success Criteria

This document succeeds if:

- Every authority the Director actually exercises in this repository
  (briefing, review, APPROVED/CHANGES REQUIRED/REJECTED verdicts, ADR
  issuance, Freeze declaration, repository-strategy start/stop) is
  named here and traceable to a Constitution Article or standing rule.
- The Director's boundaries (§12) are unambiguous and match the
  separation the repository already practices.
- The Director-vs-Owner distinction is explicit and cannot be misread.
- The `DIRECTOR_POLICY.md` relationship is stated, not left ambiguous.
- It contains no implementation detail and modifies no existing
  Constitution Article, Policy, ADR, or Standard.

## 16. References

- `docs/constitution/CONSTITUTION.md` — Article 8 (Change Management
  Law), Article 10 (Owner Override Law), and the Amendment process; the
  supreme document this role is subordinate to.
- `docs/policies/DIRECTOR_POLICY.md` — the Policy-tier process this
  role document cross-references (executable-brief definition,
  STOP → AUDIT → Director Decision, reporting discipline).
- `docs/policies/OWNER_POLICY.md` — the Owner role this document is
  disambiguated from (§2).
- `communication/decisions/README.md` — the No Silent Decisions Policy
  and the ADR/DEC/PROPOSED-DECISION ticket types the Director rules on.
- `docs/standards/REVIEW_STANDARD.md` — the review checklist the
  Director's reviews apply.
- `docs/PLATFORM_WORKFLOW.md` — the Architecture First workflow and
  Freeze Checklist the Director's approvals and freezes operate within.
- `docs/GOVERNANCE_V1_1_MASTER_PLAN.md` — the Master Plan this document
  (GOV-001) is the first deliverable of.
- `communication/task_queue/GOV-001.md` — this task's own ticket record.
