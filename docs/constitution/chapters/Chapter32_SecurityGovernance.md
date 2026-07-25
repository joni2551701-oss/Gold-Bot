# GoldBot Constitution — Chapter 32: Security Governance

**Package:** GB-CONST-032 · **Document:** Chapter32_SecurityGovernance.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–31; does not contradict any approved chapter.
**Operative sources:** [`docs/SECURITY.md`](../../SECURITY.md), [`docs/policies/SECURITY_POLICY.md`](../../policies/SECURITY_POLICY.md).

---

## Executive Summary

Chapter 32 states **security governance** — how GoldBot controls who may reach the
Core and how sensitive material is protected. Security in GoldBot is enforced
primarily at the gateway boundary, where authentication and authorization govern
access, and it is reinforced by disciplined handling of secrets and least
privilege. This chapter states the governance; the operative security documents
hold the detail.

## Table of Contents (Chapter 32)

1. Security Statement
2. Security at the Gateway Boundary
3. Authentication and Authorization
4. Secrets Handling
5. Least Privilege
6. Auditability
7. Security and Safety
8. Security Evolution

---

## 1. Security Statement

Security governs **who may reach the Core and what they may do**, and protects the
sensitive material the system holds. It is a structural property enforced at the
system's boundaries, not an afterthought applied at the edges.

## 2. Security at the Gateway Boundary

The gateway is the primary place security is enforced, because it is the single
entry point (Chapter 19). Authenticating and authorizing at one governed boundary —
rather than at many scattered points — is what makes access control consistent and
auditable across the whole system.

## 3. Authentication and Authorization

Access is governed in two steps: authentication establishes who is calling, and
authorization determines what they may reach. Both are identity and access
decisions only; neither carries trading authority. A caller reaches a capability
only when both checks pass.

## 4. Secrets Handling

Secrets are handled through the Core's dedicated secret management and never appear
in documentation, code comments, logs, or change requests. Sensitive material is
kept out of the audit trail and out of any artifact that could expose it, by rule.

## 5. Least Privilege

Access is granted at the least level required. A caller, surface, or service
receives only the capability it needs, so the reach of any single component is
bounded. Least privilege limits the impact of error or compromise.

## 6. Auditability

Security-relevant access and decisions are auditable through the correlated request
context and the audit trail (Chapters 15, 35). Who reached what, and under what
authorization, remains traceable — security governance is verifiable, not merely
asserted.

## 7. Security and Safety

Security governance reinforces Trading Safety: no authenticated or authorized path
may bypass the risk controls or grant the advisory intelligence a route to act.
Access control governs reach; it never dissolves the safety boundaries the
Constitution protects.

## 8. Security Evolution

Security governance evolves by strengthening the boundary — new authentication and
authorization backends, tighter controls — behind stable interfaces, without
weakening the guarantees it protects. As surfaces multiply, access stays governed at
one boundary rather than fragmenting.

---

*End of Chapter 32 — Security Governance.*
