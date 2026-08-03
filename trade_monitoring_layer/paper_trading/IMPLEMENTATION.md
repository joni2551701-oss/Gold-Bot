# lifecycle/

## Purpose
Phase 59 Preparation foundation (TASK 2: Paper Trading Contract,
TASK 4: Signal Lifecycle Audit). Standard, in-memory state machines
for a simulated trade (`PaperTrade`, never a real broker order) and
for a signal's own progress through the analysis pipeline
(`SignalLifecycleState`). Neither is wired into `core/pipeline.py`,
`execution/`, or the database in this phase — both are standalone
foundations, matching every Phase A/AC module's own "foundation, not a
rewrite" posture.

## Not the same as `strategies/lifecycle/`
`strategies/lifecycle/` (Phase A11) is a per-*strategy* metadata
registry (`StrategyDefinition`/`StrategyRegistry` — status/version per
SMC methodology). `lifecycle/` (this package) is a per-*trade*/
per-*signal* runtime state machine. Unrelated concepts that happen to
share the word "lifecycle" — neither package imports the other.

## Not the same as `execution/`
`execution_layer/execution_engine/execution_engine.py` and `execution_layer/execution_monitor/signal_lifecycle.py`
are pre-existing, deliberately inert stubs in the Trading-Safety-
protected `execution/` package (`ExecutionEngine.dispatch()` and
`SignalLifecycle.transition()` both always return "Not implemented").
`execution_layer/execution_monitor/signal_lifecycle.py`'s own `SignalState` enum
(`CREATED`/`SENT`/`ACKNOWLEDGED`/`CLOSED`) describes Telegram message
delivery, not a signal's analysis-pipeline progress or a trade's own
life. `lifecycle/` never imports from or calls `execution/`, and does
not make `execution/`'s own stubs any less inert — this package adds
no broker call, no real order, no MT5 integration. See
`trade_monitoring_layer/paper_trading/paper_trade.py`'s and `trade_monitoring_layer/paper_trading/signal_state.py`'s own
docstrings for the exact naming disambiguation
(`PaperTrade`/`TradeState` vs. nothing pre-existing; `SignalLifecycleState`
vs. `execution_layer.execution_monitor.signal_lifecycle.SignalState`).

## Modules

### `trade_state.py`
`TradeState` — `CREATED`/`OPEN`/`CLOSED`/`CANCELLED`. The status
vocabulary for a `PaperTrade`.

### `paper_trade.py`
`PaperTrade` (`trade_id`, `signal_id`, `symbol`, `direction`, `entry`,
`stop_loss`, `take_profit`, `status`, `result`, `opened_at`,
`closed_at`, `created_at`) plus:
- `create_paper_trade(signal)` — builds a `CREATED` `PaperTrade` from
  an already-`APPROVED` `SignalSchema`. Raises `ValueError` if the
  signal isn't `APPROVED` or is missing a price field — a genuine
  caller error, not a data-driven condition.
- `open_paper_trade(trade)` / `close_paper_trade(trade, result)` /
  `cancel_paper_trade(trade)` — pure transition functions, each
  returning a `PaperTradeTransitionResult(trade, success, reason)`.
  Never raise: an invalid transition (e.g. closing a trade that was
  never opened) returns `success=False` with the original, unchanged
  trade.
- `ALLOWED_PAPER_TRADE_RESULTS = ("TP", "SL", "BE", "EXPIRED")` —
  `docs/PHASE59_VALIDATION.md`'s own Result vocabulary, deliberately
  distinct from `database_layer/trade_repository/signal_repository.py`'s pre-existing
  `{"WIN","LOSS","BE","CANCELLED"}` (that set belongs to the real,
  persisted `signals` table, untouched by this phase, and already
  uses `CANCELLED` as a result where `PaperTrade` uses it as a
  status).

### `signal_state.py`
`SignalLifecycleState` — `CREATED`/`QUALITY_CHECKED`/`EXPLAINED`/
`APPROVED`/`REJECTED`/`PAPER_OPEN`/`CLOSED`, plus:
- `ALLOWED_TRANSITIONS` / `transition_signal_state(current, next)` —
  a pure transition validator, `SignalStateTransitionResult(success,
  reason)`, never raises.
- `derive_signal_lifecycle_state(signal, paper_trade=None)` —
  observational classification from already-computed
  `SignalSchema`/`PaperTrade` fields (same priority-ordered,
  read-only pattern `context_layer/trend/market_phase.py`'s
  `compute_market_phase()` established). Documented limitation:
  `EXPLAINED` cannot be reliably derived, since
  `SignalSchema.explanation_id` is never populated anywhere in this
  codebase today (see the function's own docstring).

## Dependencies
`paper_trade.py` imports `trade_monitoring_layer.paper_trading.trade_state` (same package) plus,
`TYPE_CHECKING`-only, `signal_layer.signal_builder.schema.SignalSchema`. `signal_state.py`
imports `trade_monitoring_layer.paper_trading.trade_state` plus, `TYPE_CHECKING`-only,
`trade_monitoring_layer.paper_trading.paper_trade.PaperTrade` and `signal_layer.signal_builder.schema.SignalSchema`.
Neither imports `context/`, `strategies/`, `ai/`, `decision/`,
`risk/`, `execution/`, `database/`, or `telegram/`.

### `paper_trade_monitor.py` (Phase 59.4, TASK 2)
`check_paper_trade_against_candles(trade, candles)` — the monitor loop
named as unimplemented below, now built: walks a caller-supplied
candle list looking for entry, then TP/SL, closing the trade via
`close_paper_trade()` (reused, not duplicated) with `"TP"`/`"SL"`, or
`"EXPIRED"` if entry is never touched across the whole window. Stateless
per call — the caller must supply the full candle history since
`trade.opened_at`, not just new candles each cycle (see the module's
own docstring for why). Ambiguity rule: SL wins if a single candle's
range covers both TP and SL (the conservative backtesting convention).

## Future Roadmap
Persistence (a `paper_trades` table, a `PaperTradeRepository` — note
`database_layer/market_repository/raw_candle_repository.py`/`market_snapshot_repository.py`,
Phase 59.3, already provide the raw candle history a real monitor loop
would feed into `paper_trade_monitor.py`) and `core/pipeline.py`
wiring (constructing a `PaperTrade` per `APPROVE`d decision
automatically, and calling the new monitor each cycle) both remain
unimplemented — each a separate, explicitly-approvable future step, in
line with `docs/PHASE59_VALIDATION.md`'s own scope notes.
