# GoldBot Constitution — Chapter 28: AI Architecture

**Package:** GB-CONST-028 · **Document:** Chapter28_AIArchitecture.md · **Status:** Approved — GoldBot Constitution v1.0 (Frozen Baseline, DR-013 and DR-014)
**Part of:** GoldBot Constitution v1.0 (chaptered edition) · **Block:** Domain (Chapters 28–37)
**Continuity:** Reuses the terminology of Chapters 01–27; does not contradict any approved chapter.
**Operative sources:** [`docs/AI_ARCHITECTURE.md`](../../AI_ARCHITECTURE.md), [`ai/interfaces.py`](../../../ai/interfaces.py), [`contracts/ai_contract.md`](../../../contracts/ai_contract.md).

---

## Executive Summary

Chapter 28 opens the domain block by describing the **AI architecture** — how the
advisory intelligence is positioned in GoldBot. The defining property is bounded
influence: the AI layer produces analysis and recommendations as input to a
decision, and it has no architectural path to act. This chapter states that
position, its provider independence, and its grounding in shared knowledge; the
detailed interface lives in the operative sources.

## Table of Contents (Chapter 28)

1. AI Statement
2. The Advisory Role
3. Position in the System
4. Provider-Agnostic Design
5. Knowledge Grounding
6. Integration Through the Gateway
7. The AI Boundary
8. AI Evolution

---

## 1. AI Statement

The AI layer is **advisory intelligence**: it produces analysis and recommendations
that inform a decision, and nothing more. Its architecture is shaped so that its
value is the quality of its input, never authority over an outcome.

## 2. The Advisory Role

The advisory role is fixed (Chapters 02, 07): the AI layer never approves, rejects,
sizes, sends, or executes a trade, and it never touches the risk controls. It
advises the decision; it does not make it. This role is a permanent term of the
Constitution, not a phase.

## 3. Position in the System

Architecturally, the AI layer sits as **input to the decision process**, not as an
actor within it. It receives context and produces advice; a separate, governed path
decides what, if anything, is done. Because the AI layer has no route to execution,
its influence cannot exceed advice.

## 4. Provider-Agnostic Design

The AI layer is designed so the specific provider can change without changing the
Core or the contracts around it (Chapter 25). Provider selection, fallback, and
health are provider concerns behind a stable advisory interface, keeping the system
independent of any single intelligence source.

## 5. Knowledge Grounding

The advisory layer reasons from **shared, Core-owned knowledge** (Chapter 04,
Knowledge First) rather than isolated assumptions. Grounding advice in one
consistent, versioned knowledge source keeps the intelligence coherent with the
rest of the system.

## 6. Integration Through the Gateway

Consumers of advisory intelligence reach it as governed capability through the
gateway (Chapter 26), like any other Core capability. The AI layer does not become a
side channel: its inputs and outputs flow through the same governed boundary as the
rest of the Core.

## 7. The AI Boundary

The AI boundary is absolute: the AI layer is advisory input to the decision process
only. It never itself approves or rejects a trade, never calls the risk controls,
and never triggers a delivery or an execution action. This boundary applies to any
present or future provider (Chapter 07, Trading Safety).

## 8. AI Evolution

The AI layer evolves by improving advice quality and adding providers behind the
advisory interface, without ever gaining authority to act. Better intelligence is
welcome; a wider boundary is not. The advisory limit holds across every version and
every provider.

---

*End of Chapter 28 — AI Architecture.*
