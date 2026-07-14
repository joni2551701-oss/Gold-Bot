# HTF Bias (Phase A2)

## Purpose

Describes the higher-timeframe (Daily/H4/H1) market state so a future
phase can weigh execution-timeframe (M15) signals against it. **HTF
Bias is context, not a decision.** It never approves, rejects, sizes,
or formats a trade — it produces one `HTFBiasResult` per pipeline
cycle that currently goes nowhere except `TradingPipeline.run()`'s
result dict, for a later, separately-approved phase (Decision Engine
v2) to consume.

This phase exists because `docs/ARCHITECTURE_AUDIT.md` (Phase A1)
found the multi-timeframe fetch/quality machinery HTF Bias needs
already existed — `data/market_data.py`'s
`MarketDataNormalizer.get_snapshot()` — but was never called by
`core/pipeline.py`. This phase wires that connection and adds the one
piece that didn't exist: the actual bias classification.

## Architecture

```
Market Data (data/)
      |
      |-- MarketDataNormalizer.get_candles()        (unchanged, M15)
      |         |
      |         v
      |   Context Engine -> Strategies -> ... (unchanged)
      |
      '-- MarketDataNormalizer.get_snapshot()        (Phase A2, new call site)
                |  Daily + H4 + H1 candles, per-timeframe quality flags
                v
          context/htf_bias.py
                |  compute_htf_bias(snapshot) -> HTFBiasResult
                v
          TradingPipeline.run()'s result dict ("htf_bias")
                |
                v
          (nothing consumes it yet -- Decision Engine v2, a future,
           separately-approved phase, is where a real consumer
           would be added)
```

HTF Bias is a **sibling** stage to the execution-timeframe fetch, not
a replacement for it — `core/pipeline.py` still calls `get_candles()`
for M15 exactly as before. The HTF fetch is independent, best-effort,
and additive: a failure anywhere in the HTF path (network error,
malformed data, an unexpected exception) degrades to
`HTFBias.UNKNOWN` with `confidence=0.0`, logs a warning, and never
raises — the rest of the pipeline cycle (Context, Strategies, Signal,
AI, Decision, Risk, Telegram, Database) runs exactly as it did before
this phase, unaffected by an HTF fetch failure.

**Reuse, not duplication** (per `CLAUDE.md`'s "No duplicate logic"
rule):
- Multi-timeframe fetch, candle validation, gap detection, and
  timeframe-alignment checking: `data/market_data.py`'s
  `MarketDataNormalizer.get_snapshot()` — unchanged logic, only two
  new dict entries added (`"Daily"` in `TwelveDataClient.INTERVAL_MAP`
  and `MarketDataNormalizer.expected_deltas`) so the existing gap
  detection covers the new timeframe instead of silently skipping it.
- Swing/structure classification: `context/market_structure.py`'s
  `detect_swing_points()`/`classify_structure()` — the exact same
  functions `context/context_orchestrator.py` already uses for the
  execution timeframe, called here once per HTF timeframe instead.

No detector, validator, or fetch routine was rewritten or copied to
produce this feature.

## Inputs

`context/htf_bias.py`'s `compute_htf_bias()` takes a
`data.market_data.MarketSnapshot` — the same object
`get_snapshot(symbol, ["Daily", "H4", "H1"])` already returns, keyed
by timeframe:
- `snapshot.candles: Dict[str, List[Candle]]`
- `snapshot.quality: Dict[str, str]` (`"OK"` / `"WARNING_GAP"` /
  `"ERROR_NO_DATA"`, per timeframe — already computed by
  `get_snapshot()`, not recomputed here)

## Outputs

`HTFBiasResult` (immutable dataclass):

| Field | Type | Meaning |
|---|---|---|
| `bias` | `HTFBias` enum | `BULLISH` / `BEARISH` / `NEUTRAL` / `UNKNOWN` — see "Confidence meaning" below for how this is derived. |
| `confidence` | `float`, 0–100 | How much of the 3 supported timeframes agreed on the winning direction. Not a trade confidence — see below. |
| `timeframes` | `Sequence[str]` | Which of `SUPPORTED_HTF_TIMEFRAMES` had usable candle data this call (may be fewer than 3). |
| `quality_score` | `float`, 0.0–1.0 | Fraction of the 3 timeframes `MarketSnapshot.quality` marked `"OK"` — a direct readout of `get_snapshot()`'s existing quality dict, not a new quality check. |

`HTFBias` never contains `BUY`/`SELL` or any execution instruction —
only the four values above.

## Confidence meaning

Each of the 3 supported timeframes (Daily, H4, H1) independently
classifies as `BULLISH` (most recent confirmed structure point is a
Higher High or Higher Low), `BEARISH` (most recent confirmed point is
a Lower High or Lower Low), or `UNKNOWN` (no candle data, or not
enough candles yet to confirm any structure — the same "first
occurrence" semantics `context/market_structure.py`'s
`classify_structure()` already uses).

The overall result:
- **All known timeframes agree** → that direction, confidence =
  `(agreeing count / 3) * 100` (so 2-of-3 agreeing with 1 UNKNOWN
  timeframe scores 66.67, not 100 — an UNKNOWN timeframe never counts
  toward either side).
- **Known timeframes split evenly** (e.g. 1 bullish, 1 bearish, 1
  unknown) → `NEUTRAL`, confidence `50.0`.
- **No timeframe resolved to bullish or bearish at all** → `UNKNOWN`,
  confidence `0.0`.

This is a **timeframe-agreement score**, not a probability or a
trade-quality signal — a future Decision Engine v2 that wants to use
this as a weighted input is expected to define its own interpretation
of what a given confidence level should mean to the final trade
decision. This phase deliberately does not make that call (see
`docs/v0.3.5_SPECIFICATION.md`'s Decision Engine v2 section).

## Supported timeframes

**Daily, H4, H1 only** — the execution timeframe (M15, unchanged) is
never part of the HTF set, and no M1/M5 logic exists in this module.
`context/htf_bias.py`'s `SUPPORTED_HTF_TIMEFRAMES` is the single
source of truth for this list.

## What this module does NOT do

- Does not generate a `BUY`/`SELL` signal.
- Does not call, modify, or receive input from `strategies/`,
  `signals/`, `ai/`, `decision/`, or `risk/` — `HTFBiasResult` is
  computed independently and is not passed into any of those layers'
  functions.
- Does not change `ContextSnapshot`'s fields, `SignalCandidate`,
  `TradeDecision`, `RiskResult`, or any existing function signature.
- Does not block, delay-gate, or filter the existing pipeline in any
  way — even a total HTF fetch failure only affects the `"htf_bias"`
  key in `run()`'s result dict, never the signal/decision/risk/
  telegram/database stages.
- Does not write to the database — no schema change, no new table, no
  persistence of `HTFBiasResult` anywhere (Task 8's explicit boundary
  for this phase).

## Future expansion

- **Decision Engine v2** (a separate, future, explicitly-approved
  phase — see `docs/v0.3.5_SPECIFICATION.md`) is where
  `HTFBiasResult` would become a real input to the final trade
  confidence, e.g. as an alignment bonus/penalty rather than a fourth
  averaged term.
- **Persistence**: if HTF bias history becomes valuable for analytics
  or backtesting, persisting `HTFBiasResult` alongside a
  `SignalRecord` is a natural, separate schema-change proposal — not
  part of this phase.
- **Per-timeframe weighting**: today Daily/H4/H1 count equally toward
  `confidence`. A future phase could weight them differently (e.g.
  Daily counting more than H1) — not implemented here, kept
  intentionally simple for this foundation phase.
