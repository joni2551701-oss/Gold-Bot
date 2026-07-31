# GoldBot Ecosystem Architecture — AI Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the AI Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

Full detail: `docs/architecture/ARCHITECTURE_MASTER.md`'s AI Layer
section (five tracks: Infrastructure/Runtime/Intelligence/Product/
Broadcast) and `docs/architecture/AI_FLOW.md`. Not restated here.

**What the diagram names vs. what exists:** the diagram above lists
Senior / Seniorita / Trading AI / Learning AI / Voice AI / Vision AI as
if they were six separate systems. In the actual repository this is
**one** `ai/` package (confirmed by this audit — no separate top-level
module per name), organized into the five ARCHITECTURE_MASTER.md
tracks plus a `voice/` package and `ai/chart_intelligence/` (the
closest thing to "Vision AI"). This is a genuine naming/structure gap
between the ecosystem vision and the real code — logged in Section 18
and Section 21, not resolved here.

**What AI does / does not do** (Constitution Article 1 — restated only
because it is this ecosystem's single most important boundary, so it
is worth stating in both documents): the AI layer explains, analyzes,
summarizes, and educates. It never approves or rejects a trade, never
calls `decision/decision_engine.py` or `risk/risk_manager.py`, never
executes an order, and never sends a Telegram message that bypasses
the pipeline's own eligibility filter. This boundary is permanent
(Constitution Article 1: "It will never give the AI a vote"), not a
temporary limitation.

