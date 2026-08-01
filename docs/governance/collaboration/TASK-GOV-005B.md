# TASK-GOV-005B — Architecture Documentation Synchronization: New_Map/

Director-ordered follow-up to `TASK-GOV-005.md`. This order explicitly
supersedes the earlier "New_Map/ is Worker-out-of-scope" default stated
in `Protected_Architecture_Documents_Policy.md` §3 — that policy itself
requires "explicit Director/Owner approval" to change/move/copy
`New_Map/`, and this task's brief is exactly that approval, scoped to a
**verbatim copy onto `claude/collaboration`**, not a modification of
`main`'s copy. `main` remains the authoritative source
(`Protected_Architecture_Documents_Policy.md` is not amended — `New_Map/`
on `main` is still READ ONLY / Director-approval-only for any future
change).

**Docs-only. No `.py` touched. No refactoring. No business logic. No
tests. No DB migration. No rewrite/reinterpretation of content. No
merge.**

## What was done

`git checkout origin/main -- New_Map/` — brings the entire `New_Map/`
tree (121 files: README/Contracts/ModuleMap/SequenceDiagram per module,
across `01_Data_Layer/` … `10_Future_Expansion/`) into
`claude/collaboration`, staged exactly as it exists on `main`.

**Verified byte-identical:** `git diff --cached origin/main -- New_Map/`
shows no difference — every file is a verbatim copy, not rewritten,
not reinterpreted, not merged with anything already on
`claude/collaboration`. No file outside `New_Map/` was touched (`git
diff --cached --name-only` confirms only `New_Map/*` paths).

## Result

- `claude/collaboration` now has the same `New_Map/` tree as `main`.
- `main` remains the official Architecture Source of Truth — this copy
  does not change that; `claude/collaboration`'s copy is a synchronized
  read-only mirror, not a fork to edit independently (consistent with
  `Protected_Architecture_Documents_Policy.md`).
- Codebase (`.py`, config, tests, DB) is completely untouched.

## Relationship to the still-open TASK-GOV-005 questions (not resolved here)

This task only synchronizes `New_Map/`. It does not resolve, and was
not asked to resolve:
- The `docs/01_Ecosystem_Architecture.md` (main) vs.
  `docs/architecture/01_Ecosystem_Architecture.md` (collaboration,
  extended) relationship.
- Whether `docs/architecture/02_Data_Layer.md` … `11_Infrastructure.md`
  move to `archive/`.
- How `New_Map/`'s own "CANONICAL REPOSITORY BLUEPRINT" claim relates to
  the Constitution / `ARCHITECTURE_MASTER.md` / `docs/architecture/0N_*.md`
  authority chain already on `claude/collaboration`.

All still await a Director decision, per `TASK-GOV-005.md`.

## Status

```
TASK-ID:    TASK-GOV-005B
Goal:       Copy main's New_Map/ tree verbatim onto claude/collaboration.
Rules:      TASK-GOV-001.md Laws 1-12; this task's 7 explicit
            prohibitions (no .py, no refactor, no business logic, no
            tests, no DB migration, no rewrite, no merge).
Forbidden:  Everything except copying New_Map/ verbatim + this report.
Allowed:    New_Map/ copy (verified byte-identical); this record.
Input:      Director order (this turn) -- explicit approval superseding
            the prior "New_Map/ out of Worker scope" default.
Output:     New_Map/ (121 files, verbatim); this document.
Owner:      Worker (this session) -- task-assignee sense.
Status:     DONE.
Next step:  None required by this task. The three open reconciliation
            questions above remain for a future Director-ordered task.
```
