# GoldBot Constitution — Chapter 29: AI Governance

**Package:** GB-CONST-029 · **Document:** Chapter29_AIGovernance.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–28; does not contradict any approved chapter.
**Operative sources:** [`docs/policies/AI_POLICY.md`](../../policies/AI_POLICY.md), [`ai_layer/ai_service/interfaces.py`](../../../ai_layer/ai_service/interfaces.py).

---

## Executive Summary

Chapter 29 states the **governance** of the AI layer — the rules that keep the
advisory architecture (Chapter 28) safe and accountable in practice. Where Chapter
28 describes what the AI layer is, this chapter states how it is governed: the
advisory-only guarantee, provider and knowledge governance, and the auditability of
advice. The operative AI policy holds the detail.

## Table of Contents (Chapter 29)

1. AI Governance Statement
2. The Advisory-Only Guarantee
3. Provider Governance
4. Knowledge Governance
5. Auditability of Advice
6. AI and Safety
7. Limits and Accountability
8. Governance Evolution

---

## 1. AI Governance Statement

The AI layer is governed to keep its influence bounded and its advice accountable.
AI governance exists to guarantee that intelligence improves the quality of
decisions without ever acquiring the authority to make them.

## 2. The Advisory-Only Guarantee

The central governed guarantee is that the AI layer is advisory only. No governance
process, provider change, or optimization may grant it the authority to approve,
reject, size, send, or execute a trade. This guarantee is permanent and
non-negotiable (Chapters 07, 28).

## 3. Provider Governance

AI providers are governed under the operative AI policy: providers plug in behind
the advisory interface, and their selection, fallback, and health are managed as
provider concerns. Governance keeps the system provider-agnostic, so no single
provider becomes a structural dependency of the Core.

## 4. Knowledge Governance

The knowledge the AI layer reasons from is Core-owned, versioned, and auditable
(Chapter 04). Governance ensures advice is grounded in this shared source rather
than in unmanaged or divergent inputs, keeping the intelligence consistent with the
rest of the system.

## 5. Auditability of Advice

Advisory output follows a defined path, so its role in a decision can be examined
after the fact. Governance requires that the influence of advice on an outcome
remains traceable, in keeping with the audit-trail commitment of the Constitution
(Chapter 15).

## 6. AI and Safety

AI governance and Trading Safety are one: the purpose of governing the AI layer is,
above all, to keep it from ever acting. A governance decision that would let the AI
layer touch the risk controls or trigger execution is out of bounds, regardless of
its other merits.

## 7. Limits and Accountability

The AI layer's authority is limited by design and its influence is accountable
through the audit trail. Governance holds the boundary and records how advice was
used, so that the advisory role can be verified rather than merely asserted.

## 8. Governance Evolution

AI governance evolves to accommodate better intelligence and new providers while
holding the advisory boundary constant. Governance may grow more capable; the
guarantee it protects does not weaken. The AI layer is governed to advise, forever.

---

*End of Chapter 29 — AI Governance.*
