# Risk Manager

## Responsibility
Validates a decision that already exists — geometry and stop-loss
distance — and suggests a lot size. **Risk never originates a trade
idea.** See `docs/DECISION_PRINCIPLES.md`'s Principle 3.

## Input
`decision_layer.decision_engine.models.TradeDecision` (required) and an optional
`account_balance: float`
(`risk_layer.risk_engine.risk_manager.RiskManager.evaluate(trade_decision, account_balance=None)`).
This matches the brief's "TradeDecision, Account Information" input
description closely — `account_balance` is exactly that "account
information," and is the one input `RiskManager` reads that isn't
already inside the `TradeDecision`. GoldBot is semi-automated (no
MT5/broker connection), so it has no built-in source of account
balance; a caller must supply it explicitly for dollar `risk_amount`/
`lot_size` to be non-zero.

## Output
`risk_layer.risk_engine.risk_manager.RiskResult` — `approved` (`bool`), `lot_size`
(`float`, a sizing *suggestion*, never an order instruction),
`risk_amount` (`float`), `risk_reward` (`float`), `reason` (`str`).
Anything the Decision Engine did not `APPROVE` is rejected
immediately (`approved=False`), without further geometry validation.

## Allowed Dependencies
✅ `decision/` (`TradeDecision`, `DecisionAction`) — the decision
being validated.
✅ `signals/` (`SignalCandidate`, reached via `TradeDecision.signal`)
— for entry/stop-loss/take-profit geometry.

## Forbidden Dependencies
❌ Finding an entry — `risk/` never imports `context/` or
`strategies/` to look for a setup of its own; it validates the
geometry a `TradeDecision` already carries.
❌ Selecting a strategy — Risk Manager has no visibility into which
strategy produced a candidate beyond what's already on
`TradeDecision.signal.strategy_name`; it does not choose, favor, or
filter by strategy.
❌ `ai/`, `database/`, `telegram/`, `execution/` — Risk Manager reads
a `TradeDecision`, nothing else; "No MT5, no SymbolInfo, no Database,
no Telegram, no Logger" per `risk_layer/risk_engine/risk_manager.py`'s own module
docstring.

## Error Contract
`evaluate()` never raises — a `REJECT`/`NO_TRADE` decision, invalid
SL/TP geometry, or a missing `account_balance` all produce a
well-formed `RiskResult` (`approved=False` with a `reason` string, or
`risk_amount`/`lot_size` at `0.0` with a reason explaining why),
never an exception. Per `contracts/error_contract.md`, this is
exactly the "structured result, not a raised exception" pattern every
Phase A module follows for an expected, non-programmer-error
condition.

## Future Extension
`RiskConfig`'s `max_daily_loss`/`max_drawdown`/`max_open_trades`
fields exist but are not yet enforced across multiple
`RiskManager.evaluate()` calls (no cross-cycle state is tracked
today) — a named, not-yet-implemented future step. No broker
specification (contract size, tick value, lot step, min/max lot) is
known to this layer; wiring one in is a future, separately-approved
phase tied to Execution actually going live.
