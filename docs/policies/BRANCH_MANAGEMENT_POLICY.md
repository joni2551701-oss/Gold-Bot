# Branch Management Policy

**Governance status:** DRAFT (Revision 1) — submitted for Director
review under TASK-CONSTITUTION-001. Revision 1 adds, at the Director's
instruction, **Rule 11 — Repository Audit Before Merge** and formalizes
the harness branch-name case as a Director-sanctioned temporary
exception. This document is produced on-disk as the deliverable; per the
task's Completion instruction ("Wait for Director review. No repository
modifications are authorized.") it is **not** committed, and no
branch/merge/history/config change was made. The
"Constitution-Ready Version" (below) is a *proposed* Article draft — a
Worker never amends `docs/constitution/CONSTITUTION.md` on its own
initiative (Amendment process); adopting it is a separate,
Director-instructed amendment phase.

Track: Constitution / Repository Workflow. Sits in `docs/policies/`
alongside the existing 11 policy documents (DEVELOPMENT, RELEASE,
VERSION, DIRECTOR, …), and is written to be promoted verbatim into the
Constitution as an Article.

---

## Executive Summary

Uncontrolled parallel-branch growth is now governed by a single,
permanent rule set. The repository keeps **one authoritative branch
(`origin/main`)**; each Worker owns **at most one active feature
branch**, cut **from `origin/main`**, carrying **exactly one approved
task**, following a **fixed lifecycle** that ends in **mandatory
deletion after merge**. Before any merge, the branch passes a
**mandatory Repository Audit** — compared against `main`, checked for
duplicated code, stripped of unnecessary files, reduced to only the
useful changes — so GoldBot runs a **Repository Audit Workflow**, not a
plain Git workflow (Rule 11). Long-lived and parallel production branches are
prohibited except by **explicit Director authorization**. A naming
standard (`feature/<task>`) replaces ad-hoc names. The Director is the
sole authority for permanent branches, exceptional workflows, branch
recovery, repository reset, and any retention beyond the normal
lifecycle.

The policy is internally consistent, conflicts with no existing
Constitution Article (1–12), directly supports a clean Repository
Reset, and scales to future multi-Worker development. Eleven rules
follow, then the Constitution-ready Article, then the validation record.

---

## Historical Context — why this policy exists

Over a short window, a large number of parallel branches were created
in this repository. That uncontrolled growth caused, in practice:

- **Repository complexity** — many simultaneous development lines with
  no single obvious "truth."
- **Duplicated work** — the same change attempted on more than one
  line.
- **Worker confusion** — uncertainty about which branch was
  authoritative or current.
- **Governance conflicts** — competing lineages that no rule
  arbitrated.
- **Merge complexity & branch-lineage issues** — tangled histories
  that were expensive to reconcile.
- **Difficult maintenance** — stale, unused branches accumulating with
  no cleanup discipline.

This policy exists to make those failure modes structurally
impossible. It is written as a permanent law, not a one-time cleanup:
the rules below hold for every Worker, every task, indefinitely, so the
condition that produced the problem cannot recur.

---

## The Rules

### Rule 1 — Single Source of Truth

Only one permanent development branch exists: **`origin/main`**. It is
the sole authoritative branch. There are **no parallel production
branches**. Any branch that is not `origin/main` is, by definition,
temporary and task-scoped (Rule 4) and destined for deletion (Rule 6).

### Rule 2 — One Worker = One Branch

Each Worker may own **only one active feature branch at a time**.
Creating a second feature branch before the current task is finished
(merged and deleted, per Rules 5–6) is **prohibited**. A Worker with an
open, unmerged branch does not start a parallel line; it finishes,
merges, deletes, then cuts the next branch.

### Rule 3 — Branch Origin

Every feature branch is created **from `origin/main`** and from nowhere
else. Branching from another feature branch, an archive branch, a
recovery branch, or any temporary branch is **prohibited** — those
paths are exactly what produce tangled lineage. `main` is always the
single point every new branch descends from.

