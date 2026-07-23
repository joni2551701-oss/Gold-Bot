# Branch Protection Policy

The authoritative policy for how GoldBot's official branches are
protected: push rules, merge approval, force-push rules, recovery,
rollback, emergency handling, and security. It is governed by
`docs/constitution/CONSTITUTION.md`, sits within Engineering Governance
v1.1 (GOV-007 / ORDER-019) beneath
`docs/governance/policies/Branch_Policy.md`, and ratifies as standing
policy the protection model proposed in
`docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §5.

This policy **defines the protection rules**; it does not enable any
GitHub branch-protection setting or touch any `.github/workflows/*.yml`
file. Enabling protection is a separate, Director-authorized
implementation step (part of Repository Migration, REPO-002), performed
only when Migration executes.

## 1. Purpose

To fix, as standing policy, exactly how each official branch is
protected — so the repository's current state of **zero branch
protection** (`REPO-001` §1: any collaborator can force-push `main` or
the production branch today, with no required review and no required
CI) is replaced by a written, enforceable standard when Migration runs.

## 2. Protected Branches

| Branch | Protection posture (target) |
|---|---|
| `main` | Fully protected. No direct push; PR-only; Director review mandatory; CI mandatory. |
| `develop` | Protected. No direct push; PR-only; CI mandatory; per-merge Director review not required. |
| `feature/core`, `feature/platform` | Unprotected working lines, single-owner; CI recommended, not required. |

`main` and `develop` are the protected branches. Feature branches are
deliberately unprotected so their owning Worker can commit freely; they
gain their gate at the PR boundary into `develop`.

## 3. Push Policy

- **`main`**: direct push forbidden. The only way in is a merge from
  `develop` via a reviewed, CI-passed PR.
- **`develop`**: direct push forbidden; PR-only, CI-gated.
- **`feature/*`**: the owning Worker (Core or Platform) may push
  directly to its own line.
- No push of any kind occurs to a protected branch except under the
  merge gates above, and no protected-branch operation happens outside
  a Director-authorized action (`Repository_Policy.md` §3).

## 4. Merge Approval Policy

- A merge into **`main`** requires the **Director's** approval
  (APPROVED verdict) and passing CI, every time — no exception, no
  self-approval by a Worker (`docs/governance/roles/Director.md` §8;
  `Collaboration_Rules.md` §9).
- A merge into **`develop`** requires passing CI; a Worker may perform
  it without a per-merge Director review, but remains bound by the No
  Silent Decisions gate for any reserved decision in the change.
- CI as a required check is a GitHub branch-protection setting applied
  only at Migration time; this policy defines the rule, not its
  enablement.

## 5. Force Push Policy

- **Force push to a protected branch (`main`, `develop`) is
  forbidden** — outright, with no routine exception. A protected branch
  is only ever moved forward by a reviewed merge.
- A force-with-lease to a *feature* branch is permitted to its owner
  where the branch carries only that owner's own unmerged work (e.g.
  cleaning up a local rebase before the PR), never after it has been
  integrated.
- The one historically-sanctioned force scenario in this repository —
  re-basing a designated branch that contains only already-merged
  history onto a fresh base — is a Director-authorized action, not a
  routine one, and never applies to a protected branch.

## 6. Recovery Policy

- Repository recovery (correcting an integrity problem, e.g. the
  `BRANCH-FORENSICS-001` corrupted-filename conflict) is performed
  under a Director Order (`Repository_Policy.md` §7), audit-first, with
  a rollback anchor created before any change.
- Recovery never force-pushes a protected branch; the corrupted-filename
  fix is a normal forward commit (a single content-neutral rename), not
  a history rewrite (`docs/BRANCH_FORENSICS_001.md` Recovery Strategy).

## 7. Rollback Policy

- **Git-level rollback** depends on a rollback anchor existing *before*
  the change — an annotated tag on the last known-good tip. The
  repository has **zero tags today** (`REPO-001` §1), so the first act
  of any structural change is to create that anchor
  (`Repository_Policy.md` §9, `Git_Workflow_Standard.md` §9–§10).
- **Deployment rollback** (the release-based VPS mechanism in
  `docs/deployment/ROLLBACK.md`) is a separate, already-built mechanism
  for the running product; it is real but unexercised (no VPS live yet)
  and is distinct from git-level rollback (`REPO-001` §0/Q4).
- A rollback of a protected branch is a Director-authorized action:
  reset to the named anchor via a new reviewed operation, never a
  silent force-push.

## 8. Emergency Policy

- A branch/repository-integrity emergency follows the emergency
  workflow (`Collaboration_Rules.md` §18): immediate report → Director
  decision → recovery Order → execution.
- Even under time pressure, no protected-branch force-push, no branch
  deletion, and no protection-bypass happens without an explicit
  Director Order. The protection rules do not weaken in an emergency;
  the Director may issue an Order that authorizes a specific exceptional
  action, and that Order is the record of it.

## 9. Security Rules

- Protection settings are themselves a security control: the current
  zero-protection state is recorded as a present-tense risk
  (`REPO-001` §8) and closing it is part of Migration.
- No branch operation exposes secrets; `.env`/credential files are
  never committed to any branch (Constitution Article 4;
  `docs/policies/SECURITY_POLICY.md`).
- Permission/authorization logic anywhere in the repository fails closed
  (ADR-010); a protection rule is never satisfied by an unknown/invalid
  state.

## 10. Compliance

- **Constitution** — consistent with Article 4 (security boundary),
  Article 8/9 (change discipline). Supremacy applies.
- **ADRs** — consistent with ADR-009 (CI as the validation gate) and
  ADR-010 (fail closed); breaks none.
- **Governance v1.1** — no contradiction with `Branch_Policy.md`,
  `Repository_Policy.md`, the role documents, or `Collaboration_Rules.md`;
  no duplication (branch *model* is GOV-006's; git *mechanics* are
  GOV-009's; this document is protection only).
- **`REPO-001` §5/§8** — ratifies the protection proposal and the
  present-tense zero-protection risk it recorded.

## 11. References

- `docs/constitution/CONSTITUTION.md` — Articles 4, 8, 9.
- `docs/governance/policies/Repository_Policy.md`,
  `docs/governance/policies/Branch_Policy.md` — the repository and
  branch policies this protection policy sits within.
- `docs/governance/standards/Git_Workflow_Standard.md` — tag/rollback
  mechanics referenced in §6–§7.
- `docs/governance/roles/Director.md`, `Collaboration_Rules.md` — the
  approval authority and emergency workflow §4/§8 rely on.
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §5/§8,
  `docs/BRANCH_FORENSICS_001.md`, `docs/deployment/ROLLBACK.md` — the
  protection proposal, the recovery root cause, and the deployment
  rollback mechanism.
- `communication/decisions/ADR-010.md` — the Fail Closed Permission
  Policy §9 applies.
- `communication/task_queue/GOV-PACKAGE-001.md` — this package's ticket.
