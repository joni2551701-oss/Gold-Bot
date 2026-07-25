# GoldBot Platform Constitution — Chapter 26: Integration Layer

**Package:** GB-PLATFORM-CONST-026 · **Document:** Chapter26_IntegrationLayer.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../CORE_GATEWAY_ARCHITECTURE.md), [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md).

---

## Executive Summary

Chapter 26 describes the **integration layer of the Platform** — how surfaces integrate with the
Core, and how platform services integrate with one another. The single rule is that Core
integration happens **only through the gateway**. This chapter states that model and the boundary
that keeps every integration governed.

## Table of Contents (Chapter 26)

1. Integration Statement
2. Integration with the Core
3. Integration Among Platform Services
4. Capability-Based Integration
5. External Integrations
6. Versioned Compatibility
7. The Integration Boundary
8. Evolution

---

## 1. Integration Statement

The integration layer connects the Platform to the Core and platform services to each other. All
**Core** integration is through the gateway; all internal integration is through defined
interfaces. Nothing integrates by reaching into another component's internals.

## 2. Integration with the Core

Surfaces and platform services integrate with the Core **only through the gateway** (GoldBot
Constitution, Integration Architecture). There is no direct-call path and no second entry point;
every Core integration is authenticated, authorized, and auditable.

## 3. Integration Among Platform Services

Platform services integrate with one another through **defined interfaces**, not by shared
internals. A change in one service does not ripple unpredictably into another, keeping the
platform layer modular.

## 4. Capability-Based Integration

A surface or service integrates against a **capability**, discovered through the gateway, rather
than a specific implementation. Capability-based integration lets the provider of a capability
change without changing its consumers (Chapters 24, 25).

## 5. External Integrations

Where the Platform integrates with an **external** system, that integration is governed:
authenticated, authorized, and bounded, and it never becomes a back door into the Core. External
integrations are consumers at the perimeter, under the same boundaries as any surface.

## 6. Versioned Compatibility

Integrations are governed by versioned compatibility: a consumer checks the versions it depends
on before relying on them, so parts evolve at different speeds without breaking each other
(Chapter 17).

## 7. The Integration Boundary

No integration path carries trading logic into a surface, places client logic into the Core, or
provides a route around the risk controls. Integration connects consumers to capability under
governance; it never dissolves a boundary (DR-015).

## 8. Evolution

The integration layer evolves by **addition** at the gateway and interface boundaries — new
surfaces, services, and external integrations — under the same governed model, without changing
the Core.

---

*End of Chapter 26 — Integration Layer.*