### Rule 4 — One Branch = One Task

Each feature branch represents **exactly one approved task**. No
unrelated work, no mixed implementations, no "while I'm in here"
additions. A branch's diff maps one-to-one to a single Director-approved
brief, which keeps review, CI, and merge decisions unambiguous.

### Rule 5 — Branch Lifecycle

Every branch follows this fixed, mandatory lifecycle:

```
main
  ↓  (cut from origin/main — Rule 3)
feature/<task>
  ↓
Implementation      (one task — Rule 4; full Commit Protocol per CLAUDE.md)
  ↓
CI                  (GitHub Actions SUCCESS required before review)
  ↓
Director Review     (approval is the merge gate)
  ↓
Repository Audit    (mandatory pre-merge audit vs main — Rule 11)
  ↓
Merge               (into main; only useful changes; only on Director
                     authorization — Rules 10, 11)
  ↓
Delete              (remote + local — Rules 6, 11)
```

No stage is skipped or reordered. A branch that has not passed CI is not
reviewed; a branch not audited against `main` is not merged (Rule 11); a
branch not approved is not merged; a merged branch is not retained.

### Rule 6 — Mandatory Branch Deletion (temporary branches only)

Immediately after a successful merge, a **temporary** branch
(`feature/*`, `bugfix/*`, `hotfix/*`) is deleted — **remote and local**.
No completed temporary branch may remain. Deletion is part of "done": a
task is not complete until its temporary branch is gone. (A merged
branch's history is already preserved in `main`; the temporary branch ref
itself is redundant and is removed.)

**Exception — the persistent primary development branch is NOT
auto-deleted** (Rule 12, TASK-BRANCH-001). `claude/*` is a long-lived
working branch: merging its work into `main` does **not** trigger its
deletion. It is removed only by a separate written Director/Owner
decision.

### Rule 7 — Long-lived Branches

Long-lived branches are **prohibited by default**. The exceptions are
**explicit Director approval** (Rule 10) and the standing
**persistent primary development branch** `claude/*` (Rule 12,
TASK-BRANCH-001). Absent such approval, every non-`main` branch is
short-lived: it exists only for the span of one task's lifecycle
(Rule 5) and is then deleted (Rule 6).

### Rule 8 — Repository Cleanliness

The repository shall **never accumulate unused branches**. Cleanup is
mandatory and continuous, not occasional: because Rule 6 deletes each
branch at merge and Rule 7 forbids long-lived branches, the steady state
is `main` plus at most the small set of in-flight, one-per-Worker
feature branches. Any branch that is neither `main`, a currently-active
task branch, nor Director-approved-permanent is a cleanup target.

### Rule 9 — Naming Convention

Feature branches use a descriptive, task-scoped name of the form:

```
feature/<task>
```

Examples: `feature/current-price`, `feature/ai-manager`,
`feature/risk-engine`, `feature/platform-api`. The `<task>` segment is a
short, kebab-case description of the single approved task the branch
carries (Rule 4). Random, temporary, personal, or opaque names
(`tmp`, `test2`, `wip-x`, `backup-final`) are prohibited. A reader must
be able to tell what a branch is for from its name alone.

### Rule 10 — Director Authority

Only the Director may authorize:

- **permanent branches** (any branch exempt from Rules 6–7),
- **exceptional workflows** (any deviation from the Rule 5 lifecycle),
- **branch recovery** (restoring a deleted or lost branch),
- **repository reset** (rebasing history / re-establishing `main`),
- **branch retention beyond the normal lifecycle**.

A Worker never self-authorizes any of these. Where a task genuinely
seems to require one, the Worker stops and requests Director authority —
the same STOP → AUDIT → Director Decision posture the Constitution's
Change Management Law already mandates for governance conflicts.

### Rule 11 — Repository Audit Before Merge

