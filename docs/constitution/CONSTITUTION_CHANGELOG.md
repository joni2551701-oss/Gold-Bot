# GoldBot Constitution — Change Log

History of the GoldBot **Chaptered Constitution** edition: its baseline and every
subsequent amendment or version. This log records **changes to the Constitution
itself**, governed by the Amendment Process
([Chapter 38](chapters/Chapter38_AmendmentProcess.md)) and Director rulings
([Decision Rulings Register](DECISION_RULINGS.md)).

Scope: this is the constitution-edition change log. It is distinct from the
phase-level product changelog ([`docs/changelog/CHANGELOG.md`](../changelog/CHANGELOG.md))
and the decision log ([`docs/changelog/DECISION_LOG.md`](../changelog/DECISION_LOG.md)).

---

## v1.0 — Frozen Baseline (2026-07-25)

**Status:** Approved · Completed · **Frozen Baseline** (DR-013, DR-014)
**Score at Final Review:** 10.0 / 10
**Contents:** 40 chapters, five blocks.

| Block | Chapters | Source packages |
|---|---|---|
| Foundational | 01–07 | GB-CONST-001, GB-CONST-002, GB-CONST-BATCH-01 |
| Governance | 08–17 | GB-CONST-BATCH-02 |
| Architecture | 18–27 | GB-CONST-BATCH-03 |
| Domain | 28–37 | GB-CONST-BATCH-04 |
| Closing | 38–40 | GB-CONST-BATCH-05 |

**Rulings adopted with this baseline:**
- **DR-013** — Chaptered Constitution v1.0 is the primary, sole normative governance
  document; `CONSTITUTION.md` / `ARTICLES.md` / `AMENDMENTS.md` become historical.
- **DR-014** — the 40 chapters are frozen as Constitution Baseline v1.0.
- **DR-015** — safety guarantees confirmed non-amendable.
- **DR-016** — Constitution states principles; operative detail lives in
  architecture docs, ADRs, standards, policies, specifications.

**Notes:**
- Chapter `Status:` headers were set to *Approved — Frozen Baseline* on adoption
  (metadata only; no normative content changed, consistent with DR-014).
- Consolidation of necessary content from the historical Articles edition into
  this edition, where not already covered, proceeds via future amendments (DR-013).

---

## How future changes are recorded here

Each future change appends an entry in this format:

```
## v1.x — <title> (<date>)
Change:       <what changed, by chapter/section>
Reason:       <why>
Type:         Amendment | Extension | Ruling
Authority:    <DR-xxx / ADR-xxx / Director approval>
Safety:       <confirmation it does not weaken DR-015 guarantees>
```

- **Extensions** (new chapters, new material that does not change settled meaning)
  are recorded as `Type: Extension`.
- **Amendments** (changes to an approved chapter's meaning) are recorded as
  `Type: Amendment` and require the Amendment Process + Director approval.
- Every entry must affirm that the DR-015 non-amendable safety guarantees remain
  intact.
