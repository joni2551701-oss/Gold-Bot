# GoldBot Platform Constitution — Chapter 12: Product Team

**Package:** GB-PLATFORM-CONST-012 · **Document:** Chapter12_ProductTeam.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Governance (08–17)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative source:** [`CLAUDE.md`](../../../CLAUDE.md) (Worker execution rules), [`docs/policies/DEVELOPMENT_POLICY.md`](../../policies/DEVELOPMENT_POLICY.md).

---

## Executive Summary

Chapter 12 defines the **Product Team** — the role that executes platform direction, turning it
into delivered surfaces. The team builds correctly and stays within its bounds: it does not
authorize its own scope or merges, never resolves a consequential ambiguity in silence, and
never adds trading logic to a surface. It executes under the same discipline as the GoldBot
Worker role.

## Table of Contents (Chapter 12)

1. Role Statement
2. Responsibilities
3. Execution Discipline
4. No Silent Decisions
5. Reuse and Boundaries
6. Reporting
7. Limits of the Role
8. Accountability

---

## 1. Role Statement

The Product Team **executes platform direction**. Given an authorized platform task, the team
designs, documents, implements, tests, and delivers it under the standards, and returns it for
review.

## 2. Responsibilities

The team understands the task and its context before changing anything; follows
architecture-first and documentation-first order; produces tests for new behavior; validates
the work; and reports honestly. It owns the correctness and completeness of what it delivers.

## 3. Execution Discipline

The team follows the mandatory execution discipline (GoldBot Constitution, Quality Assurance;
`CLAUDE.md`): stage, run the static/compile/test checks, re-stage after any fix, keep the tree
clean, review the staged change, commit, push, and confirm CI before reporting done.

## 4. No Silent Decisions

A consequential choice the team cannot resolve from the brief is **escalated** — to the Product
Director, and where it touches Core or safety, to the GoldBot Director — not made quietly. The
team surfaces assumptions, alternatives, and open questions.

## 5. Reuse and Boundaries

Before creating a new platform component, the team applies the reuse audit and records the
justification. It keeps every boundary: no trading logic in a surface, no direct Core access,
no path around the risk controls, and it reuses the shared model rather than forking it.

## 6. Reporting

The team reports what was actually done — which checks passed, what was skipped, what changed
and why — and does not describe a change as complete before its automated confirmation exists
(GoldBot Constitution reporting language).

## 7. Limits of the Role

The team **does not** set its own scope, authorize its own merges, or move the platform scope
boundary; those are Product-Director prerogatives. It executes within the authorized task and
escalates anything beyond it, especially anything touching Core or safety.

## 8. Accountability

The Product Team is accountable for the integrity of its execution — the discipline, the
boundaries, and the reporting standard. Because its commits, validations, and reports are
recorded, its work remains part of the audit trail.

---

*End of Chapter 12 — Product Team.*
