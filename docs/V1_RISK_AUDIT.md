# GoldBot V1.0 — Risk Management Audit

Part of the Phase V1.0 GoldBot V1 Final Audit Foundation (Worker Brief,
Director Approved). Scope: `risk_layer/risk_engine/risk_manager.py` (`RiskManager.evaluate()`,
a locked public signature) and `core_layer/emergency/` (emergency stop / kill
switch). Read-only audit — per RULE 1 (Trading Core Protection), no
change was made to `risk/` in this phase; findings below are reported
for the Director's review, and any fix requires a separate, explicit
approval per CLAUDE.md's Trading Safety section.

## 1. Lot / position size calculation — PASS

`risk_layer/risk_engine/risk_manager.py:125-138` `calculate_position_size()`:
`lot_size = risk_amount / stop_loss_distance`, guarded by
`if stop_loss_distance <= 0: return 0.0`. `calculate_risk_amount()`
(lines 113-123) guards `account_balance <= 0 or risk_percent <= 0 ->
0.0`. No division-by-zero path, no negative lot possible. Sizing is
risk-%-and-SL-distance derived, not a fixed lot — matches spec.

## 2. Risk % enforcement — CONCERN

`RiskConfig.risk_per_trade: float = 0.01` (line 9) is configurable via
constructor injection, but there is **no clamp or validation** that it
stays within a sane 0-100% (0.0-1.0) range. `calculate_risk_amount()`
only rejects `<= 0`. A caller-supplied `RiskConfig(risk_per_trade=2.0)`
(200%) would silently flow through and be accepted.

**Scenario**: `RiskConfig(risk_per_trade=2.0)` + `account_balance=10000`
-> `risk_amount=20000` (200% of the account), `approved=True`, no
warning.

## 3. SL distance / geometry validation — PASS

`validate_geometry()` (lines 164-178): BUY requires
`stop_loss < entry < take_profit`; SELL requires the mirror. Called
before any sizing (line 67), rejects with a descriptive reason.
`validate_stop_loss_distance()` (lines 155-162) additionally requires
`stop_loss_distance > 0`, called at line 82.

## 4. Minimum RR ratio enforcement — FAIL (known, documented limitation)

`calculate_risk_reward()` (lines 140-153) computes RR and returns it in
`RiskResult.risk_reward`, but `evaluate()` never compares it against a
threshold — no `min_risk_reward` field exists in `RiskConfig`, and no
rejection/downgrade branch exists in `risk_layer/risk_engine/risk_manager.py` or
`decision_layer/decision_engine/decision_engine.py`. A geometrically valid signal with RR =
0.1 is approved identically to one with RR = 5.0.

**Scenario**: entry=2000, stop_loss=1990 (risk=10), take_profit=2001
(reward=1) -> risk_reward=0.1, `approved=True`.

## 5. Max loss / drawdown protection — FAIL (known, documented limitation)

`RiskConfig.max_daily_loss` and `RiskConfig.max_drawdown` (lines 10-11)
are declared but never read anywhere in `evaluate()` or elsewhere in
the file. `contracts/risk_contract.md`'s own "Future Extension"
section already discloses this: *"`RiskConfig`'s
`max_daily_loss`/`max_drawdown`/`max_open_trades` fields exist but are
not yet enforced across multiple `RiskManager.evaluate()` calls (no
cross-cycle state is tracked today) — a named, not-yet-implemented
future step."* `core_layer/emergency/circuit_breaker.py`'s
`evaluate_circuit()` is the one place drawdown logic actually exists,
but it is explicitly documented as never called from
`core/pipeline.py`/`risk/`/`decision/`/`execution/` in this phase — it
is dead code today, not wired to block anything.

**Scenario**: 10 consecutive losing trades in one day never reduces
`RiskManager`'s approval rate or sizing; every subsequent signal is
evaluated identically. This is a **pre-existing, documented
architectural gap** (`contracts/risk_contract.md`), not a regression
introduced by this or any recent phase.

## 6. Duplicate trade prevention — FAIL (known, documented limitation)

No open-position/duplicate-signal check exists in `risk_layer/risk_engine/risk_manager.py`,
`decision_layer/decision_engine/decision_engine.py`, or `core/pipeline.py`.
`RiskConfig.max_open_trades: int = 1` (line 12) is declared but never
referenced anywhere outside its own declaration. `evaluate()` is
stateless per call — it has no notion of currently-open trades.

