# GoldBot Platform Constitution — Chapter 16: Documentation Governance

**Package:** GB-PLATFORM-CONST-016 · **Document:** Chapter16_DocumentationGovernance.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Governance (08–17)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_DOCUMENTATION_POLICY.md`](../../PLATFORM_DOCUMENTATION_POLICY.md), [`docs/standards/DOCUMENTATION_STANDARD.md`](../../standards/DOCUMENTATION_STANDARD.md).

---

## Executive Summary

Chapter 16 defines **documentation governance for the Platform layer** — the rules that keep
platform documentation a reliable, single-sourced record. Platform docs are written before
code, kept current, and governed by the operative platform documentation policy. This chapter
states the governance and defers to that policy for detail.

## Table of Contents (Chapter 16)

1. Documentation Statement
2. Documentation First
3. Single Source of Truth
4. Standards and Policy
5. Compose-and-Link
6. Currency and Maintenance
7. Documentation and Audit
8. Ownership

---

## 1. Documentation Statement

Platform documentation is a **first-class artifact** of every surface work package. Architecture
and intent are recorded, so the platform layer stays understandable as surfaces multiply.

## 2. Documentation First

Documentation precedes code: a surface change is designed and documented before implementation
and reviewed before merge. Intent is explicit before effort is spent.

## 3. Single Source of Truth

Each platform documentation domain has **one authoritative source** (DR-016). Platform docs do
not duplicate the GoldBot Constitution or the operative policies; they state platform specifics
and link the source for the rest.

## 4. Standards and Policy

Platform documentation follows the operative platform documentation policy and the repo-wide
documentation standard, which define structure and maintenance. The Platform Constitution states
principles and defers detail to these sources.

## 5. Compose-and-Link

Platform documents that overlap an existing source **summarize and link** it rather than
restating it, so the corpus stays consistent and the reuse principle applies to documentation as
well as code.

## 6. Currency and Maintenance

Platform documentation is kept current with the surfaces it describes. When a surface or the
shared model changes, the authoritative document is updated in its own home, not copied
elsewhere. Stale or contradictory docs are defects to correct.

## 7. Documentation and Audit

Platform documentation is part of the audit trail: recorded architecture, decisions, and
capability declarations make surface work traceable and reviewable. A change whose intent is
undocumented is incomplete.

## 8. Ownership

Each authoritative platform document has a clear home and is maintained there. The Platform
Constitution owns platform-constitutional intent; the platform policies/standards own
operational detail; the decision and changelog records own history.

---

*End of Chapter 16 — Documentation Governance.*
