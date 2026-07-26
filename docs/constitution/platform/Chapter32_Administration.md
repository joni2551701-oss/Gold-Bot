# GoldBot Platform Constitution — Chapter 32: Administration

**Package:** GB-PLATFORM-CONST-032 · **Document:** Chapter32_Administration.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md).

---

## Executive Summary

Chapter 32 describes **administration** — how privileged operators manage the Platform layer:
users, memberships, content, and configuration. Administrative power is broad but **bounded**: it
governs the platform, never the Core's trading logic or the safety guarantees, and every
administrative action is authorized and audited.

## Table of Contents (Chapter 32)

1. Administration Statement
2. Administrative Scope
3. Privileged Access
4. Least Privilege and Separation
5. Auditability of Administration
6. The Administration Boundary
7. Safety and Administration
8. Evolution

---

## 1. Administration Statement

Administration is the **privileged management of the Platform layer** — its users, memberships,
content, and configuration. It exists to operate the platform, under authorization and audit.

## 2. Administrative Scope

Administrators manage platform concerns: user and membership support (Chapters 19, 28, 29),
content and notification governance (Chapter 22), and platform configuration. Administration does
**not** manage the Core's trading logic, risk controls, or decision flow.

## 3. Privileged Access

Administrative access is a **heightened** form of authorization (Chapter 20), granted narrowly and
enforced at the gateway boundary like any access. A privileged role reaches only the administrative
capabilities it is granted, never a bypass of the Core's protections.

## 4. Least Privilege and Separation

Administration follows **least privilege** and separation of duties: an administrator holds only
the powers their role requires, and sensitive actions are separated so no single role both
performs and unilaterally approves a consequential change.

## 5. Auditability of Administration

Every administrative action is **recorded** — who did what, when, and under what authorization — in
the audit trail (GoldBot Constitution, Decision Process). Privileged power is accountable because
it is traceable.

## 6. The Administration Boundary

Administration governs the platform; it **never** modifies the Core's risk logic, bypasses the Risk
Manager, grants trading authority, or weakens a safety guarantee (DR-015). No administrative power,
however broad, reaches the Core's trading protections — those are changed only by the Core's own
strictest change control.

## 7. Safety and Administration

Because administrative power is broad, its safety boundary is stated explicitly: an administrator
cannot deliver an un-cleared signal (Chapter 31), cannot disable the risk controls, and cannot let
the advisory intelligence act. Administration operates entirely on the platform side of the safety
boundary.

## 8. Evolution

Administration evolves by adding governed administrative capability behind stable interfaces, under
least privilege and audit, without ever crossing into the Core's trading protections.

---

*End of Chapter 32 — Administration.*
