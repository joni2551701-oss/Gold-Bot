# Phase V1.0.1 — Risk Management Hardening: Foundation Audit

Worker Brief: "Risk Management Hardening Patch" (V1.0.1 Stabilization,
Priority CRITICAL, Director Approved). This audit is TASK 0 — it
re-confirms and extends `docs/V1_RISK_AUDIT.md`'s findings from the
Phase V1.0 pre-freeze audit, this time as the basis for actually
fixing the gaps (this phase is explicitly scoped to `risk/`,
`configuration/`, `database/`, `monitoring/`, `tests/`, `docs/` —
Trading Core, `decision/`, `execution/`, `strategies/`, `signals/`,
`context/`, and `ai/` remain locked).

## 1. risk/risk_manager.py — current state (read in full)

`RiskManager.evaluate(trade_decision, account_balance=None) -> RiskResult`
is the sole entry point. Confirmed gaps, matching `docs/V1_RISK_AUDIT.md`:

- `RiskConfig.risk_per_trade` (default 0.01) has no min/max bound —
  any value flows through unclamped (TASK 1 target).
- `calculate_risk_reward()` computes RR but nothing compares it to a
  minimum — a geometrically valid signal with RR=0.1 is approved the
  same as RR=5.0 (TASK 3 target).
- `account_balance <= 0` silently degrades to `risk_amount=0.0`/
  `lot_size=0.0` rather than rejecting the whole result — TASK 2
  wants an explicit REJECT for invalid input, not a silently-zeroed
  approval.
- `RiskConfig.max_daily_loss`/`max_drawdown`/`max_open_trades` are
  declared but never read anywhere in the file — no drawdown tracking,
  no daily-loss tracking, no duplicate-trade tracking exists (TASK 4/
  5/6 targets).
- `RiskManager` never imports `core_layer.emergency` — Emergency `PAUSED`
  does not stop Risk from approving/persisting; only
  `core_layer/pipeline/pipeline_guard.py`'s `before_execution()` (Telegram
  suppression) currently reacts to `PAUSED` (TASK 7 target).
- No decision is ever logged/persisted — no Error-ID-style trail for
  a specific risk verdict (TASK 8 target).
- No monitoring surface reads Risk's outcomes at all (TASK 9 target).

## 2. decision/decision_engine.py + decision/models.py

`TradeDecision` (frozen dataclass) carries `signal: SignalCandidate`
and `ai_analysis`, but **no `symbol` field** —
`signals.models.SignalCandidate` also has no `symbol` field (GoldBot
trades a single hardcoded symbol, `"XAUUSD"`, set only in
`main.py`'s `TradingPipeline(symbol="XAUUSD", ...)` construction, never
threaded down into `SignalCandidate`/`TradeDecision`). This matters for
TASK 6 (duplicate detection) and TASK 8 (per-symbol logging): since
`core/pipeline.py` (locked, `core/` is off-limits this phase) calls
`self.risk_manager.evaluate(decision)` with no `account_balance` and no
symbol today, any new input this phase needs (`symbol`, `current_equity`)
must be an **optional, additive keyword argument** on `evaluate()` that
defaults to `None` and is a no-op when omitted — preserving the exact
existing call site unchanged (`core/pipeline.py:463`,
`backtesting/backtest_engine.py:206`, both untouched, both still valid)
while making every new protection available to any future caller that
does supply richer data. This is the same "additive optional field/
parameter" pattern used throughout this codebase's history for
non-breaking extension (e.g. Phase B.0's `stage_durations_ms`).

## 3. configuration/

`configuration/settings.py`, `feature_flags.py`, `environment.py`,
`feature_registry.py`, `runtime_feature_manager.py` all exist but none
currently expose risk-specific limits. No existing config surface to
extend for `MIN_RISK_PER_TRADE`/`MAX_RISK_PER_TRADE`/
`MIN_RISK_REWARD_RATIO`/`MAX_DRAWDOWN`/daily-loss threshold — the
Module Reuse Principle's first two questions ("does this exist," "can
an existing module be extended") both resolve "no": these limits are
resolved via new fields on `risk.risk_manager.RiskConfig` itself
(the module that already owns `risk_per_trade`/`max_daily_loss`/
`max_drawdown`), not a new `configuration/` module — the existing
dataclass is the correct, minimal extension point.

## 4. database/ — schema and repository conventions

Read `database/emergency_repository.py`, `emergency_models.py`,
`database/models.py`'s `init_emergency_state_schema()`, and
`database/database.py`'s `Database` context-manager. Confirmed
convention for a new append-only log table: `CREATE TABLE IF NOT
EXISTS` + autoincrement `id` + one `init_*_schema()` function in
`database/models.py`, called from the new repository's own
`__init__`. No existing table can hold a per-decision risk audit trail
(TASK 8) or a per-symbol drawdown/daily-loss baseline (TASK 4/5) —
both require new, purpose-built tables. Two new tables are added this
phase:

- `risk_decisions` — append-only (mirrors `emergency_states`): one row
  per `RiskManager.evaluate()` call, whatever the outcome.
- `risk_account_state` — one row per symbol, upserted (mirrors
  `runtime_features`' one-row-per-name convention): holds the
  drawdown baseline (`starting_equity`/`current_equity`) and the
  daily-loss baseline (`daily_start_balance`/`daily_date`) together,
  since both are small, related, per-symbol account-state facts.

## 5. monitoring/

`monitoring/decision_logger.py`, `performance_collector.py`,
`health_monitor.py` all follow "the producer writes, monitoring reads
back" (`decision_logger.log_entry()` is called by whoever owns a
decision event; monitoring's own read functions never compute a
decision themselves). No existing monitoring module reads Risk's
outcomes. TASK 9's read-only aggregator (`monitoring/risk_risk_monitor.py`
— see Task 9 section) queries the new `risk_decisions` table
directly, the same "monitoring only reads, never mutates trading
state" posture every prior monitoring phase in this codebase has held.

## 6. tests/

`tests/unit/test_risk_manager.py` (8 tests) is the only existing
dedicated Risk coverage — construction via `RiskManager()` bare (no
config override), RR values of 3.0 and 4.65 in its two passing-geometry
tests (both comfortably above the new `MIN_RISK_REWARD_RATIO=2.0`
default), no `account_balance` ever supplied (so the new zero/negative-
balance rejection never triggers for these). Confirmed: none of these
8 tests will need modification — every new default in this phase was
chosen to keep them passing unmodified, which is itself this phase's
"existing pipeline unchanged" compatibility proof.

## 7. core_layer/emergency/ (read-only dependency, not edited this phase)

`core_layer.emergency.emergency_manager.EmergencyManager().get_status()`
returns an `EmergencyStateRecord` defaulting to `NORMAL` when nothing
has ever been recorded (confirmed empty on this sandbox's
`database/goldbot.db`, which is gitignored/not tracked). `risk/`
importing `core_layer.emergency` (read-only `get_status()` calls only, never
constructing an `EmergencyStateRecord` or calling any
`activate_*()`/`restore_normal()` mutator) is a new but fully
IMPORT_RULES.md-sanctioned dependency: "any module -> `core/*`" is
always allowed, and this phase does not modify a single line inside
`core/`.

## Conclusion

All ten remaining Known Issues from `docs/V1_RISK_AUDIT.md` (items 2,
4, 5, 6, 7 specifically) are addressed by TASK 1-9 below. No Trading
Core file is touched. Full design recorded in
`docs/PHASE_V1_0_1_RISK_FREEZE.md` and `docs/trading/RISK_SYSTEM.md`.
