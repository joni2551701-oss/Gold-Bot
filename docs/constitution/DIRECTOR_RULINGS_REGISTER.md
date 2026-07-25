# Director Rulings Register

**Objective:** maintain the authoritative register of all **Director Rulings (DR)**.
A Director Ruling is a recorded, authoritative governance decision under the
Constitution ([Chapter 11 — Director](chapters/Chapter11_Director.md),
[Chapter 15 — Decision Process](chapters/Chapter15_DecisionProcess.md)).

**Register fields (per ruling):** DR Number · Title · Decision · Rationale · Related
Chapters · Status · Effective Date · Superseded By (optional).

Related: [Constitution Index](chapters/README.md) · [Constitution Change Log](CONSTITUTION_CHANGELOG.md) · operative decision history in [`docs/changelog/DECISION_LOG.md`](../changelog/DECISION_LOG.md) and the ADRs under [`communication/decisions/`](../../communication/decisions/).

> **Provenance note (honesty).** DR-013 … DR-016 are transcribed **verbatim** from the
> Director's Final Review of Constitution v1.0; their *Decision* text is the
> Director's, and their *Rationale* is a neutral descriptive summary, not attributed
> Director wording. DR-001 … DR-012 predate that review; their authoritative content
> is **pending transcription from the Director's records** and is intentionally not
> reconstructed or invented here. **Open item for the Director:** supply the
> DR-001…012 texts, or direct how they map onto existing `DD-`/ADR/`DECISION_LOG`
> entries, and this register will be completed exactly.

---

## Active Rulings

### DR-013 — Constitution Consolidation
- **Decision:** The GoldBot Chaptered Constitution v1.0 is the primary and only
  normative governance document. `CONSTITUTION.md`, `ARTICLES.md`, and
  `AMENDMENTS.md` are retained as historical documents and are no longer independent
  normative sources; their necessary content is consolidated into the Chaptered
  Constitution v1.0 or migrated via future amendments.
- **Rationale:** Establishes a single normative source and removes ambiguity between
  the chaptered and Articles-based editions.
- **Related Chapters:** [10](chapters/Chapter10_ConstitutionStructure.md), [40](chapters/Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

### DR-014 — Constitution Freeze
- **Decision:** The present 40 chapters are frozen as Constitution Baseline v1.0
  (Frozen Baseline). Any change is made only via an ADR, the Constitution Amendment
  Process, and Director approval.
- **Rationale:** Locks a stable baseline so the ecosystem can build on it; changes
  become deliberate and governed rather than ad hoc.
- **Related Chapters:** [38](chapters/Chapter38_AmendmentProcess.md), [40](chapters/Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

### DR-015 — Safety Guarantees (non-amendable)
- **Decision:** The following are confirmed as non-amendable constitutional
  principles: (1) the Risk Manager is not bypassed; (2) the AI does not independently
  execute trades; (3) human oversight is preserved; (4) Trading Safety takes
  precedence over all other modules.
- **Rationale:** Makes the user's structural protection permanent and beyond the
  reach of the amendment process.
- **Related Chapters:** [07](chapters/Chapter07_NonGoalsAndTerminology.md), [28](chapters/Chapter28_AIArchitecture.md), [36](chapters/Chapter36_RiskGovernance.md), [40](chapters/Chapter40_FinalProvisions.md)
- **Status:** Active (non-amendable)
- **Effective Date:** 2026-07-25
- **Superseded By:** — (may be strengthened, never weakened)

### DR-016 — Single Source of Truth
- **Decision:** The Constitution defines principles; operative detail is carried via
  architecture docs, ADRs, standards, policies, and specifications. Identical rules
  are not written twice.
- **Rationale:** Prevents duplicated, drifting governance and keeps one authoritative
  source per domain.
- **Related Chapters:** [10](chapters/Chapter10_ConstitutionStructure.md), [16](chapters/Chapter16_DocumentationGovernance.md), [37](chapters/Chapter37_ComplianceFramework.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

---

## Pending Transcription (DR-001 … DR-012)

| DR | Title | Decision | Rationale | Related Chapters | Status | Effective Date | Superseded By |
|---|---|---|---|---|---|---|---|
| DR-001 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-002 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-003 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-004 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-005 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-006 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-007 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-008 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-009 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-010 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-011 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DR-012 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |

*(Placeholders only. Content will be filled solely from the Director's authoritative
ruling history — never reconstructed here.)*

---

## Register Conventions

- **Append** each new ruling with the next DR number and all eight fields.
- A ruling that changes a frozen chapter's meaning also requires the Amendment
  Process ([Chapter 38](chapters/Chapter38_AmendmentProcess.md)) and is
  cross-referenced from the [Constitution Change Log](CONSTITUTION_CHANGELOG.md).
- **Superseded By** is set (not deleted) when a later ruling replaces an earlier one,
  preserving the full history.
- Safety-related rulings may **strengthen** but never weaken the DR-015 guarantees.
