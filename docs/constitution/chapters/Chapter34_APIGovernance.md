# GoldBot Constitution — Chapter 34: API Governance

**Package:** GB-CONST-034 · **Document:** Chapter34_APIGovernance.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–33; does not contradict any approved chapter.
**Operative source:** the Core Gateway Layer API model, `docs/CORE_GATEWAY_ARCHITECTURE.md` (canonical once the Gateway is merged at the Core-complete milestone).

---

## Executive Summary

Chapter 34 states **API governance** — how GoldBot governs the interface through
which the system is reached. The system has one API surface, the gateway, with an
internal face and an external face. This chapter states how that single API is
versioned, secured, and kept free of trading logic, so that consumers can depend on
it deliberately as it grows.

## Table of Contents (Chapter 34)

1. API Statement
2. One API Surface
3. Internal and External APIs
4. Versioning
5. Access Governance
6. Compatibility
7. The API Boundary
8. API Evolution

---

## 1. API Statement

GoldBot exposes **one governed API surface** — the gateway. All programmatic access
to the Core is through it, so there is a single, consistent, auditable interface
rather than many.

## 2. One API Surface

There is no second API. Because the gateway is the single entry point (Chapter 19),
it is also the single API surface: every caller reaches Core capability through the
same governed interface. This singularity is what keeps access uniform and
auditable.

## 3. Internal and External APIs

The one API presents two faces: an **internal** API by which Core modules reach one
another, and an **external** API by which platforms and external clients reach the
Core. Both run the same governed dispatch (Chapter 26); neither is a privileged
bypass.

## 4. Versioning

The API is versioned, and its version is announced so consumers can check
compatibility before relying on it (Chapter 17). A published API version is stable;
it is extended compatibly within a version and broken only by a new version,
deliberately and on the record.

## 5. Access Governance

Every API call passes the gateway's access governance — authentication,
authorization, and rate limiting — before it reaches a capability (Chapter 32). The
API is not a way around access control; it is where access control is applied.

## 6. Compatibility

API compatibility is checked, not assumed: a consumer verifies the versions it
depends on before relying on them, so the API and its consumers can evolve at
different speeds without breaking each other. Compatibility governance is what keeps
the ecosystem coherent as the API grows.

## 7. The API Boundary

The API carries capability, not trading logic. No API path places business logic in
the gateway, exposes a route around the risk controls, or introduces a second entry
point. The API is a governed door to capability, and nothing more.

## 8. API Evolution

The API evolves by compatible extension where possible and explicit new version
where necessary, always through the single governed surface. New capability appears
as new services discovered through the same API (Chapter 24), so the interface grows
by addition without fragmenting.

---

*End of Chapter 34 — API Governance.*
