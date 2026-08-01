# TASK-GOV-005 — Bring main's Official docs/ Documents to claude/collaboration

Director-ordered. Governed by `TASK-GOV-001.md` Laws 1–12 (referenced,
not restated). **Docs-only. No `.py` touched. No config touched. No
tests touched. No refactoring. No merge/rewrite — the 5 files are
verified byte-identical copies of `main`'s versions. `New_Map/` was not
touched at all.**

## What was done

1. Copied `main`'s 5 official `docs/` documents into `claude/collaboration`
   at the same path, verbatim:
   - `docs/01_Ecosystem_Architecture.md` (200 lines)
   - `docs/02_Repository_Structure.md` (259 lines)
   - `docs/03_Module_Contracts.md` (411 lines)
   - `docs/04_Data_Flow_Contracts.md` (574 lines)
   - `docs/05_Development_Standards.md` (421 lines)
   Verified byte-identical to `origin/main` (diff: none) — no rewrite,
   no merge, no edit of any kind.
2. Compared against `claude/collaboration`'s existing architecture docs
   (below).
3. **No file was archived or moved.** Per the Director's own two-option
   instruction ("Kerak bo'lsa ... ko'chirish, yoki Director qarorigacha
   o'zgarishsiz qoldirish"), this Worker does not decide "kerak" for
   itself — `docs/architecture/`'s working family is left completely
   unchanged, pending an explicit Director decision.

## Comparison / Differences Report

### `docs/01_Ecosystem_Architecture.md` (main, just copied) vs. `docs/architecture/01_Ecosystem_Architecture.md` (collaboration's own)

These are **two different files at two different paths** — no
filesystem collision, but the content has diverged substantially:

| | `docs/01_Ecosystem_Architecture.md` (main, new copy) | `docs/architecture/01_Ecosystem_Architecture.md` (collaboration) |
|---|---|---|
| Lines | 200 | 770 |
| Content | The **original, pristine** ASCII ecosystem diagram + the original 10 Golden Rules only. No Architecture Authority section, no corrections. | The same original diagram + Golden Rules, PLUS: an Architecture Authority section (Revisions 1→2, correcting an earlier overclaim), a "Division of authority" diagram, a "Layer Detail Documents" index, and 12 numbered sections (Vision, Overview, Principles, Future Expansion, Data Flow, Dependency Rules, Refactoring Audit, Gap Analysis, Roadmap, extended Golden Rules, Conflicts Requiring Owner Decision, Self-Test) built across TASK-GOV-003/004 and TASK-ARCH-100/101 this session. |
| "LEARNING LAYER" section | Still named `LEARNING LAYER` (original) | Renamed `ACADEMY LAYER (User Education)` per an explicit Owner ruling (TASK-ARCH-101, Conflict 3) distinguishing it from the real `learning/` ML package ("Learning Engine") |
| Diagram / Golden Rules | Original | Byte-identical to the original (verified in TASK-ARCH-100/101 — never edited) |
| Layer detail | None — this is the only file; no split-out layer docs on `main` at this path | Split into `docs/architecture/02_Data_Layer.md` … `11_Infrastructure.md` (TASK-GOV-004 restructure) |

**Conclusion:** `main`'s copy is the pre-TASK-GOV-003 baseline;
`collaboration`'s version is that same baseline plus everything built
on top of it this session, with real Owner rulings embedded (the
Academy rename, the Division-of-Authority correction). Neither
supersedes the other automatically — this is exactly the divergence
flagged in `Protected_Architecture_Documents_Policy.md` §4, now
concretely visible file-by-file.

### `docs/02_Repository_Structure.md`, `03_Module_Contracts.md`, `04_Data_Flow_Contracts.md`, `05_Development_Standards.md` (main, just copied) — no collaboration equivalent exists

`claude/collaboration` has **no prior document with this exact scope**.
Its own `docs/architecture/02_Data_Layer.md` … `11_Infrastructure.md`
family is organized **by ecosystem layer** (Data Layer, GoldBot Core,
Application Services, AI Layer, Platform Layer, …) — a different
categorization from `main`'s four documents, which are organized **by
concern** (repository folder structure; module contract standard; data
flow contract standard; development standards). There is no 1:1
correspondence and no naming collision:

| main document (just copied) | Scope | Nearest collaboration content |
|---|---|---|
| `02_Repository_Structure.md` | Canonical folder-by-folder repository layout ("Hech bir modul ushbu strukturadan tashqarida yaratilmaydi") | Partially overlaps `docs/architecture/02_Data_Layer.md` (Data Layer folder detail only) and the `New_Map/` blueprint on `main` (not copied — protected) |
| `03_Module_Contracts.md` | "MASTER CONTRACT" — module contract standard (Status/Priority/Authority header format) | No direct equivalent; loosely related to `docs/architecture/LAYER_CONTRACT.md` (Constitution-governed, different format) |
| `04_Data_Flow_Contracts.md` | "MASTER CONTRACT" — data flow contract standard | Loosely related to `docs/architecture/DATA_FLOW.md` (Constitution-governed, real pipeline stage order) and `01_Ecosystem_Architecture.md`'s §5 Complete Data Flow (ecosystem-level) |
| `05_Development_Standards.md` | "MASTER STANDARD" — development standards | Loosely related to `CLAUDE.md`'s Commit Protocol / `docs/DEVELOPMENT_RULES.md` (different scope: naming/testing conventions, not this document's content) |

