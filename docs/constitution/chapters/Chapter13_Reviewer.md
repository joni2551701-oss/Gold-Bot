# GoldBot Constitution — Chapter 13: Reviewer

**Package:** GB-CONST-013 · **Document:** Chapter13_Reviewer.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Governance (Chapters 08–17)
**Continuity:** Reuses the terminology of Chapters 01–12; does not contradict any approved chapter.
**Operative source:** [`docs/standards/REVIEW_STANDARD.md`](../../standards/REVIEW_STANDARD.md), review records under [`communication/reviews/`](../../../communication/reviews/).

---

## Executive Summary

Chapter 13 defines the **Reviewer** role — the check that stands between completed
work and its taking effect. Review is where the standards, boundaries, and safety
guarantees are verified against a specific change. This chapter states the purpose,
scope, and outcomes of review; the operative checklist and review records live in
the referenced sources.

## Table of Contents (Chapter 13)

1. Role Statement
2. Purpose of Review
3. Scope of Review
4. Review Gates
5. Independence
6. Review Outcomes
7. Review and Safety
8. Review Records

---

## 1. Role Statement

The Reviewer is the role that **verifies a change before it takes effect**. Review
confirms that a deliverable meets the standards and honors the boundaries, and it
is required before any consequential change is merged.

## 2. Purpose of Review

Review protects the foundation by catching, before merge, what execution alone
might miss: a weakened boundary, a duplicated rule, a missing test, an
undocumented decision, or a safety regression. It is the last structured
opportunity to keep a change consistent with the Constitution.

## 3. Scope of Review

Review covers architecture (does the change respect the layers and the gateway
boundary), consistency (does it match approved chapters and standards), governance
(is the decision recorded, is scope respected), quality (are there tests, does
validation pass), and safety (are the risk controls and the advisory boundary
intact). Nothing consequential is out of scope for review.

## 4. Review Gates

A change passes review only when its gates are met: the standards are satisfied,
the automated checks report success, the boundaries are verifiably intact, and any
decision the change embodies is recorded. A gate that is not met blocks the merge
until it is resolved.

## 5. Independence

Review is separate from execution (Chapter 08). The party that authored a
consequential change does not unilaterally approve it; a distinct review judgment
is applied. This separation is what makes review a genuine check rather than a
formality.

## 6. Review Outcomes

Review produces a clear outcome: approved (the change may proceed), or not approved
with specific, actionable reasons. An approval is explicit and recorded; a
rejection names exactly what must change. Review does not end in ambiguity.

## 7. Review and Safety

Safety is a non-negotiable review gate. A change that would bypass the risk
controls, let the advisory intelligence execute, introduce a second entry point, or
place client logic in the Core is rejected regardless of its other merits. The
safety gate cannot be waived.

## 8. Review Records

Review outcomes are recorded, so that what was checked, decided, and approved
remains part of the audit trail. Per-review instances are captured in the review
records referenced above, applying the operative review standard rather than
restating it.

---

*End of Chapter 13 — Reviewer.*
