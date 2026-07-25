# GoldBot Constitution — Chapter 18: Core Architecture

**Package:** GB-CONST-018 · **Document:** Chapter18_CoreArchitecture.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–17; does not contradict any approved chapter.
**Operative sources:** [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md), [`docs/ARCHITECTURE_RULES.md`](../../ARCHITECTURE_RULES.md), [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md).

---

## Executive Summary

Chapter 18 opens the architecture block by describing the **Core** as a whole —
the stable, platform-independent interior that every surface reaches only through
the gateway. It states what the Core is, which components compose it, and the
boundaries that make it trustworthy. The chapters that follow (Gateway, Memory,
Event, Replay, Snapshot, Service, Contract, Integration, Core Lifecycle) detail
each part; this chapter is the map that places them.

## Table of Contents (Chapter 18)

1. Core Architecture Statement
2. The Core Boundary
3. Core Components
4. Layered Pipeline
5. Single Entry Point
6. Platform Independence
7. Safety in the Core
8. Core Evolution

---

## 1. Core Architecture Statement

The Core is GoldBot's **stable interior**: the authority for market data and
system state, built once as long-lived infrastructure and extended rather than
rewritten (Chapter 04, Foundation First). Everything a surface relies on
originates in the Core and is reached through one governed gateway.

## 2. The Core Boundary

The Core is bounded by two rules: nothing reaches it except through the gateway,
and it holds no client, presentation, or trading-surface logic. What is inside the
boundary — data, memory, events, replay, snapshots, and the gateway — is the
Core's responsibility; what is outside — surfaces and presentation — adapts to it.

## 3. Core Components

The Core is composed of cooperating foundations, each detailed in its own chapter:

- **Memory** — the authority for market data and derived state (Chapter 20).
- **Events** — the typed publish/subscribe backbone that couples producers and
  consumers loosely (Chapter 21).
- **Replay** — the time-control layer for historical and simulated flow
  (Chapter 22).
- **Snapshots** — durable, verifiable capture and management of memory state
  (Chapter 23).
- **Gateway** — the single governed entry point through which all access passes
  (Chapter 19).

## 4. Layered Pipeline

The Core's data flow is layered, and each layer speaks only to the one below it,
never skipping or reversing (Chapter 09, Architecture Philosophy). The pipeline
order and layer rules are defined in the operative architecture documents; the
constitutional commitment is that the layering is preserved so responsibility
stays local and change stays contained.

## 5. Single Entry Point

All access to Core components is through the gateway (Chapter 19). The Core
exposes no second door: a surface never imports or calls a Core component
directly. This single entry point is where access is authenticated, authorized,
rate-limited, discovered, and governed.

## 6. Platform Independence

The Core assumes nothing about its callers and carries no client- or
transport-specific logic. The same Core serves any surface, present or future,
because platform concerns are kept at the perimeter (Chapter 09). Platform
independence is what allows the ecosystem to grow without Core change.

## 7. Safety in the Core

The Core embodies Trading Safety structurally: it provides no path that bypasses
the risk controls and no route by which the advisory intelligence could execute.
These protections are properties of the architecture, held regardless of how any
single component is operated (Chapters 04, 09).

## 8. Core Evolution

The Core evolves by **evolution, not revolution** (Chapter 09): new capability is
added on top of the gateway as a work package, transports and providers change
behind stable contracts, and versioned compatibility lets surfaces and Core evolve
at different speeds. The interior, and the guarantees it carries, remains constant
while the perimeter grows.

---

*End of Chapter 18 — Core Architecture.*
