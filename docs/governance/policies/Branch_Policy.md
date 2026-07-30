# Branch Policy

The authoritative policy for GoldBot's branch model: which branches are
official, how they are named, created, integrated, merged, cleaned up,
and archived. It is governed by `docs/constitution/CONSTITUTION.md`,
sits within Engineering Governance v1.1 (GOV-006 / ORDER-019) beneath
`docs/governance/policies/Repository_Policy.md`, and ratifies as
standing policy the branch model proposed in
`docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §3–§4.

This policy **defines the branch model**; it does not create, delete,
or re-point any branch. Protection of these branches is governed by
`Branch_Protection_Policy.md` (GOV-007); the git mechanics of using
them by `Git_Workflow_Standard.md` (GOV-009).

## 1. Purpose

To fix, as standing policy, what the official branches are and the
rules for their whole lifecycle — so branch decisions are consistent
and traceable, and the transition from today's session-named branches
to a conventional model has a written target to migrate toward.

## 2. Official Branches

The ratified target model (takes effect when Repository Migration
executes; **not yet created** — Migration paused under ORDER-009):

| Branch | Role |
|---|---|
| `main` | The single source of truth for what is production-ready. Every commit is releasable. Reached only by a reviewed, CI-passed merge from `develop`. |
| `develop` | The integration branch where Core and Platform output meets. CI-gated; Worker-mergeable without a per-merge Director review. |
| `feature/core` | The Core Worker's line — Trading Engine & AI layers. |
| `feature/platform` | The Platform Worker's line — Product Experience & Platform Foundation layers. |

**Current reality (pre-migration), stated honestly**: the repository
today has `main` (configured default, not production), the production
branch (`claude/code-analysis-optimization-pwfo3q`), and the active
working branch (`claude/trading-ai-arch-review-tgszrz`). The mapping
from today's branches to the model above is executed by Repository
Migration (REPO-002), not by this policy
(`docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §4).

## 3. Branch Naming Standard

- `main` and `develop` are fixed, lowercase, singular names.
- Feature branches follow `feature/<owner>` for the two standing role
  lines (`feature/core`, `feature/platform`), or `feature/<short-topic>`
  (lowercase, hyphen-separated, ASCII only) for a scoped, temporary
  feature branch.
- Every branch name is ASCII English with no whitespace and no invisible
  Unicode characters — a rule stated explicitly because an invisible
  U+2060 character in a *filename* was the exact root cause of the
  repository's only merge conflict (`docs/BRANCH_FORENSICS_001.md`);
  the same zero-tolerance for invisible/nonstandard characters applies
  to branch names. (Language of names: `Engineering_Language_Policy.md`,
  GOV-008.)

## 4. Branch Lifecycle

A branch moves through: **Create** (from the correct base, under §5) →
**Develop** (commits under the Commit Protocol) → **Integrate** (merge
to `develop`, §6) → **Promote** (`develop` → `main`, §7, Director-
reviewed) → **Cleanup/Archive** (§8–§9). `main` and `develop` are
permanent; feature branches are temporary.

## 5. Feature Branch Rules

- A feature branch is created when a Director Order assigns work whose
  layer maps to that line (`feature/core` for Core work,
  `feature/platform` for Platform work), or a scoped `feature/<topic>`
  for a bounded piece of work.
- It is branched from the correct base (`develop` for the target model),
  carries only work for its own layer/topic, and never mixes Core and
  Platform changes.
- Branch creation itself is a repository operation performed only under
  a Director Order (`Repository_Policy.md` §3), never speculatively.

## 6. Integration Rules

- Feature branches integrate into `develop` via a Pull Request; CI must
  pass. Per-merge Director review is not required to reach `develop`
  (that is the point of the integration branch), but the No Silent
  Decisions gate still applies to any reserved decision the change
  contains.
- `develop` is never force-integrated; conflicts are resolved on the
  feature branch and re-verified before the PR merges.

## 7. Merge Rules

- The only path to `main` is a merge from `develop`, and it is always
  Director-reviewed and CI-passed (`Branch_Protection_Policy.md` §4).
- Merge mechanics (merge vs. squash vs. rebase) are defined in
  `Git_Workflow_Standard.md` §5; this policy fixes *who* may merge to
  *which* branch and *under what gate*, not the git command detail.
- A merge that would break a LOCKed/Frozen module or an ADR triggers
  STOP → AUDIT → Director Decision (Constitution Article 8/9).

## 8. Branch Cleanup

- A feature branch is deleted **only** after `develop` is confirmed to
  contain every commit it holds (a verification step, not an
  assumption), and only under a Director Order authorizing the deletion
  (`Repository_Policy.md` §3).
- The two current session-named branches
  (`claude/code-analysis-optimization-pwfo3q`,
  `claude/trading-ai-arch-review-tgszrz`) are load-bearing today and
  are cleaned up only as an explicit, verified step of Repository
  Migration (`REPO-001` §7) — never before, and never as a side effect.

## 9. Archive Rules

- History worth preserving beyond a deleted branch is captured by an
  annotated **tag** (a rollback anchor), not by keeping a stale branch
  alive (`Git_Workflow_Standard.md` §10, `Repository_Policy.md` §9).
- No separate long-lived archive branch is maintained unless a Director
  Order establishes one for a specific, stated reason.

## 10. Constraints

This policy, and any Worker acting under it, does **not**:

- Create, delete, rename, or re-point any branch — it defines the
  model, not the operation.
- Modify the Constitution or rewrite an existing Policy.
- Change branch protection (`Branch_Protection_Policy.md`) or git
  mechanics (`Git_Workflow_Standard.md`) — it references them.
- Take effect as a live branch structure before Repository Migration is
  Director-authorized and executed.

## 11. Compliance

- **Constitution** — consistent with Article 8 (change order) and
  Article 9 (no unauthorized change to a frozen state). Supremacy
  applies.
- **ADRs** — consistent with ADR-005 (Migration discipline); breaks
  none.
- **Governance v1.1** — no contradiction with the role documents,
  `Collaboration_Rules.md`, or `Repository_Policy.md`; no duplication.
- **`REPO-001`, `BRANCH-FORENSICS-001`** — ratifies the branch model
  they proposed and respects the corrupted-filename root cause they
  found (§3's invisible-character rule).

## 12. References

- `docs/constitution/CONSTITUTION.md` — Articles 8, 9.
- `docs/governance/policies/Repository_Policy.md` — the repository
  policy this branch policy sits beneath.
- `docs/governance/policies/Branch_Protection_Policy.md`,
  `docs/governance/standards/Git_Workflow_Standard.md` — protection and
  git mechanics for these branches.
- `docs/governance/policies/Engineering_Language_Policy.md` — the
  language rule branch names follow.
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §3–§4,
  `docs/BRANCH_FORENSICS_001.md` — the branch model's source and the
  invisible-character root cause §3 guards against.
- `docs/governance/roles/Core_Worker.md`, `Platform_Worker.md` — the
  owners of `feature/core` and `feature/platform`.
- `communication/task_queue/GOV-PACKAGE-001.md` — this package's ticket.
