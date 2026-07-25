# GoldBot Constitution — Chapter 24: Service Architecture

**Package:** GB-CONST-024 · **Document:** Chapter24_ServiceArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–23; does not contradict any approved chapter.
**Operative source:** the Core Gateway Layer service model, `docs/CORE_GATEWAY_ARCHITECTURE.md` (canonical once the Gateway is merged at the Core-complete milestone).

---

## Executive Summary

Chapter 24 describes the **Service** architecture — how Core capability is exposed
as governed services behind the gateway. A service is a registered, discoverable
unit with a manifest, a lifecycle, and a reliability policy. This model is how the
gateway (Chapter 19) knows what it can route to, and how the Core grows by adding
services rather than by opening new doors.

## Table of Contents (Chapter 24)

1. Service Statement
2. Services as Gateway Citizens
3. The Service Manifest
4. Lifecycle States
5. Discovery by Name and Capability
6. Reliability
7. The Service Boundary
8. Service Evolution

---

## 1. Service Statement

A service is a **registered unit of Core capability** reached only through the
gateway. Services are how the Core presents what it can do to callers, uniformly
and under governance.

## 2. Services as Gateway Citizens

Every service registers with the gateway and is reached only through it. A service
is not called directly by a surface; it is discovered and dispatched to by the
gateway. This keeps the single-entry-point boundary intact for every capability.

## 3. The Service Manifest

Each service registers a manifest declaring its identity, version, capabilities,
dependencies, and health policy. The manifest makes discovery and dependency
management declarative: the gateway can find a service by what it offers and can
reason about what it needs before starting it.

## 4. Lifecycle States

Each service moves through an explicit lifecycle — from registered, through
starting, to ready, and on to degraded, stopping, stopped, or failed as
circumstances require. The gateway routes requests only to a **ready** service, so
a service that is not yet serving, or no longer serving, does not receive traffic.

## 5. Discovery by Name and Capability

Services are discovered by name or by declared capability. Capability-based
discovery lets a caller request what it needs — a capability — without binding to a
specific provider, so providers can change behind a stable capability
(Chapter 25, Contracts).

## 6. Reliability

Each service is governed by a reliability policy at the gateway: when a service
fails repeatedly, a circuit opens and the gateway stops routing to it until a
cooldown allows a trial recovery. Reliability governance keeps one failing service
from degrading the whole Core.

## 7. The Service Boundary

Services expose Core capability; they never bypass the gateway, the risk controls,
or the safety guarantees. A service carries only its own capability — not trading
decisions that belong to the governed pipeline — and it reaches other services, if
it must, as a declared dependency, not by a private path.

## 8. Service Evolution

Services evolve by **addition**: new capability enters as a new registered service
with its own manifest and lifecycle, discovered by capability, without changing the
gateway or the Core interior. This is the concrete mechanism of Evolution Without
Revolution (Chapter 04) at the service level.

---

*End of Chapter 24 — Service Architecture.*
