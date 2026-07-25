# GoldBot Platform Constitution — Chapter 02: Mission

**Package:** GB-PLATFORM-CONST-002 · **Document:** Chapter02_Mission.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Foundation (01–07)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 02 states the **mission of the Platform layer** — the standing obligation it
undertakes in service of the vision. The Platform layer commits to delivering GoldBot's
capabilities to users across every client, through one shared model, over the gateway, with
no trading logic and no route around the Core's protections. This chapter states that
commitment and divides the responsibilities that keep it.

## Table of Contents (Chapter 02)

1. Mission Statement
2. Primary Mission
3. User Commitment
4. Platform Responsibilities
5. Relationship to the Core
6. Relationship to the Gateway
7. Long-Term Mission
8. Mission Success Metrics

---

## 1. Mission Statement

The Platform layer's mission is to **deliver GoldBot's intelligence to users across every
supported client**, through one platform-neutral model reached only via the gateway, while
holding no trading logic and preserving every Core protection.

## 2. Primary Mission

1. **Present faithfully.** Express the shared model as each client's real presentation,
   without distorting or deciding.
2. **Collect intent safely.** Gather user intent and pass it to the Core through the
   gateway, never acting on it independently.
3. **Preserve the boundaries.** Keep the gateway-only and no-trading-logic boundaries intact
   on every surface.

## 3. User Commitment

To the user, the Platform layer commits that: the experience is **consistent** across
surfaces; what is shown originates from the Core through a governed path; the user stays in
control of consequential action (the system remains semi-automatic); and the surface never
does anything the Core's protections would forbid.

## 4. Platform Responsibilities

- **Present, do not decide.** Render information and collect intent; hold no trading logic.
- **Reach the Core only through the gateway.** No direct Core access from any surface.
- **Declare capabilities honestly.** State what is supported and, where not, the reason.
- **Adapt to the shared model.** Express the one model; never push platform specifics into
  the Core.

## 5. Relationship to the Core

The Platform layer is a **consumer** of the Core, not an extension of it. It holds no Core
data, no Core state authority, and no trading logic. It consumes Core capability and returns
user intent, always through the gateway (GoldBot Constitution, Integration Architecture
chapter).

## 6. Relationship to the Gateway

The gateway is the Platform layer's **only** route to the Core. Every request a platform
makes is a governed gateway request — authenticated, authorized, and auditable. The Platform
layer never seeks a second route and never bypasses the gateway's governance.

## 7. Long-Term Mission

Over the long horizon, the Platform layer's mission holds constant as surfaces multiply: the
same commitments — consistency, gateway-only access, no trading logic, preserved safety —
apply to every new client. The layer grows in reach while owing the user exactly the same
things.

## 8. Mission Success Metrics

The mission succeeds when, over time: every surface reached the Core only through the
gateway; no platform held trading logic or bypassed the risk controls; capabilities were
expressed consistently across clients; new platforms were added on the shared model without
Core change; and the DR-015 safety guarantees remained intact on every surface.

---

*End of Chapter 02 — Mission (Platform Constitution).*
