# TASK-002B

**Title**: Navigation Architecture
**Status**: Delivered, awaiting Director review — see
`docs/NAVIGATION_ARCHITECTURE.md`. Architecture only: no
implementation, code, or API was written. 002C (Registry) does not
start until this Architecture is approved, and six Director Questions
in the document itself need answers first.

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
