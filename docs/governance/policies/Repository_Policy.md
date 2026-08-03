# Repository Policy

The authoritative policy for how the GoldBot repository itself is
governed: its structure, ownership, lifecycle, freeze, recovery,
migration, backup, and audit. It is governed by
`docs/constitution/CONSTITUTION.md`, sits within Engineering Governance
v1.1 (`docs/GOVERNANCE_V1_1_MASTER_PLAN.md`, GOV-005 / ORDER-019), and
formalizes as standing policy the facts established by the
already-delivered `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
and `docs/BRANCH_FORENSICS_001.md` audits.

It is the **repository-level** policy. Branch specifics are governed by
`docs/governance/policies/Branch_Policy.md` (GOV-006) and
`docs/governance/policies/Branch_Protection_Policy.md` (GOV-007); git
mechanics by `docs/governance/standards/Git_Workflow_Standard.md`
(GOV-009). This document references those rather than restating them,
and does not itself perform any repository operation.

## 1. Purpose

To make the governance of the repository — who may change what, how a
change is accepted, and how the repository is frozen, recovered,
migrated, backed up, and audited — explicit and standing, so that
repository-level decisions are never reconstructed from scattered
phase-audit documents and workflow-file comments again (the exact gap
`REPO-001` was commissioned to close).

## 2. Repository Structure

- The repository holds GoldBot's full codebase (Trading Core & AI
  layers, Platform layers) and its governance layer
  (`docs/constitution/`, `docs/policies/`, `docs/standards/`,
  `docs/governance/`, `communication/`).
- **Default branch vs. production branch are distinct today.** `main`
  is the configured default branch but is *not* the production branch;
  the production branch (`claude/code-analysis-optimization-pwfo3q`) is
  what `trading_bot.yml` and `production_deploy.yml` actually run, per
  `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §0–§1. The target
  branch model (`main`/`develop`/`feature/core`/`feature/platform`) is
  ratified by `Branch_Policy.md` and takes effect only when Repository
  Migration executes.
- Governance documents are the single source of truth for their
  subject; code and docs cross-reference rather than duplicate.

## 3. Repository Ownership

- The **Director** owns repository strategy: what changes to the
  repository's structure, branches, protection, and default branch are
  made, and when (`docs/governance/roles/Director.md`).
- The **Core Worker** and **Platform Worker** own changes *within*
  their respective code layers, under Director Orders; neither changes
  repository strategy (`docs/governance/roles/Core_Worker.md`,
  `Platform_Worker.md`).
- No participant performs a repository-strategy action (branch create/
  delete, merge to a protected branch, protection change, default-branch
  change) except under a Director Order authorizing that specific
  action.

## 4. Repository Governance

- Every repository-level change follows the Constitution's order
  (Article 8): Constitution → Architecture → Roadmap → Policy → Audit →
  Code. A repository change is audited (an existing state audit like
  `REPO-001`/`BRANCH-FORENSICS-001`) before it is planned, and planned
  before it is executed.
- Reserved decisions (branch-model change, default-branch change,
  protection change) require Director approval; a Worker never
  self-authorizes them (No Silent Decisions,
  `communication/decisions/README.md`).
- Repository-affecting decisions are recorded (ADR / ORDER / this
  policy's own updates) — traceability applies.

## 5. Repository Lifecycle

A repository-level change moves through: **Audit** (establish the real
current state) → **Plan** (a migration/recovery plan, Director-reviewed)
→ **Approval** (Director Order authorizing execution) → **Execution**
(under the normal Commit Protocol) → **Verification** (CI + a fresh
state re-check) → **Freeze/record**. `REPO-001` (audit + plan) and
`BRANCH-FORENSICS-001` (root-cause audit) are the current, delivered
Audit/Plan stages; Execution (REPO-002) is not authorized until the
Director lifts the relevant pause.

## 6. Repository Freeze

- A **Repository Freeze** is a Director declaration that the
  repository's structure/branches are not to be changed until the
  Freeze is lifted — for example the current ORDER-009 pause on
  Repository Migration.
- While a Repository Freeze is in effect, no branch is created,
  deleted, merged to a protected branch, renamed, or re-pointed, and
  the default branch is not changed. Ordinary code work within the
  existing branch structure continues unless the Freeze says otherwise.
- Only the Director lifts a Repository Freeze, by an explicit Order.

## 7. Repository Recovery

- **Repository Recovery** is the correction of a repository-integrity
  problem (e.g. the corrupted-filename merge conflict diagnosed in
  `docs/BRANCH_FORENSICS_001.md` — a single invisible U+2060 character
  in `strategy_layer/strategy_manager/strategy_manager.py`).
- Recovery is **audit-first**: the root cause is established before any
  fix (done — `BRANCH-FORENSICS-001`), a rollback anchor is created
  first (tagging, per `Git_Workflow_Standard.md`), the minimal
  content-neutral fix is applied, and the result is re-verified (a
  fresh `git merge-tree`/state check) before anything downstream
  proceeds.
- Recovery begins only under a Director Order (currently ORDER-010:
  Repository Recovery is queued to the backlog, to run as the first
  implementation item after Governance v1.1 is frozen).

## 8. Repository Migration

- **Repository Migration** is the transition to the ratified branch
  model (`main`/`develop`/`feature/core`/`feature/platform`,
  `Branch_Policy.md`) and its protection (`Branch_Protection_Policy.md`).
- Migration is a distinct, Director-authorized project phase (REPO-002),
  never a side effect of another task — mirroring ADR-005's
  Migration-Task discipline (Backward Compatibility plan, Rollback
  plan, full Architecture-First sequence, no modification of frozen
  history without authorization).
- Migration is currently **paused** (ORDER-009) and resumes only after
  Governance v1.1 is frozen and Repository Recovery completes. Its
  highest risk — breaking the live trading/deploy pipelines that pin the
  production branch by name — is mitigated by sequencing the workflow-
  file ref updates before/atomically with any branch rename or delete
  (`REPO-001` §8).

## 9. Repository Backup Policy

- The repository's own git history on the remote is the primary
  durable record; every branch tip is recoverable from it.
- Before any structural change (migration, recovery, a rename), a
  **rollback anchor** is created first — an annotated git tag on the
  affected branch tip(s) — so a known-good state is always nameable.
  This closes the "zero tags / zero releases / no rollback anchor" gap
  both `REPO-001` §1 and `BRANCH-FORENSICS-001` identified. Tag
  mechanics are defined in `Git_Workflow_Standard.md`.
- No backup mechanism stores secrets: `.env`/credential files are never
  committed (Constitution Article 4 / `docs/policies/SECURITY_POLICY.md`).

## 10. Repository Audit

- The repository's real state (branches, PRs, protection, tags,
  workflows, divergence) is established by direct inspection (GitHub API
  + git plumbing), never by assumption — the method `REPO-001` and
  `BRANCH-FORENSICS-001` used.
