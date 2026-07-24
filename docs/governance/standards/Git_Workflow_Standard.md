# Git Workflow Standard

The authoritative standard for GoldBot's day-to-day git mechanics under
the ratified branch model: the commit, branch, merge, release, hotfix,
recovery, and rollback workflows, plus the tag and versioning
conventions. It is governed by `docs/constitution/CONSTITUTION.md`,
sits within Engineering Governance v1.1 (GOV-009 / ORDER-019), and
operationalizes `docs/governance/policies/Branch_Policy.md` (GOV-006)
and `Branch_Protection_Policy.md` (GOV-007) into concrete git usage.

**Relationship to `docs/standards/COMMIT_STANDARD.md` (stated
explicitly, so the two never compete)**: `COMMIT_STANDARD.md` governs
the validation sequence for a *single commit* (the `git add -A` →
pyflakes → compileall → pytest → smoke run → clean status → reviewed
diff → commit → push → CI protocol). **This** standard governs the
*branch/merge/tag/release/hotfix/recovery* mechanics *around* commits.
They are complementary: a commit is made per `COMMIT_STANDARD.md`; where
it lands and how branches flow is per this document. This standard does
not restate the commit-validation sequence.

## 1. Purpose

To make git usage predictable and safe under the new branch model — so
merges, releases, hotfixes, and (critically) rollbacks follow one
written convention, and the repository's current gaps (zero tags, no
tagging convention, no rollback anchor — `REPO-001` §1) are closed.

## 2. Git Workflow Overview

A GitFlow-style model over the official branches
(`Branch_Policy.md` §2):

```
feature/core ─┐
              ├─► develop ──(Director-reviewed, CI-passed)──► main ──► (tagged release)
feature/platform ─┘
```

- Work happens on `feature/*`; integrates to `develop`; promotes to
  `main` under review; `main` is tagged at release points.
- This model is the *target* — it takes effect when Repository
  Migration executes (paused, ORDER-009). Until then, work continues on
  the current branch structure and these workflows describe what
  Migration adopts.

## 3. Commit Workflow

- Every commit follows `docs/standards/COMMIT_STANDARD.md`'s full
  validation sequence in order (referenced, not restated here).
- Commit messages are English (`Engineering_Language_Policy.md`),
  summary-plus-body, and — on a phase's final commit — carry the
  "not built" honesty note the standard requires.
- Commits are scoped to the brief's genuine gap; no uninstructed change
  rides along (`docs/standards/CODE_STANDARD.md`).

## 4. Branch Workflow

- Branch from the correct base (`feature/*` from `develop`), per
  `Branch_Policy.md` §5, and only under a Director Order authorizing the
  branch operation (`Repository_Policy.md` §3).
