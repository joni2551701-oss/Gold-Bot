# GoldBot Constitution — Chapter 02: Mission

**Package:** GB-CONST-002 · **Document:** Chapter02_Mission.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition, GB-CONST-001 … GB-CONST-040)
**Continuity:** This chapter follows and reuses the terminology established in
Chapter 01 (Vision, GB-CONST-001) and does not contradict it. It extends the
in-force governance in [`docs/constitution/CONSTITUTION.md`](../CONSTITUTION.md)
rather than replacing it.

---

## Executive Summary

Where Chapter 01 fixed the *vision* — what GoldBot aspires to be — Chapter 02
defines the **mission**: the concrete, ongoing obligation the system undertakes
in service of that vision. The mission translates aspiration into
responsibility. It states what GoldBot commits to deliver to its user, and it
assigns clear, bounded responsibilities to each part of the system: the Core, the
advisory intelligence, and the platform surfaces.

The mission is deliberately narrow and durable. GoldBot commits to producing
disciplined, auditable XAUUSD trading intelligence for a human decision-maker,
through a stable and platform-independent Core reached only through a single
governed gateway, with advisory intelligence that never executes. This chapter
makes that commitment explicit, divides the duties required to honor it, and
defines the metrics by which the mission is judged over time.

## Table of Contents (Chapter 02)

1. Mission Statement
2. Primary Mission
3. User Commitment
4. Core Responsibilities
5. AI Responsibilities
6. Platform Responsibilities
7. Long-Term Mission
8. Mission Success Metrics

---

## 1. Mission Statement

GoldBot's mission is to **deliver disciplined, auditable, and safe XAUUSD
trading intelligence to a human decision-maker**, through a stable
platform-independent Core that every client reaches only through a single
governed gateway, and through advisory intelligence that informs but never acts.

The mission is the standing obligation that gives the vision effect. The vision
describes the system GoldBot intends to be; the mission describes what GoldBot
must do, continuously, to be that system.

## 2. Primary Mission

The primary mission has three inseparable parts, each carried forward from the
strategic objectives of Chapter 01:

1. **Produce quality intelligence.** Generate trading signals and analysis for
   XAUUSD whose value lies in their discipline, consistency, and traceability —
   not in volume or novelty.
2. **Protect the user by construction.** Ensure, through the architecture itself,
   that risk controls are never bypassed and that no component converts advice
   into unauthorized action.
3. **Preserve the foundation.** Deliver new capability as additions on top of the
   Core, so that the system grows without eroding the boundaries that make it
   trustworthy.

These parts are ranked in the sense that no delivery of intelligence justifies
weakening protection or foundation. Where they conflict, safety and foundation
prevail — the same ordering established in Chapter 01's Success Definition.

## 3. User Commitment

To the human decision-maker it serves, GoldBot commits that:

- **The user remains in control.** GoldBot is semi-automatic; the human stays in
  the loop for consequential action. GoldBot informs the decision; it does not
  remove the decision.
- **The user is protected structurally.** Protection does not depend on careful
  operation alone; it is enforced by what the system is architecturally unable to
  do — namely, execute on its own or bypass its risk controls.
- **The user can trust what they are shown.** Signals and analysis are produced by
  a defined, auditable path, so the information the user acts on has a traceable
  origin.
- **The user's system remains stable over time.** Because growth is additive, the
  behavior the user relies on today is not silently changed by tomorrow's
  additions.

This commitment is the human-facing expression of the mission: every
responsibility that follows exists to keep it.

## 4. Core Responsibilities

The Core is the interior of the system — its market data, memory, event, replay,
snapshot, and gateway foundations. Its responsibilities are:

- **Own the truth of market data and state.** The Core is the single authority for
  market data and system state; surfaces consume this, never own a private copy.
- **Remain platform-independent.** The Core carries no client-, presentation-, or
  transport-specific logic, so new surfaces are added without changing it.
- **Expose itself only through the gateway.** All access to Core services is
  through the single governed entry point; the Core presents no second door.
- **Guarantee integrity and recoverability.** State is durable and verifiable, so
  the system can be restored to a known-good condition.
- **Hold no client logic and no surface concerns.** Interface and platform matters
  are explicitly outside the Core's responsibility.

The Core's overriding duty is stability: its contracts must hold across versions
so that everything built on it is protected from its internal evolution.

## 5. AI Responsibilities

The advisory intelligence layer — including the personal AI surfaces — carries a
strictly bounded responsibility, unchanged from the future-proof principles of
Chapter 01:

- **Advise only.** The AI layer produces analysis and recommendations as input to
  a decision; it never approves, rejects, sizes, sends, or executes a trade.
- **Never touch the controls.** The AI layer does not call the risk controls, does
  not trigger delivery or execution, and cannot become a path around them.
- **Remain provider-agnostic.** The specific AI provider may change without
  changing the Core or the contracts around the advisory layer.
- **Be auditable.** Advisory output follows a defined path, so its role in any
  decision is traceable.

This boundary is not a limitation to be relaxed later; it is a permanent
guarantee. "AI remains advisory only" is a fixed term of the mission.

## 6. Platform Responsibilities

The platform surfaces — Telegram, Web, Mobile, and future clients — are the
system's perimeter. Their responsibilities are:

- **Present, do not decide.** Platforms render information and collect user intent;
  they do not hold trading logic and do not make trading decisions.
- **Reach the Core only through the gateway.** No surface imports or calls a Core
  service directly; all access is through the single governed entry point.
- **Respect platform independence.** Each surface adapts the shared, platform-
  neutral model to its own presentation; it never pushes platform-specific
  assumptions back into the Core.
- **Declare their capabilities honestly.** Each surface states which capabilities
  it supports, and where it does not, the reason — so the ecosystem's true state
  is always visible.

Platforms may grow numerous and diverse; their common responsibility is to remain
thin, governed consumers of the Core rather than parallel centers of logic.

## 7. Long-Term Mission

Over the long horizon defined in Chapter 01, the mission holds that GoldBot must:

- **Keep the same commitments across every version.** The user commitment, the
  advisory-only guarantee, and the never-bypass-risk guarantee do not weaken as
  the system evolves.
- **Grow by work packages, not rewrites.** Each new capability is delivered on top
  of the gateway under the same governed lifecycle, preserving the Core.
- **Absorb change at the edges.** New providers, transports, and platforms are
  accommodated at the perimeter without disturbing the interior.
- **Remain auditable at scale.** As surfaces multiply, the traceability of
  decisions and changes is maintained, not diluted.

The long-term mission is therefore one of constancy under growth: the system does
more over time while owing the user exactly the same things it owes today.

## 8. Mission Success Metrics

The mission is measured — consistent with Chapter 01's Success Definition — by
whether these conditions hold over time:

- **Boundary integrity.** Every client reached the Core only through the gateway;
  no trading logic entered the gateway and no path bypassed the risk controls.
- **Advisory integrity.** Across the system's history, the AI layer never executed,
  approved, rejected, sized, or sent a trade.
- **Core stability.** The Core's public contracts held across versions; no surface
  was broken by the Core's internal evolution.
- **Additive growth.** New capability arrived as work packages on top of the Core,
  and the founding documents required amendment only rarely.
- **Auditability.** Any consequential decision or change could be traced to a
  recorded rationale, review, and approval.
- **User protection.** The user remained in control of consequential action, and
  the structural protections were never circumvented.

These are not one-time acceptance checks but continuing measures. The mission is
successful for exactly as long as they remain true.

---

*End of Chapter 02 — Mission. Subsequent chapters (GB-CONST-003 onward) continue
under the same enterprise documentation standard and terminology.*
