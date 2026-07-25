# GoldBot Constitution — Chapter 35: Operational Model

**Package:** GB-CONST-035 · **Document:** Chapter35_OperationalModel.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–34; does not contradict any approved chapter.
**Operative sources:** [`monitoring/`](../../../monitoring/), [`deploy/`](../../../deploy/), [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md).

---

## Executive Summary

Chapter 35 states the **operational model** — how GoldBot is run, observed, and kept
healthy in production. Operations rest on the Core lifecycle (Chapter 27): readiness
is signaled, health and metrics are observed, activity is logged with correlation,
and recovery restores a known-good state. This chapter states the operational
principles; the operative monitoring and deployment sources hold the detail.

## Table of Contents (Chapter 35)

1. Operational Statement
2. Readiness and Health
3. Monitoring and Metrics
4. Logging and Correlation
5. Recovery and Backup
6. Deployment
7. Operations and Safety
8. Operational Evolution

---

## 1. Operational Statement

GoldBot is operated to be **observable, healthy, and recoverable**. The operational
model makes the system's real state visible and its recovery reliable, so it can be
run with confidence rather than guesswork.

## 2. Readiness and Health

The system signals readiness before it serves and reports health as an honest
classification of known facts (Chapters 14, 27). Health is graded from observed
conditions, never fabricated, and the gateway exposes it so the system's state can
be read at any time.

## 3. Monitoring and Metrics

Operations observe the system through monitoring and metrics — including the
gateway's own request metrics — that read already-known facts. Monitoring reports
what is, without inventing a grade, so operational decisions rest on real signals.

## 4. Logging and Correlation

Activity is logged through the Core's logging, and the request context's identifiers
(request and correlation ids) are the standard key that ties a request's log lines
together (Chapter 19). Correlated logging makes operational investigation and audit
tractable.

## 5. Recovery and Backup

The system recovers to a known-good state through the persistence and snapshot
layers (Chapters 20, 23), preferring verified state over corrupt recent state.
Backup and recovery are operational guarantees, so state loss is survivable rather
than catastrophic.

## 6. Deployment

Deployment follows the governed release discipline (Chapter 17): a running version
is reviewed, validated, and authorized, and its version is announced so consumers
can check compatibility. Deployment is a governed event, not an informal one.

## 7. Operations and Safety

Operations never weaken Trading Safety. No operational action, configuration, or
recovery path may bypass the risk controls or grant the advisory intelligence a
route to act. The safety guarantees hold in every operational state — starting,
serving, degraded, or recovering.

## 8. Operational Evolution

The operational model evolves by adding observability and recovery capability behind
the same principles — richer health, metrics, and recovery — without weakening the
guarantees. As the ecosystem grows, the system stays observable and recoverable at
one governed boundary.

---

*End of Chapter 35 — Operational Model.*
