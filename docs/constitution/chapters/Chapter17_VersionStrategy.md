# GoldBot Constitution — Chapter 17: Version Strategy

**Package:** GB-CONST-017 · **Document:** Chapter17_VersionStrategy.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Governance (Chapters 08–17)
**Continuity:** Reuses the terminology of Chapters 01–16; does not contradict any approved chapter.
**Operative sources:** [`docs/policies/VERSION_POLICY.md`](../../policies/VERSION_POLICY.md), [`docs/standards/RELEASE_STANDARD.md`](../../standards/RELEASE_STANDARD.md).

---

## Executive Summary

Chapter 17 closes the governance block with the **version strategy** — how GoldBot
versions its Core and its interfaces so the ecosystem can evolve safely. Versioning
in GoldBot serves compatibility: the Core and gateway announce their versions so
surfaces can check them before relying on them, allowing different parts of the
system to change at different speeds without breakage. This chapter states the
strategy; the operative version policy and release standard live in the referenced
sources.

## Table of Contents (Chapter 17)

1. Version Statement
2. Versioning Principles
3. Core and Gateway Versions
4. Compatibility
5. Amend Rarely, Extend Routinely
6. Release Discipline
7. Version and Safety
8. Long-Term Versioning

---

## 1. Version Statement

GoldBot versions its Core and its interfaces so that **change is compatible and
legible**. A version is a promise about an interface, made so that consumers can
depend on it deliberately.

## 2. Versioning Principles

- **Announced versions.** The Core and the gateway expose their versions so
  consumers can check compatibility before relying on them.
- **Stable contracts.** A published contract holds for its version; breaking it
  requires a new version, not a silent change.
- **Independent evolution.** Surfaces and Core may evolve at different speeds, held
  together by versioned compatibility rather than lockstep change.

## 3. Core and Gateway Versions

The Core carries a version for its overall infrastructure, and the gateway carries
a version for its external contract. These are announced through the gateway's
version service, so a surface can determine what it is talking to and whether it is
compatible before it depends on it.

## 4. Compatibility

Compatibility is checked, not assumed. A consumer verifies the Core and gateway
versions it requires before relying on them, and an incompatible pairing is
detected rather than silently mishandled. This is the mechanism that lets the
ecosystem grow without one part breaking another.

## 5. Amend Rarely, Extend Routinely

Versioning reflects the Constitution's growth model: interfaces are **extended**
compatibly wherever possible, and **broken** (a new major version) only when
necessary and deliberately. Routine growth adds capability without breaking
consumers; breaking change is an explicit, recorded decision.

## 6. Release Discipline

A version is released through the governed process — reviewed, validated, and
authorized — under the operative release standard. A release is not made informally;
it carries the same acceptance and safety gates as any consequential change.

## 7. Version and Safety

Versioning never weakens the safety guarantees. No new version, compatibility mode,
or release path may bypass the risk controls, enable advisory execution, or breach
the gateway boundary. The safety invariants hold across every version, without
exception.

## 8. Long-Term Versioning

Over the long horizon, the version strategy keeps the **same Core with a broader
perimeter** legible: early contracts remain honored or are superseded only by
recorded, compatible evolution, so that a consumer written years ago can still
reason about what it depends on. Versioning is the long-term guarantee that
additive growth stays coherent.

---

*End of Chapter 17 — Version Strategy. This chapter completes the governance block
(Chapters 08–17) of the GoldBot Constitution v1.0 edition.*
