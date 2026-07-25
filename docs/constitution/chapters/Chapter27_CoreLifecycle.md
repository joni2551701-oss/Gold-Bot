# GoldBot Constitution — Chapter 27: Core Lifecycle

**Package:** GB-CONST-027 · **Document:** Chapter27_CoreLifecycle.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–26; does not contradict any approved chapter.
**Operative sources:** [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md), [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md).

---

## Executive Summary

Chapter 27 closes the architecture block by describing the **Core Lifecycle** — how
the Core comes up, becomes ready, operates, and recovers. The lifecycle ties the
architecture chapters together: memory is hydrated, services start in dependency
order, readiness is signaled, and the Core recovers to a known-good state when
needed. This chapter states the lifecycle and the safety that governs every stage.

## Table of Contents (Chapter 27)

1. Lifecycle Statement
2. Readiness
3. Startup and Dependency Order
4. Bootstrap and Hydration
5. Operational States
6. Recovery
7. Lifecycle and Safety
8. Lifecycle Evolution

---

## 1. Lifecycle Statement

The Core has an explicit lifecycle: it starts, becomes ready, operates, and
recovers under defined, observable states. The Core does not serve until it is
ready, and its readiness is a property the rest of the system can observe rather
than assume.

## 2. Readiness

Readiness is explicit. The Core signals when it is prepared to serve, and consumers
observe that signal before relying on it. A component that is not ready does not
receive traffic (Chapter 24), so partial or unprepared state is never mistaken for
a serving one.

## 3. Startup and Dependency Order

Services start in **dependency order**: the gateway validates the service
dependency graph — rejecting missing dependencies and cycles — and brings each
service up only after those it depends on. Startup order is derived from declared
dependencies, not assumed, so the Core comes up coherently.

## 4. Bootstrap and Hydration

The Core hydrates its memory from durable state before serving: historical data and
persisted snapshots are loaded and integrity-checked, so the Core begins from a
verified, known-good condition rather than an empty or unverified one
(Chapters 20, 23).

## 5. Operational States

In operation, the Core and its services carry observable states — ready, degraded,
or otherwise — that reflect their real condition. Degradation is visible rather than
hidden, so the system's true health can be read at any time (Chapter 14, and the
gateway's health endpoint).

## 6. Recovery

When state is lost or suspected corrupt, the Core recovers to a known-good
condition: it restores from a verified snapshot in preference to a corrupt recent
one, and it never hydrates from data that fails its integrity check. Recovery is
safe by construction (Chapter 20).

## 7. Lifecycle and Safety

Every lifecycle stage preserves the safety guarantees. Coming up, degraded, or
recovering, the Core still provides no path around the risk controls and no route
by which the advisory intelligence could execute. Safety does not depend on the
Core being in any particular state.

## 8. Lifecycle Evolution

The lifecycle evolves by adding governed states and transitions — new service kinds,
new readiness or recovery behavior — behind the same explicit model, without
weakening its guarantees. As the Core grows, how it starts, serves, and recovers
stays observable and safe.

---

*End of Chapter 27 — Core Lifecycle. This chapter completes the architecture block
(Chapters 18–27) of the GoldBot Constitution v1.0 edition.*