These four are **net-new content** to `claude/collaboration` — nothing
to reconcile at the file level (no existing file they overwrite or
duplicate exactly), but they use "MASTER CONTRACT"/"MASTER STANDARD"
status labels that raise the same authority question as §01: how they
relate to the Constitution-governed `docs/architecture/*.md` set and to
`claude/collaboration`'s own `docs/architecture/0N_*.md` family is an
open question, not resolved by this copy step.

## What is explicitly NOT decided here

- Whether `main`'s `docs/01_Ecosystem_Architecture.md` (pristine)
  supersedes, is superseded by, or coexists with `claude/collaboration`'s
  `docs/architecture/01_Ecosystem_Architecture.md` (extended).
- Whether `docs/architecture/02_Data_Layer.md` … `11_Infrastructure.md`
  should move to `archive/` — left completely unchanged, per the
  Director's own "or leave unchanged pending Director decision" option.
- How `02_Repository_Structure.md` / `03_Module_Contracts.md` /
  `04_Data_Flow_Contracts.md` / `05_Development_Standards.md`'s "MASTER
  CONTRACT"/"MASTER STANDARD" status relates to the Constitution /
  `ARCHITECTURE_MASTER.md` authority chain already established on
  `claude/collaboration`.

All three are Director decisions, per Constitution Article 8 and this
branch's own Law 4 (No hidden refactor) — not inferred or acted on by
this Worker.

## Status

```
TASK-ID:    TASK-GOV-005
Goal:       Bring main's 5 official docs/ documents to
            claude/collaboration; compare; report; do not touch
            New_Map/, code, config, tests, or refactor anything.
Rules:      TASK-GOV-001.md Laws 1-12; Director's 7 explicit
            constraints (this task's brief).
Forbidden:  New_Map/; .py files; config files; tests; refactoring;
            merge; rewrite; deciding archive-or-not unilaterally.
Allowed:    Copying the 5 named files verbatim; this comparison report.
Input:      Director order (this turn).
Output:     docs/01_Ecosystem_Architecture.md,
            docs/02_Repository_Structure.md, docs/03_Module_Contracts.md,
            docs/04_Data_Flow_Contracts.md,
            docs/05_Development_Standards.md (all copied, byte-identical
            to main); this report.
Owner:      Worker (this session) -- task-assignee sense.
Status:     DONE (copy + compare + report). Archive decision explicitly
            NOT made -- awaiting Director.
Next step:  Director decides (a) the docs/01_Ecosystem_Architecture.md
            (main) vs. docs/architecture/01_Ecosystem_Architecture.md
            (collaboration) relationship, and (b) whether
            docs/architecture/02-11 move to archive/ or stay. Until
            then both sets coexist unchanged.
```
