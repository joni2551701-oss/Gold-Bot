# GoldBot Platform Constitution — Chapter 06: Scope

**Package:** GB-PLATFORM-CONST-006 · **Document:** Chapter06_Scope.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Foundation (01–07)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 06 defines the **scope of the Platform layer** — what the layer is responsible for,
what it deliberately excludes, and the rules by which its boundary may move. A clear platform
scope keeps surfaces thin and the Core protected.

## Table of Contents (Chapter 06)

1. In Scope
2. Out of Scope
3. Current Scope
4. Future Scope
5. Responsibilities
6. Boundaries
7. Constraints
8. Expansion Rules

---

## 1. In Scope

The Platform layer is responsible for:

- **Client surfaces** (Telegram, Web, Mobile, and future clients) presenting GoldBot.
- **The shared platform-neutral model** and each surface's adaptation of it.
- **Presentation and intent collection** across surfaces.
- **Honest capability declaration** per surface.
- **Gateway-mediated consumption** of Core capability.

## 2. Out of Scope

The Platform layer deliberately excludes:

- **Trading logic** of any kind (Strategy, Decision, Signal, Risk) — it lives in the Core.
- **Direct Core access** — all access is through the gateway.
- **Core data ownership or state authority** — the Core owns these.
- **Any path around the risk controls** — none exists at the surface.
- **A second entry point** to the Core.

## 3. Current Scope

The present scope centers on the platform **foundation** — the shared model, the platform
registry and capability model, and the existing Telegram surface — as the base future
surfaces build on (GoldBot Constitution, Platform Architecture chapter; `platforms/`).

## 4. Future Scope

Future scope grows by **adding governed surfaces** — Web, Mobile, and further clients — on
the shared model, through the gateway. Future scope never grows by adding trading logic to a
surface or by expanding the Core to accommodate a platform. A material change to scope is a
recorded, Director-level decision.

## 5. Responsibilities

- **Surfaces** present and collect; they hold no trading logic.
- **The shared model** defines capability once for all surfaces.
- **Adapters** express the model in each platform's real presentation.
- **Governance** keeps the scope honest through review and capability declaration.

## 6. Boundaries

- **The gateway boundary** — all Core access passes through it.
- **The no-trading-logic boundary** — surfaces never hold or bypass trading decisions.
- **The platform-independence boundary** — platform specifics never enter the Core.
- **The safety boundary** — the DR-015 guarantees hold on every surface, inviolably.

## 7. Constraints

- **No surface may weaken a boundary** for convenience or speed.
- **No surface may couple to the Core** except through the gateway.
- **No trading logic, risk control, or execution** is added to a platform.
- **No platform rule duplicates or contradicts** the GoldBot Constitution.

## 8. Expansion Rules

- **Addition, not alteration.** New scope enters as a governed surface on the shared model,
  never as Core change.
- **Reuse first.** New surfaces reuse the shared model and existing components before adding
  new ones.
- **Governed acceptance.** New scope passes design, documentation, review, and safety gates.
- **Recorded decision.** A move of the platform scope boundary is a recorded, Director-level
  decision.

---

*End of Chapter 06 — Scope (Platform Constitution).*
