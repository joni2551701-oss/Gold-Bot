# GoldBot Ecosystem Architecture — Academy Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Academy Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

Two different things previously shared the word "Learning." Owner
ruling separates them permanently:

- **Learning Engine** — GoldBot Core's real, existing ML/feedback loop:
  `learning/` (`confidence.py`, `outcome_analyzer.py`,
  `pattern_detector.py`, `regime_memory.py`, `trade_event_bridge.py`)
  plus `database/learning_repository.py` and `ai/learning/`/
  `ai/learning_context.py`. The system learning from its own trade
  outcomes. **Status: real, implemented.** Belongs conceptually to
  GoldBot Core (Section 5) even though it has no dedicated diagram box
  there yet (no box was added by this rename — see Section 21, adding
  a diagram box is a separate decision from renaming one).
- **Academy** — the diagram's user-facing education product
  (Interactive Lessons, Simulator, AI Coach, Challenge, Tournament,
  PvP, Certification, Career Mode). **Status: vision only, does not
  exist.** This is this section's real subject now that the name no
  longer collides with the Learning Engine.

Conflict 3 (originally: same word, two systems) is **RESOLVED** by
this rename, not merely flagged — see Section 21's updated entry.