GoldBot uses a **Repository Audit Workflow**, not a plain Git workflow.
No branch is merged on the strength of a green CI run alone; every branch
passes a **mandatory pre-merge audit** first. This rule exists because
the failure modes in the Historical Context (duplicated work, tangled
lineage, stale/unnecessary files, difficult maintenance) enter `main`
precisely at merge time — the audit is the gate that stops them.

Before **any** merge, for **every** branch, in order:

1. **Compare fully against `main`.** Produce the complete branch-vs-`main`
   diff and review it in full — every file, every hunk. Nothing merges
   unseen.
2. **Detect duplicated code.** Identify any logic the branch reintroduces
   that already exists elsewhere in the repository (the same
   duplicate-detection discipline the Module Reuse Principle and the
   Phase 49/50 cleanups established). Duplicates are resolved on the
   branch — by reusing the existing module — before merge, never after.
3. **Delete unnecessary files.** Remove throwaway artifacts, scratch
   files, dead code, and anything not part of the one approved task
   (Rule 4) — and do the deletion **on the branch itself**, so `main`
   never receives them.
4. **Keep only the useful changes.** After steps 1–3 the branch's diff
   must contain nothing but the changes that serve its single approved
   task. Anything else is dropped on the branch before merge.
5. **Only then merge.** Merge into `main` is permitted only after the
   audit is clean and the Director has authorized it (Rule 10). An
   unaudited branch is not merge-eligible, regardless of CI status.
6. **Delete immediately after merge.** As soon as the merge lands, delete
   the branch — **remote and local** — with no delay (this is Rule 6,
   restated here as the closing step of the audit workflow so the
   pre-merge audit and post-merge cleanup read as one continuous
   procedure).

The audit is a Worker responsibility to *perform and report*; the merge
authorization itself remains the Director's (Rule 10). A Worker performs
steps 1–4 and 6 and presents the result; the Director gives the step-5
go-ahead.

### Rule 12 — Persistent Primary Development Branch (TASK-BRANCH-001)

Standing Director decision (TASK-BRANCH-001): the Claude Worker's main
working branch, `claude/*` (currently
`claude/code-analysis-optimization-pwfo3q`), is a **persistent Primary
Development Branch**, not a temporary task branch. Concretely:

