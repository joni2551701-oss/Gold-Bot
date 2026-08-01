# Protected Architecture Documents Policy

Governed by `docs/constitution/CONSTITUTION.md` (supreme) and
`docs/governance/collaboration/TASK-GOV-001.md` (the `claude/collaboration`
working rules). Established following the Director's ruling on the
TASK-CORE-001 audit's authority-document observation.

## 1. Director Ruling (verbatim decision)

> "Audit observation acknowledged. No action required. The authoritative
> Master Documents already exist on `main`. Worker executed correctly
> for the branch it audited. Protected architecture documents are
> outside worker scope unless explicitly authorized."

The Worker that ran TASK-CORE-001 did not err — it audited
`claude/collaboration`, the branch it was told to work on, and reported
honestly what that branch contained.

## 2. Correction to the location claim (verified, not restated blindly)

The Director's message named `main/new map/` as the location of the 5
Master Documents. Verified against `origin/main` directly — this is
**not quite where they are**:

- The 5 named files (`01_Ecosystem_Architecture.md` …
  `05_Development_Standards.md`) exist **flat under `docs/`** on `main`
  — NOT under `New_Map/`.
- `New_Map/` is a **separate**, large, self-declared "CANONICAL
  REPOSITORY BLUEPRINT" tree (`New_Map/README.md`'s own words) — a
  target folder-structure blueprint, with its own
  `01_Data_Layer/…10_Future_Expansion/` hierarchy (README/Contracts/
  ModuleMap/SequenceDiagram per module). It is a distinct artifact from
  the 5 flat `docs/0N_*.md` files, not their container.

Both are protected under this policy (§3) regardless of the location
correction.

## 3. Protected Architecture Documents

**Location:** `main`'s `docs/01_Ecosystem_Architecture.md` …
`05_Development_Standards.md`, and `main`'s `New_Map/` tree (in full).

**Status:** READ ONLY for any Worker operating on `claude/collaboration`
or any other working branch.

**Rules:**
- No Worker may modify, move, rename, or delete these documents from a
  working branch.
- They are architectural source of truth on `main`.
- Any change requires explicit Director/Owner approval.
- A Worker who needs to reference them does so read-only (e.g. `git show
  origin/main:<path>`), never by merging or copying them into a working
  branch without an explicit Director instruction to do so.

## 4. Open finding this policy does NOT resolve (flagged for Director decision)

Verified while writing this policy, and reported here rather than acted
on unilaterally (Constitution Article 8, STOP → AUDIT → Owner Decision;
`TASK-GOV-001.md` Law 10, Branch Audit First):

- `claude/collaboration` is currently **102 commits behind `main`** and
  only 26 ahead (as of this task). The two branches have been
  developing **independent, non-identical architecture documentation**
  for the same concern:
  - `main`: flat `docs/01_Ecosystem_Architecture.md` (200 lines) +
    `docs/02_Repository_Structure.md` / `03_Module_Contracts.md` /
    `04_Data_Flow_Contracts.md` / `05_Development_Standards.md` + the
    `New_Map/` blueprint tree.
  - `claude/collaboration`: `docs/architecture/01_Ecosystem_Architecture.md`
    (770 lines — extended through TASK-GOV-003/004 and
    TASK-ARCH-100/101) + `docs/architecture/02_Data_Layer.md` …
    `11_Infrastructure.md` (the TASK-GOV-004 restructure family).
  - Both branches still share `docs/constitution/CONSTITUTION.md` and
    `docs/architecture/ARCHITECTURE_MASTER.md` (present on both,
    divergence not yet checked in detail).
- This means there are currently **two independently-evolved candidate
  "ecosystem architecture" document sets**, not one, across the two
  branches — beyond the scope of "a Worker didn't see a protected
  folder." Reconciling them (which becomes canonical, whether `New_Map/`
  supersedes the `docs/architecture/` numbered family built on
  `claude/collaboration`, or the reverse, or both survive scoped
  differently) is a Director/Owner decision, not made here.
- **Recommendation:** a dedicated branch-reconciliation audit (in the
  spirit of `TASK-GOV-002.md`, refreshed for current state) before the
  next architecture-bearing task, so future audits don't rediscover this
  gap piecemeal.

## 5. References

- `docs/constitution/CONSTITUTION.md`
- `docs/governance/collaboration/TASK-GOV-001.md` (Laws, esp. 10 Branch
  Audit First, 11 Fast-Forward Only)
- `docs/governance/collaboration/TASK-GOV-002.md` (prior branch audit
  precedent)
- `docs/governance/collaboration/TASK-CORE-001.md` (the audit that
  surfaced this)
- `docs/governance/policies/Branch_Policy.md`
