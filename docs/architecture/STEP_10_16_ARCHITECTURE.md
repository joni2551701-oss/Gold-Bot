# STEP-10 → STEP-16 — Architecture Specification (Master Index)

> **Status: SPECIFICATION / DOCUMENTATION ONLY.** No code is written by
> this document. It defines, file-by-file, how each remaining layer of
> the GoldBot Core (STEP-10 … STEP-16) is to be built when its own
> TASK-CORE spec is later approved. Every layer below follows the same
> **reuse-first / additive-parallel** discipline already established by
> STEP-08 (`signals/`) and STEP-09 (`decision/`): the live, FROZEN
> trading path is never modified; new work lands as new files that
> *reuse* the frozen contracts, or as additive extensions of existing
> modules — never as a rewrite.

## 1. Where these steps sit in the whole pipeline

```
 config → data/providers → stream → market → context → strategies → signals(STEP-08)
                                                                        │  CanonicalSignal
                                                                        ▼
                                                            decision (STEP-09)
                                                                        │  DecisionOutcome
                                                        ┌───────────────┴───────────────┐
                                                        │ status == APPROVE              │ any status
                                                        ▼                                ▼
                                                  risk (STEP-10)                 database (STEP-12)
                                                        │  RiskOutcome                   ▲   (record every outcome)
                                                        ▼                                │
                                                 execution (STEP-11)                     │
                                                        │  (inert / manual today)        │
                                                        ▼                                │
                                            platform (STEP-15) ──────────────────────────┘
                                                        │  PlatformMessage
                                        ┌───────────────┼───────────────┐
                                        ▼               ▼               ▼
                                   telegram        (mobile)        (mini-app / desktop)
                                   (STEP-13)        future           future
                                        ▲
                                        │  advisory only (never executes)
                                   ai (STEP-14) ── reads: context + signals + decision + database
                                        ▲
                                        │  observes every stage (read-only)
                                   monitoring (STEP-16)
```

**Reading the diagram**
- The **vertical spine** (data → … → signals → decision → risk → execution
  → platform → telegram) is the trade path. Every arrow is one-directional
  and never skips a layer.
- **`database/` (STEP-12)** is a side consumer: every `DecisionOutcome` and
  `RiskOutcome` is *recorded*, regardless of verdict. It is written to, never
  read back into the trade path mid-flight.
- **`ai/` (STEP-14)** is advisory input only. It reads context/signals/
  decision/database and feeds the *decision* layer's blend — it never calls
  risk, execution, or a platform send (CLAUDE.md Trading Safety).
- **`monitoring/` (STEP-16)** is a pure observer: it reads counters/events
  from every stage and never writes back into the trade path.

## 2. The one contract that threads all seven steps

STEP-09 produces the **`DecisionOutcome`** (`decision/decision_model.py`):
`status ∈ {APPROVE, REJECT, HOLD, EXPIRE}` + `signal_id/symbol/direction/
confidence/reasons/rules_applied/metadata`. Everything downstream keys off
it:

| Consumer | Reads | Acts only on |
|---|---|---|
| risk (STEP-10) | `DecisionOutcome` | `APPROVE` |
| execution (STEP-11) | `RiskOutcome` | `approved == True` (inert today) |
| database (STEP-12) | `DecisionOutcome`, `RiskOutcome` | every outcome |
| telegram (STEP-13) | `PlatformMessage` | every user-eligible outcome |
| ai (STEP-14) | decision inputs/outputs | nothing — advisory |
| platform (STEP-15) | `RiskOutcome` + presentation | every deliverable outcome |
| monitoring (STEP-16) | events/counters | nothing — observes |

`decision/decision_router.py` already encodes this fan-out: `RISK` is routed
only for `APPROVE`; `DATABASE`/`AI`/`MONITORING`/`TELEGRAM` are always routed.
STEP-10…16 are the concrete consumers of that route list.

## 3. Per-step specifications (file-by-file)

Each step has its own spec doc with: purpose, position in flow, input/output,
a **file-by-file table** (role · input · output · reads-from · passes-to ·
new-or-extend), the list of **existing files to extend**, boundary/Trading-
Safety guarantees, and a **detailed flow diagram**.

