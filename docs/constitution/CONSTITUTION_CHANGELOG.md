# Constitution Change Log

**Objective:** track all Constitution changes after v1.0.

**Entry fields:** Version · Date · Summary · Chapters Changed · Amendment Reference ·
Approved By · Notes.

Scope: this log records changes to the **Chaptered Constitution** edition, governed by
the Amendment Process ([Chapter 38](chapters/Chapter38_AmendmentProcess.md)) and the
[Director Rulings Register](DIRECTOR_RULINGS_REGISTER.md). It is distinct from the
phase-level product changelog ([`docs/changelog/CHANGELOG.md`](../changelog/CHANGELOG.md))
and the decision log ([`docs/changelog/DECISION_LOG.md`](../changelog/DECISION_LOG.md)).

---

## v1.0 — Frozen Baseline

- **Version:** v1.0 (Frozen Baseline)
- **Date:** 2026-07-25
- **Summary:** Initial adoption of the GoldBot Chaptered Constitution — 40 chapters
  across five blocks (Foundational, Governance, Architecture, Domain, Closing).
  Approved at Director Final Review (10.0 / 10), completed, and frozen as the baseline.
- **Chapters Changed:** 01–40 (initial adoption of all chapters)
- **Amendment Reference:** DR-013 (Consolidation), DR-014 (Freeze), DR-015 (Safety —
  non-amendable), DR-016 (Single Source of Truth)
- **Approved By:** Director
- **Notes:**
  - Chapter `Status:` headers set to *Approved — Frozen Baseline* on adoption
    (metadata only; no normative content changed, per DR-014).
  - Per DR-013, the historical `CONSTITUTION.md` / `ARTICLES.md` / `AMENDMENTS.md`
    become non-normative; necessary content is consolidated here or migrated by
    future amendment.
  - Source packages: GB-CONST-001, GB-CONST-002, and GB-CONST-BATCH-01 … 05.

---

## Entry Format for Future Changes

Each change after v1.0 appends an entry with all seven fields:

```
## v1.x — <title>
- Version:            v1.x
- Date:               <YYYY-MM-DD>
- Summary:            <what changed and why, in brief>
- Chapters Changed:   <chapter numbers/sections, or "none (extension)">
- Amendment Reference: <DR-xxx / ADR-xxx / Amendment id>
- Approved By:        Director
- Notes:              <affirm DR-015 safety guarantees remain intact; extension vs amendment>
```

Conventions:
- **Extension** (new chapters or material that does not change settled meaning):
  `Chapters Changed: none (extension)`.
- **Amendment** (change to an approved chapter's meaning): list the chapters and cite
  the Amendment Process authorization.
- Every entry must affirm that the DR-015 non-amendable safety guarantees remain
  intact.
