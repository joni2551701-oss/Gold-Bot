# GoldBot Constitution — Chapter 30: Platform Architecture

**Package:** GB-CONST-030 · **Document:** Chapter30_PlatformArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–29; does not contradict any approved chapter.
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 30 describes the **Platform architecture** — how GoldBot's client surfaces
(Telegram, Web, Mobile, and future clients) are organized around one shared,
platform-neutral model. Platforms present information and collect intent; they
consume the Core through the gateway and hold no trading logic. This chapter states
that structure and the boundary that keeps the Core platform-independent.

## Table of Contents (Chapter 30)

1. Platform Statement
2. One Platform Model
3. Surfaces and Clients
4. Capability Declaration
5. Consumption Through the Gateway
6. Core Platform Independence
7. The Platform Boundary
8. Platform Evolution

---

## 1. Platform Statement

A platform is a **client surface** of GoldBot. Platforms are the system's
perimeter: they render what the Core provides and collect what the user intends,
without holding the logic that belongs to the Core.

## 2. One Platform Model

All platforms share one platform-neutral model. Each specific platform adapts that
shared model to its own presentation rather than inventing its own structure, so a
capability defined once is expressed consistently across surfaces. This shared model
is what lets new platforms be added without bespoke rework.

## 3. Surfaces and Clients

The platform family includes the Telegram bot and future Web, Mobile, and desktop
clients. Each is a thin, governed consumer of the Core. Adding a platform is adding
a surface at the perimeter, not adding logic to the Core (Chapter 26).

## 4. Capability Declaration

Each platform declares, per capability, whether it supports it and — where it does
not — the reason. Honest capability declaration keeps the true state of the
ecosystem visible, so consumers and reviewers can see what each surface actually
offers.

## 5. Consumption Through the Gateway

Platforms reach the Core only through the gateway (Chapters 19, 26). A platform does
not import or call a Core component directly; it presents governed requests. This
keeps platform access authenticated, authorized, and auditable like any other.

## 6. Core Platform Independence

Because platforms consume the Core through a single governed boundary and adapt the
shared model themselves, the Core carries no platform-specific logic (Chapters 04,
09). Platform independence is preserved from the Core's side by never letting a
surface push its assumptions inward.

## 7. The Platform Boundary

Platforms present and collect; they do not decide. A platform holds no trading
logic, makes no trading decision, and provides no path around the risk controls.
Presentation and intent live at the perimeter; decisions live in the governed
pipeline (Chapters 02, 06).

## 8. Platform Evolution

Platforms evolve by **addition**: new surfaces are added on the shared model,
through the gateway, without changing the Core. The ecosystem of platforms can grow
for years while the Core it consumes stays constant — Evolution Without Revolution
(Chapter 04) at the perimeter.

---

*End of Chapter 30 — Platform Architecture.*
