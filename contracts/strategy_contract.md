# Strategy Engine

## Responsibility
Finds a setup — a specific SMC-pattern confluence (Liquidity Sweep +
BOS + Order Block, FVG + structural break, AMD Distribution +
footprint) — and proposes it as a candidate. **A strategy never says
"BUY" or "SELL happened"; it says "a potential setup was found."**
The distinction matters: a `SignalCandidate` is a proposal that still
has to pass Signal Quality, Explainability, AI, Decision Engine, and
Risk Manager before it can ever reach a user — see
`docs/DECISION_PRINCIPLES.md`'s Principle 2.

## Input
`context.context_orchestrator.ContextSnapshot` (each
`strategies/*.py` file's `analyze(context)` method).
`strategies.strategy_manager.StrategyManager.run_all_strategies(context)`
runs every registered strategy against the same `ContextSnapshot` and
aggregates their output.

## Output
`List[signals.models.SignalCandidate]` per strategy —
`signal_type` (`BUY`/`SELL`/`NONE`), `entry`, `stop_loss`,
`take_profit`, `strategy_name`, `confidence`, `reasons`. Zero
candidates is a normal, expected outcome (no setup found), not an
error.

## Allowed Dependencies
✅ `context/` (`ContextSnapshot` and its fields) — the only input a
strategy reads.
✅ `signals/` (`SignalCandidate`, `SignalType`) — the output contract.

## Forbidden Dependencies
❌ `ai/` — a strategy never calls the AI layer or reads an AI
verdict; that ordering runs the other way (AI reads the candidate,
not vice versa).
❌ `telegram/` — a strategy never talks to a user.
❌ `execution/` — a strategy never opens an order; "candidate" means
exactly that, not an instruction.
❌ `decision/`, `risk/`, `database/` — a strategy has no visibility
into whether its own candidate will be approved, sized, or persisted.

## Error Contract
Never raises for missing/insufficient context data — every real
`strategies/*.py` file returns an empty `List[SignalCandidate]` when
its pattern isn't found (e.g. `LiquidityStrategy.analyze()` returns
`[]` immediately if `context.liquidity_sweeps` or `context.bos_events`
is empty). Per `contracts/error_contract.md`, a future exception here
(e.g. a malformed candidate the strategy itself cannot construct)
should be a `ValidationError`, never a bare exception — not yet
implemented.

## Future Extension
`strategies/lifecycle/` (Phase A11) adds `StrategyRegistry` metadata
(status, version, supported assets/styles/timeframes) alongside
strategy execution, but is not wired into `StrategyManager` in this
phase — a `StrategyStatus.DISABLED` entry does not currently stop
`StrategyManager` from running that strategy; wiring that gate is a
named, not-yet-done future step (`docs/STRATEGY_LIFECYCLE.md`). A
Strategy↔Asset compatibility check against `assets/` is documented,
not implemented (`docs/ASSET_INTELLIGENCE.md`).
