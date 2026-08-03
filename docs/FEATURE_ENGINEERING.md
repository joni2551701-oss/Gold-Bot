# Feature Engineering Foundation (Phase A10)

## Purpose

Builds one standard `MarketFeatures` snapshot per signal candidate —
`asset`, `timeframe`, `htf_bias`, `market_regime`, `session`,
`signal_quality`, `confidence`, `volatility`, `trend_strength`,
`liquidity_distance`, `volume`, `atr` — entirely from results already
computed elsewhere in the pipeline. **This is a standardization
layer, not an analysis layer.** It does not detect anything itself;
it turns Context Engine's, Signal Quality Score's, and
Explainability's already-computed results into one flat, stable
shape. No new indicator, no ML model, no strategy logic, no
signal-scoring change.

This phase exists because a future AI Analyzer, backtester, ML
dataset exporter, or Failure Analysis module each need the same
underlying market context and candidate-quality read, but without a
standard shape each would independently re-derive its own subset from
raw `ContextSnapshot`/`SignalQualityResult`/`SignalExplanation`
fields — the same "everyone re-reads raw candles" problem HTF Bias
(Phase A2) and Signal Quality Score (Phase A4) already solved for
their own narrower questions. `MarketFeatures` is the single,
documented answer to "what did this candidate look like, in full,"
reusable by all future consumers without any of them re-calling
Context/Strategy/Signal Quality/Explainability themselves.

## Design Rules

- Existing Context Engine, Signal Quality Score, and Explainability
  outputs are reused as-is; no detection/grading algorithm is
  reimplemented.
- Feature Engineering is a normalization layer, not an analysis
  layer — it runs at the **end** of the per-candidate analysis chain
  (after Signal Quality Score and Explainability), not before it.
- No new technical indicator is introduced (ATR, RSI, MACD, etc.).
- Unsupported values (`volume`, `atr`) remain explicit `None`
  placeholders, never synthetic estimates.
- The output model is stable and extensible so future AI, Research,
  Backtesting, and Analytics modules can consume it without schema
  changes.

## Model

```python
@dataclass(frozen=True)
class MarketFeatures:
    asset: str
    timeframe: str
    htf_bias: str                # e.g. "BULLISH"
    market_regime: str           # e.g. "TRENDING"
    session: str                 # e.g. "LONDON"
    signal_quality: str          # e.g. "A+"
    confidence: float            # 0-100
    volatility: str              # "HIGH"/"LOW"/"NORMAL"/"UNKNOWN"
    trend_strength: float        # 0.0-1.0
    liquidity_distance: Optional[float]
    volume: Optional[float] = None
    atr: Optional[float] = None
```

## How each field is computed (all reused, none re-derived)

| Field | Source | Notes |
|---|---|---|
| `asset` | Passed in by `core/pipeline.py` (`self.symbol`) | The symbol this cycle analyzed. |
| `timeframe` | Passed in by `core/pipeline.py` (`self.interval`) | The execution interval this cycle analyzed. |
| `htf_bias` | `HTFBiasResult.bias` (Phase A2, passed in externally, same pattern as Decision Engine v2/Market Regime) | `"UNKNOWN"` if no `HTFBiasResult` was supplied. |
| `market_regime` | `context.market_regime.MarketRegimeResult.regime` (Phase A7) | Direct `.value` read. |
| `session` | `context.session_events[-1].session` (Phase A6) | The most recent session transition's session. `"UNKNOWN"` if no session data. |
| `signal_quality` | `signal_layer.signal_scoring.explainability.SignalExplanation.quality` (Phase A9, itself `SignalQualityResult.grade.value`, Phase A4) | Relayed as-is — Feature Engineering does not grade anything itself. |
| `confidence` | `signal_layer.signal_scoring.explainability.SignalExplanation.confidence` (Phase A9, itself `SignalCandidate.confidence * 100`) | Relayed as-is, never recomputed. |
| `volatility` | `context.market_regime.MarketRegimeResult.regime` (Phase A7) | Direct read: `HIGH_VOLATILITY`→`"HIGH"`, `LOW_VOLATILITY`→`"LOW"`, `UNKNOWN`→`"UNKNOWN"`, anything else→`"NORMAL"`. No new volatility calculation. |
| `trend_strength` | `context.market_regime.MarketRegimeResult.confidence` (Phase A7) | `confidence / 100.0` when `regime == TRENDING`, else `0.0`. The exact same HTF+structure-agreement signal Market Regime already computed — not a new trend calculation. |
| `liquidity_distance` | `context.liquidity_zones` (unchanged) | Absolute distance from the most recent candle's close to the nearest zone's price. `None` if no candles or no zones. |
| `volume` | — | Always `None` — see "Volume hook" below. |
| `atr` | — | Always `None` — see "ATR hook" below. |

