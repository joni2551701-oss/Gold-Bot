# GoldBot Constitution — Chapter 20: Memory Architecture

**Package:** GB-CONST-020 · **Document:** Chapter20_MemoryArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–19; does not contradict any approved chapter.
**Operative source:** [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md).

---

## Executive Summary

Chapter 20 describes the **Memory** architecture — the Core's authority for market
data and derived state. Memory holds the market's recent history per timeframe,
persists it durably, verifies its integrity, and offers a read model to consumers.
It is where the Knowledge-First and Foundation-First principles meet: one
consistent, durable source of market truth that surfaces consume through the
gateway.

## Table of Contents (Chapter 20)

1. Memory Statement
2. Market Memory
3. Persistent Memory
4. Integrity and Recovery
5. The Read Model
6. Determinism
7. The Memory Boundary
8. Memory Evolution

---

## 1. Memory Statement

Memory is the **single authority for market data and system state** within the
Core. Surfaces do not hold a private copy of market data; they consume Memory
through the gateway, so the system reasons from one source rather than many.

## 2. Market Memory

Market Memory holds the market's recent, closed history organized by timeframe. It
is the working state from which context, analysis, and intelligence are derived. It
is bounded and consistent, so consumers see a coherent view of the market rather
than an ad-hoc collection.

## 3. Persistent Memory

Memory is made durable by a persistence layer that serializes state to a
backend-agnostic store and restores it safely. Persistence is what allows the Core
to survive restarts and to recover to a known-good condition, supporting the
Backup and Recovery commitments of the long-term strategy.

## 4. Integrity and Recovery

Restoration is safe by construction: state is integrity-checked before it is used,
and if the check fails the existing memory is left untouched and the restore is
aborted. Recovery prefers a verified prior state over a corrupt recent one, so the
Core is never quietly hydrated from bad data.

## 5. The Read Model

Consumers read Memory through a defined read model rather than by manipulating its
internals. The read model presents market state for analysis and presentation
while keeping the authority — and the right to mutate state — inside the Core.

## 6. Determinism

Memory is designed for determinism: time is injected rather than read ambiently, so
the same inputs produce the same state and behavior is reproducible and testable.
Determinism underpins the quality and auditability the Constitution requires
(Chapters 14, 15).

## 7. The Memory Boundary

Memory is Core-owned. It carries no surface or presentation logic, exposes itself
only through the gateway, and never becomes a path around the risk controls.
Surfaces consume market state; they do not own or fork it (Chapter 06, the
knowledge boundary).

## 8. Memory Evolution

Memory evolves behind stable contracts: storage backends and internal
representations may change without changing what consumers depend on, and
snapshots (Chapter 23) provide versioned, portable capture of its state. The
authority and the guarantees remain constant while the implementation improves.

---

*End of Chapter 20 — Memory Architecture.*
