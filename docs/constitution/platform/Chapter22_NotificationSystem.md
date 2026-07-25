# GoldBot Platform Constitution — Chapter 22: Notification System

**Package:** GB-PLATFORM-CONST-022 · **Document:** Chapter22_NotificationSystem.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Architecture (18–27)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/policies/BROADCAST_POLICY.md`](../../policies/BROADCAST_POLICY.md), [`docs/PLATFORM_ARCHITECTURE.md`](../../PLATFORM_ARCHITECTURE.md).

---

## Executive Summary

Chapter 22 describes the **notification system** — how the Platform layer delivers information to
users across surfaces. Its defining rule is that notifications **present** what the Core has
already produced and cleared; they never originate a trading signal or deliver one that has not
passed the Core's governed pipeline. This chapter states that model and its boundary.

## Table of Contents (Chapter 22)

1. Notification Statement
2. What May Be Notified
3. Delivery Across Surfaces
4. User Control and Preferences
5. Governed Content
6. The Notification Boundary
7. Auditability
8. Evolution

---

## 1. Notification Statement

The notification system **delivers information to users** — updates, alerts, and, where
applicable, trading signals the Core has already produced and cleared. It presents; it does not
decide, originate, or clear anything itself.

## 2. What May Be Notified

Notifications carry information originating in the Core and delivered through the gateway. A
trading signal that reaches a user by notification has **already passed the Core's governed
pipeline, including the Risk Manager** — the notification system only presents what was cleared,
never a signal that bypassed evaluation (Trading Safety, DR-015).

## 3. Delivery Across Surfaces

Notifications are delivered consistently across surfaces (Telegram, Web, Mobile, …), each surface
rendering the notification in its own idiom from the shared model. A capability defined once is
delivered recognizably everywhere (Chapter 04).

## 4. User Control and Preferences

Users control what notifications they receive, within governance. Notification preferences are
part of user management (Chapter 19); the system respects them and does not deliver beyond what a
user has permitted.

## 5. Governed Content

Notification content is governed by the operative broadcast policy — what may be sent, and how.
Because notifications are outward-facing, they follow the Constitution's confirmation and audit
expectations for outward-facing actions (GoldBot Constitution, Decision Process).

## 6. The Notification Boundary

The notification system presents and delivers; it holds **no** trading logic, originates **no**
trading decision, and provides **no** path around the Risk Manager. It cannot turn an
un-evaluated signal into a user-facing one — a notification is a view of a cleared Core outcome,
never a shortcut around clearance.

## 7. Auditability

Notification delivery is auditable: what was sent, to whom, and on what basis remains traceable
through the audit trail, consistent with the Constitution's requirements.

## 8. Evolution

The notification system evolves by adding channels, formats, and preference controls behind
stable platform contracts, without ever loosening the rule that it only presents cleared Core
output. New delivery capability never becomes a new origination path.

---

*End of Chapter 22 — Notification System.*
