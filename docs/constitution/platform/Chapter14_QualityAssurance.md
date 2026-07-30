# GoldBot Platform Constitution — Chapter 14: Quality Assurance

**Package:** GB-PLATFORM-CONST-014 · **Document:** Chapter14_QualityAssurance.md · **Status:** Approved — GoldBot Platform Constitution v1.0 (Frozen Baseline, DPR-008)
**Part of:** GoldBot Platform Constitution v1.0 (chaptered edition) · **Block:** Governance (08–17)
**Subordination:** Subordinate to and consistent with the GoldBot Constitution v1.0 (DR-013);
governs the Platform layer only; never weakens the non-amendable safety guarantees (DR-015).
**Operative sources:** [`docs/policies/TESTING_POLICY.md`](../../policies/TESTING_POLICY.md), [`docs/standards/TEST_STANDARD.md`](../../standards/TEST_STANDARD.md), [`CLAUDE.md`](../../../CLAUDE.md).

---

## Executive Summary

Chapter 14 defines **quality assurance for the Platform layer** — the discipline that makes
correctness a condition of delivering a surface. Platform QA applies the same gates as the
GoldBot Constitution: validation before commit, tests for new behavior, and an authoritative CI
result before any work is done. This chapter states the platform-scoped QA.

## Table of Contents (Chapter 14)

1. Quality Statement
2. Quality Gates
3. Testing Discipline
4. Validation Protocol
5. Continuous Integration Authority
6. Definition of Done
7. Quality and Safety
8. Continuous Quality

---

## 1. Quality Statement

The Platform layer treats **correctness as a precondition of delivery**. A surface change is
complete when it has passed the defined quality gates and its automated confirmation exists —
not because it appears to work.

## 2. Quality Gates

Every surface change passes ordered gates: static analysis clean, code compiles, tests pass,
and the system's behavior is unchanged where it should be. A gate that fails stops the change;
gates are not skipped for speed.

## 3. Testing Discipline

New surface behavior ships with tests, written for the area changed, run against exactly the
state that will be committed, and kept deterministic (GoldBot Constitution, Quality Assurance).
A behavior change without a test is incomplete.

## 4. Validation Protocol

Validation follows the fixed order — stage, run the checks, re-stage after any fix, keep the
tree clean, review the staged change, commit — so that what is tested is what is committed.

## 5. Continuous Integration Authority

The continuous-integration result is the authority on whether a platform change is sound in the
shared environment. A change is not reported complete until CI reports success for the exact
commit; local success alone is insufficient.

## 6. Definition of Done

A platform change is **done** when it is merged through the governed process with a passing CI
result and the required authorization, its acceptance recorded, its tree clean, and no boundary
or safety regression introduced.

## 7. Quality and Safety

Platform QA treats the DR-015 safety guarantees as quality invariants: a surface change that
would weaken them fails QA regardless of its other merits. Preserving no-trading-logic and
gateway-only access is part of "quality."

## 8. Continuous Quality

Quality is maintained continuously across every surface: standards, tests, and the CI gate
apply to each platform alike, so quality does not degrade as surfaces multiply; known gaps are
tracked and retired through the technical-debt workflow.

---

*End of Chapter 14 — Quality Assurance.*
