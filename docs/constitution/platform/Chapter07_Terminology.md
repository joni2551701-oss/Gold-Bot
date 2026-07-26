# GoldBot Platform Constitution — Chapter 07: Terminology

**Package:** GB-PLATFORM-CONST-007 · **Document:** Chapter07_Terminology.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, PLATFORM-DCR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Foundation (01–07)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 07 fixes the **terminology of the Platform layer** — the reserved terms used across
the Platform Constitution. It **inherits** the GoldBot Constitution's glossary of record (its
Terminology chapter) for all shared terms (Core, Gateway, Surface, Advisory, Trading Safety,
Work Package) and defines only the platform-specific terms here. Where a term is defined in
the GoldBot Constitution, that definition governs.

## Table of Contents (Chapter 07)

1. Terminology Statement
2. Inherited Terms
3. Platform Terms
4. Surface and Client Terms
5. Model and Adapter Terms
6. Capability Terms
7. Reserved Terms
8. Naming Rules

---

## 1. Terminology Statement

The Platform Constitution uses terms with **exactly** their defined meaning. Shared terms are
inherited from the GoldBot Constitution's glossary; platform-specific terms are defined in
this chapter, which is the terminology source of truth for the Platform edition.

## 2. Inherited Terms

The following are used with the meaning fixed by the GoldBot Constitution and are **not**
redefined here: **Core**, **Gateway**, **Surface**, **Advisory (AI) Layer**, **Trading
Safety**, **Work Package**, **Capability Declaration**, **Platform Independence**. For these,
the GoldBot Constitution is the source of truth (DR-016).

## 3. Platform Terms

- **Platform layer** — the family of client surfaces through which users reach GoldBot.
- **Platform Constitution** — this edition; the platform-scoped governance subordinate to the
  GoldBot Constitution.
- **Platform** — a specific surface family (for example Telegram, Web, or Mobile).

## 4. Surface and Client Terms

- **Surface** — a governed client of the Core (inherited term); in the Platform layer, a
  concrete presentation such as the Telegram bot or a Web client.
- **Client** — an instance of a platform through which a user interacts.
- **Perimeter** — the outer region where surfaces live and where change is absorbed without
  disturbing the Core.

## 5. Model and Adapter Terms

- **Shared (platform-neutral) model** — the single definition of navigation, menus, and
  capabilities expressed across all surfaces.
- **Platform Adapter** — the component that turns the shared model into a specific platform's
  real presentation; it touches presentation only, never business logic.
- **Navigation model** — the platform-agnostic navigation structure consumed by surfaces.

## 6. Capability Terms

- **Capability** — a supported function a surface may express.
- **Capability Declaration** — a surface's honest statement of which capabilities it supports
  and, where not, the reason (inherited from the GoldBot Constitution).
- **Supported / Not Supported (+ reason)** — the declared status of a capability on a surface.

## 7. Reserved Terms

The terms above are reserved: they carry one meaning across the Platform Constitution and are
not repurposed. A reserved term inherited from the GoldBot Constitution keeps that
constitution's meaning; a platform-specific reserved term keeps the meaning defined here.

## 8. Naming Rules

- **Use reserved terms exactly**, with their defined meaning.
- **Inherit before defining** — if the GoldBot Constitution already defines a term, use it;
  do not redefine it here.
- **Introduce new platform terms deliberately** — add them to this chapter, not ad hoc.
- **One meaning per term** across the Platform Constitution.
- **Definitions live here** for platform-specific terms; shared definitions live in the
  GoldBot Constitution.

---

*End of Chapter 07 — Terminology (Platform Constitution). This chapter completes the
Foundation block (Chapters 01–07) of the GoldBot Platform Constitution v1.0 edition.*
