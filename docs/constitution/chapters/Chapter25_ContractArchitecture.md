# GoldBot Constitution — Chapter 25: Contract Architecture

**Package:** GB-CONST-025 · **Document:** Chapter25_ContractArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Architecture (Chapters 18–27)
**Continuity:** Reuses the terminology of Chapters 01–24; does not contradict any approved chapter.
**Operative source:** [`contracts/`](../../../contracts/) (the layer contracts), [`ai/interfaces.py`](../../../ai/interfaces.py) (advisory interface).

---

## Executive Summary

Chapter 25 describes the **Contract** architecture — the stable interfaces that let
parts of GoldBot depend on each other without depending on each other's internals.
Contracts are what make the system's boundaries real: a consumer relies on a
contract, not an implementation, so the implementation can change while the
consumer keeps working. This chapter states how contracts are used and why they are
kept stable and versioned.

## Table of Contents (Chapter 25)

1. Contract Statement
2. Layer Contracts
3. Interface Stability
4. The Advisory Interface
5. Versioned Contracts
6. Contracts and Reuse
7. The Contract Boundary
8. Contract Evolution

---

## 1. Contract Statement

A contract is a **stable interface** between two parts of the system. It states
what a part promises to provide, so consumers can depend on the promise rather than
on how it is kept.

## 2. Layer Contracts

The pipeline layers interact through defined contracts, so that each layer depends
on the one below it only through a stable interface (Chapter 09). The layer
contracts are maintained as their own source of truth and referenced where needed,
rather than re-described inside each consumer.

## 3. Interface Stability

A published contract is stable for its version: consumers can rely on it, and it is
not changed silently. Stability is what allows the Core to evolve internally
without breaking the surfaces and services that depend on it — the foundation of
Evolution Without Revolution (Chapter 04).

## 4. The Advisory Interface

The advisory intelligence interacts with the rest of the system through a
well-defined advisory interface. This contract is where the advisory boundary is
enforced: the AI layer provides analysis as input, and the interface gives it no
authority to approve, reject, size, send, or execute a trade (Chapters 02, 07,
Trading Safety).

## 5. Versioned Contracts

Contracts are versioned so that consumers can check compatibility before relying on
them (Chapter 17). A contract may be extended compatibly within a version and
broken only by a new version, deliberately and on the record — never by a silent
change.

## 6. Contracts and Reuse

Contracts are the natural unit of reuse: a new component depends on an existing
contract rather than duplicating the capability behind it. Before a new interface
is created, an existing contract is preferred or extended (Chapter 04, Reuse Before
Create), so the system does not accumulate parallel interfaces for the same
concern.

## 7. The Contract Boundary

A contract states capability, not implementation, and never leaks a boundary: a
contract does not expose a path around the gateway or the risk controls, and it
does not carry trading authority into a layer that should not have it. The contract
is where a boundary is made precise.

## 8. Contract Evolution

Contracts evolve compatibly wherever possible and by explicit new version when not.
Because consumers depend on contracts rather than internals, the system can improve
behind its contracts continuously, and a breaking change is a deliberate, recorded,
governed event.

---

*End of Chapter 25 — Contract Architecture.*
