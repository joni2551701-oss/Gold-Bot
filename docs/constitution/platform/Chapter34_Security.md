# GoldBot Platform Constitution — Chapter 34: Security

**Package:** GB-PLATFORM-CONST-034 · **Document:** Chapter34_Security.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/SECURITY.md`](../../SECURITY.md), [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md).

---

## Executive Summary

Chapter 34 states **security for the Platform layer** — how the platform protects its users,
their data, and its surfaces. Platform security operates under the GoldBot Constitution's security
governance, enforced primarily at the gateway boundary and reinforced by disciplined data handling
and least privilege. This chapter states the platform-scoped security model.

## Table of Contents (Chapter 34)

1. Security Statement
2. Security at the Boundary
3. Data Protection
4. Secrets and Sensitive Material
5. Least Privilege
6. Threats to Users and Surfaces
7. Security and Safety
8. Evolution

---

## 1. Security Statement

Platform security **protects users, their data, and the surfaces** through which they interact. It
is structural — enforced at the platform's boundaries — and it operates under the GoldBot
Constitution's security governance.

## 2. Security at the Boundary

Access to the Core is authenticated and authorized at the **gateway** (Chapter 20); the Platform
layer relies on and respects that single-boundary enforcement rather than creating a parallel or
weaker path. Security is applied where access happens.

## 3. Data Protection

User and platform data are protected in keeping with the data and security governance: minimized,
guarded, and auditable. Sensitive data is never exposed beyond where it is needed.

## 4. Secrets and Sensitive Material

Secrets and sensitive material (credentials, tokens, payment data) are handled through governed
secret management and **never** appear in documentation, code comments, logs, or change requests
(GoldBot Constitution, Security Governance). This discipline is absolute.

## 5. Least Privilege

Access is granted at the **least level required** — for users, administrators (Chapter 32),
services, and integrations alike — so the reach of any component or role is bounded and the impact
of error or compromise is limited.

## 6. Threats to Users and Surfaces

Platform security addresses threats to users and surfaces — account compromise, misuse, and abuse
(with abuse prevention detailed in Chapter 36) — protecting the platform without ever weakening the
Core's protections.

## 7. Security and Safety

Platform security reinforces Trading Safety: no authenticated, authorized, or administrative path
may bypass the Risk Manager, deliver an un-cleared signal, or let the advisory intelligence act
(DR-015). Security governs reach; it never dissolves the safety boundary.

## 8. Evolution

Platform security evolves by strengthening protections behind stable interfaces — new
authentication, tighter controls, better data protection — without weakening the guarantees or
creating a bypass, as surfaces multiply.

---

*End of Chapter 34 — Security.*
