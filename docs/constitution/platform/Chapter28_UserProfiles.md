# GoldBot Platform Constitution — Chapter 28: User Profiles

**Package:** GB-PLATFORM-CONST-028 · **Document:** Chapter28_UserProfiles.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never overrides Core governance; never weakens the
non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md).

---

## Executive Summary

Chapter 28 opens the Platform domain block by describing **user profiles** — the durable,
per-user information the Platform layer holds to personalize the experience. Profiles extend user
management (Chapter 19) with lasting attributes; they are a platform concern, governed for privacy
and least data, and they hold no trading logic and no Core authority.

## Table of Contents (Chapter 28)

1. Profile Statement
2. Profile Contents
3. Ownership and Consistency
4. Privacy and Least Data
5. User Control
6. The Profile Boundary
7. Auditability
8. Evolution

---

## 1. Profile Statement

A user profile is the **durable per-user information** the Platform layer holds to personalize
GoldBot for that user across surfaces. It records who the user is to the platform and their
lasting preferences and entitlements.

## 2. Profile Contents

A profile holds platform-relevant attributes: identity references, preferences (Chapter 23),
entitlements (Chapters 21, 29), and notification choices (Chapter 22). It does **not** hold
trading parameters, risk settings, or Core state — those live in the Core.

## 3. Ownership and Consistency

A profile follows the user **consistently across surfaces**, so the experience and entitlements
are coherent wherever the user interacts (Chapter 04). The Platform layer owns profile
presentation data; authoritative Core state remains in the Core.

## 4. Privacy and Least Data

Profiles follow **least data**: only what a surface needs is held, and sensitive material is
protected under the security governance and never exposed in logs, documentation, or change
requests (GoldBot Constitution, Security Governance).

## 5. User Control

Users can view and control their profile information within governance. Changes are validated and,
where consequential, recorded, so a user's profile reflects their intent and has a traceable
basis.

## 6. The Profile Boundary

Profiles personalize; they **never** hold trading logic, alter Core behavior, or provide a route
around the risk controls (DR-015). A profile attribute governs presentation and access, not
trading.

## 7. Auditability

Consequential profile changes are recorded where they matter for audit, so the personalized state
a user experiences remains traceable, consistent with the Constitution's requirements.

## 8. Evolution

Profiles evolve by adding attributes and controls behind stable platform contracts, across more
surfaces, without crossing into Core logic or weakening a protection.

---

*End of Chapter 28 — User Profiles.*
