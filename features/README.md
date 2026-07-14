# features/

## Purpose
Feature Engineering foundation (Phase A10) — builds one standard
`MarketFeatures` snapshot per pipeline cycle, entirely from data
already computed elsewhere in `context/`. A data-shaping layer for a
future AI Analyzer, backtester, or ML dataset exporter, not a new
analysis.

## Flow
```
Context Engine
      |
      v
Feature Engineering (feature_engine.py, Phase A10)
      |     compute_market_features(context, htf_bias)
      |     -> MarketFeatures, one per cycle (not per-candidate)
      v
Strategy Engine   -- unchanged; does not read MarketFeatures
```

## Responsibilities
- `feature_model.py` — `MarketFeatures`, the frozen, immutable
  dataclass contract (`atr`, `volatility`, `trend_strength`, `session`,
  `regime`, `htf_bias`, `liquidity_distance`, `volume`).
- `feature_engine.py` — `compute_market_features()`, a read-only,
  pure function. Does **not** generate a signal, grade one, or change
  strategy/AI/decision behavior.

### Why Feature Engineering exists
A future AI Analyzer, backtester, and ML dataset exporter each need
the same underlying market context, but without a standard shape each
would independently re-derive its own subset from raw `ContextSnapshot`
fields — the same "everyone re-reads raw candles" problem HTF Bias
(Phase A2) and Signal Quality Score (Phase A4) already solved for
their own narrower questions. See `docs/FEATURE_ENGINEERING.md` for
the full field-sourcing table.

### What Feature Engineering does NOT do
- Does not train, run, or reference any ML model.
- Does not change `strategies/*.py`, `signals/signal_engine.py`,
  `signals/signal_quality.py`'s scoring, `ai/`, or
  `decision/decision_engine.py` — none read `MarketFeatures` in this
  phase.
- Does not fabricate a volume value — `volume` is always `None`; this
  codebase has no volume data source at all.
- Does not persist `MarketFeatures` anywhere — no schema change, no
  new table.
- Does not implement backtesting or a research harness — only
  produces the standard shape a future one would consume.

## Input
`ContextSnapshot` (from `context/`) and an optional `HTFBiasResult`
(from `context/htf_bias.py`, passed in externally, same pattern as
Decision Engine v2/Market Regime).

## Output
`MarketFeatures` (`atr`, `volatility`, `trend_strength`, `session`,
`regime`, `htf_bias`, `liquidity_distance`, `volume`) — one per cycle,
never raises even on an empty/minimal context.

## Dependencies
`context.market_regime` (for `MarketRegime`) and `context.session`
(for `compute_session_volatility()`/`classify_session()`) — both
already-existing `context/` computations, no new indicator. No
dependency on `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
`database/`, or `telegram/`.

## Future Roadmap
See `docs/FEATURE_ENGINEERING.md`'s "Future ML usage" section — a
real Wilder ATR, a real volume source once one exists, a backtest
harness replaying `compute_market_features()` over historical candles,
and ML dataset export are all named, explicit future steps, none
implemented in this phase.
