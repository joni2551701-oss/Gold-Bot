# features/

## Purpose
Feature Engineering foundation (Phase A10) — builds one standard
`MarketFeatures` snapshot per signal candidate, entirely from results
already computed elsewhere (`context/`, `signals/signal_quality.py`,
`signals/explainability.py`). A standardization layer for a future AI
Analyzer, backtester, ML dataset exporter, or Failure Analysis
module, not a new analysis.

## Flow
```
Context Engine
      |
      v
Strategy Engine (signal candidates)
      |
      v
Signal Quality Score (signals/signal_quality.py)
      |
      v
Explainability (signals/explainability.py)
      |
      v
Feature Engineering (feature_engine.py, Phase A10)
      |     compute_market_features(context, explanation, asset, timeframe, htf_bias)
      |     -> MarketFeatures, one per candidate
      v
AI Layer   -- unchanged; does not read MarketFeatures
```

## Responsibilities
- `feature_model.py` — `MarketFeatures`, the frozen, immutable
  dataclass contract (`asset`, `timeframe`, `htf_bias`,
  `market_regime`, `session`, `signal_quality`, `confidence`,
  `volatility`, `trend_strength`, `liquidity_distance`, `volume`,
  `atr`).
- `feature_engine.py` — `compute_market_features()`, a read-only,
  pure function. Does **not** generate a signal, grade one, or change
  strategy/AI/decision behavior.

### Why Feature Engineering exists
A future AI Analyzer, backtester, ML dataset exporter, and Failure
Analysis module each need the same underlying market context and
candidate-quality read, but without a standard shape each would
independently re-derive its own subset from raw `ContextSnapshot`/
`SignalQualityResult`/`SignalExplanation` fields — the same "everyone
re-reads raw candles" problem HTF Bias (Phase A2) and Signal Quality
Score (Phase A4) already solved for their own narrower questions. See
`docs/FEATURE_ENGINEERING.md` for the full field-sourcing table.

### What Feature Engineering does NOT do
- Does not train, run, or reference any ML model.
- Does not change `strategies/*.py`, `signals/signal_engine.py`,
  `signals/signal_quality.py`'s scoring, `signals/explainability.py`,
  `ai/`, or `decision/decision_engine.py` — none read `MarketFeatures`
  in this phase.
- Does not grade, explain, or re-derive anything itself —
  `signal_quality`/`confidence` are relayed from an already-computed
  `SignalExplanation`, never recomputed.
- Does not implement a real ATR or fabricate a volume value — both
  `atr` and `volume` are always `None`; this codebase has no volume
  data source at all, and a real ATR would be a new indicator, out of
  scope for a standardization-only phase.
- Does not persist `MarketFeatures` anywhere — no schema change, no
  new table.
- Does not implement backtesting or a research harness — only
  produces the standard shape a future one would consume.

## Input
`ContextSnapshot` (from `context/`), an already-computed
`SignalExplanation` (from `signals/explainability.py`, itself built
from `SignalQualityResult`), `asset`/`timeframe` (strings, passed in
by `core/pipeline.py`), and an optional `HTFBiasResult` (from
`context_layer/trend/htf_bias.py`, passed in externally, same pattern as Decision
Engine v2/Market Regime).

## Output
`MarketFeatures` (`asset`, `timeframe`, `htf_bias`, `market_regime`,
`session`, `signal_quality`, `confidence`, `volatility`,
`trend_strength`, `liquidity_distance`, `volume`, `atr`) — one per
candidate, never raises even on an empty/minimal context.

## Dependencies
`context_layer.trend.market_regime` (for `MarketRegime`) — an already-existing
`context/` computation, no new indicator — and `signals.explainability`
(for `SignalExplanation`, `TYPE_CHECKING`-only). No dependency on
`strategies/`, `ai/`, `decision/`, `risk/`, `database/`, or
`telegram/`.

## Future Roadmap
See `docs/FEATURE_ENGINEERING.md`'s "Future ML usage" section — a
real Wilder ATR, a real volume source once one exists, a backtest
harness replaying `compute_market_features()` over historical
candles, ML dataset export, and Failure Analysis (joining
`MarketFeatures` against actual trade outcomes) are all named,
explicit future steps, none implemented in this phase.
