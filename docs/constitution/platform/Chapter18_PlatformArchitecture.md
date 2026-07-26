# GoldBot Platform Constitution — Chapter 18: Platform Architecture

**Package:** GB-PLATFORM-CONST-018 · **Document:** Chapter18_PlatformArchitecture.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never overrides Core governance; never weakens the
non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`docs/PLATFORM_FOUNDATION.md`](../../PLATFORM_FOUNDATION.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 18 opens the Platform architecture block by describing the **Platform layer as a
whole** — the shared model, the surfaces that express it, the adapters that render it, and the
single gateway through which it reaches the Core. It is the map the later architecture chapters
(User Management, Auth, Subscription, Notification, Settings, Service, API Contracts,
Integration, Lifecycle) fit into.

## Table of Contents (Chapter 18)

1. Platform Architecture Statement
2. The Shared Model
3. Surfaces and Adapters
4. Gateway-Mediated Consumption
5. The Platform Boundary
6. Core Independence
7. Safety in the Platform Layer
8. Platform Evolution

---

## 1. Platform Architecture Statement

The Platform layer is architected as **one shared, platform-neutral model expressed by many
thin surfaces**, each reaching the Core only through the gateway. The model holds the
definition; surfaces hold the presentation; the Core holds the logic and authority.

## 2. The Shared Model

A single platform-neutral model defines navigation, menus, and capabilities once, for all
surfaces. The shared model is the source of platform structure, so a capability defined once is
expressed consistently across clients (Chapter 04).

## 3. Surfaces and Adapters

Each surface (Telegram, Web, Mobile, …) renders the shared model through a **platform adapter**
that touches presentation only. Adapters turn what the model defines into a platform's real UI;
they never hold business or trading logic (GoldBot Constitution, Platform Architecture chapter).

## 4. Gateway-Mediated Consumption

Every surface consumes Core capability **through the gateway** — authenticated, authorized,
rate-limited, and auditable. No surface imports or calls a Core component directly, and no
second entry point exists (Chapters 02, 04).

## 5. The Platform Boundary

The Platform layer presents and collects; it holds no Core data authority and no trading logic,
and it provides no route around the risk controls. The boundary between a thin surface and the
strong Core is the defining property of the architecture.

## 6. Core Independence

Because surfaces adapt the shared model themselves and reach the Core only through the gateway,
the Core carries no platform-specific logic. Platform independence is preserved from the
platform side by never pushing surface assumptions inward.

## 7. Safety in the Platform Layer

Safety is inherited and structural: the Platform layer offers no path that bypasses the Risk
Manager and no route by which the advisory intelligence could act (DR-015). Any trading signal a
surface presents has already passed the Core's governed pipeline; the surface only displays it.

## 8. Platform Evolution

The Platform layer evolves by **adding surfaces and capabilities on the shared model**, through
the gateway, without changing the Core. Growth is additive at the perimeter — Evolution Without
Revolution applied to the Platform layer.

---

*End of Chapter 18 — Platform Architecture.*
