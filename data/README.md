# data/

## Purpose
Fetches and normalizes XAUUSD market data from Twelve Data, plus
(Phase A8) assesses the resulting candle list's quality —
observationally, never filtering further.

## Flow
```
Twelve Data API
      |
      v
data/   -- fetch + validate + de-duplicate
      |
      |-- get_candles()  (single timeframe)   -> data_quality.py
      |                                           (Phase A8, NEW)
      |                                           -> Context Engine
      '-- get_snapshot() (Daily/H4/H1)        -> context/htf_bias.py
                                                  (Phase A2)
```

## Responsibilities
- Raw API calls with retry/backoff (`twelve_data_client.py`).
- Candle validation, de-duplication, and multi-timeframe snapshotting
  with per-timeframe data-quality flags (`market_data.py`).
- Scored data-quality assessment of an already-fetched candle list —
  `assess_data_quality()` (`data_quality.py`, Phase A8). Purely
  observational; does not change what `market_data.py` fetches or
  returns.
- Session/cache foundations, not yet wired into the pipeline
  (`session_filter.py`, `data_cache.py`).

### Why Data Quality Engine exists
Phase A1's audit found data quality as *input sanitization* (silent
filtering in `market_data.py`) was real, but as an *observable,
reportable signal* it was connected nowhere for the primary M15 path.
Phase A8 closes that gap with a new, independent module rather than
modifying `market_data.py` — its `_validate_and_clean()`/
`_detect_missing_candles()` are private methods on a class that
already feeds the live pipeline path, so reusing them directly was
judged higher risk than a small, documented, independently-implemented
duplication (same reasoning `docs/WYCKOFF.md`'s "Relationship to AMD"
section already established). Full detection rules and the penalty
table: `docs/DATA_QUALITY.md`.

### What Data Quality Engine does NOT do
- Does not add a new data provider, or change how `market_data.py`
  fetches or cleans candles — that file is completely unmodified.
- Does not filter, drop, or repair candles — `context/` receives the
  exact list `get_candles()` returned, regardless of
  `data_quality.valid`.
- Does not block a pipeline cycle below any quality threshold.

## Input
Symbol, interval, output size (from `core/pipeline.py`) for
`get_candles()`. Symbol + a list of intervals for `get_snapshot()`
(called by `core/pipeline.py`'s HTF Bias stage with
`context.htf_bias.SUPPORTED_HTF_TIMEFRAMES`, Phase A2).
`assess_data_quality()` takes the candle list `get_candles()` already
returned, plus the interval string.

## Output
`List[Candle]` (`get_candles()`) — validated, chronologically
ascending OHLC data for one timeframe. `MarketSnapshot`
(`get_snapshot()`) — the same, keyed by timeframe, plus a
`quality: Dict[str, str]` (`"OK"`/`"WARNING_GAP"`/`"ERROR_NO_DATA"`)
per timeframe. `DataQualityResult` (`assess_data_quality()`, Phase
A8) — `valid`, `score` (0-100), `issues` (a tuple of issue-type
names).

## Dependencies
`core/secrets.py` (API key), `config.py` (timeframe sizes, including
`"Daily"` as of Phase A2). No dependency on `context/`, `signals/`,
`database/`, or `telegram/` — `data_quality.py` follows the same
isolation as every other file in this package.

## Future Roadmap
Wire `SmartDataCache` in if the pipeline ever fetches more than one
symbol/interval per cycle (see `docs/PERFORMANCE.md`). Wire
`is_trading_time()` in if in-process trading-hours gating becomes
necessary beyond the GitHub Actions cron window. For Data Quality
Engine specifically, see `docs/DATA_QUALITY.md`'s Future Usage
section — a quality-gated cycle skip, persistence, and a future AI
input all remain unimplemented.