1. **Not auto-deleted.** Merging its work into `main` does **not** delete
   it (this overrides Rule 6's delete-after-merge *for this branch only*).
2. **Long-lived by standing approval.** It is the standing Rule 7/Rule 10
   exception — no per-task re-approval is needed to keep it.
3. **One branch, many tasks.** Opening a new `feature/*` per task is **not
   required**; ongoing work continues on `claude/*`. (This is the
   Director-approved reconciliation of the Rule 9 `feature/<task>`
   convention with the harness/agent workflow — see the Validation note.)
4. **Deletion is Director/Owner-only.** `claude/*` may be deleted **only**
   by a separate written Director or Repository-Owner decision — never
   automatically, never by the Worker on its own initiative.

Branch taxonomy (repository policy):

| Branch | Role | Lifetime | Deleted |
|---|---|---|---|
| `main` | Production branch (single source of truth) | Permanent | never |
| `claude/*` | **Primary Development Branch** (Worker) | **Persistent** | only by written Director/Owner decision |
| `feature/*` | Temporary task branch | Short-lived | after merge (Rule 6) |
| `bugfix/*` | Temporary fix branch | Short-lived | after merge (Rule 6) |
| `hotfix/*` | Temporary urgent-fix branch | Short-lived | after merge (Rule 6) |

Rules 1–11 continue to apply to the **temporary** branch classes.
`main` and `claude/*` are the two persistent branches; every other branch
is temporary and follows the full delete-after-merge lifecycle.

---

## Constitution-Ready Version (proposed Article — DRAFT)

The following is formatted to drop into
`docs/constitution/CONSTITUTION.md` verbatim, in the existing
`## Article N — …Law` style, once the Director adopts it through the
Amendment process. Article number is provisional: the current
Constitution ends at Article 12, so this is proposed as **Article 13**;
the adopting amendment phase confirms the final number and logs it in
`docs/constitution/AMENDMENTS.md`.

> ## Article 13 — Branch Management Law
>
> **The repository has one authoritative branch, `origin/main`; every
> other branch is one Worker's one task, cut from `main`, merged, and
> then deleted.**
>
> `origin/main` is the single source of truth — there are no parallel
> production branches (Rule 1). A Worker owns at most one active feature
> branch at a time and does not open a second before the first is merged
> and deleted (Rule 2, One Worker = One Branch). Every feature branch is
> cut from `origin/main`, never from another feature/archive/recovery/
> temporary branch (Rule 3), and carries exactly one Director-approved
> task with no unrelated or mixed work (Rule 4).
>
> Every branch follows one mandatory lifecycle — `main → feature/<task>
> → Implementation → CI → Director Review → Repository Audit → Merge →
> Delete` (Rule 5) — with no stage skipped. Before any merge the branch
> passes a mandatory Repository Audit: compared in full against `main`,
> checked for duplicated code, stripped of unnecessary files, and reduced
> to only the changes that serve its one task, so that only useful code
> reaches `main` (Rule 11) — GoldBot runs a Repository Audit Workflow,
> not a plain Git workflow, and a green CI run alone never authorizes a
> merge. Immediately after a successful merge the branch is deleted,
> remote and local; no completed feature branch may remain (Rule 6).
> Long-lived and permanent branches are prohibited except by
> explicit Director approval (Rule 7), and the repository never
> accumulates unused branches (Rule 8). Feature branches use the
> `feature/<task>` naming convention; random or temporary names are
> forbidden (Rule 9).
>
> Only the Director may authorize a permanent branch, an exceptional
> workflow, branch recovery, a repository reset, or branch retention
> beyond the normal lifecycle (Rule 10). A Worker never self-authorizes
> any of these; where a task appears to require one, it stops and
> returns the question to the Director, the same STOP → AUDIT →
> Director Decision protocol Article 8 already formalizes. This Article
> exists because uncontrolled parallel-branch growth previously caused
> repository complexity, duplicated work, worker confusion, governance
> conflicts, and difficult maintenance; the one-`main`, one-Worker,
> one-task, delete-after-merge discipline prevents their recurrence.
>
> Full operational detail — the eleven rules, the lifecycle diagram, the
> pre-merge Repository Audit procedure, and the naming standard — lives in
> `docs/policies/BRANCH_MANAGEMENT_POLICY.md`, the practical expression
> of this Article (the same Article-to-policy relationship Articles
> 8/9/11 already have with their `docs/policies/` documents).

---

## Validation

Per the task's Validation requirement, every rule was checked to be
internally consistent, non-conflicting with existing Constitution
Articles, supportive of the Repository Reset strategy, and supportive
of future multi-Worker development.

### Internal consistency

The eleven rules reinforce rather than contradict each other. Rule 1
(one authoritative branch) is the premise; Rules 2–4 constrain how
non-`main` branches come into being (one per Worker, from `main`, one
task); Rule 5 defines their whole life; Rules 6–8 guarantee they leave
cleanly; Rule 9 keeps them legible; Rule 10 puts every exception behind
the Director; Rule 11 gates the merge itself with a mandatory audit so
only useful, non-duplicated code reaches `main`. Rule 11 is consistent
with the rest by construction: its step 5 defers the merge to Rule 10's
Director authorization, its step 6 restates Rule 6's delete-after-merge,
and its duplicate-detection step reuses (rather than competes with) the
Module Reuse Principle. There is no rule whose obligation another rule
forbids. The steady state each rule implies is the same: `main` + a
small, one-per-Worker set of short-lived, well-named, audited task
branches.

### No conflict with existing Constitution Articles (1–12)

- **Article 8 (Change Management Law)** — reinforced. Rule 10's
  "return the question to the Director" is Article 8's STOP → AUDIT →
  Director Decision applied to branch operations; the Constitution →
  Policy → Code order is preserved (this is a Policy/Constitution
  document, not code).
- **Article 9 (Version Compatibility Law)** — orthogonal, no conflict.
  Article 9 governs LOCKed module names/paths/APIs; this policy governs
  VCS branch workflow. Neither constrains the other.
- **Article 10 (Owner Override Law)** — orthogonal. Owner control
  surfaces are a runtime concern; branch management is a development-
  workflow concern. No overlap.
- **Article 11 (Foundation Reuse Law)** — respected. Before writing this
  policy, a search confirmed no existing branch-management policy or
  Article exists (`docs/policies/` has 11 files, none on branching; no
  Article 1–12 covers it), so a new document is justified rather than a
  duplicate.
- **Articles 1–7, 12** — no interaction (they govern pipeline direction,
  imports, database access, providers, testing, reuse, and per-phase
  New/Extended/Reused shape; none touch branch workflow).
- **Amendment process** — respected. This document does not modify
  `CONSTITUTION.md`; the Article draft is a proposal for a future,
  Director-instructed amendment phase.

### Consistency with existing operational git governance

- The session's standing Git rules (develop on the designated branch;
  push only to it; never push to a different branch without explicit
  permission; on a *merged* PR, restart the branch from the latest
  default branch) are consistent with — and a subset of — this policy:
  one active branch per Worker, `main` as origin, delete/restart after
  merge.
