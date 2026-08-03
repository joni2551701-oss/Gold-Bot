# GoldBot Constitution — Amendment History

Every change to `docs/constitution/CONSTITUTION.md` is logged here,
per the Constitution's own Amendment process: explicit Director
instruction only, delivered as its own dedicated phase, never as a
side effect of an unrelated task.

## Phase 62.0 — Original ratification

**Articles 1–7 established.** Core Principle, Dependency Law, Import
Rules, Database Rule, Provider Rule, Testing Rule, Reuse Principle.
Written from a full audit of the real codebase as it stood after
Phase 61.7 (AI Runtime Integration). Self-corrected once during
drafting: the first draft of Article 1/2/3 wrongly claimed
`decision/`/`risk/` never import from `ai/`; corrected to state the
real, narrow, type-only exception (`decision/models.py`,
`decision/decision_engine.py` importing `AIAnalysisResult`) before
ratification. Commit `882c5b5`.

## Phase 62.1a — First amendment: Articles 8–12

**Added**, following the Director's explicit decision to formalize
what had been operating as unwritten Director Policy across Phase
62.2 and Phase 63.0:

- **Article 8 — Change Management Law.** Formalizes the STOP → AUDIT →
  Director Decision protocol and the Constitution → Architecture →
  Roadmap → Policy → Audit → Code reading/execution order, both of
  which were already in continuous practice since Phase 62.0 but not
  previously codified as law.
- **Article 9 — Version Compatibility Law.** Formalizes the "Foundation
  Stability Principle" the Director introduced as an immediate-effect
  Policy after Phase 63.0's freeze — a LOCKed module's name, path,
  import path, and public API do not change; only additive extension
  is permitted.
- **Article 10 — Owner Override Law.** Codifies the existing,
  previously-unwritten pattern that every critical module
  (`core_layer/emergency/`, `ai/runtime/`, `configuration/runtime_feature_manager.py`,
  and Phase 63.0's `broadcast/`/`media/`/`translation/`) surfaces
  through the Telegram Owner Panel, even when that surface is
  foundation-only.
- **Article 11 — Foundation Reuse Law.** Turns Article 7's Reuse
  Principle into an explicit, six-item mandatory checklist
  (Foundation / Manager / Contract / Model / Capability / Registry)
  for every Worker Brief's TASK 0 — the same checklist the Director
  specified by name in the post-Phase-63.0 review.
- **Article 12 — Architecture Evolution Law.** Makes the New/Extended/
  Reused table a mandatory part of every phase's Freeze document,
  with an explicit intended trend (New shrinking, Reused growing) as
  the system matures.

No existing Article (1–7) was altered by this amendment. Governance
structure also expanded alongside this amendment (not a Constitution
change itself, tracked separately): `docs/policies/` (11 files),
`docs/constitution/ARTICLES.md` (this index's sibling), and this
`AMENDMENTS.md` file were all introduced in Phase 62.1a.

## TASK-002B (Navigation Architecture) — Second amendment: Article 13

**Added**, following the Director's explicit decision (ADR-001,
`communication/decisions/ADR-001.md`) that GoldBot Platform is
architected around a Shared Platform Layer with five equal clients
(Telegram Bot, Telegram Mini App, Android, iOS, Desktop) rather than
around Telegram Bot with other clients added later:

- **Article 13 — Future First Principle.** Every Architecture document
  states its compatibility with all five target platforms, even for
  the four with zero code today, using the existing
  `platforms/capability_model.py`'s `SupportStatus` contract
  (Article 11's Foundation Reuse Law already required checking for
  this before building anything new — `SupportStatus` already existed
  from TASK-001, reused here rather than duplicated). Governs
  Architecture (design) only — does not require or authorize building
  any non-Telegram client today, and does not relax Article 8's
  Change Management order or Article 11's Reuse Audit.

No existing Article (1–12) was altered by this amendment.

## Related

- `docs/constitution/CONSTITUTION.md` — the current full text.
- `docs/constitution/ARTICLES.md` — a one-page index of all Articles.
- `docs/policies/DIRECTOR_POLICY.md` — the Director/Worker operating
  model Article 8 formalizes.
