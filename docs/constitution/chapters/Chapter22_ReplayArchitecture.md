# GoldBot Constitution — Chapter 22: Replay Architecture

**Package:** GB-CONST-022 · **Document:** Chapter22_ReplayArchitecture.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–21; does not contradict any approved chapter.
**Operative source:** [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md) (Core time layer).

---

## Executive Summary

Chapter 22 describes the **Replay** architecture — the Core's time-control layer,
which lets market data flow through the system under live time, historical time,
or simulated time. Replay makes the Core observable and testable across time
without changing how components consume data. This chapter states the time model
and the boundary that keeps Replay a feeder of memory rather than a decision-maker.

## Table of Contents (Chapter 22)

1. Replay Statement
2. Time Modes
3. The Virtual Clock
4. Timeline Control
5. Replay-to-Live Handoff
6. Data Sources
7. The Replay Boundary
8. Replay Evolution

---

## 1. Replay Statement

Replay is the Core's **control of time and data flow** into memory. It governs
whether the Core is fed by live market flow or by a controlled replay of recorded
or simulated data, without the consumers of memory needing to know which.

## 2. Time Modes

The Core operates in distinguishable time modes — live and replay — so that the
same components can run against real-time flow or a controlled timeline. The mode
is an explicit property of the Core's state, not an ambient assumption.

## 3. The Virtual Clock

Replay is driven by an injected, virtual clock rather than ambient wall-clock time.
Because time is controlled and injected (Chapter 20, Determinism), a replay is
reproducible: the same recorded data replayed the same way yields the same
behavior.

## 4. Timeline Control

Replay offers control over the timeline — starting, pausing, resuming, stepping,
seeking, and adjusting speed — so the Core's behavior can be examined at any point.
These controls operate on the flow of data into memory; they do not alter the
components that consume it.

## 5. Replay-to-Live Handoff

Replay supports a controlled handoff from replayed time back to live time, so the
Core can transition from studying the past to following the present without a
disruptive reset. The handoff is an explicit, governed transition of the Core's
time mode.

## 6. Data Sources

Replay draws from pluggable sources — recorded snapshots, historical data, or
simulated flow — behind a common interface. New sources can be added without
changing the replay control itself, an application of Reuse Before Create and
stable contracts.

## 7. The Replay Boundary

Replay feeds memory only. It carries no Strategy, Decision, Signal, or Trading
logic, and it is not wired into the trading pipeline as a decision path
(Trading Safety). It controls how data enters memory; it never decides what to do
with that data.

## 8. Replay Evolution

Replay evolves by adding sources and controls behind its stable interface. Because
it feeds the same memory that live flow does, new replay capability enriches how
the Core can be studied and tested without changing how any consumer works — growth
by addition, at the edge of the time layer.

---

*End of Chapter 22 — Replay Architecture.*
