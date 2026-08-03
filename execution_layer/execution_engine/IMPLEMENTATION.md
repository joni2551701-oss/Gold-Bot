# execution/

## Purpose
Scaffolding for a future MT5 order-execution layer (`execution_engine.py`/
`signal_lifecycle.py`, both still inert), plus — Phase 60.3 — a
simulated-fill subpackage (`simulator/`) used only by `backtesting/`
and analytics, never by live execution.

## Flow
```
Risk Manager (approved signal)
      |
      v
execution/   -- execution_engine.py/signal_lifecycle.py: NOT WIRED, "not implemented" today
      |
      v
(future) MT5 order

Separately, for backtesting only:

lifecycle.paper_trade.PaperTrade (OPEN) + RiskResult
      |
      v
execution/simulator/   -- Phase 60.3, real logic, never calls execution_engine.py
      |
      v
ExecutionSimulationResult (simulated fill or reject) -- see docs/EXECUTION_SIMULATOR.md
```

## Responsibilities
`execution_engine.py`/`signal_lifecycle.py` unconditionally return
"not implemented" — no MT5 client, no order calls, no I/O. GoldBot
v0.2/v0.3 does not place trades automatically; execution is manual by
the trader. Phase 60.3 does not change either file.

`simulator/` (Phase 60.3: Execution Simulator Foundation) —
`models.py`/`slippage.py`/`spread.py`/`latency.py`/`simulator_engine.py`.
Computes what a fill *would* look like (spread + slippage + latency),
for `backtesting/`/analytics consumption only — never calls a broker,
MT5, or `execution_engine.py`/`signal_lifecycle.py`. See
`docs/EXECUTION_SIMULATOR.md` for the full contract.

## Input
`execution_engine.py`/`signal_lifecycle.py`: none — not called from
any runtime path. `simulator/`: an already-OPEN `PaperTrade` +
`RiskResult`, from a future `backtesting/` caller (not wired as of
Phase 60.3).

## Output
`execution_engine.py`/`signal_lifecycle.py`: none.
`simulator/`: `ExecutionSimulationResult`.

## Dependencies
`execution_engine.py`/`signal_lifecycle.py`: none beyond stdlib. Not
imported by `core/pipeline.py` or `main.py` (confirmed by the Phase 48
audit). `simulator/` imports `lifecycle.paper_trade.PaperTrade` and
`risk_layer.risk_engine.risk_manager.RiskResult` (`TYPE_CHECKING`-only) — a new,
one-directional `execution/` → `lifecycle/`/`risk/` dependency, read
only, never reversed; `lifecycle/`/`risk/` do not import `execution/`.

## Future Roadmap
Real MT5 integration is the eventual purpose of this directory, but
no phase has scoped that work yet. Decide its fate (implement vs.
remove) before v0.4 rather than leaving it inert indefinitely — noted
as an open item in `docs/AUDIT_REPORT.md`.
