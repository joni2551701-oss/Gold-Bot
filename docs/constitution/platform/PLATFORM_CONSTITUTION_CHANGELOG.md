# Platform Constitution Change Log

**Objective:** track all Platform Constitution changes after v1.0.

**Entry fields:** Version · Date · Summary · Chapters Changed · Amendment Reference · Approved By ·
Notes.

Scope: this log records changes to the **Platform Constitution** edition, governed by the Amendment
Process ([Chapter 38](Chapter38_AmendmentProcess.md)) and the
[Platform Director Rulings Register](PLATFORM_DIRECTOR_RULINGS_REGISTER.md), always under the GoldBot
Constitution. It is distinct from the platform-product change log
([`docs/PLATFORM_CHANGELOG.md`](../../PLATFORM_CHANGELOG.md)) and the GoldBot
[Constitution Change Log](../CONSTITUTION_CHANGELOG.md).

---

## v1.0 — Frozen Baseline

- **Version:** v1.0 (Frozen Baseline)
- **Date:** 2026-07-25
- **Summary:** Initial adoption of the GoldBot Platform Constitution — 40 chapters across five blocks
  (Foundation, Governance, Architecture, Domain, Closing), subordinate to the GoldBot Constitution
  v1.0. Approved at Director Final Review (10.0 / 10), completed, and frozen as the platform baseline.
- **Chapters Changed:** 01–40 (initial adoption of all chapters)
- **Amendment Reference:** DPR-008 (Constitutional Hierarchy), DPR-009 (Platform Scope), DPR-010
  (Platform Safety Boundary — non-amendable), DPR-011 (Amendment Rule)
- **Approved By:** Director
- **Notes:**
  - Chapter `Status:` headers set to *Approved — Frozen Baseline* on adoption (metadata only; no
    normative content changed).
  - The Platform Constitution is subordinate to the GoldBot Constitution v1.0 (DPR-008); where the
    two meet, the GoldBot Constitution governs.
  - The [Platform Director Rulings Register](PLATFORM_DIRECTOR_RULINGS_REGISTER.md) records DPR-008…011
    verbatim; DPR-001…007 remain pending transcription from the Director's records.
  - Source packages: GB-PLATFORM-CONST-BATCH-01 … 05.

---

## v1.0 — Baseline Established on `main` (Freeze Confirmation)

- **Version:** v1.0 (Frozen Baseline — established on `main`)
- **Date:** 2026-07-26
- **Summary:** The Platform Constitution v1.0 was merged to `main` via PR #20 (merge commit
  `20e49a62`) and is hereby confirmed as the **official frozen baseline**, satisfying the baseline
  precondition required by CORE-DCR-006 before any Platform identifier migration.
- **Chapters Changed:** none (baseline confirmation; no normative content changed)
- **Amendment Reference:** — (baseline establishment, not an amendment)
- **Approved By:** Director (execution authorized)
- **Notes:**
  - The frozen baseline content is exactly what PR #20 landed; no chapter meaning changed.
  - The platform non-amendable safety boundary and the DR-015 guarantees remain intact.
  - The subsequent Platform identifier migration proceeds post-baseline as a governed amendment
    (see the following entry and the Platform Rulings Register migration record).

---

## Entry Format for Future Changes

```
## v1.x — <title>
- Version:             v1.x
- Date:                <YYYY-MM-DD>
- Summary:             <what changed and why, in brief>
- Chapters Changed:    <chapter numbers/sections, or "none (extension)">
- Amendment Reference: <DPR-xxx / ADR-xxx / Amendment id>
- Approved By:         Director
- Notes:               <affirm DPR-010 / DR-015 safety guarantees intact; consistent with GoldBot Constitution>
```

Conventions:
- **Extension** (new chapters or material that does not change settled meaning):
  `Chapters Changed: none (extension)`.
- **Amendment** (change to an approved chapter's meaning): list the chapters, cite the Amendment
  Process authorization, and confirm consistency with the GoldBot Constitution (DPR-011).
- Every entry must affirm that the DPR-010 / DR-015 safety guarantees remain intact.
