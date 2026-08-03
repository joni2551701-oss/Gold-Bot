# STEP-10 — `risk/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the risk step. No code here.
> `risk_layer/risk_engine/risk_manager.py` is a **FROZEN Trading-Safety module** — its
> geometry validation and sizing formulas are never modified. STEP-10 is
> an **additive gateway** that *reuses* `RiskManager.evaluate()`.

## 1. Purpose

Turn an **APPROVE** `DecisionOutcome` (STEP-09) into a validated,
size-suggested **`RiskOutcome`** — the last gate before a signal becomes
user-facing. It validates SL/TP geometry and computes a *sizing suggestion*
only; it never sends a broker/MT5 order.

**Does:** geometry validation, stop-distance check, R:R, lot-size suggestion,
drawdown/daily-loss/duplicate gates. **Does NOT:** decide (STEP-09 already
did), send orders (STEP-11), format platform messages (STEP-13/15), read AI.

## 2. Position in the flow

```
decision/decision_router.route(outcome)   [RISK present only if APPROVE]
        │  DecisionOutcome(status=APPROVE) + CanonicalSignal + account_balance
        ▼
risk/risk_gateway.py  ── maps DecisionOutcome→RiskManager input, REUSES evaluate()
        │
        ├─► risk_layer/risk_engine/risk_manager.py (FROZEN)        geometry + sizing  → RiskResult
        ├─► risk_layer/risk_engine/account_state_tracker.py (exists) drawdown / daily-loss state
        ├─► risk_layer/risk_validator/duplicate_checker.py   (exists)  duplicate-trade gate
        ▼
   RiskOutcome(status, approved, lot_size, risk_amount, risk_reward, reasons)
        │
        ├─► database (STEP-12)     risk_decision_repository (record)
        └─► platform (STEP-15) → telegram (STEP-13)   (only if approved)
```

## 3. Input / Output

- **Input:** `DecisionOutcome` (APPROVE), the `CanonicalSignal`
  (`signal_layer.signal_builder.schema.SignalSchema`) it references, optional `account_balance`
  / account state.
- **Output:** `RiskOutcome` — reuses the frozen `RiskResult` fields
  (`approved`, `lot_size`, `risk_amount`, `risk_reward`, `reason`) plus a
  `RiskStatus` verdict and the originating `signal_id`.

## 4. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `risk_layer/risk_engine/risk_manager.py` | **FROZEN** geometry + sizing | `TradeDecision` + balance | `RiskResult` | decision models | gateway | **UNCHANGED** |
| `risk_layer/risk_engine/account_state_tracker.py` | drawdown/daily-loss state | account state | pass/pause | database (state) | gateway | reuse (extend only if a new counter is approved) |
| `risk_layer/risk_validator/duplicate_checker.py` | duplicate-trade gate | recent trades | allow/block | database | gateway | reuse |
| `risk/risk_status.py` | verdict vocab `APPROVED/REJECTED/PAUSED/BLOCKED` + mapping from `RiskResult` | `RiskResult` | `RiskStatus` | risk_manager | model | **new** (mirrors `decision_status.py`) |
| `risk/risk_model.py` | `RiskOutcome` frozen dataclass (`to_dict`/`to_json`) | gateway fields | `RiskOutcome` | risk_status | database/platform | **new** (mirrors `decision_model.py`) |
| `risk/risk_gateway.py` | orchestrator: `DecisionOutcome`→`RiskManager` input, REUSE `evaluate()`, apply account/duplicate gates, build `RiskOutcome` | `DecisionOutcome` + signal + balance | `RiskOutcome` | risk_manager, trackers | database/platform | **new** (name sits beside the frozen `risk_manager.py`) |
| `risk/risk_router.py` | route metadata: which consumers get this `RiskOutcome` (DATABASE always; PLATFORM/TELEGRAM only if approved) | `RiskOutcome` | consumer list | risk_model | callers | **new** (mirrors `decision_router.py`) |
| `risk/__init__.py` | export STEP-10 surface; document FROZEN-vs-additive | — | — | — | — | **extend** |
| `risk/README.md` | append STEP-10 section | — | — | — | — | **extend** |

### Existing files to EXTEND (reuse-first)
- `risk/__init__.py`, `risk/README.md` — documentation + exports only.
- `account_state_tracker.py` / `duplicate_checker.py` — **reused as-is**;
  extend only if the approved spec adds a genuinely new counter, never a
  formula change.

### Existing files NEVER touched
- `risk_layer/risk_engine/risk_manager.py` — geometry + `calculate_risk_amount` /
  `calculate_position_size` / `calculate_risk_reward` are Trading-Safety
  frozen.

## 5. Reuse mapping (the fork point)

`RiskManager.evaluate()` today expects a `TradeDecision` (the frozen
engine's output). STEP-09 emits a `DecisionOutcome`. `risk_gateway.py`
**adapts** DecisionOutcome→the evaluate() input (reading entry/SL/TP/
direction duck-typed from the canonical signal), calls the frozen
`evaluate()`, then maps the returned `RiskResult` into `RiskStatus`:

| `RiskResult` | → `RiskStatus` |
|---|---|
| `approved == True` | `APPROVED` |
| `approved == False` (geometry/RR fail) | `REJECTED` |
| account tracker → drawdown/daily-loss breach | `PAUSED` |
| duplicate_checker → duplicate open trade | `BLOCKED` |

## 6. Boundary & Trading-Safety guarantees
- Risk Manager is **never bypassed** — the gateway's only path to a sizing
  suggestion is `RiskManager.evaluate()`.
- No broker/MT5 call, no order instruction, no I/O beyond reading account
  state via the existing trackers.
- Fail-safe: a None/partial `DecisionOutcome` or signal yields a `REJECTED`
  `RiskOutcome`, never a raise.

## 7. Detailed flow

```
DecisionOutcome(APPROVE) ──► risk_gateway.evaluate_decision(outcome, signal, balance)
   │ 1. adapt → RiskManager input (entry/SL/TP/direction via getattr)
   │ 2. RiskManager.evaluate()  → RiskResult            [FROZEN]
   │ 3. account_state_tracker   → drawdown/daily-loss   [reuse]
   │ 4. duplicate_checker       → duplicate gate         [reuse]
   │ 5. risk_status.from_risk_result(...)               → RiskStatus
   ▼
RiskOutcome ──► risk_router.route() ──► DATABASE (always)  + PLATFORM/TELEGRAM (if APPROVED)
```
