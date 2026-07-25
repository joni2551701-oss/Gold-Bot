# GoldBot Constitution — Chapter 06: Scope

**Package:** GB-CONST-006 · **Document:** Chapter06_Scope.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition, GB-CONST-001 … GB-CONST-040)
**Continuity:** Follows and reuses the terminology of Chapters 01–05; does not
contradict any approved chapter. Extends the in-force
[`docs/constitution/CONSTITUTION.md`](../CONSTITUTION.md).

---

## Executive Summary

Chapter 06 defines **scope** — the boundary of what GoldBot is responsible for,
now and in the future. A clear scope protects the vision from dilution: it states
what belongs inside the system, what is deliberately excluded, and the rules by
which the boundary may move. Scope is expressed in the same terms as the earlier
chapters, so that "in scope" and "out of scope" carry the same meaning throughout
the Constitution.

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

GoldBot is responsible for:

- Producing **disciplined, auditable XAUUSD trading intelligence** for a human
  decision-maker.
- A **stable, platform-independent Core** owning market data and system state.
- A **single governed gateway** as the only entry point to the Core.
- **Governed surfaces** — chart, advisory intelligence, platform, and media — that
  consume the Core through the gateway.
- **Structural safety**: risk controls that cannot be bypassed and advisory
  intelligence that cannot execute.
- **Governance artifacts**: architecture, documentation, decisions, standards, and
  the audit trail.

## 2. Out of Scope

GoldBot deliberately excludes:

- **Full autonomy.** Removing the human from consequential action is out of scope.
- **Live market execution by default.** Placing real orders is not an ambient
  capability; it is a separate, explicitly authorized decision.
- **Multi-asset trading in the current era.** The focus is XAUUSD.
- **Client or presentation logic inside the Core.** These belong to surfaces.
- **Any second entry point** that would let a surface reach the Core outside the
  gateway.

## 3. Current Scope

The present scope centers on the completed Core Infrastructure and the governance
around it: market data, memory, event, replay, snapshot, and gateway foundations,
together with the standards and decision records that govern them. Surfaces exist
as foundations to be built upon under the growth model of Chapter 05.

## 4. Future Scope

Future scope grows by **adding governed surfaces and services on top of the
gateway** — deeper chart capability, richer advisory intelligence, more platform
clients, and media surfaces built on those. Future scope never grows by expanding
the Core's internals to accommodate a surface. Any material change to what is in
or out of scope is a recorded, Director-level decision.

## 5. Responsibilities

Scope assigns responsibility along the boundaries established in Chapter 02:

- **Core** owns data, state, integrity, and the gateway; it holds no surface logic.
- **Advisory intelligence** produces analysis as input only; it owns no decision.
- **Platforms** present information and collect intent; they hold no trading logic.
- **Governance** owns the standards, decisions, and audit trail that keep the scope
  honest.

## 6. Boundaries

The boundaries that define the scope are:

- **The gateway boundary** — all Core access passes through it; nothing goes around
  it.
- **The safety boundary** — risk controls are never bypassed; advisory intelligence
  never executes.
- **The platform boundary** — client logic stays in surfaces; the Core stays
  platform-independent.
- **The knowledge boundary** — shared knowledge is Core-owned and versioned;
  surfaces consume, they do not fork it.

A boundary is not a temporary constraint to be worked around; it is a defining
property of the system.

## 7. Constraints

The scope is held within these constraints:

- **No implementation may weaken a boundary** for the sake of speed or convenience.
- **No surface may couple to the Core** except through a governed gateway service.
- **No change to trading logic, risk controls, or execution** occurs without
  explicit, specific authorization.
- **No governance rule is duplicated**; each domain has a single source of truth.

## 8. Expansion Rules

The scope may expand only under these rules:

- **Addition, not alteration.** New scope enters as a work package on top of the
  gateway, never as a rewrite of the Core.
- **Reuse first.** New scope reuses existing components before introducing new
  ones, with any new component justified and recorded.
- **Governed acceptance.** New scope passes architecture, documentation, review,
  and safety gates before it is part of the system.
- **Recorded decision.** A move of the scope boundary is a recorded, Director-level
  decision, not an incidental result of feature work.

---

*End of Chapter 06 — Scope.*