**Scenario**: two near-simultaneous signal candidates for the same
symbol/direction can both independently receive `approved=True` in
the same cycle with no mutual awareness. Since GoldBot is
semi-automatic (Telegram delivery only, human decides whether to act),
the practical blast radius today is a duplicate Telegram alert, not a
duplicate live order — there is no live execution layer (see Execution
Audit in `docs/PHASE_V1_AUDIT.md`).

## 7. Emergency stop — CONCERN (real gap vs. documented behavior)

`core_layer/emergency/emergency_manager.py` and `core_layer/pipeline/pipeline_guard.py`
are real and wired: `core/pipeline.py:226` constructs `PipelineGuard()`,
consulted at `before_signal()`, `before_ai()`,
`before_execution()`/Telegram delivery, and `before_database()`.
`KILLED` aborts the whole run before `decision_engine.evaluate()`/
`risk_manager.evaluate()` ever run — load-bearing for `KILLED`, as
`docs/trading/RISK_SYSTEM.md:33-36` documents: *"the Emergency Kill
Switch... can halt the pipeline before `risk/` is ever reached."*

**However**: `RiskManager.evaluate()` itself never imports or consults
emergency state (no `core_layer.emergency` import anywhere in the file), and
`core/pipeline.py` has no guard hook around the decision/risk stages —
only signal, AI, execution/Telegram, and database are gated. Under
`EmergencyState.PAUSED`, `before_execution()` skips only Telegram
delivery; signal generation, `DecisionEngine.evaluate()`, and
`RiskManager.evaluate()` still run and produce `approved=True`
`RiskResult`s, and since `before_database()` doesn't check `PAUSED`,
those approved signals are still persisted to the database — only the
outbound Telegram message is suppressed.

This means `docs/trading/RISK_SYSTEM.md:33-36`'s claim is only true for
`KILLED`, not for `PAUSED` — a real documentation-vs-implementation gap.

**Scenario**: owner sets `EmergencyState.PAUSED` intending to stop new
trade approvals; `RiskManager` keeps approving and persisting signals
to the DB every cycle, just without a Telegram alert reaching the
user. No unsafe signal reaches a user (the REJECT/BLOCKED-to-Telegram
filter and the PAUSED Telegram-suppression both still hold), but the
Owner's mental model of "PAUSED = nothing new gets approved" does not
match what actually happens internally.

## 8. Public signature stability — PASS

`RiskManager.evaluate(self, trade_decision: TradeDecision,
account_balance: Optional[float] = None) -> RiskResult` matches both
call sites exactly (`core/pipeline.py:463`,
`backtesting/backtest_engine.py:206`), both omitting `account_balance`
by design (`contracts/risk_contract.md` confirms GoldBot has "no
built-in source of account balance"). Note: in production,
`account_balance` is never supplied, so `lot_size`/`risk_amount` are
always `0.0` in live pipeline output — sizing is effectively unused in
the wired system today. This is a functional gap consistent with the
documented contract, not a signature break.

## Summary

| # | Item | Verdict |
|---|---|---|
| 1 | Lot/position sizing | PASS |
| 2 | Risk % enforcement (0-100% clamp) | CONCERN |
| 3 | SL distance / geometry validation | PASS |
| 4 | Minimum RR ratio enforcement | FAIL (documented limitation) |
| 5 | Max loss / drawdown protection | FAIL (documented limitation) |
| 6 | Duplicate trade prevention | FAIL (documented limitation) |
| 7 | Emergency stop (PAUSED vs docs) | CONCERN |
| 8 | Public signature stability | PASS |

Items 4, 5, 6 are **pre-existing, already-disclosed architectural
limitations** (see `contracts/risk_contract.md`'s own "Future
Extension" section) — not regressions, and not silent. Item 2 (no
risk-% clamp) and item 7 (PAUSED doesn't stop Risk from evaluating/
persisting, only suppresses the Telegram send) are the two findings
this audit is newly surfacing with concrete reproduction scenarios.
None of these allow an unsafe/rejected signal to reach a Telegram
user — the notification-eligibility filter (APPROVE + risk-approved
only) and the PAUSED Telegram-suppression both remain intact and were
independently re-verified in the Trading Pipeline Audit
(`docs/PHASE_V1_AUDIT.md`). These are approval-logic and
observability gaps, not user-facing safety failures.

Per CLAUDE.md's Trading Safety rules, `risk_layer/risk_engine/risk_manager.py` and
`core_layer/emergency/` are locked; no fix is applied in this phase. These
findings are carried into `docs/PHASE_V1_FREEZE.md`'s Known Issues /
Remaining Risks section for the Director's explicit decision on
whether/how to address them in a future, separately-approved phase.
