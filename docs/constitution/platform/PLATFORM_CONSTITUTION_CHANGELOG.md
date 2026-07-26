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
- **Amendment Reference:** PLATFORM-DCR-008 (Constitutional Hierarchy), PLATFORM-DCR-009 (Platform Scope), PLATFORM-DCR-010
  (Platform Safety Boundary — non-amendable), PLATFORM-DCR-011 (Amendment Rule)
- **Approved By:** Director
- **Notes:**
  - Chapter `Status:` headers set to *Approved — Frozen Baseline* on adoption (metadata only; no
    normative content changed).
  - The Platform Constitution is subordinate to the GoldBot Constitution v1.0 (PLATFORM-DCR-008); where the
    two meet, the GoldBot Constitution governs.
  - The [Platform Director Rulings Register](PLATFORM_DIRECTOR_RULINGS_REGISTER.md) records PLATFORM-DCR-008…011
    verbatim; PLATFORM-DCR-001…007 remain pending transcription from the Director's records.
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

## v1.0.1 — Platform Identifier Migration (DPR → PLATFORM-DCR)

- **Version:** v1.0.1 (post-baseline governed amendment — identifier migration)
- **Date:** 2026-07-26
- **Summary:** Migrated all Platform ruling identifiers 1:1 from `DPR-###` to `PLATFORM-DCR-###` per the
  ratified Ruling Prefix Standard (CORE-DCR-001) and CORE-DCR-006, after the v1.0 baseline was
  established on `main`. Identifier-only change: ruling text, rationale, category, related chapters,
  effective dates, and status preserved; nothing invented or renumbered.
- **Chapters Changed:** identifier references across chapters 01–40 and the register (no meaning changed)
- **Amendment Reference:** CORE-DCR-001, CORE-DCR-006; Platform Amendment Process (Chapter 38)
- **Approved By:** Director (execution authorized)
- **Notes:**
  - Old → new mapping and full traceability recorded in the Platform Rulings Register migration record.
  - The PLATFORM-DCR-010 / DR-015 safety guarantees remain intact; no scope or status changed.
  - No Core, Chart, GoldBot, Personal AI, or Media identifiers were changed.

---

## Entry Format for Future Changes

```
## v1.x — <title>
- Version:             v1.x
- Date:                <YYYY-MM-DD>
- Summary:             <what changed and why, in brief>
- Chapters Changed:    <chapter numbers/sections, or "none (extension)">
- Amendment Reference: <PLATFORM-DCR-xxx / ADR-xxx / Amendment id>
- Approved By:         Director
- Notes:               <affirm PLATFORM-DCR-010 / DR-015 safety guarantees intact; consistent with GoldBot Constitution>
```

Conventions:
- **Extension** (new chapters or material that does not change settled meaning):
  `Chapters Changed: none (extension)`.
- **Amendment** (change to an approved chapter's meaning): list the chapters, cite the Amendment
  Process authorization, and confirm consistency with the GoldBot Constitution (PLATFORM-DCR-011).
- Every entry must affirm that the PLATFORM-DCR-010 / DR-015 safety guarantees remain intact.