| STEP | Layer | Spec | Package status | Dominant action |
|---|---|---|---|---|
| STEP-10 | `risk/` | [steps/STEP_10_RISK.md](steps/STEP_10_RISK.md) | exists, FROZEN core | **Reuse** `RiskManager.evaluate` via an additive gateway |
| STEP-11 | `execution/` | [steps/STEP_11_EXECUTION.md](steps/STEP_11_EXECUTION.md) | exists, inert | **Keep inert**; additive status/model contracts only |
| STEP-12 | `database/` | [steps/STEP_12_DATABASE.md](steps/STEP_12_DATABASE.md) | exists, mature | **New repos** on the existing `*_models`/`*_repository` convention |
| STEP-13 | `telegram/` | [steps/STEP_13_TELEGRAM.md](steps/STEP_13_TELEGRAM.md) | exists, mature | **Extend** formatter/notify/reply-menu; add current-price header |
| STEP-14 | `ai/` | [steps/STEP_14_AI.md](steps/STEP_14_AI.md) | exists, mature | **Reuse** `AIAnalyzerInterface`; advisory-only, no execution |
| STEP-15 | `platform/` | [steps/STEP_15_PLATFORM.md](steps/STEP_15_PLATFORM.md) | **does not exist** | **New top-level package** (highest-cost — needs explicit approval) |
| STEP-16 | `monitoring/` | [steps/STEP_16_MONITORING.md](steps/STEP_16_MONITORING.md) | exists, mature | **Extend** existing monitors; observer-only |

## 4. Cross-cutting rules (apply to every step)

1. **FROZEN never edited.** `risk/risk_manager.py` (geometry/sizing),
   `decision/decision_engine.py` (blend + thresholds),
   `strategies/`, `signals/` core, and the `core/pipeline.py` live flow are
   untouched by any of these steps. Reuse their verdicts; don't reimplement.
2. **One layer down only.** Each layer imports the layer immediately below
   it, never two down. Handlers → service → repository in `telegram/`; no
   direct DB from handlers.
3. **Module Reuse Principle order** (CLAUDE.md): (1) does it exist? →
   (2) can an existing module be extended? → (3) only then a new module,
   with a docstring justifying why (1) and (2) were both "no". A **new
   top-level package** (only STEP-15 `platform/`) is the highest cost and
   requires explicit Director approval before any code.
4. **Additive-parallel naming.** When a new orchestrator would collide with
   a frozen one, it takes a sibling name — as `decision_manager.py` sits
   beside the frozen `decision_engine.py`, and `signals/manager.py` beside
   `signal_engine.py`. STEP-10 uses the same rule (`risk_gateway.py` beside
   the frozen `risk_manager.py`).
5. **Fail-safe, duck-typed inputs.** Cross-layer inputs are read via
   `getattr`, so a None/partial upstream object yields a defined outcome,
   never a raise (matches `strategies.result.from_signal_candidate` and the
   STEP-09 rules style).
6. **Trading Safety boundary.** Risk Manager is never bypassed; AI never
   executes; secrets are read only by `config.py`/`core/secrets.py` and are
   never logged.
7. **Every step ships:** a reuse audit, the code, `tests/<layer>/…`, a
   `docs/…FREEZE.md`, and passes the full Commit Protocol before it is
   called done — same as STEP-08/09.

## 5. Build order & dependencies

```
STEP-10 risk ─────────────┐
                          ├─► STEP-12 database (persists both outcomes)
STEP-11 execution ────────┘
STEP-10 risk ─► STEP-15 platform ─► STEP-13 telegram
STEP-14 ai   ─► feeds decision (STEP-09), read by STEP-13 presentation
STEP-16 monitoring ─► observes STEP-10..15 (built last / incrementally)
```

Recommended sequence: **10 → 12 → 15 → 13 → 11 → 14 → 16.** Risk first (it
gates everything user-facing), database next (so outcomes are recorded),
platform + telegram to make outcomes visible, execution/ai/monitoring last
(execution stays inert; ai is advisory; monitoring wraps the finished chain).

> Each `TASK-CORE-0NN` spec will still be issued and approved individually.
> This document is the map; the per-step docs are the blueprints.
