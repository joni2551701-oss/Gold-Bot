# GoldBot Performance Report (Phase 53)

## Method

`main.py`'s scheduled `TradingPipeline` cannot be benchmarked
end-to-end with live data in this environment (no
`TWELVE_DATA_API_KEY`/network egress to Twelve Data or Telegram in
this sandbox — the same limitation documented in Phase 48.2). Two
measurements were taken instead, both real, both honest about their
scope:

1. **Pipeline compute stages** (Context → Signal → AI → Decision →
   Risk → Format → Persist) were benchmarked directly against a
   synthetic 200-candle series (matching `Config.TIMEFRAME_HISTORY["M15"]`),
   averaged over 20 iterations, using `time.perf_counter()`. This is
   real production code, running for real — only the market-data
   *source* is synthetic.
2. **Process startup cost** (module import time) was measured
   directly, since it doesn't depend on network access at all.

## 1. Before Benchmark

### Pipeline compute stages (200 candles, 3 strategies, averaged over 20 runs)

| Stage | Duration |
|---|---|
| Context (SMC structure detection) | 0.571 ms |
| Signal (3 strategies) | 0.005 ms |
| AI (stub) | 0.120 ms |
| Decision | 0.009 ms |
| Risk | 0.005 ms |
| Format | 0.014 ms |
| **Compute total** | **~0.72 ms** |

### Database (real SQLite, temp file)

| Operation | Duration |
|---|---|
| `SignalRepository()` construction (schema + Phase 50 index creation, one-time per pipeline run) | 14.6 ms |
| `save_signal_record()` marginal insert | 3.2 ms |

### Process startup (module import cost — measured directly, reproducible)

| Import | Duration |
|---|---|
| Bare Python interpreter startup | 13 ms |
| `import aiogram` alone | 2,435–2,553 ms (3 runs) |
| `from core.pipeline import TradingPipeline` (full transitive chain, includes aiogram) | 3,137 ms |

## 2. Bottlenecks Found

**#1 — `aiogram` import dominates every single `python main.py`
invocation, by roughly 3 orders of magnitude over everything else
combined.** The entire pipeline compute chain (Context through
Persist) totals under 1 millisecond. Importing `aiogram` alone costs
~2.5 seconds — confirmed stable across 3 repeated measurements. Every
scheduled run (`trading_bot.yml`, every 5 minutes) pays this cost
before any real work happens, because `core/pipeline.py` imports
`platform_layer.telegram.notifier` unconditionally at module load time, which
imports `platform_layer.telegram.bot`, which imports `aiogram`.

