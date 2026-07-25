# Platform Director Rulings Register

**Objective:** maintain the authoritative register of all **Director Platform Rulings (DPR)** —
recorded, authoritative governance decisions for the Platform layer, made under the GoldBot
Constitution and the Platform Constitution ([Chapter 11 — Product Director](Chapter11_ProductDirector.md),
[Chapter 15 — Decision Process](Chapter15_DecisionProcess.md)).

**Register fields (per ruling):** DPR Number · Title · Decision · Rationale · Related Chapters ·
Status · Effective Date · Superseded By (optional).

Related: [Platform Constitution Index](README.md) · [Platform Constitution Change Log](PLATFORM_CONSTITUTION_CHANGELOG.md) · [GoldBot Director Rulings Register](../DIRECTOR_RULINGS_REGISTER.md).

> **Provenance note (honesty).** DPR-008 … DPR-011 are transcribed **verbatim** from the Director's
> Final Review of the Platform Constitution v1.0; their *Decision* text is the Director's, and their
> *Rationale* is a neutral descriptive summary. DPR-001 … DPR-007 predate that review; their
> authoritative content is **pending transcription from the Director's records** (and/or
> reconciliation with the earlier platform decisions recorded as ADRs under
> `communication/decisions/`). They are listed as placeholders and are **not** reconstructed or
> invented here. **Open item for the Director:** supply the DPR-001…007 texts, or direct how they
> map onto the existing platform ADRs, and this register will be completed exactly.

---

## Active Rulings

### DPR-008 — Constitutional Hierarchy
- **Decision:** The Platform Constitution is subordinate to the GoldBot Constitution: it obeys it,
  does not modify it, and cannot come into conflict with it.
- **Rationale:** Fixes a single primary governing document and removes any ambiguity between the two
  editions.
- **Related Chapters:** [10](Chapter10_PlatformStructure.md), [38](Chapter38_AmendmentProcess.md), [40](Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

### DPR-009 — Platform Scope
- **Decision:** The Platform governs only: User Experience, Accounts, Subscriptions, Notifications,
  Payments, Analytics, Administration, and Services. Trading decisions remain the Core's authority.
- **Rationale:** Draws a clear line between platform (product/experience) concerns and Core (trading)
  authority.
- **Related Chapters:** [06](Chapter06_Scope.md), [18](Chapter18_PlatformArchitecture.md), [28](Chapter28_UserProfiles.md)–[35](Chapter35_Operations.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

### DPR-010 — Platform Safety Boundary
- **Decision:** The Platform does not create a signal, evaluate a signal, compute risk, alter AI
  decisions, or bypass Core logic. It only delivers to users results the Core has already cleared.
- **Rationale:** States the platform's non-amendable safety boundary in concrete terms, protecting
  Trading Safety at the surface layer.
- **Related Chapters:** [31](Chapter31_SignalDelivery.md), [36](Chapter36_RiskAndAbusePrevention.md), [40](Chapter40_FinalProvisions.md)
- **Status:** Active (non-amendable)
- **Effective Date:** 2026-07-25
- **Superseded By:** — (may be strengthened, never weakened)

### DPR-011 — Amendment Rule
- **Decision:** All future Platform changes must: (1) be consistent with the GoldBot Constitution;
  (2) not weaken Core safety principles; (3) not break the Gateway architecture.
- **Rationale:** Binds every future platform amendment to the primary constitution, safety, and the
  single-entry-point architecture.
- **Related Chapters:** [38](Chapter38_AmendmentProcess.md), [40](Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

---

## Pending Transcription (DPR-001 … DPR-007)

| DPR | Title | Decision | Rationale | Related Chapters | Status | Effective Date | Superseded By |
|---|---|---|---|---|---|---|---|
| DPR-001 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DPR-002 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DPR-003 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DPR-004 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DPR-005 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DPR-006 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| DPR-007 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |

*(Placeholders only. Content will be filled solely from the Director's authoritative ruling history —
never reconstructed here.)*

---

## Register Conventions

- **Append** each new ruling with the next DPR number and all eight fields.
- A ruling that changes a frozen platform chapter's meaning also requires the Amendment Process
  ([Chapter 38](Chapter38_AmendmentProcess.md)) and is cross-referenced from the
  [Platform Constitution Change Log](PLATFORM_CONSTITUTION_CHANGELOG.md).
- No DPR may conflict with the GoldBot Constitution or a GoldBot Director Ruling (DR); where they
  meet, the GoldBot ruling governs (DPR-008).
- Safety-related rulings may **strengthen** but never weaken the DPR-010 / DR-015 guarantees.