- A repository audit precedes every repository-level change (Article 8),
  and a fresh state re-check precedes execution, since best-effort audit
  facts can go stale between plan and execution.

## 11. Documentation Policy

- Repository-level facts have a single source of truth: this policy for
  governance, `Branch_Policy.md` for branches, `Branch_Protection_Policy.md`
  for protection, `Git_Workflow_Standard.md` for git mechanics. Audit
  reports (`REPO-001`, `BRANCH-FORENSICS-001`) are the evidence these
  policies formalize and are cross-referenced, not restated.
- Honesty over completeness: where the repository's real state differs
  from an ideal (default branch ≠ production branch today), the
  documentation states it plainly (`docs/policies/DOCUMENTATION_POLICY.md`).

## 12. Constraints

This policy, and any Worker acting under it, does **not**:

- Modify the Constitution or rewrite an existing Policy.
- Perform any repository operation (branch, merge, tag, protection,
  default-branch change) — this document defines governance, not
  execution.
- Restate `Branch_Policy.md`, `Branch_Protection_Policy.md`, or
  `Git_Workflow_Standard.md` — it references them.
- Lift any active Repository Freeze or authorize Recovery/Migration —
  those are Director Orders.

## 13. Out of Scope

- The specific branch model and naming (`Branch_Policy.md`, GOV-006).
- Protection rules and rollback mechanics detail
  (`Branch_Protection_Policy.md`, GOV-007).
- Commit/merge/tag/release/hotfix git mechanics
  (`Git_Workflow_Standard.md`, GOV-009).
- CI pipeline content (`.github/workflows/*.yml`) — untouched here and
  changed only under separate explicit authorization.

## 14. Compliance

- **Constitution** — consistent with all Articles, in particular
  Article 8 (change order) and Article 9 (a LOCKed/Frozen state is not
  changed without the STOP → AUDIT → Director Decision protocol).
  Constitution supremacy applies.
- **ADRs** — consistent with ADR-005 (Migration-Task discipline) and
  ADR-009 (CI validation); breaks none.
- **Governance v1.1** — no contradiction with the role documents or
  `Collaboration_Rules.md`; no duplication of their content.
- **`REPO-001`, `BRANCH-FORENSICS-001`, `docs/TECHNICAL_DEBT.md`** —
  formalizes their findings as policy; cross-references, does not
  restate.

## 15. References

- `docs/constitution/CONSTITUTION.md` — Articles 4, 8, 9.
- `docs/governance/roles/Director.md`, `Core_Worker.md`,
  `Platform_Worker.md`, `Collaboration_Rules.md` — the roles and
  collaboration model this policy operates within.
- `docs/governance/policies/Branch_Policy.md`,
  `Branch_Protection_Policy.md`;
  `docs/governance/standards/Git_Workflow_Standard.md` — the
  branch/protection/git specifics this policy defers to.
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`,
  `docs/BRANCH_FORENSICS_001.md` — the audits this policy formalizes.
- `docs/PHASE_BRANCH_SYNC_AUDIT.md`, `docs/PHASE_P1_AUDIT.md`,
  `docs/DEPLOYMENT.md` — prior records of the production-branch decision.
- `docs/TECHNICAL_DEBT.md` — the queued Security Backlog and
  `owner_snapshot.yml` items.
- `communication/decisions/README.md` — the No Silent Decisions Policy.
- `communication/task_queue/GOV-PACKAGE-001.md` — this package's ticket.