**This is not a fixable "wasted work" bottleneck — it's necessary
work that happens to be slow.** Production's real `main.py` always
constructs `TradingPipeline(..., send_notifications=True)` — it
*needs* `aiogram` loaded to actually deliver a signal to Telegram.
Making the import lazy (moving it inside `TradingPipeline.__init__()`
or `run()`) would not save any time for the real scheduled job: the
import still has to happen before a message can be sent, so the same
~2.5s is paid either at module-load time (today) or at first-use time
(after a lazy-import change) — same total cost, just relocated. It
would only help a caller that *never* sends notifications
(`send_notifications=False`, e.g. a hypothetical future backtesting
entrypoint) — not the actual production path. Per this phase's rule
("Agar katta refactor kerak bo'lsa: QILINMASIN. Avval report
qilinsin"), this is reported, not changed — see Remaining
Recommendations.

**#2 — Network I/O (Market Data fetch, Telegram delivery) is almost
certainly the real per-cycle bottleneck in production, but isn't
measurable here.** `TwelveDataClient.fetch_candles()` makes one HTTP
request per pipeline run (10s timeout, up to 3 retries with
exponential backoff on rate-limit); `Notifier.send_messages()` makes
zero-or-one HTTP request per run (at most one Telegram message per
cycle, confirmed by the Phase 48 fix). Both are real network calls
this sandbox cannot reach. Given the compute-stage numbers above (sub-
millisecond), any meaningful per-cycle latency in a real production
run is coming from these two calls, not from GoldBot's own logic.

**#3 — No duplicate API calls found within a single pipeline cycle.**
`TradingPipeline.run()` calls `get_candles()` exactly once per run
(single symbol, single interval) — there is no redundant/duplicate
fetch to eliminate today. `data_layer/market_memory/data_cache.py`'s `SmartDataCache`
(built, unused — flagged in the Phase 48 audit) exists to avoid
redundant fetches *across* separate 5-minute cron invocations, not
*within* one — its value is real but doesn't apply to the "duplicate
call in one cycle" question this phase asked. Wiring it in would mean
changing `TradingPipeline`'s data-fetch call from
`MarketDataNormalizer.get_candles(symbol, interval, outputsize)` to
`SmartDataCache.get_cached_snapshot(symbol, intervals)` — a different
method signature and a different return shape (`MarketSnapshot` with
multiple intervals vs. a flat `List[Candle]` for one) — this is a
real interface change to `core/pipeline.py`'s data layer, which
exceeds "minimal" per this phase's own file-change policy. Reported,
not applied.

**#4 — Database, memory, logging: all clean, nothing found.** See
sections 3–5 below.

## 3. Database Audit

- **Indexes**: Phase 50 already added the evidence-based indexes
  (`users.status/created_at`, `signals.status/created_at`,
  `feedback.status/created_at`); confirmed still present and actually
  consulted by the query planner
  (`tests/performance/test_database_query_speed.py::test_query_plan_uses_index_for_status_filter`
  runs `EXPLAIN QUERY PLAN` and asserts `idx_signals_status` appears).
- **`SELECT *` re-audited**: `signal_repository.py`'s 5 `SELECT *`
  calls were deliberately left un-narrowed in Phase 50 pending a fuller
  consumer audit. That audit is now done: grepping every reader of a
  signals-table row dict (`platform_layer/telegram/signal_formatter.py`,
  `core_layer/health_monitor/performance.py`, `platform_layer/telegram/admin_service.py`, and every
  test) found 16 of the table's 25 columns actually read somewhere.
  **Still not narrowed** — three reasons: (1) the expected saving is
  microseconds on a table that stays small (this app persists a
  handful of signals per day), utterly dwarfed by bottleneck #1/#2
  above; (2) `dict(row)` is deliberately flexible so `SignalRepository`
  doesn't need to track every consumer's exact column needs — narrowing
  creates an implicit, easy-to-silently-break contract across 3+
  files; (3) missing a consumer would be a real regression risk for a
  near-zero measured benefit. This is the same "report, don't force
  it" call Phase 50 made, now backed by a completed audit instead of a
  deferred one.
- **Duplicate connections**: none found — `database_layer/database_manager/database.py`'s
  `Database.__enter__()`/`__exit__()` opens and closes a connection
  per `with self.db as conn:` block, always (commit-and-close on
  success, rollback-and-close on exception). No repository holds a
  connection open across calls.
- **Full table scans**: `get_all_users()`, `get_all_subscriptions()`,
  `get_all_admins()` remain unindexed full scans (already flagged in
  the Phase 48 audit as a "Future Risk" at 10,000+ rows) — unchanged
  this phase, since these tables are still small and no query in the
  current codebase filters them by anything indexable.
- **Pagination / batch operations**: `get_recent_signals(limit=)` and
  `get_all_feedback(limit=)` already provide a `limit`-based
  foundation. True offset-based pagination isn't needed yet at current
  data volumes — noted as a future consideration, not built.

## 4. Memory Audit

- Zero `global` keyword usage anywhere in production code; zero
  module-level mutable accumulator containers (`grep` confirmed).
- `Database.__exit__()` always closes its connection, both success and
  exception paths.
- `TelegramBot.close()`/`Notifier._send_all()`'s `finally: await
  self._bot.close()` already closes the aiohttp session every run
  (confirmed present, unchanged from Phase 33.1/51).
- `main.py` invocations are one-shot OS processes (GitHub Actions
  spins a fresh runner per scheduled job) — no possibility of
  cross-run accumulation by architecture; `GoldBot`/`TradingPipeline`
  go out of scope and are reclaimed at process exit.
- `platform_layer/telegram/polling.py`'s long-running loop creates one `Bot` and one
  `Dispatcher` for the process lifetime; each incoming message
  constructs small, stateless service objects
  (`UserService()`/`AdminService()`/etc.) that are garbage-collected
  immediately after the handler returns — no per-message growth found.

**No memory findings requiring a fix.**

## 5. Logging Performance

- Zero `logger.debug()` calls anywhere (confirmed Phase 51) — no
  DEBUG noise exists to suppress.
- No secret, token, or full user-message content is ever logged
  (confirmed Phase 51's privacy audit).
- This phase's new instrumentation adds 9 INFO lines per pipeline
  cycle (`pipeline_started`, 7× `stage=... duration=...`,
  `pipeline_finished`) — at one cycle per 5 minutes in production,
  this is negligible volume, not noise, and is the direct enabler for
  diagnosing bottleneck #2 in a real deployment (the network-bound
  stages) the next time this report is updated with live numbers.

## 6. Optimizations Applied

1. **Stage-by-stage timing instrumentation** (`core/pipeline.py`):
   every stage (`market_data`, `context`, `signal`, `ai`, `decision`,
   `risk`, `telegram_format`, `telegram_delivery`, `database`) now
   logs `stage=<name> duration=<seconds>s` at INFO, bracketed by
   `pipeline_started`/`pipeline_finished` (with total duration). Purely
   additive — no stage's logic, order, or return value changed.
2. **Slow-operation detection** (`core/pipeline.py`,
   `SLOW_OPERATION_THRESHOLD_SECONDS = 2.0`): any stage exceeding 2s
   logs a `slow_operation module=TradingPipeline stage=... duration=...
   threshold=2.0s` WARNING. Monitoring only — never raises, retries, or
   alters behavior. Verified firing correctly against an artificially
   slowed stage (2.1s sleep → WARNING logged) and staying silent for
   every real (sub-millisecond) stage.
3. **Everything else audited, nothing else changed** — every other
   area (data layer, database, memory, network, logging) was found
   already sound; forcing a change with no measurable benefit was
   avoided per this phase's explicit instruction.

## 7. After Benchmark

Compute-stage timings are unchanged (instrumentation adds
`time.perf_counter()` calls, themselves sub-microsecond, and a log
line — no measurable overhead): re-running the same synthetic
benchmark after instrumentation still shows sub-millisecond compute
stages. The material change is **visibility**, not speed:
`docs/PERFORMANCE.md`'s "Before" numbers were only obtainable
by writing a one-off script; every future `python main.py` run now
emits this data as a normal part of its logs, so a real production
slowdown (most likely bottleneck #2, network I/O) is now directly
diagnosable from `trading_bot.yml`'s own GitHub Actions logs without
any extra tooling.

```
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] pipeline_started
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=market_data duration=0.523s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=context duration=0.001s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=signal duration=0.000s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=ai duration=0.000s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=decision duration=0.000s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=risk duration=0.000s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=telegram_format duration=0.000s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=telegram_delivery duration=0.412s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] stage=database duration=0.015s
2026-07-13 ... - TradingPipeline - INFO - [XAUUSD|M15] pipeline_finished duration=0.951s
```
(illustrative — `market_data`/`telegram_delivery` durations above are
representative network-call estimates, not measurements; every other
line is this phase's actual measured/observed shape.)

## 8. Remaining Recommendations (Not Applied This Phase)

1. **If a future phase ever adds a Telegram-free entrypoint**
   (backtesting, historical replay, analysis CLI), move
   `from telegram.notifier import Notifier` in `core/pipeline.py` to a
   lazy import inside `__init__`, gated on `send_notifications`. Zero
   benefit to today's `main.py` (always `send_notifications=True`) —
   only worth doing once a caller that doesn't need Telegram exists.
2. **Wire `SmartDataCache` in if `TradingPipeline` ever fetches more
   than one symbol/interval per cycle.** Today there's exactly one
   `get_candles()` call per run, so there's nothing to cache within a
   cycle; the moment that changes, `data_layer/market_memory/data_cache.py` is
   ready-built for it.
3. **Revisit `get_all_users()`/`get_all_subscriptions()`/
   `get_all_admins()` pagination** if any of those tables cross
   roughly 10,000 rows (per the Phase 48 audit's original estimate) —
   not a concern at today's scale.
4. **Re-run this report's "Before Benchmark" numbers against real
   Twelve Data/Telegram network calls** the first time this pipeline
   runs somewhere with live credentials — this phase's stage-timing
   instrumentation (section 6) makes that a matter of reading
   `trading_bot.yml`'s existing logs, not writing new tooling.
