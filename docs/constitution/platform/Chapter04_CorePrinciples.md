# GoldBot Platform Constitution — Chapter 04: Core Principles

**Package:** GB-PLATFORM-CONST-004 · **Document:** Chapter04_CorePrinciples.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Foundation (01–07)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../CORE_GATEWAY_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 04 states the **core principles of the Platform layer** — the standing rules that
govern every platform decision. These principles are the platform-scoped application of the
GoldBot Constitution's own principles; where the two meet, the GoldBot Constitution governs.

## Table of Contents (Chapter 04)

1. One Platform Model
2. Gateway-Only Access
3. No Trading Logic in the Platform
4. Core Platform Independence
5. Honest Capability Declaration
6. Reuse Before Create
7. Consistency and Accessibility
8. Evolution Without Fragmentation

---

## 1. One Platform Model

All surfaces share **one platform-neutral model**. Each client adapts that model to its own
presentation rather than inventing its own structure, so a capability defined once is
expressed consistently across surfaces.

## 2. Gateway-Only Access

Every platform reaches the Core **only through the gateway** (GoldBot Constitution, Gateway
and Integration chapters). No surface imports or calls a Core component directly, and no
second route to the Core is introduced.

## 3. No Trading Logic in the Platform

Platforms hold **no** Strategy, Decision, Signal, or Trading logic, and provide no path
around the risk controls. Presentation and intent live at the perimeter; decisions and
protections live in the Core (Trading Safety, DR-015).

## 4. Core Platform Independence

Platforms **adapt to the Core**, never the reverse. A surface never pushes platform-specific
assumptions into the shared model or the Core, preserving the Core's platform independence
so new clients can be added without Core change.

## 5. Honest Capability Declaration

Each surface declares, per capability, whether it supports it and — where it does not — the
reason. Honest declaration keeps the true state of every surface visible to users and
reviewers.

## 6. Reuse Before Create

Before a new platform component is created, an existing one is preferred or extended, and any
new component is justified and recorded (GoldBot Constitution, Core Principles). The shared
model and existing surfaces are reused rather than duplicated per platform.

## 7. Consistency and Accessibility

Surfaces present the shared model **consistently and accessibly**, so users move between
clients without relearning, and each client meets its platform's accessibility expectations.
Consistency is a principle, not an afterthought.

## 8. Evolution Without Fragmentation

The Platform layer evolves by **adding surfaces on one model**, not by fragmenting into
divergent bespoke clients. New platforms and features are additions at the perimeter, under
governance, that leave the shared model and the Core intact.

---

*End of Chapter 04 — Core Principles (Platform Constitution).*
