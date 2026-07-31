# TASK-GOV-001 — `claude/collaboration` Working Rules

**Revision 2** (supersedes Revision 1 of this same document — role name
`Director` renamed to `Owner`, and the no-new-branch restriction made
explicit, per the reissued task brief).

Governance-only task. **No source code is written, read for editing, or
modified by this task. No new branch is opened by this task.** This
document defines the working order for the `claude/collaboration`
branch: branch rules, the single-Worker queue, the task lifecycle,
Owner/Worker responsibilities, the handover format, and the task-status
model.

This document does not replace, restate, or contradict the existing
Governance v1.1 documents (`docs/governance/roles/Collaboration_Rules.md`,
`docs/governance/policies/Branch_Policy.md`, `docs/governance/roles/
Director.md`, `Core_Worker.md`, `Platform_Worker.md`). Those govern the
repository-wide Director / Core Worker / Platform Worker model.
`claude/collaboration` is a distinct, single-track working branch with
its own, simpler single-Worker queue — this document is its own,
self-contained operating rule, scoped to that branch only. Where the
two overlap (final approval authority, No Silent Decisions, the Commit
Protocol, Trading Safety), this document defers to the existing ones
rather than duplicating them. **Terminology note:** this document's
"Owner" role is local to `claude/collaboration` and is not a rename of,
or a claim on, the repository-wide "Director" role defined elsewhere —
it names who holds final say specifically for this branch's queue.

## 1. Purpose

To fix, before any further work happens on `claude/collaboration`, an
explicit, binding operating order: one branch, one Worker active at a
time, one task at a time, a fixed task lifecycle, a fixed handover
format, and a fixed set of things a Worker on this branch never does —
including opening a branch.

## 2. Core Principle

- `main` is production.
- `claude/collaboration` is the **single** working branch. All Workers
  queue and work on this one branch, in turn.

## 3. Hard Restrictions

A Worker operating under this document does **not**:

1. Write source code.
2. Modify any `.py` file.
3. Refactor pipeline, provider, stream, market, context, strategy,
   signal, decision, risk, or execution logic.
4. Touch `main` directly.
5. Open a new branch.
6. Create a branch without Owner approval.
7. Modify an existing FROZEN layer.
8. Mix tasks — one task is completed (or explicitly handed over)
   before the next begins.

A task that requires code, or a new branch, falls outside this
document's scope; it is executed under its own, separately issued and
Owner-approved task.

## 4. Branch Rules

1. `main` — production.
2. `claude/collaboration` — the single development branch.
3. A new branch is opened only when the Owner explicitly authorizes it.
4. A branch name is changed only with Owner approval.
5. A Worker never creates a branch on its own initiative.

## 5. Worker Queue

1. Exactly one Worker is active at any time.
2. When a Worker finishes, the next Worker continues on the same
   branch.
3. Two Workers never work at the same time.
4. Every Worker reads the previous Handover before starting work.

## 6. Task Flow

Every task on `claude/collaboration` moves through this fixed sequence:

1. Task name
2. Goal
3. Rules
4. Restrictions
5. Deliverable
6. Owner approval
7. Worker executes
8. Handover
9. Handoff to the next Worker

No step is skipped and no step is reordered. A task does not reach
step 7 (execution) without step 6 (Owner approval) having happened.

## 7. Director / Owner Roles

### Owner

- Sets the direction of work.
- Chooses which task is active now.
- Makes the final decision on opening or closing a branch.
- Makes the merge decision.

### Worker

- Executes only the task assigned.
- Does not step outside the rules.
- Leaves a Handover.
- Writes code only when a task explicitly assigns it — never in a
  governance-only task such as this one.

## 8. Handover Rule

Every Worker ends its turn with a Handover stating:

1. What was reviewed.
2. What was accepted.
3. What was rejected.
4. What is left for the next Worker.
5. Which layer is FROZEN.
6. Which layer opens next.

A turn without a written Handover is not considered complete, and the
next Worker does not treat the branch as ready to continue from.

## 9. Task File Format

Every task file has these sections. **Note:** `Owner` here names the
task's assignee (the Worker executing it), not the branch-level Owner
role defined in §7 — the same word, two different, context-clear
meanings, exactly as specified in the task brief that defines this
format.

```
TASK-ID
Goal
Rules
Forbidden
Allowed
Input
Output
Owner
Status
Next step
```

## 10. Laws