- Branch names are ASCII English, no whitespace, no invisible Unicode
  characters (`Branch_Policy.md` §3 — the same class of character that
  caused the repository's only conflict).
- Keep a feature branch current with `develop` by merging `develop` in
  (or rebasing, where the branch is the owner's own unmerged work);
  resolve conflicts on the feature branch, never on `develop`/`main`.

## 5. Merge Workflow

- **`feature/*` → `develop`**: via PR, CI must pass. Merge method:
  a standard merge commit preserves the feature's history for the
  integration branch; a squash is acceptable for a small, single-topic
  feature — the owning Worker chooses per change, defaulting to a merge
  commit for traceability.
- **`develop` → `main`**: via PR, **Director-reviewed and CI-passed**
  (`Branch_Protection_Policy.md` §4), always a merge commit (never a
  squash that would erase `develop`'s integration history on `main`).
- **Force-merging a protected branch is forbidden**
  (`Branch_Protection_Policy.md` §5). Conflicts are resolved and
  re-verified (a fresh `git merge-tree` check for a known-risky merge,
  as `BRANCH-FORENSICS-001` demonstrated) before the merge completes.

## 6. Release Workflow

- A release is a Director-reviewed promotion of `develop` → `main`,
  followed by an annotated **release tag** on the `main` merge commit
  (§10), with the version taken from `docs/roadmap/VERSIONS.md`
  (`docs/policies/RELEASE_POLICY.md`, `VERSION_POLICY.md`).
- A release does not cross a version boundary silently: an additive
  release stays within the current version line; a version-boundary
  change requires explicit Director approval
  (`docs/policies/VERSION_POLICY.md`).
- CI `success` on the exact `main` commit is the release gate; local
  validation alone is never a release (`docs/policies/RELEASE_POLICY.md`).

## 7. Hotfix Workflow

- A hotfix (an urgent production-affecting fix) follows the emergency
  workflow (`Collaboration_Rules.md` §18): immediate report → Director
  decision → recovery/hotfix Order → execution.
- Mechanically: branch a `feature/hotfix-<topic>` from `main`
  (the production-ready tip), apply the minimal fix under the full
  Commit Protocol, merge to `main` via a Director-reviewed PR, tag the
  new release, and merge the same fix back into `develop` so it is not
  lost on the next promotion.
- No hotfix bypasses `main`'s protection; the Director's Order
  authorizes the expedited review, not a protection bypass.

## 8. Recovery Workflow

- Repository recovery (an integrity fix such as the corrupted-filename
  conflict) follows `Repository_Policy.md` §7 and
  `Branch_Protection_Policy.md` §6: audit-first, rollback anchor
  created before any change, minimal content-neutral fix, re-verify with
  a fresh `git merge-tree`.
- For the known case (`BRANCH-FORENSICS-001`): the fix is a single
  `git mv` removing the U+2060 character from
  `strategies/strategy_manager.py` on `main` — a normal forward commit,
  no history rewrite, no force-push — executed only under its Director
  Order (ORDER-010, queued).

## 9. Rollback Workflow

- Rollback requires a **pre-existing anchor**. Because the repository
  has zero tags today (`REPO-001` §1), the first step of any structural
  change is to create the anchor (§10).
- **Git-level rollback**: reset the affected branch to its named
  known-good tag via a Director-authorized operation — never a silent
  force-push of a protected branch (`Branch_Protection_Policy.md` §7).
- **Deployment rollback** is the separate release-based VPS mechanism
  (`docs/deployment/ROLLBACK.md`), distinct from git-level rollback.

## 10. Tag Standard

- Tags are **annotated** (not lightweight), English, and named by
  purpose:
  - **Rollback anchors**: `pre-<operation>-<branch>` (e.g.
    `pre-migration-main`, `pre-migration-production`) — created before
    any structural change, closing the no-rollback-anchor gap.
  - **Release tags**: semantic version from `docs/roadmap/VERSIONS.md`
    (e.g. `v0.4.7`), on the `main` release merge commit.
- A tag is immutable once pushed; a mistaken tag is superseded by a new,
  clearly-named one, never force-moved.
- The repository currently has **zero tags**; this standard is the
  convention the first tag (a Migration rollback anchor) will follow.

## 11. Versioning Standard

- Versions are governed by `docs/roadmap/VERSIONS.md` as the single
  source of truth, and `docs/policies/VERSION_POLICY.md`'s
  additive-within-version vs. version-boundary distinction — this
  standard references that policy and adds only the *tagging* of a
  version at release (§10), not a competing versioning scheme.

## 12. Constraints

This standard, and any Worker acting under it, does **not**:

- Perform any git operation (branch, merge, tag, push, rollback) — it
  defines the mechanics, executed only under a Director Order at
  Migration/Recovery time.
- Modify the Constitution or rewrite `COMMIT_STANDARD.md` /
  `RELEASE_POLICY.md` / `VERSION_POLICY.md` — it references them.
- Touch `.github/workflows/*.yml` — CI content is changed only under
  separate explicit authorization.
- Take effect as live git practice before Repository Migration is
  Director-authorized and executed.

## 13. Compliance

- **Constitution** — consistent with Article 8/9 (change discipline).
  Supremacy applies.
- **ADRs** — consistent with ADR-005 (Migration discipline) and ADR-009
  (CI as the validation gate); breaks none.
- **Governance v1.1** — no contradiction with `Branch_Policy.md`,
  `Branch_Protection_Policy.md`, `Repository_Policy.md`,
  `Engineering_Language_Policy.md`, the role documents, or
  `Collaboration_Rules.md`. Explicitly complementary to
  `docs/standards/COMMIT_STANDARD.md` (commit-validation) — this
  standard is branch/merge/tag/release/hotfix/recovery mechanics, no
  overlap.
- **`REPO-001`, `BRANCH-FORENSICS-001`** — closes the tagging/rollback
  gap and encodes the recovery method they established.

## 14. References

- `docs/constitution/CONSTITUTION.md` — Articles 8, 9.
- `docs/standards/COMMIT_STANDARD.md` — the single-commit validation
  sequence this standard is complementary to and references.
- `docs/governance/policies/Branch_Policy.md`,
  `Branch_Protection_Policy.md`, `Repository_Policy.md`,
  `Engineering_Language_Policy.md` — the policies this standard
  operationalizes.
- `docs/policies/RELEASE_POLICY.md`, `VERSION_POLICY.md`,
  `docs/roadmap/VERSIONS.md` — release and versioning governance.
- `docs/governance/roles/Collaboration_Rules.md` — the emergency/hotfix
  and approval workflows §6–§8 rely on.
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`,
  `docs/BRANCH_FORENSICS_001.md`, `docs/deployment/ROLLBACK.md` — the
  tagging/rollback gap, the recovery method, and the deployment-rollback
  mechanism.
- `communication/task_queue/GOV-PACKAGE-001.md` — this package's ticket.
