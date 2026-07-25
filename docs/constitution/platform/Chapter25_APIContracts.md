# GoldBot Platform Constitution — Chapter 25: API Contracts

**Package:** GB-PLATFORM-CONST-025 · **Document:** Chapter25_APIContracts.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative source:** [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../CORE_GATEWAY_ARCHITECTURE.md).

---

## Executive Summary

Chapter 25 describes the **API contracts** the Platform layer relies on — the stable, versioned
interfaces between surfaces and the gateway. Surfaces depend on contracts, not implementations,
so the Core can evolve behind them. This chapter states how platform API contracts are used,
kept stable, and versioned, under the GoldBot Constitution's API governance.

## Table of Contents (Chapter 25)

1. Contract Statement
2. The Gateway Contract
3. Contract Stability
4. Versioning
5. Compatibility Checking
6. Contracts and Reuse
7. The Contract Boundary
8. Evolution

---

## 1. Contract Statement

An API contract is a **stable interface** a surface depends on. The Platform layer relies on the
gateway's contracts to reach Core capability, depending on the promise rather than on how the
Core keeps it.

## 2. The Gateway Contract

The Platform layer's primary contract is the **gateway's external API** (GoldBot Constitution,
API Governance). Surfaces present governed requests to this contract and receive governed
responses; there is no other contract to the Core, and no second entry point.

## 3. Contract Stability

A published contract is **stable for its version**: surfaces can rely on it, and it is not
changed silently. Stability is what lets the Core evolve internally without breaking the surfaces
that depend on it.

## 4. Versioning

Platform-facing contracts are **versioned**, and the gateway announces its version so surfaces
can check compatibility before relying on it (Chapter 17). A contract is extended compatibly
within a version and broken only by a new version, deliberately and on the record.

## 5. Compatibility Checking

Surfaces **check** the contract and Core/gateway versions they require before depending on them,
so an incompatible pairing is detected rather than silently mishandled. Compatibility is verified,
not assumed.

## 6. Contracts and Reuse

Contracts are the unit of reuse between the Platform layer and the Core: a surface depends on an
existing gateway contract rather than duplicating the capability behind it. New contracts are
preferred over duplicated capability only when genuinely needed.

## 7. The Contract Boundary

A contract states capability, not trading authority: no platform API contract exposes a path
around the gateway or the risk controls, or carries trading logic into a surface. The contract is
where the platform/Core boundary is made precise.

## 8. Evolution

Platform API contracts evolve compatibly where possible and by explicit new version when not,
always through the single gateway contract. New Core capability appears to surfaces as new
services discovered through the same governed API.

---

*End of Chapter 25 — API Contracts.*
