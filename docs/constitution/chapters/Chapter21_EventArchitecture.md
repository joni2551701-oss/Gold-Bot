# GoldBot Constitution — Chapter 21: Event Architecture

**Package:** GB-CONST-021 · **Document:** Chapter21_EventArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–20; does not contradict any approved chapter.
**Operative source:** [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md) (event backbone).

---

## Executive Summary

Chapter 21 describes the **Event** architecture — the typed publish/subscribe
backbone that couples the Core's producers and consumers loosely. Events let
components announce what has happened without knowing who is listening, so the Core
stays modular and extensible. This chapter states the event model, its
namespaces, and the boundary that keeps it infrastructure rather than logic.

## Table of Contents (Chapter 21)

1. Event Statement
2. Typed, Namespaced Events
3. Publish and Subscribe
4. Loose Coupling
5. Namespaces
6. Validation and Priority
7. The Event Boundary
8. Event Evolution

---

## 1. Event Statement

Events are the Core's **announcement backbone**. A component publishes a typed
event describing something that happened; interested components subscribe. The bus
depends on neither producer nor consumer — only on the typed event.

## 2. Typed, Namespaced Events

Every event is typed and namespaced, its identity expressed as a namespace and a
name. Typing makes events explicit and validated; namespacing keeps a large and
growing set of event kinds manageable and allows subscription by whole namespace.

## 3. Publish and Subscribe

Producers publish; consumers subscribe. Neither needs a reference to the other, so
components can be added, removed, or changed without rewiring the rest. This is the
mechanism by which the Core grows modularly.

## 4. Loose Coupling

The event backbone exists to keep coupling loose. Because communication flows
through typed events rather than direct calls, a new consumer can observe existing
events without any producer being modified — an expression of Evolution Without
Revolution (Chapter 04) inside the Core.

## 5. Namespaces

Events are grouped into namespaces by domain — for example market, bootstrap,
stream, replay, snapshot, and gateway. Namespacing lets a consumer subscribe to an
entire domain of events, and it keeps the vocabulary organized as new domains are
added over time.

## 6. Validation and Priority

Events are validated before they enter the bus, so a malformed event never
propagates, and they carry priority so that ordering can reflect importance. These
properties make the backbone reliable enough for the Core to depend on it.

## 7. The Event Boundary

The event backbone is infrastructure: it carries no Strategy, Decision, Signal, or
Trading logic, and it is not a path around the risk controls. It transports typed
facts; it does not make decisions. Business logic never lives on the bus
(Chapters 04, 09).

## 8. Event Evolution

The event vocabulary grows by **addition**: new event kinds and namespaces are
added without disturbing existing ones, and consumers subscribe to what they need.
This additive growth lets new components — including future surfaces reached
through the gateway — integrate by observing events rather than by changing the
Core.

---

*End of Chapter 21 — Event Architecture.*
