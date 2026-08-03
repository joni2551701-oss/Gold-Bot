# Data Quality Engine Foundation (Phase A8)

## Purpose

Assesses the quality of the candle list `MarketDataNormalizer.get_candles()`
already returned — missing candles, duplicate timestamps, invalid
OHLC, and timeframe consistency — into a structured, scored report.
**Data Quality is observability, not gatekeeping.** It never blocks,
filters, or alters the candles the rest of the pipeline uses, even
when the result says `valid=False`. See `context/market_regime.py`'s
sibling docs for the same "context, not a decision" framing applied
here to data instead of price action.

This phase exists because Phase A1's audit found data quality as
*input sanitization* (silent filtering) was real and active for the
M15 path, but data quality as an *observable, reportable signal* was
not connected anywhere — the same gap Phase A2 found and closed for
HTF Bias's multi-timeframe fetch, applied here to the primary
execution-timeframe fetch.

## Pipeline position

```
TwelveData API
      |
      v
Market Data (data_layer/live_data/market_data.py's get_candles(),
              already fetches + silently cleans, unchanged)
      |
      v
Data Quality (data_layer/data_validation/data_quality.py, Phase A8 -- NEW)
      |         assess_data_quality(candles, interval)
      |         -> DataQualityResult, purely observational
      v
Context Engine (unchanged -- receives the same candles
                 Data Quality just assessed, whether or
                 not any issue was found)
```

"Minimal: after the Market Data layer" per this phase's brief — Data
Quality runs on the pipeline's already-fetched candle list, not
instead of or before `get_candles()`'s own fetch/clean step. This is
a deliberate scope boundary, not an oversight: no new data provider,
and `data_layer/live_data/market_data.py`'s existing fetch/validate/clean behavior is
completely unchanged by this phase.

## Relationship to `data_layer/live_data/market_data.py`

`MarketDataNormalizer._validate_and_clean()` already silently filters
out invalid-price, bad-OHLC, and duplicate-timestamp candles before
anything downstream ever sees them; `_detect_missing_candles()`
already logs (but doesn't structurally report) a gap. Both are
**private instance methods** on a class that already feeds the real,
live M15 pipeline path — this phase deliberately does **not** reuse
them directly (would mean either changing `market_data.py`'s public
interface or reaching into its "private" methods) and does **not**
modify `market_data.py` at all. This mirrors the exact reasoning
`docs/WYCKOFF.md`'s "Relationship to AMD" section already established
for a strategy-feeding file: independently-implemented, smaller-blast-
radius logic in a new module, over reusing/modifying an already-tested,
production-critical file. `data_layer/data_validation/data_quality.py` therefore
independently implements its own OHLC/duplicate/gap checks — a small,
deliberate, documented duplication of *intent*, not of code (see that
module's own docstring for the same explanation).

One practical consequence: on real production data, `assess_data_quality()`'s
`invalid_ohlc`/`duplicate_candle` checks will typically find nothing,
since `_validate_and_clean()` has already removed those candles
upstream. They remain as defense-in-depth observability (this
visibility didn't exist at all before this phase) and because
`assess_data_quality()` is a general-purpose function any caller could
hand an arbitrary candle list, not only one that already passed
through `MarketDataNormalizer`.

## Model

```python
@dataclass(frozen=True)
class DataQualityResult:
    valid: bool            # True only when issues is empty
    score: float           # 0-100
    issues: Sequence[str]  # one entry per distinct issue type found
```

Example (matching the brief's own worked examples):
```json
{"valid": true, "score": 100.0, "issues": []}
{"valid": false, "score": 60.0, "issues": ["missing_candle", "duplicate_candle"]}
```

## Quality checks

| Check | Detects | Issue name | Penalty |
|---|---|---|---|
| Missing candle | A gap strictly larger than the interval's expected delta, and smaller than 1 day (matching `market_data.py`'s own weekend/holiday-gap convention) | `missing_candle` | 15 |
| Duplicate candle | Two or more candles sharing the same timestamp | `duplicate_candle` | 10 |
| OHLC validation | `high < max(open, close)` or `low > min(open, close)` — a physically impossible candle | `invalid_ohlc` | 25 |
| Timeframe consistency | A gap strictly smaller than the interval's expected delta (e.g. 5-minute spacing inside M15 data) | `timeframe_mismatch` | 15 |
| Empty data | `candles == []` | `empty_data` | score fixed at `0.0` |

`score` starts at `100.0` and subtracts each detected issue's penalty
once (not once per bad candle), floored at `0.0`. `valid` is `True`
only when `issues` is empty — `score` communicates *how bad*, `valid`
communicates *pass/fail*, and they can diverge in the sense that a
single mild issue still makes `valid=False` even at a relatively high
score.

An unrecognized `interval` (not `M5`/`M15`/`H1`/`H4`/`Daily`) simply
skips the gap/timeframe-consistency checks — never raises.

## Pipeline integration

New stage in `core/pipeline.py`, immediately after `market_data`:

```
stage=market_data duration=...
stage=data_quality duration=...   <- new
stage=htf_bias duration=...
```

`TradingPipeline.run()`'s result dict gains one new key:

```python
{
    "context": ...,
    "data_quality": DataQualityResult(valid=True, score=100.0, issues=()),
    "htf_bias": ...,
    ...
}
```

No new `"market_data"` key was added — the candle list is already
reachable via `result["context"].candles`; only the new
`DataQualityResult` is genuinely new information.

## What this does NOT do

- Does not add a new data provider or change how `get_candles()`
  fetches data.
- Does not filter, drop, or repair candles — the exact list
  `get_candles()` returned is what `context/` receives, regardless of
  `data_quality.valid`.
- Does not change `strategies/`, `signals/` signal-generation logic,
  `ai/`, or `decision/decision_engine.py`.
- Does not persist `DataQualityResult` anywhere — no schema change, no
  new table.
- Does not block a pipeline cycle below any quality threshold — that
  would be a policy decision belonging to a future, separately-
  approved phase.

## Future usage

- **A quality-gated skip**: a future phase could have
  `core/pipeline.py` skip signal generation (or flag results) when
  `data_quality.score` falls below some threshold — not implemented
  here; this phase only reports.
- **Persistence**: if data-quality history becomes valuable (e.g. for
  spotting a degrading provider over time), persisting
  `DataQualityResult` alongside a `SignalRecord` is a natural,
  separate schema-change proposal.
- **AI input**: like `context.market_regime` (`docs/MARKET_REGIME.md`'s
  "Significance for AI" section), a `DataQualityResult` is exactly the
  kind of structured signal a future real AI provider could use to
  down-weight its own confidence when the underlying data was shaky —
  not wired in this phase.
