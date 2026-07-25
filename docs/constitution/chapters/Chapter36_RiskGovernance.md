# GoldBot Constitution — Chapter 36: Risk Governance

**Package:** GB-CONST-036 · **Document:** Chapter36_RiskGovernance.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–35; does not contradict any approved chapter.
**Operative sources:** [`contracts/risk_contract.md`](../../../contracts/risk_contract.md), the Risk Manager (`risk/risk_manager.py`), and the Trading Safety rules in [`CLAUDE.md`](../../../CLAUDE.md).
**Note:** This chapter states risk *governance* at the constitutional level. It does not define, alter, or restate any risk formula, threshold, or logic — those remain the exclusive domain of the operative risk sources and are changed only by explicit, specific authorization.

---

## Executive Summary

Chapter 36 states **risk governance** — the constitutional rules that keep the
user's protection structural and permanent. The central rule is that the Risk
Manager is never bypassed: every signal that could reach a user passes through it,
and no path — from the AI layer, a surface, or anywhere else — goes around it. This
chapter governs *that the protection holds*; it does not touch how the protection is
computed.

## Table of Contents (Chapter 36)

1. Risk Governance Statement
2. The Risk Manager Is Never Bypassed
3. Structural Enforcement
4. Risk in the Pipeline
5. The AI Layer Never Sizes or Executes
6. Change Control on Risk Logic
7. The Risk Register
8. Risk Governance Evolution

---

## 1. Risk Governance Statement

Risk governance exists to guarantee that the user is **protected by construction**.
The protections are structural properties of the system, enforced regardless of how
any component is operated, and they are permanent.

## 2. The Risk Manager Is Never Bypassed

The governing rule is absolute: every signal that could reach a user passes through
the Risk Manager. There is no shortcut path to delivery, and no component may route
around risk evaluation. This rule holds for every surface and every version
(Trading Safety, `CLAUDE.md`).

## 3. Structural Enforcement

Risk protection is enforced by the architecture, not by vigilance. The system
provides no path that reaches a user without risk evaluation and no route by which
the advisory intelligence could act. Because the protection is built into the
structure, it does not depend on careful operation to hold.

## 4. Risk in the Pipeline

Risk evaluation is a governed stage of the decision pipeline: signals are evaluated
before they can be delivered, and blocked or rejected outcomes do not reach a user.
The exact geometry, sizing, and thresholds are defined solely in the operative risk
sources; this chapter governs only that the stage is always present and never
bypassed.

## 5. The AI Layer Never Sizes or Executes

Consistent with Chapters 07, 28, and 29, the advisory intelligence never sizes,
approves, rejects, sends, or executes a trade, and never calls the Risk Manager. The
AI layer advises the decision; risk evaluation and the decision itself remain in the
governed pipeline, never in the advisory layer.

## 6. Change Control on Risk Logic

Risk logic — the Risk Manager's geometry, stop-loss validation, and sizing — is
changed only by explicit, specific authorization for that change. It is never
altered as a side effect of other work, and this chapter does not authorize any such
change. Risk logic is protected by the Constitution's strictest change control
(Trading Safety).

## 7. The Risk Register

Risks to the system's integrity are tracked in a living risk register, with
mitigations recorded and reviewed. The register keeps known risks visible and
accountable, so they are managed deliberately rather than discovered late — part of
the audit trail the Constitution requires (Chapter 15).

## 8. Risk Governance Evolution

Risk governance may strengthen over time, but the guarantees it protects do not
weaken. No future feature, provider, optimization, or platform may bypass the Risk
Manager or grant the advisory intelligence a route to act. The user's structural
protection is permanent and non-expiring.

---

*End of Chapter 36 — Risk Governance.*
