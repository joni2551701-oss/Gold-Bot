# GoldBot Platform Constitution — Chapter 24: Service Architecture

**Package:** GB-PLATFORM-CONST-024 · **Document:** Chapter24_ServiceArchitecture.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../CORE_GATEWAY_ARCHITECTURE.md).

---

## Executive Summary

Chapter 24 describes the **service architecture of the Platform layer** — how platform-side
capability (user management, subscriptions, notifications, settings) is organized as services,
and how those services consume the Core through the gateway. Platform services present and
coordinate; they do not hold trading logic and do not reach the Core outside the gateway.

## Table of Contents (Chapter 24)

1. Service Statement
2. Platform Services
3. Consuming Core Services via the Gateway
4. Service Boundaries
5. Composition and Reuse
6. Reliability
7. The Service Boundary
8. Evolution

---

## 1. Service Statement

A platform service is a **unit of platform-side capability** — such as user management,
subscriptions, notifications, or settings — that coordinates presentation and consumes the Core
through the gateway. Platform services organize the surface layer's own work.

## 2. Platform Services

The Platform layer's services cover its concerns: identity and sessions (Chapter 19), access
(Chapter 20), entitlements (Chapter 21), delivery (Chapter 22), and preferences (Chapter 23).
Each is a bounded platform capability, not a piece of Core logic.

## 3. Consuming Core Services via the Gateway

Platform services reach Core services **only through the gateway**, by name or capability
(GoldBot Constitution, Service and Integration chapters). A platform service is a governed
*consumer* of Core capability, never a component that reaches into the Core.

## 4. Service Boundaries

Each platform service owns one concern and coordinates with others through defined interfaces,
not by reaching into their internals. Concerns are not mixed — a notification service does not
hold subscription logic, and none holds trading logic.

## 5. Composition and Reuse

Platform capability is built by **composing existing services and the shared model** before
adding new ones (Chapter 04, Reuse Before Create). New platform services are justified only when
no existing one serves or can be extended.

## 6. Reliability

Platform services depend on Core capability through the gateway, which governs reliability (its
circuit breaker) for the Core side. Platform services handle Core unavailability gracefully —
presenting a governed, honest state to the user rather than failing opaquely.

## 7. The Service Boundary

Platform services present and coordinate; they never bypass the gateway, the risk controls, or
the safety guarantees, and they carry no trading logic. A platform service reaches the Core as a
consumer, under governance.

## 8. Evolution

Platform services evolve by **addition**: new platform capability enters as a new platform
service that consumes the Core through the gateway, without changing the Core — Evolution Without
Revolution at the platform-service level.

---

*End of Chapter 24 — Service Architecture.*
