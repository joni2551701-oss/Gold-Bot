# GoldBot Platform Constitution — Chapter 31: Signal Delivery

**Package:** GB-PLATFORM-CONST-031 · **Document:** Chapter31_SignalDelivery.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never overrides Core governance; never weakens the
non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../CORE_GATEWAY_ARCHITECTURE.md), [`docs/policies/BROADCAST_POLICY.md`](../../policies/BROADCAST_POLICY.md).
**Note:** This chapter governs the *delivery* of trading signals to users. It defines **no** signal
logic, risk evaluation, sizing, or decision — those are exclusively the Core's, under Trading
Safety. The Platform layer only presents signals the Core has already produced and cleared.

---

## Executive Summary

Chapter 31 describes **signal delivery** — how the Platform layer presents trading signals to
users across surfaces. Its single, overriding rule is that a signal reaches a user **only after it
has passed the Core's governed pipeline, including the Risk Manager**. The Platform layer delivers
cleared signals; it never originates, sizes, evaluates, or bypasses one. This is the most
safety-critical platform boundary, and it is absolute.

## Table of Contents (Chapter 31)

1. Signal Delivery Statement
2. Signals Originate in the Core
3. The Risk Manager Is Never Bypassed
4. Delivery Across Surfaces
5. Presentation, Not Decision
6. User Control and Eligibility
7. The Signal Delivery Boundary
8. Auditability

---

## 1. Signal Delivery Statement

Signal delivery **presents to users the trading signals the Core has produced and cleared**. The
Platform layer's role is delivery and presentation; it makes no trading decision and holds no
trading logic.

## 2. Signals Originate in the Core

Every trading signal **originates in the Core** and travels to the Platform layer through the
gateway. The Platform layer never creates a signal, never derives one, and never turns
non-signal information into a trading recommendation.

## 3. The Risk Manager Is Never Bypassed

A signal reaches a user **only after it has passed the Core's governed pipeline, including the Risk
Manager** (Trading Safety, DR-015). The Platform layer has no path that delivers a signal which
was blocked, rejected, or never evaluated. There is no shortcut from a raw signal to a user; the
only signals the platform can deliver are those the Core has already cleared.

## 4. Delivery Across Surfaces

Cleared signals are delivered **consistently across surfaces** (Telegram, Web, Mobile, …), each
rendering the signal in its own idiom from the shared model (Chapters 04, 22). The same cleared
signal is presented recognizably everywhere.

## 5. Presentation, Not Decision

The Platform layer **presents** a signal — its content, context, and status as cleared by the Core
— and lets the human decide, consistent with GoldBot being semi-automatic. It never sizes,
approves, rejects, executes, or acts on a signal, and it never invites the advisory intelligence
to do so.

## 6. User Control and Eligibility

Which cleared signals a user receives follows their eligibility and preferences (Chapters 19, 21,
22, 29) — an access and delivery matter. Eligibility governs **who receives a cleared signal**; it
never causes an un-cleared signal to be delivered.

## 7. The Signal Delivery Boundary

Signal delivery holds **no** trading logic, originates **no** signal, performs **no** risk
evaluation, and provides **no** path around the Risk Manager (DR-015). It is a governed view of a
cleared Core outcome. This boundary is non-amendable and may never be relaxed for any surface,
feature, plan, or version.

## 8. Auditability

Signal delivery is auditable: which cleared signal was delivered, to whom, and when remains
traceable through the audit trail, so delivery can be verified against the Core's cleared output.

---

*End of Chapter 31 — Signal Delivery.*
