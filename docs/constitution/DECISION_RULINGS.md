# GoldBot — Decision Rulings Register (DR)

Central register of **Director Rulings (DR)**. A Director Ruling is a recorded,
authoritative governance decision (Constitution [Chapter 15](chapters/Chapter15_DecisionProcess.md),
[Chapter 11](chapters/Chapter11_Director.md)). This register is the single place
DR rulings are collected; the operative decision history also lives in
[`docs/changelog/DECISION_LOG.md`](../changelog/DECISION_LOG.md) and the ADRs under
[`communication/decisions/`](../../communication/decisions/).

> **Provenance note (honesty):** DR-013 … DR-016 below are transcribed **verbatim**
> from the Director's Final Review of Constitution v1.0. DR-001 … DR-012 predate
> that review; their **authoritative text is pending transcription from the
> Director's ruling history** (and/or reconciliation with the existing
> `DECISION_LOG.md`/ADR records). They are listed as placeholders and must be
> filled from the Director's own records — they are intentionally **not**
> reconstructed or invented here. **Open item for the Director:** confirm or supply
> the DR-001…012 texts, or direct how they map onto existing DD-/ADR entries.

---

## DR-013 … DR-016 — Constitution v1.0 Final Review (recorded verbatim)

### DR-013 — Constitution Consolidation
The GoldBot **Chaptered Constitution v1.0** is the primary and only governance
document. The earlier `CONSTITUTION.md`, `ARTICLES.md`, and `AMENDMENTS.md` are
retained as **historical documents** but are no longer independent normative
sources; their necessary content is consolidated into the Chaptered Constitution
v1.0 or migrated via future amendments.

### DR-014 — Constitution Freeze
The present **40 chapters** are frozen as **Constitution Baseline v1.0 (Frozen
Baseline)**. Any change is made only via: an **ADR**, the **Constitution Amendment
Process** ([Chapter 38](chapters/Chapter38_AmendmentProcess.md)), and **Director
approval**.

### DR-015 — Safety Guarantees (non-amendable)
The following are confirmed as **non-amendable constitutional principles**:
1. The **Risk Manager is not bypassed**.
2. The **AI does not independently execute trades**.
3. **Human oversight is preserved**.
4. **Trading Safety takes precedence** over all other modules.

### DR-016 — Single Source of Truth
The Constitution defines **principles**. Operative detail is carried via
**architecture docs, ADRs, standards, policies, and specifications**. Identical
rules are not written twice.

---

## DR-001 … DR-012 — pending transcription

| DR | Title | Status | Authoritative text |
|---|---|---|---|
| DR-001 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-002 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-003 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-004 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-005 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-006 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-007 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-008 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-009 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-010 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-011 | *(pending)* | recorded earlier | to be transcribed from Director records |
| DR-012 | *(pending)* | recorded earlier | to be transcribed from Director records |

*(These rows are placeholders. Their content will be filled only from the
Director's authoritative ruling history — not reconstructed here.)*

---

## Register conventions

- **New rulings are appended** with the next DR number, their verbatim text, and
  the date/context of the ruling.
- A ruling that changes a frozen chapter's meaning also requires the Amendment
  Process (Chapter 38) and is cross-referenced from the
  [Constitution Change Log](CONSTITUTION_CHANGELOG.md).
- Safety-related rulings may **strengthen** but never weaken the DR-015
  guarantees.
