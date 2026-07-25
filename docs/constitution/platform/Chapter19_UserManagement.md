# GoldBot Platform Constitution — Chapter 19: User Management

**Package:** GB-PLATFORM-CONST-019 · **Document:** Chapter19_UserManagement.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 19 describes **user management** in the Platform layer — how users and their sessions
are represented and handled across surfaces. User management identifies who is interacting and
carries their preferences and entitlements, always as a platform concern that consumes the Core
through the gateway and never as a route around any protection.

## Table of Contents (Chapter 19)

1. User Management Statement
2. The User and the Session
3. Identity Across Surfaces
4. User Data Governance
5. Access Through the Gateway
6. Privacy and Least Data
7. The User Management Boundary
8. Evolution

---

## 1. User Management Statement

User management represents **who is interacting with GoldBot and in what session**, so a surface
can present the right experience and pass the right identity to the Core. It is a platform
concern; it holds no trading logic and no Core state authority.

## 2. The User and the Session

A **user** is the person interacting; a **session** is a bounded interaction context. User
management associates a session with a user identity and the user's platform preferences and
entitlements, so surfaces behave consistently for that user.

## 3. Identity Across Surfaces

A user may reach GoldBot through more than one surface. User management aims for a **consistent
identity** across surfaces, so the user's experience and entitlements are coherent regardless of
which client they use, consistent with the one-model principle (Chapter 04).

## 4. User Data Governance

User data is governed under the GoldBot Constitution's data and security governance and the
operative platform policies: it is collected minimally, protected, and auditable. The Platform
layer manages user *presentation and preference* data; authoritative Core state remains in the
Core.

## 5. Access Through the Gateway

User identity is presented to the Core **through the gateway**, where authentication and
authorization apply (Chapter 20). User management never gives a user a path around the gateway or
the risk controls; it establishes who is asking, not what they may do to trading.

## 6. Privacy and Least Data

User management follows **least data**: it holds only the user information a surface needs, and
sensitive material is handled under the security governance and never exposed in logs, docs, or
change requests (GoldBot Constitution, Security Governance).

## 7. The User Management Boundary

User management identifies and personalizes; it never decides trades, never holds trading logic,
and never bypasses a protection. Entitlements govern **feature access**, not trading authority
(Chapter 21).

## 8. Evolution

User management evolves by adding identity, preference, and entitlement capability behind stable
platform contracts, across more surfaces, without changing the Core or weakening a protection.

---

*End of Chapter 19 — User Management.*
