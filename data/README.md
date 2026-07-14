# data/

## Purpose
Fetches and normalizes XAUUSD market data from Twelve Data.

## Flow
```
Twelve Data API
      |
      v
data/   -- fetch + validate + de-duplicate
      |
      |-- get_candles()  (single timeframe)   -> Context Engine
      '-- get_snapshot() (Daily/H4/H1)        -> context/htf_bias.py
                                                  (Phase A2)
```

## Responsibilities
- Raw API calls with retry/backoff (`twelve_data_client.py`).
- Candle validation, de-duplication, and multi-timeframe snapshotting
  with per-timeframe data-quality flags (`market_data.py`).
- Session/cache foundations, not yet wired into the pipeline
  (`session_filter.py`, `data_cache.py`).

## Input
Symbol, interval, output size (from `core/pipeline.py`) for
`get_candles()`. Symbol + a list of intervals for `get_snapshot()`
(called by `core/pipeline.py`'s HTF Bias stage with
`context.htf_bias.SUPPORTED_HTF_TIMEFRAMES`, Phase A2).

## Output
`List[Candle]` (`get_candles()`) — validated, chronologically
ascending OHLC data for one timeframe. `MarketSnapshot`
(`get_snapshot()`) — the same, keyed by timeframe, plus a
`quality: Dict[str, str]` (`"OK"`/`"WARNING_GAP"`/`"ERROR_NO_DATA"`)
per timeframe.

## Dependencies
`core/secrets.py` (API key), `config.py` (timeframe sizes, including
`"Daily"` as of Phase A2). No dependency on `context/`, `signals/`,
`database/`, or `telegram/`.

## Future Roadmap
Wire `SmartDataCache` in if the pipeline ever fetches more than one
symbol/interval per cycle (see `docs/PERFORMANCE.md`). Wire
`is_trading_time()` in if in-process trading-hours gating becomes
necessary beyond the GitHub Actions cron window.
