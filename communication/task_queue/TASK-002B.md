# TASK-002B

**Title**: Navigation Architecture
**Status**: In Progress — Director-authorized. Architecture only: no
implementation, code, or API is written. 002C (Registry) does not
start until this Architecture is approved.

## Objective

Design (not implement) Universal Navigation, Screen Model, Navigation
Graph, Route Registry, Back Stack, Deep Link System, Permission Layer,
Platform Adapter, Navigation State, Session Navigation, Navigation
Events, Screen Lifecycle, and Platform Capability Mapping — each with
a stated compatibility (per Constitution Article 13) across Telegram
Bot, Telegram Mini App, Android, iOS, Desktop. Governed by ADR-001
(Shared Platform Layer, five equal clients) and the Universal UI
Abstraction rule (`docs/PLATFORM_WORKFLOW.md`).

Deliverable: `docs/NAVIGATION_ARCHITECTURE.md`, ending with a
"Director Questions" section per `docs/PLATFORM_WORKFLOW.md`.

## Depends on

TASK-002A (Navigation Analysis) — Approved.
