# STEP-11 — `execution/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the execution step. No code here.
> `execution/` is **intentionally inert**: GoldBot is a semi-automatic
> signal bot — the trader places orders manually. Wiring a real order call
> is itself a change requiring explicit approval (CLAUDE.md Trading Safety).

## 1. Purpose

Define *where* a future automated order path would attach, and keep it a
**no-op contract** today. STEP-11 records an execution *intent/status* for a
risk-approved signal (for the trader and for analytics) — it does **not**
place, modify, or close any live order.

**Does (today):** produce a defined "execution intent" object; return
"not implemented" from any live-order call. **Does NOT:** connect to MT5/a
broker, hold funds, or bypass the trader's manual action.

## 2. Position in the flow

```
risk/ (STEP-10)  RiskOutcome(approved=True)
        │
        ▼
execution/execution_status.py   ── builds an ExecutionIntent (PENDING_MANUAL)
        │
        ├─► execution/execution_engine.py (FROZEN INERT)   → "not implemented"
        ├─► execution/signal_lifecycle.py (FROZEN INERT)   → "not implemented"
        │
        ▼
   ExecutionIntent(status=PENDING_MANUAL)  ──► database (STEP-12)  + platform (STEP-15)

Separately, backtesting-only (unchanged, Phase 60.3):
   PaperTrade(OPEN) + RiskResult ──► execution/simulator/ ──► ExecutionSimulationResult
```

## 3. Input / Output

- **Input:** a `RiskOutcome` (approved) + the canonical signal.
- **Output:** `ExecutionIntent` — `status ∈ {PENDING_MANUAL, ACKNOWLEDGED,
  SKIPPED}`, `signal_id`, entry/SL/TP echoed for the trader, `note`. No order
  ticket, because no order is placed.

## 4. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `execution/execution_engine.py` | **FROZEN INERT** live-order stub | none | "not implemented" | — | — | **UNCHANGED** |
| `execution/signal_lifecycle.py` | **FROZEN INERT** order-lifecycle stub | none | "not implemented" | — | — | **UNCHANGED** |
| `execution/simulator/` | simulated fills for backtesting only | `PaperTrade`+`RiskResult` | `ExecutionSimulationResult` | lifecycle/risk | backtesting/analytics | **UNCHANGED** (Phase 60.3) |
| `execution/execution_status.py` | `ExecutionStatus` vocab + `ExecutionIntent` model (manual-mode, no order) | `RiskOutcome` | `ExecutionIntent` | risk_model | database/platform | **new** (records intent, calls no broker) |
| `execution/__init__.py` | export STEP-11 surface; restate inert boundary | — | — | — | — | **extend** |
| `execution/README.md` | append STEP-11 section | — | — | — | — | **extend** |

### Existing files to EXTEND
- `execution/__init__.py`, `execution/README.md` — docs/exports only.

### Existing files NEVER touched
- `execution_engine.py`, `signal_lifecycle.py` (inert), `simulator/` (Phase
  60.3 backtesting logic).

## 5. Boundary & Trading-Safety guarantees
- No MT5/broker client, no order call, no funds, no I/O to a market.
- `ExecutionIntent` is a *record of what the trader should do manually*, not
  an instruction to the platform.
- Turning any of this into a real order path is a separate, explicitly-
  approved change — documented as an open item in `docs/AUDIT_REPORT.md`.

## 6. Detailed flow

```
RiskOutcome(approved) ──► execution_status.build_intent(risk_outcome, signal)
   │  status = PENDING_MANUAL  (never auto-executes)
   ▼
ExecutionIntent ──► database (STEP-12: record)  +  platform (STEP-15: show trader the plan)
                    execution_engine / signal_lifecycle stay "not implemented"
```
