# GoldBot Platform Constitution — Chapter 36: Risk and Abuse Prevention

**Package:** GB-PLATFORM-CONST-036 · **Document:** Chapter36_RiskAndAbusePrevention.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Domain (28–37)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never overrides Core governance; never weakens the
non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md), [`docs/SECURITY.md`](../../SECURITY.md).
**Critical distinction:** "Risk" in this chapter means **platform risk** — abuse, fraud, spam, and
misuse of the platform. It is **entirely distinct from** the Core **Risk Manager** (trading risk).
This chapter defines, alters, and touches **no** trading-risk logic, threshold, or formula; the
Core Risk Manager is governed solely under Trading Safety and the GoldBot Constitution's Risk
Governance chapter, and is never modified here.

---

## Executive Summary

Chapter 36 describes **platform risk and abuse prevention** — how the Platform layer protects
itself and its users from misuse, fraud, spam, and abuse. This is a **platform-security** concern
and must not be confused with the Core Risk Manager, which governs *trading* risk. The two are
separate systems with separate purposes; this chapter governs the platform one and never touches
the trading one.

## Table of Contents (Chapter 36)

1. Statement and Distinction
2. Platform Risks Addressed
3. Abuse Prevention
4. Fraud and Payment Abuse
5. Rate and Access Controls
6. Relationship to the Core Risk Manager
7. The Prevention Boundary
8. Evolution

---

## 1. Statement and Distinction

Platform risk and abuse prevention protects the **platform and its users** from misuse. It is
distinct from the Core **Risk Manager**: the Risk Manager governs *trading* risk inside the Core
under Trading Safety; this chapter governs *platform* risk (abuse, fraud, spam) at the surface
layer. The two never merge, and this chapter never modifies the Risk Manager.

## 2. Platform Risks Addressed

The platform risks addressed include: account compromise and misuse, spam and unwanted content,
automated abuse of surfaces, fraudulent payments (Chapter 30), and attempts to gain unauthorized
access or entitlements. These are threats to the platform, not to trading logic.

## 3. Abuse Prevention

The Platform layer prevents abuse through governed controls: detecting and limiting misuse of
surfaces, protecting users from unwanted or harmful content (within the broadcast and notification
governance), and responding to abusive behavior under administration (Chapter 32) and audit.

## 4. Fraud and Payment Abuse

Payment and entitlement fraud is prevented through the payment integrity and security discipline
(Chapters 30, 34): payments are verified, entitlements follow only from valid payment states, and
suspected fraud is handled under governance. Fraud prevention protects access integrity, not
trading.

## 5. Rate and Access Controls

The Platform layer applies **rate and access controls** — through the gateway's rate limiting and
the platform's own governed limits — to prevent automated abuse and protect availability. These
controls govern request volume and access, never trading behavior.

## 6. Relationship to the Core Risk Manager

The Core **Risk Manager** is untouched by this chapter. Platform risk and abuse prevention neither
calls, modifies, bypasses, nor substitutes for the Risk Manager. A trading signal still reaches a
user only after the Core has cleared it through the Risk Manager (Chapter 31); platform abuse
prevention operates only on platform-side misuse, entirely separate from that clearance.

## 7. The Prevention Boundary

Platform risk and abuse prevention holds **no** trading logic and provides **no** path around the
Core's protections (DR-015). It may restrict or protect platform access; it may never weaken the
trading-risk controls, deliver an un-cleared signal, or grant trading authority. Its power is
confined to the platform side of the safety boundary.

## 8. Evolution

Platform abuse prevention evolves by adding detection and response capability behind stable platform
contracts, under audit, without ever crossing into the Core Risk Manager or the trading-safety
boundary.

---

*End of Chapter 36 — Risk and Abuse Prevention.*
