# TASK-GOV-003 — Architecture Authority

Governance-only task. **No source code is written or modified.** No new
branch opened, no diagram changed, no module added to the architecture.
Rules per this task's brief and per `TASK-GOV-001.md` (FROZEN, Revision
3), whose Laws 1–12 govern this task without restatement.

## 1. Goal

Formalize `01_Ecosystem_Architecture.md` as the single official **Master
Architecture** of the Senior Trading AI Ecosystem (GoldBot), so that
every future technical task derives from it and no implementation
contradicts it.

## 2. What was done

1. Prepended an **Architecture Authority** section to the master
   architecture document. The section states the five binding
   principles (Master Architecture; basis for all technical tasks;
   placement-before-implementation; no-contradiction; the
   architecture-first change protocol) and the governance control chain
   (Architecture → Architecture Tasks → Technical Tasks → Implementation
   → Review → Merge). The existing diagram and the Golden Architecture
   Rules below it were left **byte-for-byte unchanged** (Forbidden:
   "Diagrammani o'zgartirmaydi" / "Arxitekturaga yangi modul
   qo'shmaydi").
2. Established the governance ↔ architecture linkage here (§4) and via
   the master document's own "Relationship to governance" block, which
   references this task, `TASK-GOV-001.md`, `Collaboration_Rules.md`,
   and `Branch_Policy.md`.

## 3. Path discrepancy (flagged, not silently changed)

The brief names the file `docs/architecture/01_Ecosystem_Architecture.md`.
The file actually exists at **`docs/01_Ecosystem_Architecture.md`** (added
by commit `6666f62` on `claude/collaboration`, and independently by
`4e92989` on `main`). This Worker did **not** move the file — a
relocation is a repository action the brief did not request, and the
Owner created the file at `docs/`. The Architecture Authority section
was added to the file where it actually lives. If the Owner wants the
file relocated under `docs/architecture/`, that is a separate,
explicitly-authorized action (its references would then be updated in
lockstep).

## 4. Governance linkage

- `01_Ecosystem_Architecture.md` is the **Architecture Authority** — the
  root of the technical-task chain. Every Architecture Task and every
  Technical Task derives from it.
- `TASK-GOV-001.md` (FROZEN) already carries **Architecture First** in
  spirit (Law 2 Reuse First, Law 4 No hidden refactor, the task
  lifecycle). This task adds the concrete architecture those rules point
  at. **`TASK-GOV-001.md` was deliberately NOT edited** — it is FROZEN
  (its §10.6 requires a new Owner-approved task to change it, and even
  then a frozen-doc edit is a heavier action than this task's brief
  authorized). The governance→architecture reference therefore lives
  here and in the master document, not inside the frozen file. If the
  Owner wants a cross-reference embedded directly in `TASK-GOV-001.md`,
  that needs an explicit go-ahead (it would be a Revision 4 of a FROZEN
  document).
- Repository-wide, `docs/governance/roles/Collaboration_Rules.md` §2
  already states **Architecture First** as a mandatory collaboration
  principle; this task supplies the single architecture document that
  principle now resolves to.

## 5. Deliverable checklist

1. Architecture Authority section — added to
   `docs/01_Ecosystem_Architecture.md`. ✅
2. Governance linkage — §4 above + the master doc's "Relationship to
   governance" block. ✅
3. Cross-references between documents — master doc ⇄ this task ⇄
   TASK-GOV-001/002 ⇄ Collaboration_Rules/Branch_Policy. ✅
4. Final audit — §6. ✅

## 6. Final audit

- **Code unchanged:** no `.py` file touched (verified: `git diff
  --cached --stat` shows only Markdown under `docs/`).
- **Master Architecture formalized:** the Architecture Authority section
  is present at the top of the document, above the unchanged diagram.
- **Aligned with governance:** references the collaboration rules and
  branch policy; does not edit the FROZEN `TASK-GOV-001.md`.
- **Future tasks anchored:** the governance control chain
  (Architecture → Architecture Tasks → Technical Tasks → Implementation
  → Review → Merge) is written into the authority document, so every
  future task now has a single document to derive from.
- **Diagram integrity:** the ASCII architecture diagram and the 10
  Golden Architecture Rules are unchanged.

## 7. Handover

1. **What was reviewed:** the master document
   (`docs/01_Ecosystem_Architecture.md`), the frozen `TASK-GOV-001.md`,
   `TASK-GOV-002.md`, and the branch state (`main` vs
   `claude/collaboration`).
2. **What was accepted:** the master document as the single Architecture
   Authority; its existing diagram and Golden Rules as authoritative and
   unchanged.
3. **What was rejected:** editing the FROZEN `TASK-GOV-001.md`; moving
   the file to `docs/architecture/`; any change to the diagram — all out
   of scope / freeze-protected.
4. **What is left for the next Worker:**
   - **main ↔ collaboration reconciliation:** `main` (`4e92989`) and
     `claude/collaboration` (`6666f62`) each added
     `docs/01_Ecosystem_Architecture.md` as a *separate* commit with
     identical 201-line content; `claude/collaboration` is 1 commit
     behind `main`. Reconciling the two branches is an Owner-approved
     merge (Law 11), not done here.
   - **Optional:** relocating the file under `docs/architecture/` and/or
     embedding an Architecture-Authority cross-reference into the frozen
     `TASK-GOV-001.md` — both need explicit Owner authorization.
5. **FROZEN:** `TASK-GOV-001.md`; the architecture diagram + Golden
   Rules inside the master document; all `.py` source under every
   CLAUDE.md change-controlled module.
6. **Opens next:** whichever Architecture Task or Technical Task the
   Owner issues — now formally required to derive from
   `01_Ecosystem_Architecture.md`.

## 8. Status

```
TASK-ID:    TASK-GOV-003
Goal:       Formalize 01_Ecosystem_Architecture.md as the single
            official Master Architecture (Architecture Authority).
Rules:      TASK-GOV-001.md Laws 1-12; architecture-first change protocol.
Forbidden:  Code changes; diagram changes; adding a module to the
            architecture; editing the FROZEN TASK-GOV-001.md; new branch.
Allowed:    Governance/architecture-document authoring only.
Input:      TASK-GOV-003 brief (Owner instruction).
Output:     Architecture Authority section in
            docs/01_Ecosystem_Architecture.md; this document.
Owner:      Worker (this session) -- task-assignee sense.
Status:     SUPERSEDED -- see Section 9 below.
Next step:  n/a -- corrected under TASK-ARCH-001.
```

## 9. Correction (recorded under TASK-ARCH-001)

This task's central claim -- that `01_Ecosystem_Architecture.md` is
"the single official Master Architecture... where any other document
appears to describe the ecosystem's shape, this document is the one
that governs" -- was **wrong** and has been withdrawn. It was written
without checking for `docs/constitution/CONSTITUTION.md` (which
predates this task and already states "This is the single
highest-authority governance document in this repository") or
`docs/architecture/ARCHITECTURE_MASTER.md` and its siblings
(`LAYER_CONTRACT.md`, `MODULE_DEPENDENCIES.md`, `DATA_FLOW.md`,
`SYSTEM_LAYERS.md`) -- an existing, Constitution-governed,
code-verified architecture set covering most of what this task
believed it was establishing for the first time. This was a
Reuse-First failure (Constitution Article 7 / CLAUDE.md Module Reuse
Principle) on this Worker's part.

Corrected under `docs/governance/collaboration/TASK-ARCH-001.md`
(Owner-directed): `01_Ecosystem_Architecture.md`'s Architecture
Authority section is now Revision 2, scoped honestly as the
**Ecosystem Architecture** document (the wider vision layers the
Constitution-governed set does not cover) rather than a supreme
authority over the whole repository. See that task's record for the
full correction and the "Division of authority" section it added.

This task (TASK-GOV-003) is marked **SUPERSEDED**, not DONE and not
deleted -- its audit and cross-reference work stand, only its central
authority claim is withdrawn. Kept in place per this branch's own Law
4 (No hidden refactor) -- the record of the mistake stays visible
rather than being quietly rewritten.
