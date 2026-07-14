# Execution

## Responsibility
Foundation only — **`execution/` is intentionally inert today.** No
MT5/broker connection exists; `ExecutionEngine.dispatch()` always
returns `dispatched=False, reason="Not implemented"` regardless of
input. It exists as a stable contract point for a future,
separately-approved phase to implement against, not as working
functionality. See `docs/DECISION_PRINCIPLES.md`'s Principle 4:
execution takes an already-approved signal and places an order — it
must never gain the ability to alter a candidate's entry/stop-loss/
take-profit, re-run a strategy, or override a `TradeDecision`.

## Input
`risk.risk_manager.RiskResult` (`execution.execution_engine.ExecutionEngine.dispatch(risk_result)`)
— an already Decision-Engine-approved, Risk-Manager-validated result.
This is the concrete carrier of what the brief calls "Approved Trade."

## Output
`execution.execution_engine.ExecutionResult` — `dispatched` (`bool`),
`reason` (`str`).

## Allowed Dependencies
✅ `risk/` (`RiskResult`) — the only input this layer reads.

## Forbidden Dependencies
❌ Changing the strategy — `execution/` never imports `strategies/`
and never alters a `SignalCandidate`'s entry/stop-loss/take-profit.
❌ Generating a signal — `execution/` never imports `context/` or
`signals/` to look for a setup of its own.
❌ `ai/`, `decision/`, `database/`, `telegram/` — per
`execution/execution_engine.py`'s own module docstring: "No MT5, no
Telegram, no HTTP, no Database, no Logger, no async/threading/queue.
No knowledge of message formatting or delivery mechanics."

## Error Contract
`dispatch()` never raises today (it is a no-op stub). Once a real
broker connection is wired in, any execution failure (rejected order,
connection loss, slippage beyond tolerance) should surface as a
`contracts/error_contract.md`-shaped `ExternalAPIError` inside a
still-well-formed `ExecutionResult(dispatched=False, reason=...)` —
never let a broker-side failure raise past this layer uncaught, since
a live trading cycle must not crash mid-run. Not yet implemented.

## Future Extension
`execution/signal_lifecycle.py` exists alongside `execution_engine.py`
as additional foundation scaffolding, also inert. Wiring up a real
MT5/broker connection is explicitly named in `CLAUDE.md`'s Trading
Safety rules as "itself a change requiring explicit approval, not a
routine addition" — the highest-scrutiny future step in this entire
roadmap.
