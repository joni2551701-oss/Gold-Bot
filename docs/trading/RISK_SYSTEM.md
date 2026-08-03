# GoldBot — Risk System

Governed by `docs/constitution/CONSTITUTION.md` Article 1 ("Never
bypass Risk Manager" — `CLAUDE.md`'s own Trading Safety hard rule).
Verified directly against `risk_layer/risk_engine/risk_manager.py`. Updated by Phase
V1.0.1 (Risk Management Hardening Patch, Director Approved) — see
`docs/PHASE_V1_0_1_RISK_AUDIT.md` and `docs/PHASE_V1_0_1_RISK_FREEZE.md`
for the full audit/freeze trail behind every change on this page.

## What `RiskManager.evaluate()` does

```
RiskManager.evaluate(trade_decision, account_balance=None, current_equity=None, symbol=None)
    │
    ├── decision.action != APPROVE?               → REJECT "not APPROVE"
    ├── Emergency state PAUSED/KILLED/MAINTENANCE? → REJECT "no new trade approval" (Phase V1.0.1 TASK 7)
    ├── validate_geometry()                        → REJECT "geometry" if invalid
    ├── validate_stop_loss_distance()               → REJECT "Invalid stop-loss distance" if invalid
    ├── risk_per_trade within [min, max]?           → REJECT "Risk limit exceeded" if not (Phase V1.0.1 TASK 1)
    ├── calculate_risk_reward() >= min_risk_reward_ratio? → REJECT "RR below minimum" if not (Phase V1.0.1 TASK 3)
    ├── account_balance/current_equity > 0?         → REJECT "Invalid account balance/equity" if not (Phase V1.0.1 TASK 2)
    ├── duplicate check (symbol supplied)?          → REJECT "Duplicate trade" if found (Phase V1.0.1 TASK 6)
    ├── drawdown check (current_equity supplied)?   → REJECT "Drawdown ... exceeds max" if over limit (Phase V1.0.1 TASK 4)
    ├── daily loss check (account_balance supplied)? → REJECT "Daily loss ... exceeds max" if over limit (Phase V1.0.1 TASK 5)
    ├── calculate_position_size()
    │       risk_amount = account_balance * risk_per_trade
    │       lot_size = risk_amount / stop_loss_distance
    ├── every outcome logged to risk_decisions (Phase V1.0.1 TASK 8)
    └── RiskResult(approved, lot_size, risk_amount, risk_reward, reason, risk_percent, drawdown_percent)
```

`lot_size` is a **suggested** sizing output — the Risk Manager
computes it, it does not itself place an order (that boundary belongs
to `execution/`, and `execution/` is intentionally inert today).

`account_balance`, `current_equity`, and `symbol` are all optional,
additive parameters (Phase V1.0.1) — `core/pipeline.py` and
`backtesting_layer/backtest_engine/backtest_engine.py` (both Trading Core, both untouched by
this phase) call `evaluate(trade_decision)` with none of them, so
duplicate/drawdown/daily-loss checking is dormant in the live pipeline
today until a future, separately-approved phase supplies real
equity/balance/symbol data. Risk-per-trade bounds, RR minimum, and
Emergency-state checking are **not** gated behind any new parameter —
they are active unconditionally, on every `evaluate()` call, starting
with this phase.

## Risk rules

- **risk %** — `RiskConfig.risk_per_trade`, applied against
  `account_balance` to get a dollar `risk_amount`. Bounded by
  `min_risk_per_trade` (default 0.001 = 0.1%) and `max_risk_per_trade`
  (default 0.02 = 2%) — a configured value outside this range is
  rejected with "Risk limit exceeded" (Phase V1.0.1 TASK 1).
- **lot calculation** — `risk_amount / stop_loss_distance`, never a
  fixed lot size regardless of account size or stop distance.
- **minimum risk/reward** — `RiskConfig.min_risk_reward_ratio`
  (default 2.0). A geometrically valid signal whose reward:risk ratio
  falls below this is rejected with "Risk Reward ratio below minimum"
  (Phase V1.0.1 TASK 3) — closes the gap `docs/V1_RISK_AUDIT.md`
  documented (RR=0.1 previously approved identically to RR=5.0).
- **drawdown** — `RiskConfig.max_drawdown` (default 0.10 = 10%).
  When `current_equity` is supplied, `risk_layer.risk_engine.account_state_tracker.AccountStateTracker`
  tracks a per-symbol starting-equity baseline
  (`database_layer.trade_repository.risk_state_repository.RiskStateRepository`,
  `risk_account_state` table) and computes drawdown % against it; an
  excess drawdown rejects the trade and marks that symbol's status
  `TRADING_PAUSED` (Phase V1.0.1 TASK 4).
- **daily loss** — `RiskConfig.max_daily_loss` (default 0.05 = 5%).
  When `account_balance` is supplied, the same tracker maintains a
  per-symbol, per-UTC-day starting-balance baseline and blocks new
  trades once the day's loss % exceeds the limit (Phase V1.0.1 TASK 5).
- **duplicate trade protection** — when `symbol` is supplied,
  `risk_layer.risk_validator.duplicate_checker.DuplicateTradeChecker` rejects a signal
  matching an already-APPROVEd (symbol, direction, strategy) within a
  configurable time window (`RiskConfig.duplicate_window_seconds`,
  default 300s) — reusing the `risk_decisions` log itself as the
  "was this recently approved" source, since GoldBot has no persisted
  open-position store (Phase V1.0.1 TASK 6).
- **emergency stop** — **corrected by Phase V1.0.1 TASK 7.** Risk now
  consults `core_layer.emergency.emergency_manager.EmergencyManager`
  (read-only `get_status()` only) directly: `PAUSED`, `KILLED`, and
  `MAINTENANCE` all reject every new trade approval at the Risk layer
  itself, not only at Telegram delivery. The exact model:
  ```
  PAUSED
    ↓
  No new trade approval   (RiskManager.evaluate() rejects, reason names the state)
    ↓
  No execution             (core_layer/pipeline/pipeline_guard.py's before_execution() still also skips Telegram delivery, unchanged)
    ↓
  Monitoring continues     (monitoring/ keeps reading — observer-only, unaffected)
    ↓
  Logs saved               (every reject, including this one, is persisted to risk_decisions, TASK 8)
  ```
  `WARNING` remains advisory-only and does not block (matches
  `core_layer.emergency.emergency_state.EmergencyState`'s own docstring).
  This corrects the previous version of this page's claim that
  Emergency-state blocking was "not `risk/`'s own concern" — that was
  true for `PAUSED` specifically before this phase (only Telegram
  delivery reacted to it), a gap `docs/V1_RISK_AUDIT.md` (item 7)
  documented and this phase fixes.
- **risk logging** — every `evaluate()` call, whatever the outcome, is
  persisted to the `risk_decisions` table
  (`database_layer.trade_repository.risk_decision_repository.RiskDecisionRepository`):
  timestamp, symbol, strategy, direction, risk %, risk/reward,
  drawdown %, decision (APPROVE/REJECT), reason, and a machine-readable
  `reject_category` (Phase V1.0.1 TASK 8).
- **monitoring integration** — `core_layer/health_monitor/risk_monitor.py` is a
  read-only aggregator over `risk_decisions`: total checks, approve/
  reject counts, and per-category reject counts (risk-limit, RR,
  drawdown, daily-loss, duplicate, emergency-pause), plus a combined
  "pause events" figure (emergency-pause + drawdown-pause). Monitoring
  never writes to `risk_decisions` itself (Phase V1.0.1 TASK 9).

## What Risk can and cannot do

- **CAN**: evaluate a signal's geometry/stop-loss validity, size a
  position, reject on risk-limit/RR/drawdown/daily-loss/duplicate/
  emergency-state violation via `evaluate()`.
- **CANNOT**: be skipped for any signal reaching a user; consult the
  AI layer (`risk/` imports nothing from `ai/` and has no sanctioned
  reason to — `docs/architecture/IMPORT_RULES.md`); generate a signal
  of its own; change `BUY`/`SELL`/entry/TP/SL/strategy/AI score (RULE
  2/3 of the Phase V1.0.1 brief — Risk only ever returns ALLOW/REJECT).
- **Depends on**: `decision/` (the decision being validated),
  `core_layer.emergency` (read-only state check, Phase V1.0.1), and
  `database/` (append-only decision logging + per-symbol account-state
  persistence, Phase V1.0.1) — the latter two are new, deliberate,
  documented exceptions to this module's earlier "no Database" posture,
  authorized by the Phase V1.0.1 Worker Brief's own RULE 1 (which
  explicitly scoped this phase to `risk/`, `configuration/`,
  `database/`, `monitoring/`, `tests/`, `docs/`).

## Related

- `docs/trading/DECISION_ENGINE.md` — what `risk/` receives as input.
- `docs/trading/EXECUTION_SYSTEM.md` — what happens to `RiskResult`
  next.
- `docs/EMERGENCY_SYSTEM.md` — the Emergency state model itself.
- `docs/V1_RISK_AUDIT.md` — the Phase V1.0 pre-freeze audit that found
  every gap this phase closes.
- `docs/PHASE_V1_0_1_RISK_AUDIT.md`, `docs/PHASE_V1_0_1_RISK_FREEZE.md`
  — this phase's own audit and freeze documents.