### ATR hook

`atr` is always `None` in this phase. A textbook Average True Range
(`max(high-low, |high-prev_close|, |low-prev_close|)`, typically
Wilder-smoothed over a fixed period) is a genuinely new indicator —
out of scope for a standardization-only foundation phase whose rule
is "no new technical indicators." A real ATR is deferred to a future,
separately-approved phase (Advanced Risk / Quant Research / ML), at
which point only `feature_engine.py`'s `atr=None` line would need to
change.

### Volume hook

`volume` is always `None`. This codebase has no volume data source at
all — `data_layer/providers/twelve_data_client.py`'s `Candle` is OHLC-only, confirmed
repeatedly since Phase A1's architecture audit. `volume` is an
honest, named hook, never a fabricated number. Wiring in a real
volume source is a future, separately-approved phase; only
`feature_engine.py`'s `volume=None` line would need to change.

## Pipeline position

```
Context Engine
      |
      v
Strategy Engine (signal candidates)
      |
      v
Signal Quality Score  -- per-candidate letter grade (Phase A4)
      |
      v
Explainability  -- per-candidate reasons + quality + confidence (Phase A9)
      |
      v
Feature Engineering (features/feature_engine.py, Phase A10)
      |         compute_market_features(context, explanation, asset, timeframe, htf_bias)
      |         -> MarketFeatures, one per candidate
      v
AI Layer   -- unchanged; does not read MarketFeatures in this phase
```

Feature Engineering runs at the **end** of the per-candidate analysis
chain, not between Context and Strategy — putting it before Strategy
would eventually pull it into reimplementing strategy logic just to
know what a candidate looks like. Instead it is the layer that
converts everything already known about a candidate (Context,
Strategy's own candidate, Signal Quality's grade, Explainability's
confidence) into one standard, exportable object. One
`MarketFeatures` per `SignalCandidate` — same list shape as
`quality_results`/`explanations`, not the once-per-cycle shape HTF
Bias/Market Regime use. `TradingPipeline.run()`'s result dict gains
one new key, `"features"` (`List[MarketFeatures]`, same order as
`"signals"`).

## What this does NOT do

- Does not train, run, or reference any ML model.
- Does not change `strategies/*.py`, `signal_layer/signal_engine/signal_engine.py`,
  `signal_layer/signal_scoring/signal_quality.py`'s scoring, `signal_layer/signal_scoring/explainability.py`,
  `ai/`, or `decision_layer/decision_engine/decision_engine.py` — none are modified by this
  phase, and none read `MarketFeatures`.
- Does not grade, explain, or re-derive anything itself — `signal_quality`/
  `confidence` are relayed from `SignalExplanation`, not recomputed.
- Does not implement a real ATR or fabricate a volume value.
- Does not persist `MarketFeatures` anywhere — no schema change, no
  new table.
- Does not implement backtesting or a research harness — `features/`
  only produces the standard shape a future one would consume.

## Significance for AI

`ai/ai_analyzer.py`'s `AIAnalyzer.analyze()` is still a permanent-
reject heuristic stub (`docs/AI_ARCHITECTURE.md`). `MarketFeatures` is
exactly the flat, numeric/categorical shape a future real AI
provider's prompt or feature vector would want for a specific
candidate — one object per candidate, already carrying the market
context (`htf_bias`, `market_regime`, `session`, `volatility`,
`trend_strength`, `liquidity_distance`) alongside the
candidate-quality read (`signal_quality`, `confidence`), instead of
re-deriving either from raw `ContextSnapshot`/`SignalQualityResult`
on every call. It is already sitting in `run()`'s result dict
(`"features"`), the same "available, not yet consumed" posture Market
Regime (`docs/MARKET_REGIME.md`) and Explainability
(`docs/EXPLAINABILITY.md`) both have.

## Future ML usage

- **Backtesting**: `compute_market_features()` is a pure function
  over already-computed results — a future backtest harness could
  replay historical candles through the existing `context/`/
  `signals/` pipeline and call this function identically to how
  `core/pipeline.py` does live, producing a consistent feature history
  without new code here.
- **ML dataset export**: `MarketFeatures`'s flat, dataclass shape
  (verified stable via `dataclasses.fields()` in
  `tests/features/test_feature_engine.py`) is directly serializable
  (e.g. to a CSV/Parquet row) for a future training dataset — not
  implemented in this phase.
- **Failure Analysis**: because `MarketFeatures` already carries
  `signal_quality`/`confidence` alongside full market context, a
  future module could join it against actual trade outcomes without
  re-deriving either — not implemented in this phase.
- **A real ATR / real volume**: both named above as the two
  deliberate hooks this phase carries forward, each with an explicit,
  minimal path to becoming real once the underlying data source or
  scope decision exists.
