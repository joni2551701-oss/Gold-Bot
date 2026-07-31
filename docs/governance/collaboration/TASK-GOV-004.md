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
4. **File location** (`docs/01_Ecosystem_Architecture.md` vs.
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
   `docs/01_Ecosystem_Architecture.md`:
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

This Worker is asking rather than picking one, per Constitution Article
8's own distinction between an executable brief and roadmap/vision
guidance, and this branch's Law "No hidden refactor." Recorded here so
the next Worker (or this session, once answered) does not have to
re-derive why execution paused.

## 4. Status

```
TASK-ID:    TASK-GOV-004
Goal:       Record the Owner's ruling on TASK-ARCH-001's 4 conflicts
            and execute the unambiguous parts (Learning -> Academy
            rename); clarify scope before the docs/architecture/
            restructure.
Rules:      TASK-GOV-001.md Laws 1-12; Constitution Article 8.
Forbidden:  .py changes; moving/merging files before the Sec 3
            question is answered; silently choosing Option A or B.
Allowed:    Documentation edits (Learning rename only, this task);
            this record.
Input:      Owner's ruling message (this turn).
Output:     docs/01_Ecosystem_Architecture.md (Learning->Academy rename
            + Sec 21 updated); this document.
Owner:      Worker (this session) -- task-assignee sense.
Status:     ACTIVE -- rename done; restructure BLOCKED pending Sec 3 answer.
Next step:  Owner answers Option A vs Option B (or a third option);
            Worker executes the docs/architecture/ restructure under
            that answer as its own, separately validated commit.
```
