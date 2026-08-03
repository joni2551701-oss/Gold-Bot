# GoldBot Foundation Gap Analysis (Phase A1, Task 3)

For each roadmap item named in the Phase A1 brief: **READY** / **PARTIAL**
/ **MISSING**, with the concrete evidence behind the classification —
every claim here was verified against actual source this phase, not
assumed. No code was changed to produce this analysis.

## Summary table

| Item | Status | Priority |
|---|---|---|
| HTF Bias | PARTIAL | HIGH |
| Wyckoff | MISSING | HIGH |
| Trading Style | PARTIAL (cosmetic only) | MEDIUM |
| Asset Manager | MISSING | MEDIUM |
| Session Intelligence | PARTIAL | MEDIUM |
| Market Regime | MISSING | MEDIUM |
| Economic Calendar | MISSING | LOW |
| Explainability | PARTIAL | LOW |
| Signal Quality Score | MISSING | HIGH |
| Data Quality | PARTIAL | MEDIUM |
| Feature Flags | MISSING | LOW |
| Configuration Management | PARTIAL | LOW |

---

### 1. HTF Bias — **PARTIAL**, Priority: **HIGH**

The single most encouraging finding of this audit: **the hard part is
already built, just not connected.**

- `data_layer/live_data/market_data.py`'s `MarketDataNormalizer.get_snapshot(symbol,
  intervals)` fetches and normalizes **multiple timeframes in one
  call** (`Config.TIMEFRAME_HISTORY` already defines M5/M15/H1/H4
  sizing), returning a `MarketSnapshot` with one candle list per
  interval — exactly the input shape an H4/H1 → M15 execution-context
  bias engine would need.
- **But `core/pipeline.py` never calls `get_snapshot()`.** It calls
  the single-timeframe `get_candles()` instead (`core/pipeline.py`
  line 108, re-confirmed this phase) — the pipeline only ever sees one
  interval (`M15`) per run, never H4/H1 alongside it.
- No `HTFBias` type, no bias-classification function, and no field on
  `ContextSnapshot` for it exist anywhere — `context_config.py` line
  12 names "HTF bias" only as a forward-looking comment.
- **Reason real-market validation needs this**: without an HTF bias
  gate, every M15 setup is evaluated in isolation from the higher-
  timeframe trend — exactly the gap the roadmap's "H4/H1 Analysis →
  HTF Bias → M15 Execution Context" diagram names.

**What's genuinely missing** (see `docs/v0.3.5_SPECIFICATION.md`):
(a) wiring `core/pipeline.py` to call `get_snapshot()` for H4+H1+M15
instead of `get_candles()` for M15 alone; (b) a new bias-classification
function/module (context-layer, pure function, same shape as
`market_structure.py`'s `classify_structure()`); (c) a new
`ContextSnapshot` field to carry the result; (d) a decision on whether/
how `DecisionEngine.evaluate()` incorporates it (see Decision Engine
finding below — currently a flat 2-input average with no room for a
third input).

---

### 2. Wyckoff — **MISSING**, Priority: **HIGH**

- No file, class, function, or even a comment naming Wyckoff phases
  (Accumulation/Markup/Distribution/Markdown), Spring, UTAD, or phase
  detection exists anywhere in the codebase — confirmed by a
  case-insensitive full-repo grep this phase.
- `context_layer/amd/amd.py`'s Accumulation-Manipulation-Distribution cycle
  detector uses **overlapping vocabulary** (`ACCUMULATION`/
  `DISTRIBUTION` appear as `AmdEventType` values) but is a distinct,
  narrower SMC concept — it correlates a liquidity sweep
  (Manipulation) with a subsequent structural break (Distribution),
  not a multi-phase Wyckoff schematic with volume analysis, Spring/
  UTAD tests, or explicit phase boundaries (A/B/C/D/E).
- No volume data is fetched or normalized anywhere in `data/` — a real
  Wyckoff engine's phase/Spring/UTAD tests conventionally lean on
  volume confirmation, which this codebase has no source for today
  (Twelve Data's candle payload is OHLC-only in `data_layer/providers/twelve_data_client.py`,
  re-confirmed this phase).
- **Reason this is HIGH priority per the roadmap**: named explicitly
  as a "multi-market framework" foundation piece — Wyckoff's phase
  model is symbol/asset-class-agnostic (works the same on Gold, Forex,
  or Crypto), unlike the current SMC strategies which were built and
  tuned specifically around XAUUSD's behavior.

**What's genuinely missing**: everything — a `context_layer/wyckoff/wyckoff.py`
(or new subpackage) detector, a `WyckoffPhase` enum, a
`strategies/wyckoff_strategy.py`, and (if phase/Spring/UTAD detection
is meant to use volume) a volume data source, which does not exist in
`data/` today. This is the largest single gap found in this audit.

---

### 3. AMD Strategy — status confirmed, not a gap

Not one of Task 3's 12 named roadmap items, but explicitly asked about
in the brief's Trading Context Audit section, so recorded here for
completeness: `context_layer/amd/amd.py` (detector, 30% test coverage — lowest
in the repo) and `strategies/amd_strategy.py` (candidate generator,
37% coverage) both exist, are registered in `strategy_manager.py`, and
do influence real `SignalCandidate` output — re-confirmed by reading
`strategy_manager.py`'s `self.strategies` list this phase. Status:
**built and wired in, but the least-tested code in the `context/`+
`strategies/` layers** — a test-coverage gap, not a missing-component
gap.

---

### 4. Trading Style — **PARTIAL (cosmetic only)**, Priority: **MEDIUM**

- `database/user_models.py`'s `UserRecord.trading_style` field exists,
  is persisted (`database/models.py` line 134, `TEXT DEFAULT
  'Intraday'`), is settable via the `/strategy` Telegram command
  ("Change trading style" per `telegram/commands.py`), and is
  displayed back to the user in their profile
  (`telegram/handlers.py` line 217).
- **It is never read by `core/pipeline.py`, `decision/`, `risk/`, or
  any `strategies/*.py` file** — confirmed by a full-repo grep this
  phase limited to exactly one non-display, non-storage hit (none
  found). The pipeline generates and broadcasts one global decision
  per cycle to `TELEGRAM_CHAT_ID`; it has no concept of per-user
  personalization at all today.
- **Classification rationale**: PARTIAL, not MISSING, because the data
  model, storage, and UI already exist — what's missing is the
  connection from "user's stored preference" to "pipeline's actual
  signal filtering/formatting," which doesn't exist in any layer.

---

### 5. Asset Manager — **MISSING**, Priority: **MEDIUM**

- No multi-asset orchestration exists — `main.py` calls
  `TradingPipeline(symbol="XAUUSD", interval="M15")` once, hardcoded,
  every scheduled run.
- **Encouraging detail**: `TradingPipeline.__init__` itself already
  takes `symbol`/`interval` as constructor parameters (not hardcoded
  at the class level), and `data_layer/providers/twelve_data_client.py`'s `XAUUSD` →
  `XAU/USD` conversion is documented as an example in its own
  docstring, not a hardcoded restriction — so the *class* is already
  symbol-parameterized; only the *entry point* (`main.py`) and the
  *scheduling* (one GitHub Actions job, one symbol) are single-asset.
- No config file or class enumerates "which symbols does GoldBot
  track," no per-symbol database partitioning need was found
  (`signals` table has no symbol column separation issue since it's
  single-symbol today), and no orchestrator exists to run N pipeline
  instances concurrently or sequentially.

**What's genuinely missing**: an `AssetManager`-shaped orchestrator
(or a config-driven symbol list `main.py` iterates), and a decision on
whether multi-asset means N sequential `TradingPipeline` runs (simple,
matches today's shape) or a genuinely concurrent architecture (bigger
change, out of scope for a specification-only phase to decide).

---

### 6. Session Intelligence — **PARTIAL**, Priority: **MEDIUM**

- `data_layer/live_data/session_filter.py`'s `is_trading_time()` is fully built:
  Tashkent-timezone-aware, Monday–Friday 08:00–23:59 window check —
  but it is **not called anywhere** (confirmed by grep this phase,
  same as `data_cache.py`) — `core/pipeline.py` runs regardless of
  session, relying entirely on
  `.github/workflows/trading_bot.yml`'s own cron window
  (`*/5 3-18 * * 1-5` UTC) to approximate a trading-hours restriction
  externally, outside any Python code path.
- This is "session gating" (when to run at all), not "session
  intelligence" in the fuller sense the roadmap likely means (e.g.
  London/New York/Asia session classification feeding into
  signal-quality scoring, or session-specific liquidity-sweep
  behavior) — no session-*classification* logic (as opposed to a
  binary trading-hours gate) exists anywhere.
- **Classification rationale**: PARTIAL — the narrowest form (a
  trading-hours boolean gate) is fully built and tested-adjacent, but
  unwired; the broader form (session-aware signal scoring) doesn't
  exist as a concept anywhere in the codebase.

---

### 7. Market Regime — **MISSING**, Priority: **MEDIUM**

- No trending-vs-ranging, volatility-regime, or any regime
  classification exists anywhere — confirmed by a case-insensitive
  full-repo grep this phase (zero hits for "regime").
- `context_layer/market_structure/market_structure.py`'s HH/HL/LH/LL classification is the
  closest existing concept (structure direction), but it operates
  candle-by-candle/swing-by-swing, not as a persistent regime state
  a strategy or the decision engine could condition on.

---

### 8. Economic Calendar — **MISSING**, Priority: **LOW**

- No news/event calendar integration, no economic-event data source,
  no pre/post-news signal suppression exists anywhere — confirmed by
  grep this phase. `TWELVE_DATA_API_KEY` is used for candle data only
  (`data_layer/providers/twelve_data_client.py`); Twelve Data does offer an economic
  calendar endpoint in principle, but nothing in this codebase calls
  it.
- **Priority rationale**: LOW relative to HTF Bias/Wyckoff/Signal
  Quality Score — those three affect every signal every cycle;
  economic-calendar awareness affects a minority of cycles (around
  scheduled news events) and is a reasonable v0.4+ concern rather than
  a v0.3.5 blocker.

---

### 9. Explainability — **PARTIAL**, Priority: **LOW**

- A textual reason/explanation trail already exists end-to-end:
  `AIAnalysisResult.explanation`, `TradeDecision.reason`,
  `RiskResult.reason` are all populated at every stage
  (re-confirmed by reading `ai/ai_analyzer.py`,
  `decision/decision_engine.py`, `risk/risk_manager.py` this phase) —
  every REJECT/NO_TRADE/APPROVE already carries a human-readable why.
- **What's missing**: no aggregated, queryable "explain this signal"
  view — the reason strings are attached to in-memory objects for one
  pipeline cycle and then (via `database/signal_record.py`'s
  `ai_decision`/`risk_status` flattened columns) partially persisted,
  but nothing surfaces the full reason chain back to a user or admin
  after the fact (no Telegram command reads
  `AIAnalysisResult.explanation` or `RiskResult.reason` from the
  database — only the flattened `ai_decision`/`risk_status` strings
  are stored, not the free-text explanation itself).
- **Classification rationale**: PARTIAL — the raw material for
  explainability exists at generation time; a persistence/retrieval
  path for it does not.

---

### 10. Signal Quality Score — **MISSING**, Priority: **HIGH**

- `DecisionEngine.evaluate()`'s entire confidence formula, read in
  full this phase:
  ```python
  final_confidence = (signal.confidence + ai_analysis.confidence) / 2
  ```
  A flat, unweighted average of exactly two inputs. There is no
  separate "Technical Score," no per-strategy weighting (a
  Liquidity-Sweep candidate and an AMD candidate contribute their
  `SignalCandidate.confidence` identically, with no visibility into
  which methodology produced it), and no third "Risk Score" input
  despite `decision/decision_engine.py` defining a `DecisionResult`
  dataclass with a `risk_score` field — that field is **dead**, never
  populated or read (confirmed by grep: zero external references to
  `DecisionResult` anywhere in the codebase).
- **Answers the brief's explicit Decision Engine Audit questions**:
  "weightlar to'g'rimi?" — there is only one weight, 0.5/0.5, applied
  uniformly; "HTF bias qo'shilganmi?" — no, HTF bias doesn't exist
  as data yet (see item 1); "strategy score mavjudmi?" — no, all
  strategies feed one opaque `confidence` float with no per-strategy
  differentiation visible to the Decision Engine.
- **Priority rationale**: HIGH — this is the formula that, combined
  with `AIAnalyzer.analyze()`'s permanent-reject stub (see
  `docs/ARCHITECTURE_AUDIT.md`), determines whether a signal ever
  reaches a user. Both items block real signal output today; both are
  natural, connected v0.3.5-adjacent specification targets even though
  neither is being implemented in this documentation-only phase.

---

### 11. Data Quality — **PARTIAL**, Priority: **MEDIUM**

Same pattern as HTF Bias: **already built, not connected.**

- `data_layer/live_data/market_data.py`'s `MarketDataNormalizer.get_snapshot()` (see
  item 1) produces a `quality: Dict[str, str]` per timeframe —
  `"OK"` / `"WARNING_GAP"` (from `_detect_missing_candles()`) /
  `"ERROR_NO_DATA"` — plus a separate `_verify_timeframe_alignment()`
  check that logs a warning if timeframes desync by more than 4 hours.
  All of this is real, working logic.
- `core/pipeline.py` calls `get_candles()`, not `get_snapshot()` — so
  none of this quality signal ever reaches the Context Engine, the AI
  layer, or gets persisted. `MarketSnapshot`/`.quality` has zero
  external readers (confirmed by grep this phase).
- The narrower validation that *is* wired in —
  `_validate_and_clean()`'s price-integrity/OHLC-relation/duplicate-
  timestamp filtering, called from the `get_candles()` path the
  pipeline actually uses — is real and active. So "data quality" as
  *input sanitization* is READY; "data quality" as *observable,
  reportable signal* is not connected anywhere.

---

### 12. Feature Flags — **MISSING**, Priority: **LOW**

- No feature-flag mechanism (environment-driven, database-driven, or
  otherwise) exists anywhere — confirmed by grep this phase. Every
  behavioral toggle found in the codebase is a hardcoded dataclass
  default (`DecisionConfig.min_confidence`, `RiskConfig`'s fields,
  `MonitorConfig.enabled`) requiring a code change (and, for
  `DecisionConfig`/`RiskConfig`, `CLAUDE.md`-mandated approval) to
  flip, not a runtime-toggleable flag.
- **Priority rationale**: LOW — genuinely useful for the v0.4+
  multi-module future (turning Wyckoff or HTF Bias on/off without a
  deploy), but nothing in the current architecture is blocked without
  it.

---

### 13. Configuration Management — **PARTIAL**, Priority: **LOW**

- `config.py`'s `Config` class centralizes environment-detection
  (`APP_ENV`/`DEBUG`), paths, and `TIMEFRAME_HISTORY` — a real, if
  minimal, central config.
- Each safety-relevant module also has its own local, dataclass-based
  config (`DecisionConfig`, `RiskConfig`, `MonitorConfig`) — a
  reasonable, already-established pattern (constructor-injectable,
  documented in each module's docstring as "extracted to allow easy
  optimization... without code changes") that a v0.3.5 `HTFBiasConfig`
  or `WyckoffConfig` could follow directly, requiring no new pattern
  to be invented.
- **What's missing**: no environment-driven override for these
  dataclass configs (they're Python-literal defaults only, not
  `.env`-readable), and no single place documenting "here is every
  tunable in the system" — each config class is independently
  discoverable only by reading its module.

---

## Recommended Order

This mirrors, and gives evidence for, the order implied by the
roadmap diagram in the Phase A1 brief:

1. **HTF Bias** — highest leverage-to-effort ratio found in this
   audit: `MarketDataNormalizer.get_snapshot()` already does the hard
   part (multi-timeframe fetch + quality/alignment checks); the
   remaining work is a new context-layer classifier plus wiring
   `core/pipeline.py` to call `get_snapshot()` instead of
   `get_candles()`.
2. **Signal Quality Score** — directly adjacent to HTF Bias (a
   redesigned `DecisionEngine.evaluate()` formula is the natural place
   an HTF-bias input would plug into), and independently justified by
   the flat/unweighted formula and dead `DecisionResult.risk_score`
   found in this audit.
3. **Wyckoff Integration** — the largest genuinely-missing piece;
   correctly sequenced after HTF Bias/Signal Quality Score since it's
   a new detector + strategy + scoring-input, not a wiring fix.
4. **Data Quality surfacing** — low effort (the data already exists in
   `get_snapshot()`'s `quality` dict, needs only a consumer), pairs
   naturally with the HTF Bias wiring work since both require the same
   `get_candles()` → `get_snapshot()` pipeline change.
5. **Session Intelligence** — extend the already-built
   `is_trading_time()` gate, then grow toward session classification.
6. **AMD Review** — not a missing component, but its 30% test coverage
   (lowest in the repo) makes it the natural next thing to harden
   once the higher-priority missing pieces above are speced.
7. **Trading Style / Asset Manager** — both PARTIAL/MISSING but lower
   urgency than the signal-quality chain above; natural v0.4-adjacent
   work once the core scoring pipeline is upgraded.
8. **Monitoring improvements** — `monitoring/performance.py`'s
   dormant `database/` dependency and `monitoring/README.md`'s
   absence, both flagged in the Architecture Audit.
9. **Remaining docs** — `core/README.md`, `strategies/README.md`,
   `monitoring/README.md`, and the stale root `README.md` (see
   `docs/DOCUMENTATION_AUDIT.md`).
10. **Feature Flags / Economic Calendar / Configuration Management
    centralization** — lowest priority; genuinely nothing in the
    current architecture is blocked without them.
