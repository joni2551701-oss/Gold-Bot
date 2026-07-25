# GoldBot Platform Constitution — Chapter 15: Decision Process

**Package:** GB-PLATFORM-CONST-015 · **Document:** Chapter15_DecisionProcess.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Governance (08–17)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/changelog/DECISION_LOG.md`](../../changelog/DECISION_LOG.md), ADRs under [`communication/decisions/`](../../../communication/decisions/).

---

## Executive Summary

Chapter 15 defines the **decision process for the Platform layer** — how consequential platform
choices are made, escalated, and recorded. As in the GoldBot Constitution, no consequential
decision is silent, and anything touching Core or safety escalates upward. This chapter states
the process.

## Table of Contents (Chapter 15)

1. Decision Statement
2. Kinds of Platform Decisions
3. No Silent Decisions
4. Escalation
5. Recording Decisions
6. Reversibility
7. Decisions and Safety
8. Traceability

---

## 1. Decision Statement

The Platform layer makes consequential decisions **deliberately and on the record**. A decision
that affects platform direction, the shared model, surface scope, or anything touching Core or
safety is made by the authorized role, with its rationale captured.

## 2. Kinds of Platform Decisions

- **Direction decisions** (set by the Product Director) — which surfaces and capabilities.
- **Design decisions** (recorded as decision-log entries or ADRs) — how the shared model and
  surfaces are structured.
- **Acceptance decisions** — the recorded acceptance of a completed platform work package.

## 3. No Silent Decisions

A consequential platform choice that cannot be resolved from the brief is escalated, not made
quietly. An undocumented consequential decision is a defect (GoldBot Constitution, Decision
Process).

## 4. Escalation

Platform ambiguities escalate to the Product Director. Anything that touches the Core boundary,
the shared model in a Core-affecting way, or a safety guarantee escalates further to the
**GoldBot Director**, because those matters are governed above the Platform layer.

## 5. Recording Decisions

A consequential platform decision is recorded with its rationale and authorization, in the
appropriate decision record. Recording turns a choice into institutional memory the platform can
build on.

## 6. Reversibility

Where outcomes are uncertain, the more reversible platform option is preferred, and
irreversible or user-facing actions are confirmed before they are taken.

## 7. Decisions and Safety

No platform decision process may weaken the safety guarantees. A choice that would place trading
logic in a surface, bypass the gateway, or route around the risk controls is out of bounds
regardless of how it is recorded (DR-015).

## 8. Traceability

Because decisions are recorded, platform direction is traceable: any consequential outcome can
be followed back to the decision, rationale, and authorization behind it — part of the audit
trail.

---

*End of Chapter 15 — Decision Process.*
