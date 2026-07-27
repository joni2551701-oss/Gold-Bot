# Branch Management Policy

**Governance status:** DRAFT — submitted for Director review under
TASK-CONSTITUTION-001. This document is produced on-disk as the
deliverable; per the task's Completion instruction ("Wait for Director
review. No repository modifications are authorized.") it is **not**
committed, and no branch/merge/history/config change was made. The
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
deletion after merge**. Long-lived and parallel production branches are
prohibited except by **explicit Director authorization**. A naming
standard (`feature/<task>`) replaces ad-hoc names. The Director is the
sole authority for permanent branches, exceptional workflows, branch
recovery, repository reset, and any retention beyond the normal
lifecycle.

The policy is internally consistent, conflicts with no existing
Constitution Article (1–12), directly supports a clean Repository
Reset, and scales to future multi-Worker development. Ten rules follow,
then the Constitution-ready Article, then the validation record.

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
Merge               (into main; only on Director authorization — Rule 10)
  ↓
Delete              (remote + local — Rule 6)
```

No stage is skipped or reordered. A branch that has not passed CI is not
reviewed; a branch not approved is not merged; a merged branch is not
retained.

### Rule 6 — Mandatory Branch Deletion

Immediately after a successful merge, the feature branch is deleted —
**remote and local**. No completed feature branch may remain. Deletion
is part of "done": a task is not complete until its branch is gone. (A
merged branch's history is already preserved in `main`; the branch ref
itself is redundant and is removed.)

### Rule 7 — Long-lived Branches

Long-lived branches are **prohibited**. The only exception is
**explicit Director approval** (Rule 10). Absent that approval, every
non-`main` branch is short-lived: it exists only for the span of one
task's lifecycle (Rule 5) and is then deleted (Rule 6).

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
> → Implementation → CI → Director Review → Merge → Delete` (Rule 5) —
> with no stage skipped. Immediately after a successful merge the branch
> is deleted, remote and local; no completed feature branch may remain
> (Rule 6). Long-lived and permanent branches are prohibited except by
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
> Full operational detail — the ten rules, the lifecycle diagram, and
> the naming standard — lives in
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

The ten rules reinforce rather than contradict each other. Rule 1
(one authoritative branch) is the premise; Rules 2–4 constrain how
non-`main` branches come into being (one per Worker, from `main`, one
task); Rule 5 defines their whole life; Rules 6–8 guarantee they leave
cleanly; Rule 9 keeps them legible; Rule 10 puts every exception behind
the Director. There is no rule whose obligation another rule forbids.
The steady state each rule implies is the same: `main` + a small,
one-per-Worker set of short-lived, well-named task branches.

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
- **Naming reconciliation (flagged for Director):** harness/agent
  sessions may operate on an environment-assigned branch name (e.g.
  `claude/<...>`) rather than `feature/<task>`. This is an accepted
  operational form of "one Worker = one branch" for web/agent
  workflows; the `feature/<task>` convention (Rule 9) is the canonical
  standard for human/CLI workflows. Whether to normalize agent branch
  names to `feature/<task>` is a Director decision, noted here rather
  than silently resolved.

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

- **Final Branch Management Policy** — the ten rules, historical
  context, lifecycle, and naming standard above.
- **Constitution version** — the proposed Article 13 draft above,
  Constitution-formatted and ready for a Director-instructed amendment
  phase.
- **Executive Summary** — at the top of this document.

No branches were created, deleted, or merged; no history or GitHub
configuration was changed. This is a governance/documentation
deliverable, held for Director review.
