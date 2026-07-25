# GoldBot Platform Constitution — Chapter 13: Review Process

**Package:** GB-PLATFORM-CONST-013 · **Document:** Chapter13_ReviewProcess.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Governance (08–17)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative source:** [`docs/standards/REVIEW_STANDARD.md`](../../standards/REVIEW_STANDARD.md), platform reviews under [`communication/reviews/`](../../../communication/reviews/).

---

## Executive Summary

Chapter 13 defines the **review process for the Platform layer** — the check between completed
surface work and its taking effect. Platform review verifies the platform standards and the
inherited safety gate against a specific change. This chapter states the process; the operative
review standard holds the checklist.

## Table of Contents (Chapter 13)

1. Review Statement
2. Purpose of Review
3. Scope of Review
4. Review Gates
5. Independence
6. Review Outcomes
7. Review and Safety
8. Review Records

---

## 1. Review Statement

Platform review **verifies a surface change before it takes effect**. Review confirms that a
deliverable meets the platform standards and honors the boundaries, and it is required before
any consequential platform change is merged.

## 2. Purpose of Review

Review protects the shared model and the Core boundary by catching, before merge, what
execution alone might miss: a thickening surface, an inconsistency across clients, a duplicated
rule, a missing test, an undocumented decision, or — most seriously — a safety regression.

## 3. Scope of Review

Platform review covers: consistency with the shared model and approved platform chapters;
architecture (gateway-only access, no trading logic in the surface); quality (tests,
validation); documentation and recorded decisions; capability declaration; and the inherited
**safety gate**.

## 4. Review Gates

A platform change passes only when its gates are met: the platform standards are satisfied, the
automated checks succeed, the boundaries are verifiably intact, capability is honestly declared,
and any decision is recorded. A gate that is not met blocks the merge.

## 5. Independence

Platform review is separate from execution (Chapter 08): the party that authored a change does
not unilaterally approve it. This separation makes review a genuine check.

## 6. Review Outcomes

Review produces a clear outcome — approved, or not approved with specific, actionable reasons.
An approval is explicit and recorded; a rejection names exactly what must change.

## 7. Review and Safety

The inherited safety gate is non-negotiable: a surface change that would place trading logic in
a platform, bypass the gateway, or provide a route around the risk controls is rejected
regardless of its other merits (DR-015). The safety gate cannot be waived, and a change touching
Core or safety is escalated to GoldBot-level review.

## 8. Review Records

Platform review outcomes are recorded, so what was checked, decided, and approved remains part
of the audit trail, applying the operative review standard rather than restating it.

---

*End of Chapter 13 — Review Process.*
