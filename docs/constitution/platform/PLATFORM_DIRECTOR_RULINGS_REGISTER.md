# Platform Director Rulings Register

**Objective:** maintain the authoritative register of all **Director Platform Rulings (PLATFORM-DCR)** —
recorded, authoritative governance decisions for the Platform layer, made under the GoldBot
Constitution and the Platform Constitution ([Chapter 11 — Product Director](Chapter11_ProductDirector.md),
[Chapter 15 — Decision Process](Chapter15_DecisionProcess.md)).

**Register fields (per ruling):** PLATFORM-DCR Number · Title · Decision · Rationale · Related Chapters ·
Status · Effective Date · Superseded By (optional).

Related: [Platform Constitution Index](README.md) · [Platform Constitution Change Log](PLATFORM_CONSTITUTION_CHANGELOG.md) · [GoldBot Director Rulings Register](../DIRECTOR_RULINGS_REGISTER.md).

> **Provenance note (honesty).** PLATFORM-DCR-008 … PLATFORM-DCR-011 are transcribed **verbatim** from the Director's
> Final Review of the Platform Constitution v1.0; their *Decision* text is the Director's, and their
> *Rationale* is a neutral descriptive summary. PLATFORM-DCR-001 … PLATFORM-DCR-007 predate that review; their
> authoritative content is **pending transcription from the Director's records** (and/or
> reconciliation with the earlier platform decisions recorded as ADRs under
> `communication/decisions/`). They are listed as placeholders and are **not** reconstructed or
> invented here. **Open item for the Director:** supply the PLATFORM-DCR-001…007 texts, or direct how they
> map onto the existing platform ADRs, and this register will be completed exactly.

---

## Active Rulings

### PLATFORM-DCR-008 — Constitutional Hierarchy
- **Decision:** The Platform Constitution is subordinate to the GoldBot Constitution: it obeys it,
  does not modify it, and cannot come into conflict with it.
- **Rationale:** Fixes a single primary governing document and removes any ambiguity between the two
  editions.
- **Related Chapters:** [10](Chapter10_PlatformStructure.md), [38](Chapter38_AmendmentProcess.md), [40](Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

### PLATFORM-DCR-009 — Platform Scope
- **Decision:** The Platform governs only: User Experience, Accounts, Subscriptions, Notifications,
  Payments, Analytics, Administration, and Services. Trading decisions remain the Core's authority.
- **Rationale:** Draws a clear line between platform (product/experience) concerns and Core (trading)
  authority.
- **Related Chapters:** [06](Chapter06_Scope.md), [18](Chapter18_PlatformArchitecture.md), [28](Chapter28_UserProfiles.md)–[35](Chapter35_Operations.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

### PLATFORM-DCR-010 — Platform Safety Boundary
- **Decision:** The Platform does not create a signal, evaluate a signal, compute risk, alter AI
  decisions, or bypass Core logic. It only delivers to users results the Core has already cleared.
- **Rationale:** States the platform's non-amendable safety boundary in concrete terms, protecting
  Trading Safety at the surface layer.
- **Related Chapters:** [31](Chapter31_SignalDelivery.md), [36](Chapter36_RiskAndAbusePrevention.md), [40](Chapter40_FinalProvisions.md)
- **Status:** Active (non-amendable)
- **Effective Date:** 2026-07-25
- **Superseded By:** — (may be strengthened, never weakened)

### PLATFORM-DCR-011 — Amendment Rule
- **Decision:** All future Platform changes must: (1) be consistent with the GoldBot Constitution;
  (2) not weaken Core safety principles; (3) not break the Gateway architecture.
- **Rationale:** Binds every future platform amendment to the primary constitution, safety, and the
  single-entry-point architecture.
- **Related Chapters:** [38](Chapter38_AmendmentProcess.md), [40](Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

---

## Pending Transcription (PLATFORM-DCR-001 … PLATFORM-DCR-007)

| PLATFORM-DCR | Title | Decision | Rationale | Related Chapters | Status | Effective Date | Superseded By |
|---|---|---|---|---|---|---|---|
| PLATFORM-DCR-001 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| PLATFORM-DCR-002 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| PLATFORM-DCR-003 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| PLATFORM-DCR-004 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| PLATFORM-DCR-005 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| PLATFORM-DCR-006 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |
| PLATFORM-DCR-007 | *(pending)* | pending transcription from Director records | pending | — | Pending | — | — |

*(Placeholders only. Content will be filled solely from the Director's authoritative ruling history —
never reconstructed here.)*

---

## Register Conventions

- **Append** each new ruling with the next PLATFORM-DCR number and all eight fields.
- A ruling that changes a frozen platform chapter's meaning also requires the Amendment Process
  ([Chapter 38](Chapter38_AmendmentProcess.md)) and is cross-referenced from the
  [Platform Constitution Change Log](PLATFORM_CONSTITUTION_CHANGELOG.md).
- No PLATFORM-DCR may conflict with the GoldBot Constitution or a GoldBot Director Ruling (DR); where they
  meet, the GoldBot ruling governs (PLATFORM-DCR-008).
- Safety-related rulings may **strengthen** but never weaken the PLATFORM-DCR-010 / DR-015 guarantees.

---

## Identifier Migration Record (DPR → PLATFORM-DCR)

Per the ratified Ruling Prefix Standard (CORE-DCR-001) and CORE-DCR-006 — executed **after** the
Platform Constitution v1.0 baseline was established on `main` via PR #20 (merge commit `20e49a62`) —
all Platform ruling identifiers were migrated **1:1** from the legacy `DPR-###` scheme to
`PLATFORM-DCR-###`. Ruling text, rationale, category, related chapters, effective dates, and status
were preserved unchanged; **no ruling was invented, renumbered, or altered in meaning**.

- **Migration timestamp (UTC):** 2026-07-26T07:18:24Z
- **Branch:** `feature/gb-platform-dcr-migration`
- **Baseline commit (PR #20 merge):** `20e49a62`
- **Scope:** `docs/constitution/platform/` only — no Core, Chart, GoldBot, Personal AI, or Media
  identifiers were changed.

### Identifier mapping (old → new)

| Old (legacy) | New (standard) | Status |
|---|---|---|
| DPR-001 | PLATFORM-DCR-001 | Pending (placeholder) |
| DPR-002 | PLATFORM-DCR-002 | Pending (placeholder) |
| DPR-003 | PLATFORM-DCR-003 | Pending (placeholder) |
| DPR-004 | PLATFORM-DCR-004 | Pending (placeholder) |
| DPR-005 | PLATFORM-DCR-005 | Pending (placeholder) |
| DPR-006 | PLATFORM-DCR-006 | Pending (placeholder) |
| DPR-007 | PLATFORM-DCR-007 | Pending (placeholder) |
| DPR-008 | PLATFORM-DCR-008 | Active |
| DPR-009 | PLATFORM-DCR-009 | Active |
| DPR-010 | PLATFORM-DCR-010 | Active (non-amendable) |
| DPR-011 | PLATFORM-DCR-011 | Active |

*The legacy `DPR-###` identifiers above are retained here solely as historical traceability; they are
no longer active identifiers. New Platform rulings use `PLATFORM-DCR-###` — next available:
**PLATFORM-DCR-012**.*
