# GoldBot Platform Constitution — Chapter 37: Compliance

**Package:** GB-PLATFORM-CONST-037 · **Document:** Chapter37_Compliance.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/AUDIT_REPORT.md`](../../AUDIT_REPORT.md), [`docs/standards/`](../../standards/), the GoldBot Constitution compliance framework.

---

## Executive Summary

Chapter 37 closes the Platform domain block with **compliance** — how the Platform layer verifies
that it follows its own Constitution and the GoldBot Constitution above it. Platform compliance
ties the platform edition together: the constitutions and standards are the measure, review and
acceptance are the gates, and the audit trail is the evidence. This chapter states how platform
conformance is established and kept.

## Table of Contents (Chapter 37)

1. Compliance Statement
2. The Constitutions as the Standard
3. Review and Acceptance Gates
4. The Audit Trail as Evidence
5. Single Source of Truth
6. Standards and Policy Conformance
7. Compliance and Safety
8. Continuous Compliance

---

## 1. Compliance Statement

Platform compliance is the discipline of **verifying that the Platform layer follows its rules** —
both the Platform Constitution and the GoldBot Constitution above it. A constitution that is not
checked is only an aspiration; compliance makes platform conformance demonstrable.

## 2. The Constitutions as the Standard

The Platform Constitution, **under** the GoldBot Constitution, together with the standards and
policies they reference, is the measure against which surface work is judged. Where the two
constitutions meet, the GoldBot Constitution governs (DR-013). Compliance is conformance to these,
not to preference.

## 3. Review and Acceptance Gates

Platform conformance is enforced at review and acceptance (Chapters 13, 14). A surface change
passes only when it meets the standards, its automated checks succeed, its boundaries are intact,
capability is honestly declared, and its decisions are recorded. A gate not met blocks the change.

## 4. The Audit Trail as Evidence

The audit trail — decisions, reviews, changelog, and acceptance records — is the evidence of
platform compliance. Because consequential surface work is recorded, conformance can be
demonstrated after the fact rather than merely claimed.

## 5. Single Source of Truth

Platform compliance depends on one authoritative source per domain (DR-016). Conformance is checked
against that single source; the compose-and-link discipline is itself a compliance requirement, so
rules are never duplicated or drifting between the platform and GoldBot editions.

## 6. Standards and Policy Conformance

Surface work conforms to the operative standards and policies — code, tests, reviews, documentation,
releases, versions — which the constitutions reference rather than restate. Compliance is measured
against those operative sources.

## 7. Compliance and Safety

The highest platform compliance obligation is Trading Safety. A surface change that would deliver an
un-cleared signal, bypass the Risk Manager, place trading logic in a surface, or grant trading
authority is non-compliant regardless of its other merits, and the safety gate cannot be waived
(Chapters 13, 31, 36; DR-015).

## 8. Continuous Compliance

Platform compliance is maintained continuously, not audited once. The gates apply to every surface
work package alike, known gaps are tracked and retired through the technical-debt workflow, and
lessons are recorded — so conformance does not erode as the surface family grows.

---

*End of Chapter 37 — Compliance. This chapter completes the Domain block (Chapters 28–37) of the
GoldBot Platform Constitution v1.0 edition.*
