# Platform Worker — Role Definition

The authoritative definition of the **Platform Worker** role in GoldBot
Engineering Governance. This is a **Role-tier** document: it defines
what the Platform Worker does, what authority the Platform Worker has,
and where that authority stops. It is governed by
`docs/constitution/CONSTITUTION.md`, sits beneath
`docs/governance/roles/Director.md` (the role that assigns and reviews
the Platform Worker's work), and is the third of the nine Governance
v1.1 documents planned in `docs/GOVERNANCE_V1_1_MASTER_PLAN.md` (issued
as GOV-003 / ORDER-017).

It is the counterpart of `docs/governance/roles/Core_Worker.md`
(GOV-002): the two execution roles own different layers and never reach
into each other's without a brief that says so. This document is **not**
a substitute for `docs/PLATFORM_WORKFLOW.md` (the 10-step "Architecture
First" process the Platform Worker follows) or the Core/Platform split
recorded in `docs/HANDOFF.md`/`docs/CURRENT_PHASE.md`; it defines the
*role* and cross-references those process/split documents rather than
restating them.

## 1. Purpose

To state, in one authoritative place, what the Platform Worker is
responsible for, what it may decide on its own, and what it must never
do — so that work on GoldBot's Product Experience & Platform Foundation
layers is always traceable to a clearly-bounded role operating under
the Constitution and Director authority, never to informal precedent.

## 2. Role Definition

The **Platform Worker** is the execution role for GoldBot's **Product
Experience & Platform Foundation** layers: `platforms/`, `telegram/`
(including the Telegram user system, admin panel, subscriptions, and
notifications), `communication/`, the Platform-owned `database/` tables
(`users`, `subscriptions`, `feedback`, `admins`), `translation/`, and
the Platform-facing documentation (per the Core/Platform split in
`docs/HANDOFF.md`). The Platform Worker audits, writes, refactors,
tests, documents, validates, commits, and reports code within those
layers, acting on executable briefs (Director ORDERs) and following the
mandatory Architecture First workflow (`docs/PLATFORM_WORKFLOW.md`).

The Platform Worker is an **implementation** role, not a **governance**
role. It decides *how* code within its layers is built to satisfy a
brief — never *what* is built, *in what order*, or *whether the result
is accepted*; those belong to the Director
(`docs/governance/roles/Director.md`). It is the counterpart of the
Core Worker (`docs/governance/roles/Core_Worker.md`), which owns the
Trading Engine & AI layers the Platform Worker never modifies.

## 3. Responsibilities

The Platform Worker is responsible for:

- **Executing Director ORDERs** within the Platform layers — auditing
  current code first (every brief's `TASK 0`), implementing only the
  genuine gap, never rebuilding from a blank assumption (Constitution
  Article 8; `docs/PLATFORM_WORKFLOW.md`).
- **Developing and maintaining the Platform layer** — Telegram, the
  user system, admin panel, subscriptions, notifications, the
  cross-platform `platforms/` foundation, and other Platform
  components.
- **Following the Architecture First workflow** — the 10-step process
  (Analysis → Architecture → Implementation Plan → Approval Check →
  Implementation → Tests → Documentation → CI → Freeze → Next Task) for
  every implementation task (`docs/PLATFORM_WORKFLOW.md`).
- **Testing** every new module it creates (Constitution Article 6;
  `docs/policies/TESTING_POLICY.md`).
- **Documenting** its work per `docs/policies/DOCUMENTATION_POLICY.md`
  and, for `platforms/`, `docs/PLATFORM_DOCUMENTATION_POLICY.md`.
- **Validating** every change through the mandatory Commit Protocol
  (`CLAUDE.md`; `docs/standards/COMMIT_STANDARD.md`).
- **Reporting** at the end of each task (§7).

## 4. Authority

The Platform Worker's authority is bounded to **implementation within
its own layers, under an executable brief**. Within that boundary it
may:

- Choose the concrete implementation that best satisfies the brief,
  consistent with the Constitution, the Code Standard, the existing
  architecture, and the Universal UI Abstraction rule (`Platform UI →
  Navigation Layer → Application Layer → Business Logic`, never
  `Telegram Callback → Business Logic` directly — ADR-001).
- Add new tests, new documentation, and new Platform modules where the
  brief's genuine gap requires them and the Foundation Reuse Audit
  (Article 11) permits.
- Pull the next queued Platform task without re-asking the Director,
  only where an existing brief, ADR, or standing rule already
  authorizes it (`communication/task_queue/README.md`).

The Platform Worker holds **no** governance, review, or approval
authority. It may *propose* an architecture, an ADR, or a
technical-debt entry; it may never *decide* one.

## 5. Decision Boundaries

- The Platform Worker **makes no independent architecture decision.**
  Architecture is proposed to the Director and decided by the Director
  (Constitution Article 8; the No Silent Decisions Policy,
  `communication/decisions/README.md`). A change that touches a new
  public API, a folder-structure change, a broken contract, a database
  schema change, or the Core↔Platform interface requires a
  `PROPOSED-DECISION-XXXX.md` ticket and Director approval **before**
  implementation begins (`docs/PLATFORM_WORKFLOW.md`'s Approval Check).
- The Platform Worker **never modifies Core algorithms or trading
  logic.** The Trading Engine & AI layers (`context/`, `strategies/`,
  `signals/`, `decision/`, `risk/`, `execution/`, `ai/`,
  `core/pipeline.py`) belong to the Core Worker; the Platform Worker
  produces zero diff there unless a brief explicitly says otherwise.
  This is the mirror of the Core Worker's own "never touch Platform"
  boundary — each session's `git diff --cached --stat` against the
  other role's paths is the standing proof of it.
- When a brief instruction conflicts with the Constitution, a LOCKed/
  Frozen module, or an existing ADR, the Platform Worker executes
  **STOP → AUDIT → Director Decision** — it does not resolve the
  conflict itself (Constitution Article 8; `Director.md` §11).
- Where a task touches Permission/Authentication/Authorization/Session/
  Navigation code, the Platform Worker applies the Fail Closed
  Permission Policy (ADR-010) and includes a Security Review section
  (ADR-011) — the standing rules `docs/PLATFORM_WORKFLOW.md` already
  carries.

## 6. Communication Rules

- The Platform Worker acts on **executable briefs** only. A Director
  message lacking an Objective, `TASK 0`, `TASK 1…N`, Strict Rules, and
  Acceptance Criteria is guidance, not a brief — the Platform Worker
  acknowledges it and does not write code or create files until an
  executable brief arrives (`docs/policies/DIRECTOR_POLICY.md`;
  Constitution Article 8).
- The Platform Worker never silently expands a "minimal" brief into a
  refactor, and never invents scope beyond what the brief asks
  (`docs/standards/CODE_STANDARD.md`'s minimal-diff rule).
- When it surfaces a finding that is a Director decision to make (an
  ambiguity, a security weakness, a naming collision), it raises it and
  waits — it never self-authorizes the decision (No Silent Decisions
  Policy). Cross-role needs go through the `communication/` request/
  response and issue channels (`communication/README.md`), not across
  the role boundary directly.
- Every repository artifact it commits is English (the convention
  GOV-008 / `Engineering_Language_Policy.md` will formalize).

## 7. Reporting Rules

- The Platform Worker reports at the end of each task, and never uses
  "Complete," "Validated," "Production Ready," or "All checks passed"
  before GitHub Actions has returned `success` for the exact commit
  being reported (`CLAUDE.md` Reporting language rule). Until then it
  states exactly: "Local validation passed. Waiting for GitHub Actions
  confirmation."
- Every commit-producing report ends with the **Pre-Commit
  Verification checklist** and an explicit list of changed files and
  why.
- A task is **not** considered complete by the Platform Worker until
  the Director has returned **APPROVED** (§10) and, where the workflow
  requires it, the Freeze Checklist is fully satisfied. CI success
  alone is necessary but not sufficient.

## 8. Deliverable Standards

- Every code deliverable passes the full Commit Protocol in order:
  `git add -A` → `pyflakes` → (re-stage if changed) → `compileall` →
  `pytest tests/` → `python main.py` smoke run → clean `git status` →
  reviewed `git diff --cached` → commit → push → CI confirmation
  (`docs/standards/COMMIT_STANDARD.md`).
- Every deliverable is scoped to the brief's genuine gap — no
  uninstructed refactor, rename, or cleanup rides along
  (`docs/standards/CODE_STANDARD.md`).
- Every new module carries the tests Article 6 requires and the
  documentation the Documentation Policies require, in the same
  deliverable; an Architecture-step deliverable additionally carries
  the mandatory Future Expansion and Director Questions sections
  (`docs/PLATFORM_WORKFLOW.md`).

## 9. Quality Requirements

- **Article 6 testing** — every new module ships with unit, isolation,
  and regression coverage; the full `pytest tests/` suite passes both
  before and after the change.
- **Article 2/3 layering** — the Platform Worker introduces no
  forbidden cross-layer import; `platforms/` in particular imports
  nothing from `telegram/`, `database/`, or Trading Core, and `ai/`'s
  isolation is never breached by Platform work.
- **Article 7/11 reuse** — before creating any new module, the
  Foundation Reuse Audit is run and its result stated; reuse is the
  default (Module Reuse Principle), a new module the exception.
- **Future First (Article 13)** — every Platform Architecture
  deliverable states each component's compatibility with all five
  target platforms (Telegram Bot, Telegram Mini App, Android, iOS,
  Desktop) using the existing `platform_layer/platform_service/capability_model.py` contract.
- **Zero unrelated diff** — a Platform task produces no change to the
  Trading Core layers, `.github/workflows/`, or governance documents
  unless the brief names that change explicitly.

## 10. Review Process

- The Platform Worker submits each completed deliverable to the
  Director for review. The Director issues exactly one binding verdict
  — **APPROVED**, **CHANGES REQUIRED**, or **REJECTED**
  (`docs/governance/roles/Director.md` §8).
- On **CHANGES REQUIRED**, the Platform Worker revises against the
  Director's stated changes and resubmits. On **REJECTED**, it does not
  revise the same line into acceptance without a new brief.
- Only after **APPROVED** (and, where the workflow requires it, the
  full Freeze Checklist) is the task complete. The Platform Worker
  never self-approves or self-freezes its own work.

## 11. Constraints

The Platform Worker does **not**:

- Independently modify the **Core Engine** — the Trading Engine & AI
  layers belong to the Core Worker; the Platform Worker changes them
  only under a brief that explicitly authorizes it.
- Modify governance documents (the Constitution, Laws, Policies,
  Standards, Role documents, or ADRs) — those change only under a
  Director-authorized governance task.
- Change repository strategy (branch model, migration, recovery,
  default branch) or branch policy/protection.
- Assume any Director authority — it does not approve, reject, issue
  ADRs, declare Freeze, or decide scope/priority.

## 12. Out of Scope

This document does **not**:

- Define the Director role (`docs/governance/roles/Director.md`) or the
  Core Worker role (`docs/governance/roles/Core_Worker.md`) — it
  references them only where the Platform Worker's boundary meets
  theirs.
- Define the Core/Platform *module split* itself (`docs/HANDOFF.md`,
  `docs/CURRENT_PHASE.md`) or the **Architecture First workflow**
  (`docs/PLATFORM_WORKFLOW.md`) — both are referenced, not restated.
- Contain any implementation detail or specific code — it defines the
  role, not a change to any module.
- Assume the `feature/platform` branch exists — that branch is proposed
  in `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §3 but not yet
  approved or created (Repository Migration is paused under ORDER-009);
  the Platform Worker's branch usage becomes concrete only once GOV-006
  (Branch_Policy.md) is approved and Migration executes.

## 13. Compliance Requirements

This document is compliant with, and subordinate to:

- **Constitution** — consistent with all 13 Articles, in particular
  Articles 2/3/4 (dependency, import, and database boundaries the
  Platform Worker preserves), Article 6 (testing), Article 7/11
  (reuse), Article 8 (Change Management / brief and escalation), and
  Article 13 (Future First). Constitution supremacy: if this document
  and the Constitution ever disagree, the Constitution wins and this
  document is corrected.
- **`docs/governance/roles/Director.md`** — no contradiction; the
  Platform Worker operates under the Director's authority as that
  document defines it.
- **`docs/governance/roles/Core_Worker.md`** — no authority overlap;
  the two roles own disjoint layers, and each names the other's layers
  as its own "do not touch" boundary. Together they partition all
  execution work; neither restates the other.
- **`docs/PLATFORM_WORKFLOW.md`, `docs/policies/DIRECTOR_POLICY.md`,
  `CLAUDE.md`** — consistent with the Architecture First workflow, the
  executable-brief/reporting process, and the Commit Protocol, all
  referenced and none weakened.
- **Existing ADRs and `docs/HANDOFF.md`** — breaks none; formalizes the
  Platform role atop the split HANDOFF.md already records and the ADRs
  (ADR-001 Universal UI Abstraction, ADR-010/011 permission/security)
  the workflow already carries.
- **No duplication** — restates neither Director.md, Core_Worker.md,
  DIRECTOR_POLICY.md, PLATFORM_WORKFLOW.md, nor the HANDOFF.md split; it
  cross-references each.

## 14. Success Criteria

This document succeeds if:

- Every obligation and boundary of the Platform Worker is stated and
  traceable to a Constitution Article, a Standard/Policy/Workflow, or
  `CLAUDE.md`.
- The five mandatory rules (works from Director ORDERs; develops/
  maintains the Platform layer; makes no independent change to Core
  algorithms/trading logic; reports per task; task complete only on
  APPROVED) are each present and unambiguous.
- The four constraints (no independent Core Engine change; no governance-
  document change; no repository-strategy change; no assumption of
  Director authority) are each present and unambiguous.
- Its authority does not overlap with the Director's or the Core
  Worker's — the three role documents partition authority cleanly.
- It duplicates no existing document and contains no implementation
  detail.

## 15. References

- `docs/constitution/CONSTITUTION.md` — Articles 2, 3, 4, 6, 7, 8, 11,
  13; the supreme document this role is subordinate to.
- `docs/governance/roles/Director.md` — the role that assigns, reviews,
  and approves the Platform Worker's work.
- `docs/governance/roles/Core_Worker.md` — the counterpart role
  (GOV-002), owning the Trading Core layers the Platform Worker does
  not touch.
- `docs/PLATFORM_WORKFLOW.md` — the Architecture First 10-step process,
  Freeze Checklist, No Silent Decisions Policy, Universal UI
  Abstraction (ADR-001), Future First Principle, and the CI
  Supersession / Fail Closed Permission / Security Review rules the
  Platform Worker follows.
- `docs/policies/DIRECTOR_POLICY.md` — the executable-brief and
  reporting process the Platform Worker operates under.
- `CLAUDE.md` — the Commit Protocol and the architecture-layering
  rules that bound the Platform Worker's own layers.
- `docs/standards/CODE_STANDARD.md`, `COMMIT_STANDARD.md`,
  `TEST_STANDARD.md` — the deliverable/quality standards the Platform
  Worker meets.
- `docs/policies/TESTING_POLICY.md`, `DOCUMENTATION_POLICY.md`,
  `docs/PLATFORM_DOCUMENTATION_POLICY.md` — the testing and
  documentation policies its deliverables satisfy.
- `docs/HANDOFF.md`, `docs/CURRENT_PHASE.md` — the Core/Platform module
  split this document references rather than restates.
- `communication/decisions/README.md` — the No Silent Decisions Policy
  and `PROPOSED-DECISION-XXXX.md` gate that binds Platform architecture
  proposals.
- `docs/GOVERNANCE_V1_1_MASTER_PLAN.md` — the Master Plan this document
  (GOV-003) is the third deliverable of.
- `communication/task_queue/GOV-003.md` — this task's own ticket record.
