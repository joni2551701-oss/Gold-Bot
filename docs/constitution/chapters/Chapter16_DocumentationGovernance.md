# GoldBot Constitution — Chapter 16: Documentation Governance

**Package:** GB-CONST-016 · **Document:** Chapter16_DocumentationGovernance.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Governance (Chapters 08–17)
**Continuity:** Reuses the terminology of Chapters 01–15; does not contradict any approved chapter.
**Operative sources:** [`docs/standards/DOCUMENTATION_STANDARD.md`](../../standards/DOCUMENTATION_STANDARD.md), [`docs/policies/DOCUMENTATION_POLICY.md`](../../policies/DOCUMENTATION_POLICY.md).

---

## Executive Summary

Chapter 16 defines **documentation governance** — the rules that keep GoldBot's
documentation a reliable, single-sourced record of intent. Documentation is a
first-class artifact in GoldBot: it is written before code, kept current, and
organized so that each governance domain has exactly one source of truth. This
chapter states the governance; the operative standard and policy live in the
referenced sources.

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

GoldBot treats documentation as a **first-class artifact** of every work package.
Architecture and intent are recorded, not merely implied by code, so the system
remains understandable across its whole life.

## 2. Documentation First

Documentation precedes code. A change is designed and documented before it is
implemented and reviewed before it is merged. This ordering ensures that intent is
explicit before effort is spent, and that the record reflects the system as built.

## 3. Single Source of Truth

Each governance and architecture domain has **one authoritative document**. Rules
are not duplicated across files, because duplicated rules drift apart and undermine
the record. Where two documents touch the same domain, one is the source and the
other refers to it.

## 4. Standards and Policy

Documentation follows the operative documentation standard and policy, which define
required structure, section content, and maintenance expectations. The chaptered
Constitution states principles at the constitutional level and defers detail to
these operative documents rather than restating them.

## 5. Compose-and-Link

The Constitution and its supporting documents follow a compose-and-link
discipline: a document that overlaps an existing source **summarizes and links** it
rather than restating it. This keeps the corpus consistent and makes the reuse
principle (Chapter 04) apply to documentation as well as code.

## 6. Currency and Maintenance

Documentation is kept current with the system it describes. When behavior or
governance changes, the authoritative document is updated in its own home, not
copied into a second place. Stale or contradictory documentation is treated as a
defect to be corrected.

## 7. Documentation and Audit

Documentation is part of the audit trail. Recorded architecture, decisions, and
standards make consequential work traceable and reviewable. A change whose intent
is undocumented is incomplete, because it cannot be audited against its purpose.

## 8. Ownership

Each authoritative document has a clear home in the repository and is maintained
there. The chaptered Constitution owns constitutional intent; the standards and
policies own operational detail; the decision and changelog records own history.
Ownership prevents the same rule from being half-maintained in several places.

---

*End of Chapter 16 — Documentation Governance.*
