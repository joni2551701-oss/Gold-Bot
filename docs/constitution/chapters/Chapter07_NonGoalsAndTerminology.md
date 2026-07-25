# GoldBot Constitution — Chapter 07: Non-Goals and Terminology

**Package:** GB-CONST-007 · **Document:** Chapter07_NonGoalsAndTerminology.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition, GB-CONST-001 … GB-CONST-040)
**Continuity:** Follows and reuses the terminology of Chapters 01–06; does not
contradict any approved chapter. Extends the in-force
[`docs/constitution/CONSTITUTION.md`](../CONSTITUTION.md).

---

## Executive Summary

Chapter 07 closes the foundational block of the Constitution by fixing two things
that keep every later chapter consistent: the system's **non-goals** — what
GoldBot deliberately will not become — and its **terminology** — the definitions
of the reserved terms already used throughout Chapters 01–06. This chapter is the
Constitution's glossary of record: where an earlier chapter uses a term, this
chapter defines it, so the whole document speaks one language.

## Table of Contents (Chapter 07)

1. Non-Goals
2. Glossary
3. Definitions
4. Reserved Terms
5. Architecture Terms
6. AI Terms
7. Platform Terms
8. Naming Rules

---

## 1. Non-Goals

GoldBot deliberately does **not** aim to be, at any point in the horizon of this
Constitution:

- A **fully autonomous trader** — the human remains in the loop for consequential
  action.
- A **live-execution engine by default** — placing real orders is never an ambient
  capability; it is a separate, explicitly authorized decision.
- A **multi-asset platform** in the current era — the focus is XAUUSD.
- A system with **client logic in the Core** — presentation and platform concerns
  belong to surfaces.
- A system with a **second entry point** — nothing reaches the Core outside the
  gateway.
- A project that **favors feature speed over foundation integrity** — where they
  conflict, the foundation prevails.

Non-goals are binding: a proposal that moves the system toward a non-goal is out
of scope unless the boundary is formally, explicitly moved by a recorded decision.

## 2. Glossary

The glossary lists the reserved terms of the Constitution. Sections 3–7 define
them by category. A term written in these documents carries exactly its glossary
meaning; it is not used loosely or redefined locally.

## 3. Definitions

Foundational definitions used across all chapters:

- **GoldBot** — the semi-automatic XAUUSD trading-intelligence system governed by
  this Constitution.
- **Semi-automatic** — the property that GoldBot produces intelligence and
  recommendations while a human remains responsible for consequential action.
- **Trading Safety** — the permanent, structural guarantees that risk controls are
  never bypassed and that advisory intelligence never executes.
- **Work Package** — a governed unit of new capability, delivered on top of the
  gateway through architecture, documentation, implementation, testing, review,
  and acceptance.
- **Audit Trail** — the maintained record of decisions, reviews, and changes that
  makes consequential actions traceable.
- **Foundation** — the long-lived Core infrastructure that is built once and
  extended, not rewritten.

## 4. Reserved Terms

The following are reserved: they always carry their defined meaning and are not
repurposed.

- **Core** — the platform-independent interior of the system (Section 5).
- **Gateway** — the single governed entry point (Section 5).
- **Surface** — a governed client of the Core (Section 7).
- **Advisory** — the bounded role of the AI layer (Section 6).
- **In Scope / Out of Scope** — as defined in Chapter 06.
- **Boundary** — a defining property of the system, not a temporary constraint.

## 5. Architecture Terms

- **Core** — the interior authority for market data and system state
  (market-data, memory, event, replay, snapshot, and gateway foundations). Holds
  no client or presentation logic.
- **Gateway** — the single governed entry point into the Core. Routes and governs
  access; contains no trading logic; introduces no second door.
- **Platform Independence** — the property that the Core carries no client-,
  presentation-, or transport-specific logic.
- **Layer** — a level in the pipeline that talks only to the level immediately
  below it; layers are not skipped or reversed.
- **Transport-Agnostic** — the property that how a request travels (in-process, or
  later a network protocol) is an edge concern and does not affect Core contracts.
- **Versioned Compatibility** — the practice by which the Core and gateway announce
  versions so surfaces can check compatibility before relying on them.

## 6. AI Terms

- **Advisory (AI) Layer** — the intelligence component that produces analysis and
  recommendations as **input only**. It never approves, rejects, sizes, sends, or
  executes a trade, and never touches the controls.
- **Provider-Agnostic** — the property that the specific AI provider may change
  without changing the Core or the contracts around the advisory layer.
- **Advisory Boundary** — the permanent limit that keeps the AI layer advisory; it
  does not weaken over any version or surface.
- **Knowledge** — the Core-owned, versioned, auditable domain and trading
  knowledge that surfaces consume and the advisory layer reasons from.

## 7. Platform Terms

- **Surface** — a governed client of the Core (for example a chart, platform, or
  media client) that consumes Core services only through the gateway and holds no
  trading logic.
- **Platform** — a specific surface family such as Telegram, Web, or Mobile,
  adapting the shared platform-neutral model to its own presentation.
- **Capability Declaration** — a surface's honest statement of which capabilities
  it supports and, where it does not, the reason.
- **Perimeter** — the outer region of the system where surfaces live and where
  change is absorbed without disturbing the Core.

## 8. Naming Rules

To keep terminology consistent across GB-CONST-001 … GB-CONST-040:

- **Use reserved terms exactly.** A reserved term is used only with its glossary
  meaning; it is not redefined in a later chapter.
- **Introduce new terms deliberately.** A genuinely new term is added to this
  glossary (by amendment) rather than used ad hoc.
- **Prefer the established word.** Where a concept already has a reserved term, that
  term is used rather than a synonym, to avoid drift.
- **One meaning per term.** A term carries a single meaning across the whole
  Constitution; overloading is not permitted.
- **Definitions live here.** New or changed definitions are recorded in this
  chapter, which is the terminology source of truth for the chaptered edition.

---

*End of Chapter 07 — Non-Goals and Terminology. This chapter completes the
foundational block (Chapters 01–07) of the GoldBot Constitution v1.0 edition.*
