# GoldBot Platform Constitution — Chapter 17: Version Strategy

**Package:** GB-PLATFORM-CONST-017 · **Document:** Chapter17_VersionStrategy.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Governance (08–17)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/policies/VERSION_POLICY.md`](../../policies/VERSION_POLICY.md), [`docs/PLATFORM_CHANGELOG.md`](../../PLATFORM_CHANGELOG.md).

---

## Executive Summary

Chapter 17 closes the Platform governance block with the **version strategy** — how the Platform
layer versions its surfaces and checks compatibility with the Core. Platforms evolve at their
own pace, held to the Core by the gateway's announced versions. This chapter states the
platform-scoped strategy under the GoldBot Constitution's version strategy.

## Table of Contents (Chapter 17)

1. Version Statement
2. Versioning Principles
3. Platform Versions and Core Compatibility
4. Compatibility Checking
5. Amend Rarely, Extend Routinely
6. Release Discipline
7. Version and Safety
8. Long-Term Versioning

---

## 1. Version Statement

The Platform layer versions its surfaces so that **change is compatible and legible**, and it
depends on the Core only through announced, checked versions. A platform version is a promise
about a surface's behavior.

## 2. Versioning Principles

- **Announced versions.** Surfaces carry versions, and the Core/gateway announce theirs.
- **Stable behavior.** A published surface behavior holds for its version; breaking it requires
  a new version.
- **Independent evolution.** Surfaces and Core evolve at different speeds, held together by
  versioned compatibility (GoldBot Constitution, Version Strategy).

## 3. Platform Versions and Core Compatibility

A surface checks the **Core and gateway versions** it requires — announced by the gateway's
version service — before it relies on them. The Platform layer never assumes Core compatibility;
it verifies it.

## 4. Compatibility Checking

Compatibility is checked, not assumed: an incompatible Core/surface pairing is detected and
handled, not silently mishandled. This is what lets surfaces evolve without breaking against a
changing Core.

## 5. Amend Rarely, Extend Routinely

Surface interfaces are **extended** compatibly wherever possible and **broken** (a new version)
only when necessary and deliberately. Routine growth adds capability without breaking users;
breaking change is an explicit, recorded decision.

## 6. Release Discipline

A surface version is released through the governed process — reviewed, validated, authorized —
and recorded in the platform change log. A release carries the same acceptance and safety gates
as any consequential change.

## 7. Version and Safety

No platform version, compatibility mode, or release path may weaken the safety guarantees
(DR-015). The DR-015 guarantees hold across every surface version, without exception.

## 8. Long-Term Versioning

Over the long horizon, the version strategy keeps the growing family of surfaces **legible**:
surfaces evolve at their own pace against a Core whose versions they check, so a surface written
years ago can still reason about what it depends on. Versioning is the long-term guarantee that
additive surface growth stays coherent.

---

*End of Chapter 17 — Version Strategy. This chapter completes the Governance block (Chapters
08–17) of the GoldBot Platform Constitution v1.0 edition.*
