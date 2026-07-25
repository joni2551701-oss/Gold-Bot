# GoldBot Constitution — Chapter 31: Media Architecture

**Package:** GB-CONST-031 · **Document:** Chapter31_MediaArchitecture.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–30; does not contradict any approved chapter.
**Operative sources:** [`media/`](../../../media/), [`docs/policies/BROADCAST_POLICY.md`](../../policies/BROADCAST_POLICY.md).

---

## Executive Summary

Chapter 31 describes the **Media architecture** — the surface that turns Core
output into shareable media (such as chart images and broadcasts) and distributes
it. Media is a consumer surface, built on the chart output and broadcast
capabilities, reaching the Core through the gateway. This chapter states that
structure and the boundary that keeps media a consumer, never a decision-maker.

## Table of Contents (Chapter 31)

1. Media Statement
2. Media as a Surface
3. Built on Chart and Broadcast
4. Consumption Through the Gateway
5. Content Governance
6. Distribution
7. The Media Boundary
8. Media Evolution

---

## 1. Media Statement

Media is a **consumer surface** that presents and distributes GoldBot's output in
shareable form. Like every surface, it consumes the Core rather than extending it.

## 2. Media as a Surface

Media sits at the perimeter alongside the platforms (Chapter 30). It renders and
distributes; it holds no trading logic and makes no trading decision. Its role is
presentation and distribution, not computation of what to present.

## 3. Built on Chart and Broadcast

Media is built on existing capabilities — chart output and the broadcast layer —
rather than on new Core internals (Chapter 04, Reuse Before Create). It composes
what already exists, so media capability grows without widening the Core.

## 4. Consumption Through the Gateway

Media reaches Core capability through the gateway (Chapter 26). It does not query the
Core directly; it consumes chart and broadcast outputs and Core capability through
the governed boundary, keeping its access auditable.

## 5. Content Governance

Media content is governed by the operative broadcast policy, which sets what may be
distributed and how. Governance keeps media honest and consistent with the rest of
the system, and it never turns distribution into a path around the Core's
boundaries.

## 6. Distribution

Media distributes to its channels under governance, carrying Core output outward. It
is an outward-facing surface, so its actions follow the confirmation and audit
expectations the Constitution places on outward-facing behavior (Chapter 15).

## 7. The Media Boundary

Media presents and distributes; it does not decide. It holds no trading logic,
provides no path around the risk controls, and consumes rather than owns the Core's
data and output. The boundary that applies to every surface applies to media.

## 8. Media Evolution

Media evolves by **addition** on top of existing surfaces and capabilities: new
formats and channels are added through the gateway and the broadcast layer, without
changing the Core. Media deepens the ecosystem rather than widening the foundation.

---

*End of Chapter 31 — Media Architecture.*
