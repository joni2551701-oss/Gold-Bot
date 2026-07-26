# GoldBot Platform Constitution — Chapter 30: Payments

**Package:** GB-PLATFORM-CONST-030 · **Document:** Chapter30_Payments.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md), [`docs/SECURITY.md`](../../SECURITY.md).

---

## Executive Summary

Chapter 30 describes **payments** — how the Platform layer handles the commercial transactions
behind memberships and plans. Payments are governed with the strictest security discipline:
sensitive financial data is protected and never exposed, and payment state governs **access only**,
never trading. This chapter states the model and its boundaries.

## Table of Contents (Chapter 30)

1. Payments Statement
2. Payments and Access
3. Sensitive Data Discipline
4. Payment Providers
5. Payment Lifecycle
6. The Payments Boundary
7. Auditability and Integrity
8. Evolution

---

## 1. Payments Statement

Payments handle the **commercial transactions** that grant memberships and plans (Chapter 29). A
payment's effect is to establish or change a user's entitlements — an access outcome — and nothing
about trading.

## 2. Payments and Access

A completed payment updates a user's membership and, through it, their entitlements
(Chapters 21, 29). Payment state changes what a user may access; it never changes the Core's
logic, the risk controls, or the safety guarantees.

## 3. Sensitive Data Discipline

Payment handling follows the **strictest** security discipline: sensitive financial material is
protected, minimized, and **never** appears in documentation, code comments, logs, or change
requests (GoldBot Constitution, Security Governance). The Platform layer holds only what it must.

## 4. Payment Providers

Payments are processed through governed **payment providers**. Provider integration follows the
integration governance (Chapter 26) and the security discipline; a provider is a bounded external
integration, never a back door into the Core.

## 5. Payment Lifecycle

A payment has a governed lifecycle — initiated, authorized, completed, refunded, or failed — with
an auditable, integrity-checked record. Entitlement changes follow only from a payment reaching
the appropriate state.

## 6. The Payments Boundary

Payments govern **access and commerce only**. No payment, state, or provider integration may
bypass the Risk Manager, place trading logic in a surface, grant trading authority, or weaken a
safety guarantee (DR-015). Paying more grants more access, never different trading behavior.

## 7. Auditability and Integrity

Payment events are auditable and integrity-checked, so a user's entitlements can always be traced
to a valid payment record, and discrepancies are detectable — part of the audit trail the
Constitution requires.

## 8. Evolution

Payments evolve by adding providers, methods, and lifecycle capability behind stable platform
contracts and the security discipline, without changing the Core or weakening a protection.

---

*End of Chapter 30 — Payments.*
