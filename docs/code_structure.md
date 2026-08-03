# GoldBot Architecture — Code Structure Map

Top-level map of every package in the repository and its
responsibility. For deeper detail on a specific layer, see the
dedicated docs linked inline; this file is the index, not a
replacement for them.

## Shape

```
Market Data (data/)
      v
Context Engine (context/)
      v
Strategies (strategies/)
      v
Signal Generation (signals/)
      v
AI Layer (ai/)
      v
Decision Engine (decision/)
      v
Risk Manager (risk/)
      v
Execution Layer (execution/)  -- inert in v0.2, manual execution only
      v
Database (database/) <----> Telegram Product Layer (telegram/)
      ^
      |
Monitoring (monitoring/) -- reads persisted signals, not wired to any live command yet
```

`core/pipeline.py` (`TradingPipeline`) wires Data through Persistence
into one synchronous `run()`, invoked by `main.py` on a schedule
(`.github/workflows/trading_bot.yml`). `platform_layer/telegram/polling.py` is a
separate, long-running process for the Telegram product layer — see
`docs/telegram_layer.md` for its full shape and permission model.

## Modules

### `core/`
Cross-cutting infrastructure used by every other layer: `pipeline.py`
(the `TradingPipeline` orchestrator), `logger.py` (one shared
`setup_logger()`), `secrets.py` (the only place environment variables
holding credentials are read).

### `data/`
Market data acquisition and normalization.
- `twelve_data_client.py` — `TwelveDataClient`, raw Twelve Data API
  calls with retry/backoff; defines the `Candle` dataclass used
  throughout the codebase.
- `market_data.py` — `MarketDataNormalizer`, validates and cleans raw
  candles (rejects inverted OHLC, de-duplicates by timestamp) before
  anything downstream sees them; fails gracefully (`[]`) on any error,
  including a missing API key.
- `data_cache.py` — `SmartDataCache`, a complete disk-persisted
  caching layer built to reduce redundant API calls. Not currently
  wired into `TradingPipeline` (see Phase 48 audit / Phase 50+
  backlog) — kept intentionally as staged v0.3+ work, not dead code to
  delete.
- `session_filter.py` — `is_trading_time()`, a Tashkent
  business-hours gate. Same status as `data_cache.py`: built, not yet
  wired in, intentionally deferred.

### `context/`
Smart Money Concepts market-structure analysis. Pure functions over a
`Sequence[Candle]`, no I/O, no mutable state between calls.
- `candle.py` — single source of truth for candle sentiment
  (`is_bullish`/`is_bearish`/`is_doji`, wick/body/range helpers).
- `market_structure.py` — swing-point detection and HH/HL/LH/LL
  classification.
- `bos.py` / `choch.py` — Break of Structure / Change of Character
  detection from classified swings.
- `liquidity.py` — equal-highs/lows clustering and liquidity sweep
  detection.
- `order_block.py` — last opposite-direction candle before a
  sweep-confirmed break.
- `fvg.py` — Fair Value Gap (3-candle imbalance) detection.
- `amd.py` — Accumulation-Manipulation-Distribution cycle detection,
  correlating sweeps with subsequent structural breaks.
- `context_orchestrator.py` — `ContextEngine`/`build_context_snapshot()`,
  runs all of the above in sequence and returns one immutable
  `ContextSnapshot`.

### `strategies/`
Independent Smart-Money-Concepts strategies, each stateless and
isolated: `amd_strategy.py`, `fvg_strategy.py`, `liquidity_strategy.py`.
`strategy_manager.py` (`StrategyManager`) runs all registered
strategies against one `ContextSnapshot` and aggregates their
`SignalCandidate` output — no dedup or ranking at this layer (that
happens in the Signal Layer, below).

### `signals/`
- `models.py` — `SignalCandidate`, the immutable data contract every
  strategy produces and every downstream layer (AI/Decision/Risk/
  Telegram) consumes.
- `signal_engine.py` — `SignalEngine`, a thin router to
  `StrategyManager`.

The candidate-filtering and single-best-candidate selection that
prevents duplicate Telegram notifications lives in
`core/pipeline.py`'s `TradingPipeline.run()`, not in `signals/` itself.

### `ai/`
- `ai_analyzer.py` — `AIAnalyzer.analyze()`, currently a stub that
  always returns `approved=False` (documented in the README and the
  Phase 48 audit as the top v0.3+ item — not a hidden bug).
- `confidence_model.py` — deterministic technical confidence scoring,
  built but not yet called by `AIAnalyzer`.
- `ai_prompt.py` — Gemini prompt/schema builder, built but not yet
  called.
- `trade_journal.py` — a complete trade-outcome record model, not yet
  wired to any writer.

### `decision/`
- `decision_engine.py` — `DecisionEngine.evaluate()`, blends signal
  and AI confidence and returns `APPROVE`/`REJECT`/`NO_TRADE`.
- `models.py` — `TradeDecision`, `DecisionAction`.

### `risk/`
`risk_manager.py` — `RiskManager.evaluate()`, the only layer allowed
to compute risk/reward and position sizing. Validates SL/TP geometry
(BUY: `stop_loss < entry < take_profit`; SELL: mirrored) and
stop-loss distance before approving; a sizing suggestion only, no
broker/MT5 dependency.

### `execution/`
`execution_engine.py` / `signal_lifecycle.py` — scaffolding for future
MT5 order dispatch. Both unconditionally return "not implemented" and
are not imported by `core/pipeline.py` or `main.py`. GoldBot v0.2 does
not place trades automatically; execution is manual.

### `monitoring/`
- `performance.py` — `PerformanceTracker`, complete win-rate/strategy-
  breakdown statistics reading from `SignalRepository`. Not yet wired
  to a Telegram command.
- `signal_monitor.py` — inert stub, same status as `execution/`.

### `database/`
SQLite persistence — the only place SQL is written. One
repository/model pair per table (`users`, `signals`, `subscriptions`,
`feedback`, `admins`); every query is parameterized. See
`docs/database_schema.md` for the full column-by-column schema and
`database_layer/database_manager/models.py` for idempotent, `PRAGMA`-guarded migrations.

### `telegram/`
The Telegram product layer — registration, settings, subscriptions,
signal access control, admin panel, feedback. See
`docs/telegram_layer.md` for the full routing/permission/service map
and `docs/commands_reference.md` for every command.

## Related docs

- `docs/telegram_layer.md` — Telegram service/permission map.
- `docs/database_schema.md` — table-by-table schema.
- `docs/commands_reference.md` — every Telegram command.
- `docs/v0.2_release_notes.md` — v0.2 release notes.
- `docs/AUDIT_REPORT.md` — Phase 48 full-system audit (findings this
  cleanup phase acted on).
