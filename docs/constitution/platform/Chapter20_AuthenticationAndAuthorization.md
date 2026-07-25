# GoldBot Platform Constitution — Chapter 20: Authentication and Authorization

**Package:** GB-PLATFORM-CONST-020 · **Document:** Chapter20_AuthenticationAndAuthorization.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../CORE_GATEWAY_ARCHITECTURE.md), [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md).

---

## Executive Summary

Chapter 20 describes **authentication and authorization** in the Platform layer — establishing
who a caller is and what they may access. Both are **identity and access** decisions only,
never trading authority, and both ultimately run at the gateway boundary. This chapter states
the platform-scoped model under the GoldBot Constitution's security and API governance.

## Table of Contents (Chapter 20)

1. Statement
2. Authentication
3. Authorization
4. Enforcement at the Gateway
5. Roles and Entitlements
6. No Trading Authority
7. Auditability
8. Evolution

---

## 1. Statement

Authentication answers **"who is calling?"** and authorization answers **"what may they
access?"** Together they govern access to platform capability and, through the gateway, to Core
capability — as access control, never as trading control.

## 2. Authentication

Authentication establishes a caller's identity before their request is honored. A surface passes
credentials or tokens to be resolved to a principal; an unidentifiable caller is not granted
access. Authentication is identity only.

## 3. Authorization

Authorization determines what an authenticated principal may reach — which surfaces, features,
and Core capabilities. It is decided from roles and entitlements (Chapters 19, 21), and it
grants access only, never the authority to make a trading decision.

## 4. Enforcement at the Gateway

Access to the Core is authenticated and authorized **at the gateway** — the single governed
boundary (GoldBot Constitution, Gateway and Security chapters). The Platform layer relies on and
respects that enforcement; it does not create a parallel or weaker access path.

## 5. Roles and Entitlements

Access is granted by **role and entitlement**: a principal receives the least access needed for
what they are permitted to do. Roles and entitlements govern feature access consistently across
surfaces.

## 6. No Trading Authority

Authentication and authorization **never** confer trading authority. No authenticated or
authorized path may bypass the Risk Manager, place trading logic in a surface, or let the
advisory intelligence act (DR-015). Access control governs reach, not trading.

## 7. Auditability

Authentication and authorization decisions are auditable through the correlated request context
and the audit trail (GoldBot Constitution, Decision Process): who was granted what access, and
under what authorization, remains traceable.

## 8. Evolution

The access model evolves by strengthening authentication and authorization backends behind
stable interfaces — new methods, tighter controls — without weakening the guarantees or creating
a bypass. Access stays governed at one boundary as surfaces multiply.

---

*End of Chapter 20 — Authentication and Authorization.*
