# GoldBot Constitution — Chapter 04: Core Principles

**Package:** GB-CONST-004 · **Document:** Chapter04_CorePrinciples.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition, GB-CONST-001 … GB-CONST-040)
**Continuity:** Follows and reuses the terminology of Chapters 01–03; does not
contradict any approved chapter. Extends the in-force
[`docs/constitution/CONSTITUTION.md`](../CONSTITUTION.md).

---

## Executive Summary

Chapter 04 states the **core principles** — the eight standing rules that govern
every engineering and architectural decision in GoldBot. Where the values
(Chapter 03) express convictions, the principles express operating rules: they
are the concrete tests a proposal must pass. Each principle is durable, and each
is applied to every work package regardless of the surface it belongs to.

## Table of Contents (Chapter 04)

1. Foundation First
2. Gateway First
3. Platform Independence
4. Knowledge First
5. Documentation First
6. Reuse Before Create
7. Safety First
8. Evolution Without Revolution

---

## 1. Foundation First

The foundation is built carefully once and thereafter extended, not rewritten.
The Core — market data, memory, event, replay, snapshot, and gateway — is
long-lived infrastructure whose stability is protected before any feature. A
recurring need to rewrite the foundation is treated as a governance failure, not
a normal event.

## 2. Gateway First

The gateway is the single governed entry point into the Core. Every client —
chart, artificial intelligence, platform, media, or any future surface — reaches
Core services only through it. No second entry point is introduced, and no
surface calls a Core service directly. The gateway routes and governs; it never
contains trading logic.

## 3. Platform Independence

The Core makes no assumption about who is calling. It carries no client-,
presentation-, or transport-specific logic. New platforms are added at the
perimeter without changing the Core, and platform-specific assumptions are never
pushed back into it. Platform independence is what allows the ecosystem to grow
without disturbing the interior.

## 4. Knowledge First

Domain and trading knowledge is a Core-owned, versioned, auditable resource,
exposed through the gateway and consumed by surfaces — never embedded as a
private copy inside a surface. Decisions and intelligence are grounded in this
shared knowledge, so the system reasons from one consistent source rather than
many divergent ones.

## 5. Documentation First

Architecture and intent are written before code and kept current. A change is
designed and documented before it is implemented, and reviewed before it is
merged. Documentation is a first-class artifact of every work package, not an
afterthought, so the system remains understandable over its whole life.

## 6. Reuse Before Create

Before any new component — a file, a package, or a top-level function or class —
three questions are answered in order: does this already exist; can an existing
module be extended without breaking its contract; and only if both are "no", a
new component is created and its justification recorded. Reuse is the default
outcome; creation is the exception that must be argued.

## 7. Safety First

The protections owed to the user are structural and permanent. Risk controls are
never bypassed, and the advisory intelligence never approves, rejects, sizes,
sends, or executes a trade. Live execution is never an ambient capability; any
movement toward it is a separate, explicitly authorized decision. Safety
outranks every other principle when they conflict.

## 8. Evolution Without Revolution

The system evolves by addition on top of the gateway, under a governed lifecycle,
not by upheaval of the Core. New capability arrives as work packages; the
governing documents are amended rarely and extended routinely. Change is absorbed
at the edges so that the interior — and the guarantees it carries — remains
constant.

---

*End of Chapter 04 — Core Principles.*
