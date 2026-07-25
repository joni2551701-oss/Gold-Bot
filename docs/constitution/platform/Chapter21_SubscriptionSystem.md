# GoldBot Platform Constitution — Chapter 21: Subscription System

**Package:** GB-PLATFORM-CONST-021 · **Document:** Chapter21_SubscriptionSystem.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md), [`platforms/`](../../../platforms/).

---

## Executive Summary

Chapter 21 describes the **subscription system** — how the Platform layer governs a user's
entitlements to features. Subscriptions decide **what a user may access**, never how trading
works. This chapter states the subscription model and the boundary that keeps entitlements a
matter of access, not of trading authority or safety.

## Table of Contents (Chapter 21)

1. Subscription Statement
2. Entitlements
3. Tiers and Access
4. Enforcement Through Authorization
5. Billing and Lifecycle
6. The Subscription Boundary
7. Fairness and Transparency
8. Evolution

---

## 1. Subscription Statement

The subscription system governs a user's **entitlements** — which platform features and Core
capabilities they may access. It is a platform access concern; it holds no trading logic and
grants no trading authority.

## 2. Entitlements

An **entitlement** is a grant of access to a feature or capability. Subscriptions map a user to
a set of entitlements, which authorization then enforces (Chapter 20). Entitlements describe
access, not behavior of the Core.

## 3. Tiers and Access

Subscriptions may define **tiers** that bundle entitlements. Tiers change what a user can access
and how a surface presents features to them; they never change the Core's logic, the risk
controls, or the safety guarantees.

## 4. Enforcement Through Authorization

Entitlements are **enforced through authorization** at the gateway boundary (Chapter 20). A user
reaches a gated capability only when their entitlements permit it; the subscription system does
not create a separate access path or bypass the gateway.

## 5. Billing and Lifecycle

A subscription has a lifecycle — created, active, changed, lapsed — governed as a platform
concern with an auditable record. Billing and payment handling follow the security governance
(sensitive material protected, never exposed in logs, docs, or change requests).

## 6. The Subscription Boundary

Subscriptions govern **access only**. No entitlement, tier, or subscription state may bypass the
Risk Manager, place trading logic in a surface, or grant the advisory intelligence a route to
act (DR-015). A higher tier grants more access, never different trading behavior or weaker
safety.

## 7. Fairness and Transparency

Entitlements and tiers are presented **transparently**, so a user understands what their
subscription grants. Honest capability declaration (Chapter 04) applies: what a tier does and
does not include is clear.

## 8. Evolution

The subscription system evolves by adding entitlements, tiers, and lifecycle capability behind
stable platform contracts, without changing the Core or weakening a protection. New commercial
models are added at the perimeter, under governance.

---

*End of Chapter 21 — Subscription System.*
