# GoldBot Constitution — Chapter 23: Snapshot Architecture

**Package:** GB-CONST-023 · **Document:** Chapter23_SnapshotArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–22; does not contradict any approved chapter.
**Operative source:** [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md) (persistence and snapshot layers).

---

## Executive Summary

Chapter 23 describes the **Snapshot** architecture — how the Core captures,
verifies, and manages durable copies of memory state. Snapshots underpin recovery,
replay, and portability. The design separates two responsibilities cleanly: the
persistence layer creates and stores snapshots, and the snapshot-management layer
governs their lifecycle. This chapter states that architecture and the boundaries
that keep it safe.

## Table of Contents (Chapter 23)

1. Snapshot Statement
2. Create-and-Store versus Manage
3. Catalog and Registry
4. Lifecycle and State
5. Locking and Transactions
6. Import, Export, and Compatibility
7. The Snapshot Boundary
8. Snapshot Evolution

---

## 1. Snapshot Statement

A snapshot is a **durable, verifiable capture of memory state**. Snapshots let the
Core be restored to a known-good condition, replayed from a recorded point, and
moved between environments, supporting the Backup and Recovery strategy.

## 2. Create-and-Store versus Manage

Snapshot responsibility is split to keep each part simple: the persistence layer
**creates and stores** snapshots (serialization, storage, integrity), and the
management layer **manages** them (catalog, lifecycle, retention, import and
export). The management layer reuses the persistence layer rather than
re-implementing it — an application of Reuse Before Create (Chapter 04).

## 3. Catalog and Registry

Snapshots are indexed by a metadata-only catalog and queried through a registry, so
they can be listed, found, and selected without loading their contents. The catalog
holds descriptive metadata; the snapshot data itself stays in storage.

## 4. Lifecycle and State

Each snapshot moves through an explicit lifecycle — created, verified, archived,
imported, exported, deleted, or flagged corrupt — with only legal transitions
permitted. The explicit state machine makes the snapshot's condition unambiguous
and its handling consistent.

## 5. Locking and Transactions

A snapshot in use is locked so it cannot be deleted or archived while a consumer
(such as a replay) depends on it. Snapshot operations that touch both storage and
catalog run transactionally, rolling back on failure, so the catalog and storage
never disagree.

## 6. Import, Export, and Compatibility

Snapshots can be exported as a portable, self-describing package carrying a manifest
(identity, versions, integrity), and imported elsewhere. Import is gated by a
compatibility check on schema, version, and asset, so an incompatible snapshot is
rejected rather than silently mishandled — an application of versioned
compatibility (Chapter 17).

## 7. The Snapshot Boundary

Snapshots are Core data infrastructure. They carry no trading logic, are reached
only through the Core's own components (and, for consumers, the gateway), and never
provide a path around the risk controls. They capture state; they do not act on it.

## 8. Snapshot Evolution

Snapshots evolve behind their manifest and compatibility gate: the stored format
can change across versions while imports remain safe, and the management layer can
add retention or metrics capability without changing how snapshots are created.
Growth is additive and compatibility-checked.

---

*End of Chapter 23 — Snapshot Architecture.*
