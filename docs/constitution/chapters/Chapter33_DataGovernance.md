# GoldBot Constitution — Chapter 33: Data Governance

**Package:** GB-CONST-033 · **Document:** Chapter33_DataGovernance.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–32; does not contradict any approved chapter.
**Operative sources:** [`docs/MARKET_DATA_ARCHITECTURE.md`](../../MARKET_DATA_ARCHITECTURE.md), [`data/`](../../../data/).

---

## Executive Summary

Chapter 33 states **data governance** — how GoldBot owns, protects, and shares the
market data and derived state at the heart of the system. Data is Core-owned;
surfaces consume it through the gateway. Governance ensures the data is a single,
integrity-checked, auditable source, retained and recoverable, and never forked into
divergent private copies. This chapter states that governance; the operative data
architecture holds the detail.

## Table of Contents (Chapter 33)

1. Data Statement
2. Core Ownership of Data
3. Integrity
4. Provenance and Auditability
5. Access Through the Gateway
6. Retention and Recovery
7. The Data Boundary
8. Data Evolution

---

## 1. Data Statement

Data is a **Core-owned asset**. The Core is the single authority for market data and
system state, and data governance keeps that authority consistent, protected, and
auditable.

## 2. Core Ownership of Data

The Core owns market data and derived state; surfaces consume it, never own it
(Chapters 06, 20). Because there is one owner, the system reasons from one
consistent source rather than reconciling many, and the responsibility for data is
unambiguous.

## 3. Integrity

Data integrity is enforced structurally: state is integrity-checked before it is
used, and data that fails a check is not admitted (Chapter 20). Governance treats
integrity as a precondition of use, so the Core is never quietly populated with bad
data.

## 4. Provenance and Auditability

Data carries enough provenance to be traceable, and consequential handling of data
is recorded in the audit trail. Governance keeps the origin and handling of data
examinable, in keeping with the Constitution's auditability commitment
(Chapter 15).

## 5. Access Through the Gateway

Consumers access data as governed capability through the gateway (Chapter 26), not
by reaching into the Core. Access is authenticated, authorized, and auditable, and
the Core retains the authority to mutate state while surfaces read it.

## 6. Retention and Recovery

Data is retained durably and is recoverable to a known-good condition through the
persistence and snapshot layers (Chapters 20, 23). Retention and recovery are
governed so the system can be restored safely, preferring verified state over
corrupt recent state.

## 7. The Data Boundary

Data is owned by the Core and consumed at the perimeter. Surfaces do not own, fork,
or mutate Core data, and no data path provides a route around the risk controls.
The data boundary keeps one authoritative source rather than many divergent ones.

## 8. Data Evolution

Data governance evolves behind stable contracts: storage backends, formats, and
representations may change without changing what consumers depend on, and versioned
snapshots keep captured data portable and compatibility-checked. The authority and
the guarantees remain constant as the implementation improves.

---

*End of Chapter 33 — Data Governance.*
