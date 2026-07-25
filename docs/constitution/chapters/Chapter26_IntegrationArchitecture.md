# GoldBot Constitution — Chapter 26: Integration Architecture

**Package:** GB-CONST-026 · **Document:** Chapter26_IntegrationArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–25; does not contradict any approved chapter.
**Operative source:** the Core Gateway Layer integration model, `docs/CORE_GATEWAY_ARCHITECTURE.md` (canonical once the Gateway is merged at the Core-complete milestone).

---

## Executive Summary

Chapter 26 describes the **Integration** architecture — how surfaces and external
clients integrate with the Core. The single rule that shapes all integration is
that it happens **only through the gateway**. This chapter states the internal and
external faces of that integration, how surfaces consume capability, and why no
integration path bypasses the gateway or the risk controls.

## Table of Contents (Chapter 26)

1. Integration Statement
2. Integration Through the Gateway
3. Internal and External Faces
4. Surfaces as Consumers
5. Capability-Based Integration
6. Versioned Compatibility
7. The Integration Boundary
8. Integration Evolution

---

## 1. Integration Statement

All integration with the Core happens **through the gateway**. Whether a caller is
an internal Core module or an external surface, it reaches Core capability by the
same single governed entry point.

## 2. Integration Through the Gateway

There is no integration path that avoids the gateway. A surface does not import or
call a Core component directly; it presents governed requests to the gateway, which
authenticates, authorizes, and dispatches them. This is what keeps every
integration auditable and uniform.

## 3. Internal and External Faces

The gateway presents two faces of the same discipline: an **internal** face, by
which Core modules integrate with one another, and an **external** face, by which
platforms and external clients integrate with the Core. Both faces run the same
governed dispatch; neither is a privileged shortcut.

## 4. Surfaces as Consumers

Surfaces — chart, platform, media, and the advisory intelligence's consumers —
integrate as **consumers** of Core capability, not as extensions of the Core. They
hold presentation and intent; they consume capability through the gateway; they do
not hold trading logic (Chapters 02, 06).

## 5. Capability-Based Integration

A surface integrates against a **capability**, discovered through the gateway,
rather than against a specific implementation. Capability-based integration lets the
provider of a capability change without changing the surfaces that depend on it, an
application of contracts (Chapter 25) and service discovery (Chapter 24).

## 6. Versioned Compatibility

Integration is governed by versioned compatibility: a surface can check the Core and
gateway versions before relying on them, so surfaces and Core can evolve at
different speeds without breaking each other (Chapter 17). Compatibility is checked,
not assumed.

## 7. The Integration Boundary

No integration path carries trading logic into the gateway, places client logic in
the Core, or provides a route around the risk controls. Integration connects
surfaces to capability under governance; it never dissolves the boundaries that
protect the user.

## 8. Integration Evolution

New surfaces, transports, and external clients integrate by **addition** at the
gateway boundary, under the same governed model, without changing the Core. This is
how the ecosystem grows for years on top of a stable Core — the integration
expression of Evolution Without Revolution (Chapter 04).

---

*End of Chapter 26 — Integration Architecture.*
