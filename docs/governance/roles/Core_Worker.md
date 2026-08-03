# Core Worker — Role Definition

The authoritative definition of the **Core Worker** role in GoldBot
Engineering Governance. This is a **Role-tier** document: it defines
what the Core Worker does, what authority the Core Worker has, and
where that authority stops. It is governed by
`docs/constitution/CONSTITUTION.md`, sits beneath
`docs/governance/roles/Director.md` (the role that assigns and reviews
the Core Worker's work), and is the second of the nine Governance v1.1
documents planned in `docs/GOVERNANCE_V1_1_MASTER_PLAN.md` (issued as
GOV-002 / ORDER-016).

It is **not** a substitute for the existing Core/Platform split already
recorded in `docs/HANDOFF.md` and `docs/CURRENT_PHASE.md`'s "Role
boundary" section. Those describe *which modules* Core owns as a
practical handoff fact; this document formalizes the *role* — its
authority, obligations, and boundaries — and cross-references that
split rather than restating or replacing it. Where they touch the same
subject, `HANDOFF.md`'s module list remains the practical reference and
this document governs the role.

## 1. Purpose

To state, in one authoritative place, what the Core Worker is
responsible for, what it may decide on its own, and what it must never
do — so that work on GoldBot's Trading Engine & AI layers is always
traceable to a clearly-bounded role operating under the Constitution
and Director authority, never to informal precedent.

## 2. Role Definition

The **Core Worker** is the execution role for GoldBot's **Trading
Engine & AI** layers: `context/`, `strategies/`, `signals/`,
`decision/`, `risk/`, `execution/`, `ai/`, `core/pipeline.py`, and the
Trading-owned parts of `database/` (per the Core/Platform split in
`docs/HANDOFF.md`). The Core Worker audits, writes, refactors, tests,
documents, validates, commits, and reports code within those layers,
acting on executable briefs (Director ORDERs).

The Core Worker is an **implementation** role, not a **governance**
role. It decides *how* code within its layers is built to satisfy a
brief — never *what* is built, *in what order*, or *whether the result
is accepted*; those belong to the Director
(`docs/governance/roles/Director.md`). The Core Worker is the
counterpart of the Platform Worker
(`docs/governance/roles/Platform_Worker.md`, GOV-003), which owns the
Product Experience & Platform Foundation layers; the two never reach
into each other's layers without a brief that says so.

## 3. Responsibilities

The Core Worker is responsible for:

- **Executing Director ORDERs** within the Trading Engine & AI layers —
  auditing current code first (every brief's `TASK 0`), implementing
  only the genuine gap, never rebuilding from a blank assumption
  (Constitution Article 8).
- **Writing, refactoring, and implementing** code in its layers to the
  standard of `docs/standards/CODE_STANDARD.md`.
- **Testing** every new module it creates (unit, isolation, regression
  — Constitution Article 6, `docs/policies/TESTING_POLICY.md`).
- **Documenting** its work per `docs/policies/DOCUMENTATION_POLICY.md`.
- **Validating** every change through the mandatory Commit Protocol
  (`CLAUDE.md`; `docs/standards/COMMIT_STANDARD.md`).
- **Reporting** at the end of each task (§7).

## 4. Authority

The Core Worker's authority is bounded to **implementation within its
own layers, under an executable brief**. Within that boundary it may:

- Choose the concrete implementation that best satisfies the brief
  (data structures, function shapes, internal refactoring) consistent
  with the Constitution, the Code Standard, and the existing
  architecture.
- Add new tests, new documentation, and new non-safety-critical modules
  where the brief's genuine gap requires them and the Foundation Reuse
  Audit (Article 11) permits.
- Pull the next queued Core task without re-asking the Director, only
  where an existing brief, ADR, or standing rule already authorizes it
  (`communication/task_queue/README.md`).

The Core Worker holds **no** governance, review, or approval authority.
It may *propose* an architecture, an ADR, or a technical-debt entry;
it may never *decide* one.

## 5. Decision Boundaries

- The Core Worker **makes no independent architecture decision.**
  Architecture is proposed to the Director and decided by the Director
  (Constitution Article 8; the No Silent Decisions Policy,
  `communication/decisions/README.md`). A change that touches a new
  public API, a folder-structure change, a broken contract, a database
  schema change, or the Core↔Platform interface requires a
  `PROPOSED-DECISION-XXXX.md` ticket and Director approval **before**
  implementation begins.
- **Trading Safety is an absolute boundary.** Even within its own
  layers, the Core Worker must never modify — without the Director's
  explicit approval for that specific change — signal logic
  (`strategies/`, `signals/`), risk limits (`risk_layer/risk_engine/risk_manager.py`'s
  geometry/stop-loss validation and sizing), or decision flow
  (`decision_layer/decision_engine/decision_engine.py`'s confidence-blending and
  APPROVE/REJECT/NO_TRADE thresholds); and it must never bypass the
  Risk Manager, never give the AI layer direct execution/decision/
  Telegram authority, and never wire up `execution/` (intentionally
  inert) as a routine change (`CLAUDE.md` Trading Safety; Constitution
  Articles 1, 3). These are the exact modules the Core Worker touches
  most, which is precisely why the boundary is stated here.
- When a brief instruction conflicts with the Constitution, a LOCKed/
  Frozen module, or an existing ADR, the Core Worker executes
  **STOP → AUDIT → Director Decision** — it does not resolve the
  conflict itself (Constitution Article 8; `Director.md` §11).

## 6. Communication Rules

- The Core Worker acts on **executable briefs** only. A Director
  message lacking an Objective, `TASK 0`, `TASK 1…N`, Strict Rules, and
  Acceptance Criteria is guidance, not a brief — the Core Worker
  acknowledges it and does not write code or create files until an
  executable brief arrives (`docs/policies/DIRECTOR_POLICY.md`;
  Constitution Article 8).
- The Core Worker never silently expands a "minimal" brief into a
  refactor, and never invents scope beyond what the brief asks
  (`docs/standards/CODE_STANDARD.md`'s minimal-diff rule).
- When it needs something only the Platform Worker or Core can provide,
  or surfaces a cross-role concern, it uses the `communication/`
  request/response and issue channels
  (`communication/README.md`) rather than reaching across the role
  boundary itself.
- Every repository artifact it commits is English (the convention
  GOV-008 / `Engineering_Language_Policy.md` will formalize).

## 7. Reporting Rules

- The Core Worker reports at the end of each task, and never uses
  "Complete," "Validated," "Production Ready," or "All checks passed"
  before GitHub Actions has returned `success` for the exact commit
  being reported (`CLAUDE.md` Reporting language rule;
  `docs/policies/DIRECTOR_POLICY.md`). Until then it states exactly:
  "Local validation passed. Waiting for GitHub Actions confirmation."
- Every commit-producing report ends with the **Pre-Commit
  Verification checklist** and an explicit list of changed files and
  why.
- A task is **not** considered complete by the Core Worker until the
  Director has returned **APPROVED** (§10). CI success alone is
  necessary but not sufficient.

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
  documentation `DOCUMENTATION_POLICY.md` requires, in the same
  deliverable.

## 9. Quality Requirements

- **Article 6 testing** — every new module ships with unit, isolation
  (proof it introduces no forbidden cross-layer import, especially the
  `ai/` → `decision`/`risk`/`execution` prohibition of Article 3), and
  regression coverage; the full `pytest tests/` suite passes both
  before and after the change.
- **Article 2/3 layering** — dependency flows forward only; the Core
  Worker introduces no backward or forbidden import.
- **Article 7/11 reuse** — before creating any new module, the
  Foundation Reuse Audit is run and its result stated; reuse is the
  default, a new module the exception.
- **Zero unrelated diff** — a Core task produces no change to the
  Platform layers (`telegram/`, `platforms/`, `communication/`),
  `.github/workflows/`, or governance documents unless the brief names
  that change explicitly.

## 10. Review Process

- The Core Worker submits each completed deliverable to the Director
  for review. The Director issues exactly one binding verdict —
  **APPROVED**, **CHANGES REQUIRED**, or **REJECTED**
  (`docs/governance/roles/Director.md` §8).
- On **CHANGES REQUIRED**, the Core Worker revises against the
  Director's stated changes and resubmits. On **REJECTED**, it does not
  revise the same line into acceptance without a new brief.
- Only after **APPROVED** (and, where applicable, Freeze) is the task
  complete. The Core Worker never self-approves or self-freezes its own
  work.

## 11. Constraints

The Core Worker does **not**:

- Independently modify governance documents (the Constitution,
  Laws, Policies, Standards, Role documents, or ADRs) — those change
  only under a Director-authorized governance task.
- Change repository strategy (branch model, migration, recovery,
  default branch).
- Change branch policy or branch protection.
- Assume any Director authority — it does not approve, reject, issue
  ADRs, declare Freeze, or decide scope/priority.
- Make an independent architecture decision, bypass the Risk Manager,
  or modify a Trading-Safety-critical module without explicit
  per-change Director approval (§5).

## 12. Out of Scope

This document does **not**:

- Define the Director role (`docs/governance/roles/Director.md`) or the
  Platform Worker role (`docs/governance/roles/Platform_Worker.md`) —
  it references them only where the Core Worker's boundary meets
  theirs.
- Define the Core/Platform *module split* itself — that is recorded in
  `docs/HANDOFF.md` and `docs/CURRENT_PHASE.md` and referenced here,
  not restated.
- Define a Core-specific workflow document — day-to-day mechanics live
  in the universal disciplines (`CLAUDE.md` Commit Protocol,
  `docs/standards/*`) and, for branch mechanics, the future
  `Git_Workflow_Standard.md` (GOV-009); if a Core-specific workflow is
  ever needed it is its own separate task, not this one.
- Contain any implementation detail or specific code — it defines the
  role, not a change to any module.
- Assume the `feature/core` branch exists — that branch is proposed in
  `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §3 but not yet
  approved or created (Repository Migration is paused under ORDER-009);
  the Core Worker's branch usage becomes concrete only once GOV-006
  (Branch_Policy.md) is approved and Migration executes.

## 13. Compliance Requirements

This document is compliant with, and subordinate to:

- **Constitution** — consistent with all 13 Articles, in particular
  Article 1 (Trading Engine ≠ AI Engine), Articles 2/3 (dependency and
  import direction the Core Worker must preserve), Article 6 (testing),
  Article 7/11 (reuse), and Article 8 (Change Management / the brief and
  escalation model). Constitution supremacy: if this document and the
  Constitution ever disagree, the Constitution wins and this document
  is corrected.
- **`docs/governance/roles/Director.md`** — no contradiction; the Core
  Worker operates under the Director's authority as that document
  defines it.
- **`docs/policies/DIRECTOR_POLICY.md`** — consistent with the
  executable-brief, STOP → AUDIT → Director Decision, and reporting-
  discipline process it defines.
- **`CLAUDE.md`** — consistent with its Trading Safety rules and Commit
  Protocol, which this document references and does not weaken.
- **Existing ADRs and `docs/HANDOFF.md`** — breaks none; formalizes the
  Core role atop the split HANDOFF.md already records.
- **No duplication** — this document restates neither Director.md,
  Platform_Worker.md, DIRECTOR_POLICY.md, nor the HANDOFF.md module
  split; it cross-references each.

## 14. Success Criteria

This document succeeds if:

- Every obligation and boundary of the Core Worker is stated and
  traceable to a Constitution Article, a Standard/Policy, or
  `CLAUDE.md`.
- The five mandatory rules (works from Director ORDERs; no independent
  architecture decision; writes code/refactoring/implementation;
  reports per task; task complete only on APPROVED) are each present
  and unambiguous.
- The four constraints (no independent governance change; no repository-
  strategy change; no branch-policy change; no assumption of Director
  authority) are each present and unambiguous.
- The Trading-Safety boundary is stated explicitly, since the Core
  Worker is the role that touches those modules.
- It duplicates no existing document and contains no implementation
  detail.

## 15. References

- `docs/constitution/CONSTITUTION.md` — Articles 1, 2, 3, 6, 7, 8, 11;
  the supreme document this role is subordinate to.
- `docs/governance/roles/Director.md` — the role that assigns, reviews,
  and approves the Core Worker's work.
- `docs/governance/roles/Platform_Worker.md` — the counterpart role
  (GOV-003), owning the Platform layers the Core Worker does not touch.
- `docs/policies/DIRECTOR_POLICY.md` — the executable-brief and
  reporting process the Core Worker operates under.
- `CLAUDE.md` — the Commit Protocol and the Trading Safety rules that
  bound the Core Worker's own layers.
- `docs/standards/CODE_STANDARD.md`, `COMMIT_STANDARD.md`,
  `TEST_STANDARD.md` — the deliverable/quality standards the Core
  Worker meets.
- `docs/policies/TESTING_POLICY.md`, `DOCUMENTATION_POLICY.md` — the
  testing and documentation policies its deliverables satisfy.
- `docs/HANDOFF.md`, `docs/CURRENT_PHASE.md` — the Core/Platform module
  split this document references rather than restates.
- `communication/decisions/README.md` — the No Silent Decisions Policy
  and `PROPOSED-DECISION-XXXX.md` gate that binds Core architecture
  proposals.
- `docs/GOVERNANCE_V1_1_MASTER_PLAN.md` — the Master Plan this document
  (GOV-002) is the second deliverable of.
- `communication/task_queue/GOV-002.md` — this task's own ticket record.