1. A FROZEN layer is never broken.
2. Reuse First.
3. No duplicate logic.
4. No hidden refactor.
5. No merge into `main` without Owner approval.
6. No code change inside a governance-only task.
7. Every task has one clear owner and one clear status.
8. Every branch action is traceable.
9. No new branch is opened without Owner approval.

## 11. Status Model

| Status | Meaning |
|---|---|
| `PLANNED` | Task is written but not yet Owner-approved. |
| `ACTIVE` | Owner-approved; a Worker is currently executing it. |
| `REVIEW` | Worker has delivered; awaiting Owner review. |
| `APPROVED` | Owner has accepted the deliverable as-is. |
| `BLOCKED` | Execution cannot continue without an Owner decision. |
| `FROZEN` | Layer/task is locked against further change until explicitly reopened. |
| `DONE` | Task is closed; its Handover has been consumed. |

## 12. Deliverable

1. Branch working order (§4).
2. Worker queue rule (§5).
3. Handover procedure (§8).
4. Task status model (§11).
5. List of forbidden actions (§3).
6. Situations requiring Owner approval (§3.6, §4.3, §4.4, §6 step 6,
   §10.5, §10.9).
7. This final governance document.

## 13. Acceptance Criteria

This task is considered done when:

1. No code was written.
2. The rules are unambiguous.
3. The branch order is clear.
4. Worker / Owner roles are separated.
5. The Handover system is written.
6. FROZEN layers are protected (§3.7, §10.1).
7. It is explicitly stated that a new branch opens only with Owner
   approval (§3.5, §3.6, §4.3, §10.9).

## 14. Handover (Revision 2)

1. **What was reviewed:** the Revision 1 document (single-commit
   history at the time) against the reissued brief; the repository's
   actual current `claude/collaboration` state (the branch's remote
   tip had, in the interim, moved to match `main`'s real head, which
   already includes this document's Revision 1 commit as an ancestor —
   no content was lost, and no rebase/force-push was performed by this
   Worker to reconcile that).
2. **What was accepted:** all of Revision 1's structure, laws, task
   flow, Handover format, and status model — carried forward unchanged
   in substance.
3. **What was rejected:** the `Director` role label for this branch's
   local authority — replaced with `Owner` per the reissued brief; the
   implicit allowance for a Worker to ever open a branch — replaced
   with an explicit, standalone prohibition (§3.5) separate from the
   "without Owner approval" clause (§3.6), matching the brief's own
   two-part phrasing.
4. **What is left for the next Worker:** any code-bearing task on this
   branch remains out of scope until the Owner issues one, per §3 and
   §10.6; §9's `Owner`-field naming collision (task-assignee vs.
   branch-authority) is flagged, not eliminated — a future Worker
   should not silently "fix" it without an Owner decision, since the
   brief specifies that exact field list verbatim.
5. **FROZEN:** all `.py` source under `data/`, `core/`, `context/`,
   `strategies/`, `signals/`, `decision/`, `risk/`, `execution/`, and
   every other module CLAUDE.md marks as change-controlled — untouched
   by this or the prior revision, and out of this document's authority
   to reopen.
6. **Opens next:** whatever code-bearing task the Owner explicitly
   authorizes next; until then, no `.py` file on this branch is in
   scope for any Worker.

## 15. Status

```
TASK-ID:    TASK-GOV-001 (Revision 2)
Goal:       Define the binding working order for claude/collaboration,
            with Owner terminology and an explicit no-new-branch rule.
Rules:      Sections 2, 4, 5, 6, 10 of this document.
Forbidden:  Section 3 of this document.
Allowed:    Governance/documentation authoring only (this file).
Input:      TASK-GOV-001 reissued brief (Owner instruction).
Output:     This document.
Owner:      Worker (this session) -- task-assignee sense, see Section 9.
Status:     REVIEW -- awaiting Owner approval.
Next step:  Owner reviews and either APPROVES (task closes DONE) or
            returns CHANGES REQUIRED with the specific correction.
```

## 16. References

- `docs/governance/roles/Collaboration_Rules.md` — the repository-wide
  Director / Core Worker / Platform Worker collaboration model this
  document does not replace.
- `docs/governance/policies/Branch_Policy.md` — the repository's branch
  model and branch-creation authorization rule.
- `CLAUDE.md` — the repository-wide Module Reuse Principle and Commit
  Protocol this document defers to for any future code-bearing task on
  this branch.
