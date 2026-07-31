# TASK-GOV-001 — `claude/collaboration` Branch Rules

Governance-only task. **No source code is written, read for editing, or
modified by this task.** This document defines the working order for
the `claude/collaboration` branch: branch rules, the single-Worker
queue, the task lifecycle, Director/Worker responsibilities, the
handover format, and the task-status model.

This document does not replace, restate, or contradict the existing
Governance v1.1 documents (`docs/governance/roles/Collaboration_Rules.md`,
`docs/governance/policies/Branch_Policy.md`, `docs/governance/roles/
Director.md`, `Core_Worker.md`, `Platform_Worker.md`). Those govern the
Director / Core Worker / Platform Worker model across the whole
repository. `claude/collaboration` is a distinct, single-track working
branch with its own, simpler single-Worker queue — this document is
its own, self-contained operating rule, scoped to that branch only.
Where the two overlap (Director authority, No Silent Decisions, the
Commit Protocol, Trading Safety), this document defers to the existing
ones rather than duplicating them.

## 1. Purpose

To fix, before any further work happens on `claude/collaboration`, an
explicit, binding operating order: one branch, one Worker active at a
time, one task at a time, a fixed task lifecycle, a fixed handover
format, and a fixed set of things a Worker on this branch never does.

## 2. Core Principles

1. `main` is production. It is never touched directly from this branch.
2. `claude/collaboration` is the single working branch for the tasks
   this document governs.
3. Workers work in strict sequence — never two at once.
4. Every task is handled as its own, separately bounded unit.
5. Architecture and working-order rules take precedence over code —
   nothing is implemented before its rule is written and approved.

## 3. Hard Restrictions

A Worker operating under this document does **not**:

1. Write source code.
2. Modify any `.py` file.
3. Refactor pipeline, provider, stream, market, context, strategy,
   signal, decision, risk, or execution logic.
4. Touch `main` directly.
5. Work concurrently with another Worker on this branch.
6. Modify an existing FROZEN layer.
7. Mix tasks — one task is completed (or explicitly handed over)
   before the next begins.

A task that requires code falls outside this document's scope; it is
executed under its own, separately issued task once this governance
task is APPROVED and closed.

## 4. Branch Rules

- All new work under this governance model happens on
  `claude/collaboration`.
- A new branch is opened only when the Director explicitly authorizes
  it for that specific purpose — never speculatively, never by a
  Worker's own initiative.
- The branch name is fixed and is not renamed.
- `claude/collaboration` was branched from `main` (per Director
  direction for this task) and stays in sync with `main` at the
  Director's discretion — a Worker does not merge, rebase onto, or
  fast-forward it on its own initiative.

## 5. Worker Queue Rule

- Exactly one Worker is active on `claude/collaboration` at any time.
- When a Worker finishes (or is stopped mid-task with a Handover
  written), the next Worker continues on the same branch, from the
  same history — no parallel branches, no parallel Workers.
- Workers never overwrite another Worker's completed work; a
  disagreement with prior work is raised to the Director (No Silent
  Decisions), not silently rewritten.

## 6. Task Flow

Every task on `claude/collaboration` moves through this fixed sequence:

1. Task name is written.
2. Goal is written.
3. Rules are written.
4. Restrictions are written.
5. Deliverable is written.
6. Director approves the task definition.
7. Worker executes.
8. Worker writes the Handover.
9. The next Worker continues.

No step is skipped and no step is reordered. A task does not reach
step 7 (execution) without step 6 (Director approval) having happened.

## 7. Director and Worker Roles

### Director

- Sets the direction of work.
- Chooses which task is active now.
- Approves the rules and this governance document itself.
- Reviews the Worker's result against the task definition.
- Makes the merge decision (including into `main`).

### Worker

- Executes only the task assigned.
- Does not step outside the task's stated rules.
- Leaves a Handover at the end of its turn.
- Writes code only when a task explicitly assigns code — never in a
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

## 9. Task Record Format

Every task on `claude/collaboration` is recorded as exactly one entry,
in this fixed field order:

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
2. Reuse First — an existing module/document is extended before a new
   one is created (mirrors the repository-wide Module Reuse Principle
   in `CLAUDE.md`).
3. No duplicate logic.
4. No hidden refactor — a change outside a task's stated scope does not
   ride along inside it.
5. No merge into `main` without Director approval.
6. No code change inside a governance-only task.
7. Every task has one clear owner and one clear status at all times.
8. Every branch action is traceable to a task record and a commit.

## 11. Status Model

Every task is in exactly one of these states at any time:

| Status | Meaning |
|---|---|
| `PLANNED` | Task is written but not yet Director-approved. |
| `ACTIVE` | Director-approved; a Worker is currently executing it. |
| `REVIEW` | Worker has delivered; awaiting Director review. |
| `APPROVED` | Director has accepted the deliverable as-is. |
| `BLOCKED` | Execution cannot continue without a Director decision. |
| `FROZEN` | Layer/task is locked against further change until explicitly reopened. |
| `DONE` | Task is closed; its Handover has been consumed. |

## 12. Deliverable

This task's deliverable, all contained in this document:

1. The rule set (§2–§4, §10).
2. The branch working order (§4).
3. The Worker queue rule (§5).
4. The Handover procedure (§8).
5. The task status model (§11).
6. The list of forbidden actions (§3).
7. This final governance document, for Director approval.

## 13. Acceptance Criteria

This task is considered done when:

1. No code was written.
2. The rules are unambiguous.
3. The branch order is clear.
4. Worker/Director roles are separated.
5. The Handover system is written.
6. FROZEN layers are protected (§3.6, §10.1).
7. A future Worker can follow this document without further
   clarification.

## 14. Status

```
TASK-ID:    TASK-GOV-001
Goal:       Define the binding working order for claude/collaboration.
Rules:      Sections 2, 4, 5, 6, 10 of this document.
Forbidden:  Section 3 of this document.
Allowed:    Governance/documentation authoring only (this file).
Input:      TASK-GOV-001 brief (Director instruction).
Output:     This document.
Owner:      Worker (this session).
Status:     REVIEW — awaiting Director approval.
Next step:  Director reviews and either APPROVES (task closes DONE) or
            returns CHANGES REQUIRED with the specific correction.
```

## 15. References

- `docs/governance/roles/Collaboration_Rules.md` — the repository-wide
  Director / Core Worker / Platform Worker collaboration model this
  document does not replace.
- `docs/governance/policies/Branch_Policy.md` — the repository's branch
  model and branch-creation authorization rule (§5's "only under
  Director authorization" mirrors that policy's §5).
- `CLAUDE.md` — the repository-wide Module Reuse Principle (§10.2) and
  Commit Protocol this document defers to for any future code-bearing
  task on this branch.
