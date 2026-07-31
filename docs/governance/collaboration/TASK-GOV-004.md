# TASK-GOV-004 — Owner Decision on TASK-ARCH-001 Conflicts

Governance/documentation-only. **No `.py` file touched.** Records the
Owner's ruling on the 4 conflicts `TASK-ARCH-001.md` §5 listed, and
the resulting documentation changes. Rules per `TASK-GOV-001.md`
(FROZEN, Revision 3), Laws 1–12, referenced not restated.

## 1. Owner Decision (received, APPROVED with rulings)

TASK-ARCH-001 was APPROVED. The Owner ruled on all four listed
conflicts rather than leaving them open indefinitely:

1. **Market Engine / Analysis Engine / Confluence Engine** —
   **RETAINED, "Accepted as Future Architecture."** The diagram is the
   target; code has not reached it, and the diagram is not lowered to
   match current code.
2. **AI Layer (Senior/Seniorita/Trading AI/Learning AI/Voice AI/Vision
   AI)** — **RETAINED, "Accepted."** These are logical services, not a
   claim of physical folder structure; the real single-`ai/`-package
   implementation underneath is correctly described elsewhere
   (Section 7).
3. **"Learning" naming collision** — **Owner agreed a rename was
   needed.** Split into "Learning Engine" (GoldBot Core's real ML/
   feedback loop) vs. "Academy" (the vision's user-facing education
   product). Status: RESOLVED.
4. **File location** (`docs/architecture/01_Ecosystem_Architecture.md` vs.
   `docs/architecture/`) — **Owner directed a restructure**: consolidate
   under `docs/architecture/`, with `01_Ecosystem_Architecture.md`
   (high-level) plus `02_Data_Layer.md` through `11_Infrastructure.md`
   (per-layer detail), and `docs/constitution/CONSTITUTION.md` staying
   separate above it. Status: PLANNED, execution paused on one
   clarifying question (§3 below) before any file is moved.

The Owner additionally proposed a hierarchy: "CONSTITUTION —
governance. `01_Ecosystem_Architecture` — the single source of
technical architecture. The rest elaborate on 01." This is a real,
substantive shift from `TASK-ARCH-001`'s "Division of authority"
(where `ARCHITECTURE_MASTER.md`+siblings remained independently
authoritative for the Trading Core/AI/Telegram system, and
`01_Ecosystem_Architecture.md` was scoped only to the wider vision
layers). See §3 — this Worker did not silently adopt the new hierarchy
without confirming its depth first, per Constitution Article 8 (STOP →
AUDIT → Owner Decision) and this branch's Law 4 (No hidden refactor).

## 2. What was done immediately (unambiguous, low-risk)

