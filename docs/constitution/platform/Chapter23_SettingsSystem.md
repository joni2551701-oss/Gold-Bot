# GoldBot Platform Constitution — Chapter 23: Settings System

**Package:** GB-PLATFORM-CONST-023 · **Document:** Chapter23_SettingsSystem.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 23 describes the **settings system** — how the Platform layer holds a user's preferences
and presentation choices. Settings personalize the experience; they never change Core logic, risk
controls, or the safety guarantees. This chapter states the settings model and its boundary.

## Table of Contents (Chapter 23)

1. Settings Statement
2. What Settings Cover
3. Scope of Settings
4. Consistency Across Surfaces
5. Defaults and Validation
6. The Settings Boundary
7. Auditability
8. Evolution

---

## 1. Settings Statement

The settings system holds a user's **preferences and presentation choices** across surfaces, so
the experience is personalized and consistent. Settings are a platform concern; they carry no
trading logic and no authority over the Core.

## 2. What Settings Cover

Settings cover **presentation and platform behavior** — display preferences, notification
choices (Chapter 22), language, and similar. They do not cover trading parameters, risk
thresholds, or any Core logic, which are governed solely in the Core.

## 3. Scope of Settings

Settings are scoped per user (and, where relevant, per surface). A user's settings follow them
across surfaces for a consistent experience, consistent with user management (Chapter 19) and the
one-model principle (Chapter 04).

## 4. Consistency Across Surfaces

A setting defined once is honored **consistently** wherever it applies. Surfaces express the same
preference in their own idiom, so the user does not reconfigure the same choice per client.

## 5. Defaults and Validation

Settings have safe **defaults** and are **validated** before they take effect, so an invalid or
missing setting never produces undefined behavior. Defaults favor clarity and safety.

## 6. The Settings Boundary

Settings personalize; they **never** change trading behavior, risk controls, or the safety
guarantees (DR-015). No setting may bypass the Risk Manager, place trading logic in a surface, or
alter Core logic. A setting adjusts presentation, not protection.

## 7. Auditability

Consequential settings changes are recorded where they matter for audit, consistent with the
Constitution's requirements, so the state a user experiences has a traceable basis.

## 8. Evolution

The settings system evolves by adding preferences and validation behind stable platform
contracts, across more surfaces, without ever crossing into Core logic or weakening a protection.

---

*End of Chapter 23 — Settings System.*