- **Environment-assigned branch names — now a standing persistent-branch
  decision (Rule 12, TASK-BRANCH-001; supersedes the earlier "temporary
  exception" reading):** the `claude/*` branch the agent/web session runs
  on is no longer treated as a temporary Rule 9 exception. Per
  TASK-BRANCH-001 it is the **persistent Primary Development Branch**
  (Rule 12): long-lived by standing Director approval, not auto-deleted at
  merge, and not required to be re-cut per task. It still obeys the
  merge-safety rules — pre-merge Repository Audit (Rule 11) and, when its
  work reaches `main`, the same review/CI gate — but Rules 6 (mandatory
  deletion) and the one-branch-per-task expectation do **not** apply to
  it. The `feature/<task>` convention remains the canonical standard for
  the *temporary* branch classes (`feature/*`, `bugfix/*`, `hotfix/*`);
  this decision does **not** authorize a Worker to invent arbitrary
  persistent names — only `main` and the Director-designated `claude/*`
  are persistent.

### Supports the Repository Reset strategy

A clean reset needs exactly what this policy provides: a single
authoritative line to reset *to* (Rule 1, `origin/main`), no competing
permanent branches to reconcile (Rules 1, 7), no stale branches to sweep
(Rules 6, 8), and a single authority to sanction the reset (Rule 10,
which names "repository reset" explicitly). After adoption, a reset is a
Director-authorized, low-ambiguity operation rather than a negotiation
across tangled lineages.

### Supports future multi-Worker development

"One Worker = one branch" (Rule 2) + "one branch = one task" (Rule 4) +
descriptive naming (Rule 9) means N Workers produce N independent,
clearly-labelled, `main`-rooted branches that never cross-depend (Rule 3
forbids branching off each other). Each merges and deletes on its own
Director-gated lifecycle (Rules 5–6). The model scales: adding Workers
adds parallel *tasks*, never parallel *production lines*.

---

## Deliverables (this submission)

- **Final Branch Management Policy** — the eleven rules (including
  Rule 11 — Repository Audit Before Merge), historical context,
  lifecycle, and naming standard above.
- **Constitution version** — the proposed Article 13 draft above,
  Constitution-formatted and ready for a Director-instructed amendment
  phase.
- **Executive Summary** — at the top of this document.

No branches were created, deleted, or merged; no history or GitHub
configuration was changed. This is a governance/documentation
deliverable, held for Director review.
