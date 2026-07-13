# data/

## Purpose
Fetches and normalizes XAUUSD market data from Twelve Data.

## Responsibilities
- Raw API calls with retry/backoff (`twelve_data_client.py`).
- Candle validation and de-duplication (`market_data.py`).
- Session/cache foundations, not yet wired into the pipeline
  (`session_filter.py`, `data_cache.py`).

## Input
Symbol, interval, output size (from `core/pipeline.py`).

## Output
`List[Candle]` — validated, chronologically ascending OHLC data.

## Dependencies
`core/secrets.py` (API key), `config.py` (timeframe sizes). No
dependency on `context/`, `signals/`, `database/`, or `telegram/`.

## Future Roadmap
Wire `SmartDataCache` in if the pipeline ever fetches more than one
symbol/interval per cycle (see `docs/performance_report.md`). Wire
`is_trading_time()` in if in-process trading-hours gating becomes
necessary beyond the GitHub Actions cron window.
