# GoldBot Constitution — Chapter 19: Gateway Architecture

**Package:** GB-CONST-019 · **Document:** Chapter19_GatewayArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–18; does not contradict any approved chapter.
**Operative source:** the Core Gateway Layer design, `docs/CORE_GATEWAY_ARCHITECTURE.md` (canonical once the Gateway is merged at the Core-complete milestone).

---

## Executive Summary

Chapter 19 describes the **Gateway** — the single governed entry point that is the
architectural expression of the Gateway-First principle (Chapter 04). It states
how access is routed and governed, how services are discovered, and why the
gateway holds no trading logic and depends on no transport. This is the interface
through which the whole ecosystem reaches the Core.

## Table of Contents (Chapter 19)

1. Gateway Statement
2. The Single Entry Point
3. Dispatch Pipeline
4. Service Registry and Discovery
5. Governance Concerns
6. Transport Independence
7. The Gateway Boundary
8. Gateway Evolution

---

## 1. Gateway Statement

The Gateway is the **one governed door** into the Core. Every request from every
surface passes through it, and it is the place where cross-cutting access
concerns are enforced uniformly, once, for all callers.

## 2. The Single Entry Point

There is exactly one entry point, and no second door is ever introduced
(Chapter 04). A surface does not reach a Core component directly; it presents a
request to the Gateway, which resolves and governs it. This singularity is what
makes access auditable and platform-independent.

## 3. Dispatch Pipeline

Every request runs the same ordered sequence of gates before any component is
reached: a standard request context is built; the caller is authenticated; the
target service is discovered by name or capability; authorization is checked;
readiness is confirmed; rate limits are applied; a reliability check is made; and
only then is the request dispatched to the service. Each stage has a defined
outcome, and a failing gate stops the request with a clear status.

## 4. Service Registry and Discovery

The Gateway maintains a registry of Core services and discovers them for callers
(Chapter 24). Services are found by name or by declared **capability**, so a caller
can ask for a capability without knowing which service provides it. Discovery is
governed by the same boundary as dispatch — a caller reaches a service only
through the Gateway.

## 5. Governance Concerns

The Gateway is where access governance lives: authentication (who is calling),
authorization (what they may reach), rate limiting (how often), reliability (a
per-service circuit breaker), and the health, metrics, and version endpoints that
let the ecosystem observe and check the Core. None of these concerns leak into the
Core components themselves.

## 6. Transport Independence

The Gateway is independent of transport (Director Decision, Core Gateway design):
a request is a plain value, governed the same way whether it arrives in-process
today or over a network protocol in future. Adding a transport is an edge change
at the Gateway boundary, not a change to the Core.

## 7. The Gateway Boundary

The Gateway routes and governs; it holds **no** Strategy, Decision, Signal, or
Trading logic, and it offers no execution route. It can never become a shortcut
around the risk controls. This boundary is absolute: business logic never enters
the Gateway (Chapters 04, 09).

## 8. Gateway Evolution

The Gateway evolves by adding governed capability at its own boundary — new
transports, new authentication or authorization backends, new service kinds —
without changing the Core it fronts. Its external contract is versioned
(Chapter 17), so surfaces can depend on it deliberately as it grows.

---

*End of Chapter 19 — Gateway Architecture.*
