# GoldBot Platform Constitution — Chapter 33: Analytics

**Package:** GB-PLATFORM-CONST-033 · **Document:** Chapter33_Analytics.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`analytics/`](../../../analytics/), [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md).

---

## Executive Summary

Chapter 33 describes **analytics** — how the Platform layer measures usage and product health.
Analytics observe and report; they inform product decisions and never drive trading. This chapter
states the analytics model, its privacy discipline, and the boundary that keeps analytics
observational.

## Table of Contents (Chapter 33)

1. Analytics Statement
2. What Analytics Measure
3. Observation, Not Action
4. Privacy and Aggregation
5. Analytics and Product Decisions
6. The Analytics Boundary
7. Integrity of Measurement
8. Evolution

---

## 1. Analytics Statement

Analytics **measure platform usage and product health** — how surfaces are used, where the
experience succeeds or fails — to inform product decisions. Analytics observe; they do not act.

## 2. What Analytics Measure

Analytics measure platform-side facts: engagement, feature use, delivery success, and error rates.
They read already-known events; they do not measure or influence the Core's trading logic, and they
never fabricate a metric.

## 3. Observation, Not Action

Analytics are **observational**. They produce measurements and reports for humans and product
governance; they never make or trigger a decision, and they have no path to trading action. An
analytic result informs a decision; it is not one.

## 4. Privacy and Aggregation

Analytics follow **privacy and least data**: they prefer aggregated, minimized data, protect
sensitive material, and never expose it in reports, logs, documentation, or change requests
(GoldBot Constitution, Security Governance). User data used for analytics is governed like all user
data.

## 5. Analytics and Product Decisions

Analytics feed the product decision process (Chapters 09, 15) as **input**. The Product Director
and team use analytics to inform direction; analytics do not set direction themselves, and they
never justify weakening a boundary.

## 6. The Analytics Boundary

Analytics observe the platform; they hold **no** trading logic, drive **no** trading decision, and
provide **no** path around the risk controls (DR-015). Nothing measured by analytics may become a
trigger for trading action.

## 7. Integrity of Measurement

Analytics measurements are honest: they report what was observed, without fabrication or distortion,
so product decisions rest on real signals (consistent with the Constitution's monitoring
discipline).

## 8. Evolution

Analytics evolve by adding measurements and reports behind stable platform contracts and the privacy
discipline, without ever crossing from observation into action or into the Core's trading logic.

---

*End of Chapter 33 — Analytics.*
