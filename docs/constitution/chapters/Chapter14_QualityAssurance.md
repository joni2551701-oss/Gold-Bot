# GoldBot Constitution — Chapter 14: Quality Assurance

**Package:** GB-CONST-014 · **Document:** Chapter14_QualityAssurance.md · **Status:** Draft (pending Director review)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Governance (Chapters 08–17)
**Continuity:** Reuses the terminology of Chapters 01–13; does not contradict any approved chapter.
**Operative sources:** [`docs/policies/TESTING_POLICY.md`](../../policies/TESTING_POLICY.md), [`docs/standards/TEST_STANDARD.md`](../../standards/TEST_STANDARD.md), [`CLAUDE.md`](../../../CLAUDE.md) (commit protocol).

---

## Executive Summary

Chapter 14 defines **quality assurance** — the discipline that makes correctness a
condition of delivery rather than an aspiration. Quality in GoldBot is enforced by
gates: validation before commit, tests for new behavior, and an authoritative
continuous-integration result before any work is called done. This chapter states
the quality philosophy and its gates; the operative testing rules live in the
referenced sources.

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

GoldBot treats **correctness as a precondition of delivery**. Work is not
considered complete because it appears to work; it is complete when it has passed
the defined quality gates and its automated confirmation exists.

## 2. Quality Gates

Every change passes ordered gates: static analysis is clean, the code compiles, the
tests pass, and the system's smoke behavior is unchanged where it should be. A gate
that fails stops the change; gates are not skipped for speed.

## 3. Testing Discipline

New behavior ships with tests. Tests are written for the area changed, run against
exactly the state that will be committed, and kept deterministic. A change to
behavior without a corresponding test is incomplete by this standard.

## 4. Validation Protocol

Validation follows a fixed order so that what is tested is what is committed: stage
first, then run the checks; if a fix changes anything, re-stage before continuing;
keep the working tree clean; review the staged change; then commit. This order
exists specifically to prevent a validated state from diverging from the committed
one.

## 5. Continuous Integration Authority

The continuous-integration result is the authority on whether a change is sound in
the shared environment. A change is not reported as complete until integration
reports success for the exact commit in question; local success alone is not
sufficient.

## 6. Definition of Done

A change is **done** when it is merged through the governed process with a passing
integration result and the required authorization, its acceptance recorded, its
working tree clean, and no boundary or safety regression introduced. Anything short
of this is in progress, not done.

## 7. Quality and Safety

Quality assurance and Trading Safety reinforce each other. The safety guarantees —
risk controls never bypassed, advisory intelligence never executing — are treated
as quality invariants that every change must preserve, and a change that would
weaken them fails quality assurance regardless of its other merits.

## 8. Continuous Quality

Quality is maintained continuously, not audited once. Standards, tests, and the
integration gate apply to every work package alike, so quality does not degrade as
the ecosystem grows; managed technical debt and recorded lessons keep known gaps
visible and retired through a defined workflow.

---

*End of Chapter 14 — Quality Assurance.*