1. **Learning → Academy rename** (Owner ruling on Conflict 3), in
   `docs/architecture/01_Ecosystem_Architecture.md`:
   - Diagram section header `LEARNING LAYER` → `ACADEMY LAYER (User
     Education)`, with a short note distinguishing it from the real
     `learning/` package ("Learning Engine").
   - Documentation Section 11 retitled "Academy Layer (renamed from
     'Learning Layer' — Owner ruling, Conflict 3 RESOLVED)," explicitly
     splitting Learning Engine (real, GoldBot Core) from Academy
     (vision, does not exist).
   - No other diagram content changed (per rulings 1/2, "Accepted as
     Future Architecture" / "Accepted" — no edit needed for those).
2. **Section 21 (Conflicts Requiring Owner Decision) updated** with all
   four rulings and their resulting status (Accepted as Future
   Architecture / Accepted / RESOLVED / PLANNED).
3. **This record** (`TASK-GOV-004.md`).

## 3. Clarifying question before the restructure (§4's ruling)

The Owner's directed structure —
`docs/architecture/{01_Ecosystem_Architecture,02_Data_Layer,
03_GoldBot_Core,...,11_Infrastructure}.md` — is clear as a target
*filename layout*. What is not yet clear, and materially changes how
much this Worker would touch, is **what `02_Data_Layer.md`,
`03_GoldBot_Core.md`, etc. actually contain**:

- **Option A** — they are new files created by *splitting this
  document's own Sections 4–14* (currently one file) into one file per
  section, keeping the Division of Authority from TASK-ARCH-001
  unchanged: each new file stays an ecosystem-level summary that
  cross-references `ARCHITECTURE_MASTER.md`/`MODULE_DEPENDENCIES.md`/
  `LAYER_CONTRACT.md`/`DATA_FLOW.md`/`MARKET_DATA_FOUNDATION.md`/
  `PRICE_STREAM.md`/`LIVE_PRICE.md` for Trading-Core mechanical detail,
  same as today, just relocated and split into 10 files instead of 10
  sections in one file. Low blast radius: pure move/split of content
  this Worker already wrote and the Owner already approved.
- **Option B** — `02_Data_Layer.md`, `03_GoldBot_Core.md` etc. absorb
  the *actual detailed content* of `ARCHITECTURE_MASTER.md`,
  `LAYER_CONTRACT.md`, `MODULE_DEPENDENCIES.md`, `DATA_FLOW.md`,
  `MARKET_DATA_FOUNDATION.md`, `PRICE_STREAM.md`, `LIVE_PRICE.md` etc.
  into themselves, making the numbered family the *single* technical
  architecture source the Owner's own wording ("texnik arxitekturaning
  yagona manbai") suggests. High blast radius: this would mean merging/
  migrating ~2,000 lines of Constitution-referenced, code-verified
  content that `docs/constitution/CONSTITUTION.md` itself names
  specifically (Article 1/2 reference `ARCHITECTURE_MASTER.md` by
  name) — a change to what the Constitution points at, which
  Constitution Article 8 requires explicit sign-off for before
  execution, not inference from a roadmap-style message.

This Worker asked rather than picking one, per Constitution Article
8's own distinction between an executable brief and roadmap/vision
guidance, and this branch's Law "No hidden refactor." **Owner answered:
Option A** (ecosystem-level summaries, low blast radius — the
Division of Authority from TASK-ARCH-001 is unchanged; nothing merges
into the numbered files that isn't already this document's own former
Section content).

## 4. Restructure executed (Option A)

1. `docs/01_Ecosystem_Architecture.md` moved (`git mv`) to
   `docs/architecture/01_Ecosystem_Architecture.md` — now alongside
   `ARCHITECTURE_MASTER.md` and its siblings, resolving Conflict 4.
2. Its former Sections 4–12 and 14 (Data Layer, GoldBot Core,
   Application Services, AI Layer, Platform Layer, User Experience,
   Business Layer, Academy Layer, Media Layer, Infrastructure) were
   extracted verbatim into ten new standalone files —
   `02_Data_Layer.md` through `11_Infrastructure.md` — each carrying a
   standard header restating its scope (ecosystem-level summary,
   cross-references the Constitution-governed set, does not duplicate
   it). No section content was rewritten in extraction, only relocated
   and given a file-level header.
3. `01_Ecosystem_Architecture.md` itself was rebuilt: the extracted
   sections were replaced by a "Layer Detail Documents" index (near the
   top, listing all ten files); its remaining sections (Vision,
   Ecosystem Overview, Architecture Principles, Future Expansion,
   Complete Data Flow, Dependency Rules, Refactoring Audit, Gap
   Analysis, Future Roadmap, Golden Rules extended, Conflicts, Self-
   Test) were renumbered sequentially (1–12) and every internal
   `Section N` cross-reference was mechanically rewritten — either to
   the new section number (for content that stayed in `01`) or to the
   new filename (for content that moved out). The original ASCII
   diagram and the original 10 Golden Rules are untouched (same
   verification as TASK-ARCH-001: their header strings each appear
   exactly once).
4. `docs/architecture/01_Ecosystem_Architecture.md`'s own "Division of
   authority" diagram updated to show the `02`–`11` family under `01`,
   consistent with the new file layout.
5. Every reference to the old path (`docs/01_Ecosystem_Architecture.md`)
   across `TASK-GOV-003.md`, `TASK-ARCH-001.md`, and this file updated
   to the new path; `TASK-GOV-003.md` §3's now-resolved path
   discrepancy rewritten for clarity (was describing a live problem,
   now describes a resolved one, per its own note pointing here).

**Note on the Owner's proposed hierarchy** ("CONSTITUTION — governance.
`01_Ecosystem_Architecture` — the single source of technical
architecture. The rest elaborate on 01."): Option A confirms this reads
as *file-layout* guidance (numbered files under one directory), not a
reversal of TASK-ARCH-001's Division of Authority (`ARCHITECTURE_MASTER.md`
+siblings remain independently authoritative for the Trading Core/AI/
Telegram system's mechanical detail). If the Owner intends something
stronger later, that is Option B, and remains a separate,
explicitly-authorized action per §3 above — not inferred here.

## 5. Status

```
TASK-ID:    TASK-GOV-004
Goal:       Record the Owner's ruling on TASK-ARCH-001's 4 conflicts
            and execute them: Learning -> Academy rename (Conflict 3),
            and the docs/architecture/ restructure (Conflict 4, Option A).
Rules:      TASK-GOV-001.md Laws 1-12; Constitution Article 8.
Forbidden:  .py changes; Option B (absorbing Constitution-governed
            content) without further explicit authorization.
Allowed:    Documentation edits, file moves/splits within docs/.
Input:      Owner's ruling message + Option A confirmation (this turn).
Output:     docs/architecture/{01..11}_*.md (moved/split);
            docs/governance/collaboration/{TASK-GOV-003,TASK-ARCH-001}.md
            (path references updated); this document.
Owner:      Worker (this session) -- task-assignee sense.
Status:     DONE.
Next step:  None required. A future Architecture Task may choose to
            act on Conflicts 1/2 (diagram-vs-ARCHITECTURE_MASTER.md
            mismatch, AI Layer naming) -- both remain "Accepted as
            Future Architecture" / "Accepted" per the Owner's rulings,
            not open questions.
```
