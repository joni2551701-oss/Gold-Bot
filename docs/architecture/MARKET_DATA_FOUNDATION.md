# Market Data Foundation — GoldBot v1.1 Phase 1

**Status:** Director-APPROVED — **FROZEN** (DD-037). This is the official
GoldBot v1.1 architecture. During implementation, significant architectural
changes require a new Director Decision. Coding begins after this document
is merged to `main` via PR (DD-036).
**Scope:** Price Stream Foundation & Multi-Timeframe Memory Engine — the
single Market Data Layer every future component reads from.
**Governance:** incorporates Director amendments **DD-026 … DD-035**
(recorded individually in `docs/governance/director/`). Trading Safety:
this layer never touches signal/risk/decision logic.

> **Design only.** No code, no pipeline change is made by this document.
> When implemented, the Memory-First refactor is *pipeline-adjacent* and
> `docs/AUDIT_REPORT.md` will be re-read first; the change lands behind a
> fallback flag with the existing `MarketDataNormalizer` path retained.

---

## 1. Design principle — reuse the existing `data/` layer

Per Constitution Article 11 (Foundation Reuse Law) / CLAUDE.md, this is a
**wire-and-extend of the existing `data/` package**, not a new top-level
system. The existing modules are reused as the foundation:

| Requirement | Existing module | Decision |
|---|---|---|
| API client (retry/backoff) | `data_layer/providers/twelve_data_client.py` | REUSE |
| Normalize / validate / dedup | `data_layer/live_data/market_data.py` (`MarketDataNormalizer`) | REUSE |
| Historical bootstrap | `data_layer/historical_data/historical_data_collector.py`, `data_layer/data_validation/historical_validator.py` | REUSE/EXTEND |
| Cache + candle clock + API budget | `data_layer/market_memory/data_cache.py` (`SmartDataCache`) | EXTEND |
| Data quality / missing candle | `data_layer/data_validation/data_quality.py` | REUSE |
| Error classification | `data_layer/providers/api_error_classifier.py` | REUSE |
| Session state | `data_layer/live_data/session_filter.py` | REUSE |
| TF config | `config.TIMEFRAME_HISTORY` | EXTEND (add M1, D1) |

Genuinely new (all land **inside `data/`**): the live stream, candle
builder, the multi-asset Memory + registry, the event bus, the reader
contract, snapshot, and the orchestrating Central Data Manager.

---

## 2. Multi-asset topology (DD-030) — no singleton

`MarketMemory` is **not** a singleton. A registry owns one memory per
asset so Gold, BTC, EURUSD, NASDAQ, SP500 can run concurrently without an
architecture rewrite.

```
MarketMemoryRegistry
├─ MarketMemory("XAUUSD")
├─ MarketMemory("BTCUSD")
└─ MarketMemory("EURUSD") ...

Asset ─▶ MarketMemory ─▶ PriceStream ─▶ History ─▶ Chart ─▶ AI
```

Each `MarketMemory(asset)` owns its own PriceStream, CandleBuilder, and
per-TF memories. Nothing in the design assumes a single global instance;
call sites resolve `registry.get(asset)`.

## 3. Target module layout (extension of `data/`)
```
data/
├─ twelve_data_client.py        REUSE   API adapter
├─ market_data.py               REUSE   normalize/validate/dedup
├─ historical_data_collector.py REUSE   bootstrap fetch
├─ historical_validator.py      REUSE   bootstrap validation
├─ data_cache.py                EXTEND  persistence + candle clock + API budget
├─ data_quality.py              REUSE   health / missing-candle
├─ api_error_classifier.py      REUSE   error → recovery
├─ session_filter.py            REUSE   session / trading-day
├─ candle_clock.py              NEW     TF boundaries (from data_cache._get_next_candle_time)
├─ candle_builder.py            NEW     tick/quote → OHLC; close/open on boundary
├─ stream/
│   ├─ price_stream.py          NEW     live stream + reconnect (transport-agnostic)
│   └─ stream_event.py          NEW     PriceTick / QuoteEvent
├─ memory/
│   ├─ candle_record.py         NEW     full candle model (DD-027)
│   ├─ timeframe_memory.py      NEW     per-TF ring buffer + revision (DD-029)
│   ├─ market_memory.py         NEW     per-asset multi-TF memory; LIVE/REPLAY (DD-033)
│   ├─ market_memory_registry.py NEW    asset → MarketMemory (DD-030)
│   ├─ memory_events.py         NEW     event types + event bus (DD-028)
│   ├─ memory_reader.py         NEW     full read + subscribe contract (DD-031)
│   └─ memory_snapshot.py       NEW     immutable snapshot model (DD-034)
└─ market_data_manager.py       NEW     Central Data Manager (per asset, orchestrator)
```

---

## 4. Candle record model (DD-027)

Memory stores more than OHLC. Per candle, per timeframe:

| Field | Purpose |
|---|---|
| `open, high, low, close` | OHLC |
| `timestamp` | candle open time (UTC) |
| `status` | `FORMING` / `CLOSED` |
| `volume` | if the provider supplies it |
| `candle_id` | stable unique id (asset+tf+open_time) |
| `sequence_number` | monotonic per (asset, tf) — ordering/replay |
| `source` | `bootstrap` / `stream` / `recovery` |
| `last_update_time` | wall-clock of the last mutation |
| `session` | trading session (from `session_filter.py`) |
| `trading_day` | logical trading day the candle belongs to |
| `metadata` | open dict (provider tags, gap-fill marks, revision) |

`candle_id` + `sequence_number` make replay (DD-033), chart diffing
(DD-029), and AI context deterministic.

## 5. Multi-Timeframe Memory (independent per TF, versioned — DD-029)
```
MarketMemory(asset)  mode = LIVE | REPLAY   (DD-033)
├─ TimeframeMemory[M1]   revision:int   closed[] (ring) + forming
├─ TimeframeMemory[M5]   revision:int   own RLock, own depth, own health
├─ TimeframeMemory[M15]  ...
├─ TimeframeMemory[H1]
├─ TimeframeMemory[H4]
└─ TimeframeMemory[D1]   (all six default ON — DD-026)
```
- Each `TimeframeMemory` carries a **`revision`** counter. Every mutation
  (open / update / close) does `revision++`. Chart/AI compare a cached
  revision to detect new data without polling contents (DD-029).
- Bounded ring buffer (depth = `TIMEFRAME_HISTORY[tf]`) → memory-efficient,
  O(1) append.

## 6. Memory Event Bus (DD-028) — no polling
Every candle transition emits an event; consumers subscribe.
```
CandleBuilder ─▶ MarketMemory.emit(event) ─▶ EventBus ─▶ subscribers
   OnNewCandle(asset, tf, candle_id)          Chart
   OnCandleUpdate(asset, tf, candle_id, rev)   AI
   OnCandleClose(asset, tf, candle_id)         Telegram / Desktop / API server
```
- Publish/subscribe; **polling is not used**. Delivery is decoupled
  (subscribers never block the writer — events are dispatched off the
  write path or via a bounded queue).
- Reuses the codebase's existing observer patterns where present rather
  than inventing a second event mechanism (to confirm against
  `docs/architecture/DESIGN_PATTERNS.md` at implementation time).

## 7. MemoryReader contract (DD-031) — the one interface all platforms use
```python
class MemoryReader:              # read-only + subscription; never fetches API
    get_last_candle(asset, tf)        -> CandleRecord      # forming or last
    get_last_closed(asset, tf)        -> CandleRecord
    get_forming(asset, tf)            -> CandleRecord | None
    get_series(asset, tf, n)          -> list[CandleRecord]  # copy-on-read
    subscribe(asset, tf, handler)     -> SubscriptionHandle
    unsubscribe(handle)               -> None
    health(asset)                     -> HealthReport
    snapshot(asset, tfs=None)         -> MemorySnapshot     # DD-034
    revision(asset, tf)               -> int                # DD-029
    mode(asset)                       -> LIVE | REPLAY      # DD-033
```
Every future client (Telegram, Mini App, Android, iOS, Desktop, Web, AI,
Chart, Signal/Risk) works **only** through this contract.

## 8. Snapshot API (DD-034)
`snapshot(asset, tfs)` returns an **immutable** point-in-time copy of the
requested timeframes (candles + revisions + health). Used for debug, AI
context, export, mobile sync, and the future API server. A snapshot is a
value object — safe to serialize and hand across a process/network boundary.

## 9. Replay Mode (DD-033)
`MarketMemory` supports two modes behind the same `MemoryReader`:
- **LIVE** — fed by PriceStream + CandleBuilder.
- **REPLAY** — fed from stored/snapshotted candles, advanced by a replay
  clock. AI and Chart consume replay identically to live (same reader,
  same events, driven by `sequence_number`), enabling backtest-style and
  visual replay with no code fork on the consumer side.

## 10. Historical Bootstrap Flow (once per TF)
```
for tf in configured_timeframes(asset):        # M1..D1, all ON (DD-026)
    if cache.fresh(asset, tf): load_from_cache  # restart fast-path
    else:
        candles = collect_historical_candles(asset, tf, depth)  # 1 API call
        historical_validator.validate(candles)
        memory[asset][tf].hydrate(candles)      # source=bootstrap, status=CLOSED
        cache.save_state()
memory[asset].mode = LIVE
```
Exactly **one API request per timeframe** (guarded by
`SmartDataCache._check_api_limit`); restart resumes from a fresh cache
with **zero** calls.

## 11. Live Stream Flow
```
StreamEvent ─▶ CandleBuilder.on_event(e):
    for tf in timeframes:
        tfm = memory[asset][tf]
        tfm.update_forming(e.price)             # C=price; H=max; L=min; revision++
        emit OnCandleUpdate(asset, tf, rev)
        if candle_clock.boundary_crossed(tf, e.time):
            tfm.close_forming();  emit OnCandleClose(...)
            tfm.open_new(e.time); emit OnNewCandle(...)
```
Historical API is **never** re-called here (only recovery/gap-fill/manual).

## 12. Candle Builder Design
- Transport-agnostic: Twelve Data quote snapshots (not raw ticks) are
  aggregated into OHLC per TF — the same builder works for WS ticks or
  polled quotes.
- Uses `candle_clock` (**extracted** from the existing
  `data_cache._get_next_candle_time` — reuse, not reinvent) for boundaries.
- Guarantees: closed candles immutable; exactly one `FORMING` per TF;
  monotonic `sequence_number`; out-of-order events clamped or dropped with
  a health flag.

## 13. Synchronization Model (thread-safe, race-free)
- **Single-writer per TF** (only CandleBuilder / bootstrap / recovery write
  a given TF) + per-TF `RLock`.
- **Copy-on-read**: `get_series` / `snapshot` return copies (or immutable
  records); no reader ever holds a reference to mutable internal state.
- Cross-TF reads acquire locks in a **fixed TF order** (deadlock-free).
- Closed candles are never mutated in place → readers always see a
  consistent series. `revision` lets readers detect change lock-free after
  the copy.

## 14. Cache Strategy
- **Tier 1 (hot):** in-RAM `MarketMemory` — the Memory-First path.
- **Tier 2 (durable):** `SmartDataCache.save_state/load_state` — restart
  snapshot. Freshness keyed on candle-close time (`_get_next_candle_time`);
  fresh TFs skip bootstrap on restart.

## 15. Recovery Strategy (no data loss)
| Failure | Detection | Action (least-cost first) |
|---|---|---|
| Stream disconnect | heartbeat/timeout | reconnect w/ backoff; serve last-good as `DEGRADED` |
| Internet / API error | `api_error_classifier` (`API_001/002`) | backoff + retry; stay `DEGRADED` |
| Missing candle (gap) | `data_quality._detect_missing_candles` | **windowed gap-fill** (fetch only the hole) |
| Corruption / manual / stale restart | validator fail / operator | full `REBUILD` (bootstrap that TF) |
Closed candles persist in cache; recovery re-fetches only what is missing.

## 16. Health Monitoring Strategy
`health(asset)` reports: API status, stream status, per-TF memory status +
revision, reconnect count, missing-candle flags, **time drift** (server vs
local), recovery state. Integrates with the existing top-level
`monitoring/` package (reuse target — confirm at implementation) rather
than a new monitoring system.

## 17. API Optimization (DD-026 constraint: all 6 TFs ON)
M1 is mandatory (Liquidity Sweep / SMC / ICT / entry precision), so
optimization is achieved **without** dropping timeframes:
- Steady state: **0 historical calls/day** — stream feeds all TFs; M1..D1
  are all built by the CandleBuilder from a single price stream, so adding
  M1 adds **no** extra API polling, only in-memory aggregation.
- Startup: 1 call × 6 TFs; restart often 0 (cache fresh).
- Gap-fill is windowed; full rebuild is rare.
- `_check_api_limit` enforces the budget.
- M1 cost is **memory/CPU**, not API — bounded ring buffer + single-writer
  keep it efficient; M1 depth is tuned in `TIMEFRAME_HISTORY`.

## 18. Chart Integration (DD-032) — never calls API
```
MarketMemory ─▶ MemoryReader.get_series / subscribe(OnCandleClose) ─▶ Chart.render
```
Supports TradingView-style, Lightweight-Charts, custom charts, and
**replay** charts — all from Memory, many charts concurrently (read-only,
lock-guarded, revision-diffed). Charts never touch the provider.

## 19. Future API Server (DD-035) — Memory stays internal
```
MarketMemory ─▶ MemoryReader ─▶ [Future] REST / WebSocket API Server ─▶
      Telegram · Mini App · Desktop · Android · iOS · Web
```
External platforms talk to a **future API server** over REST/WebSocket, not
to `MarketMemory` directly. Memory remains an **internal layer**; the API
server is a thin adapter over `MemoryReader` + the event bus (WS pushes the
DD-028 events). This phase only guarantees the design supports it (the
`MemoryReader`/snapshot/event contracts are network-serializable); the API
server itself is a later phase.

## 20. Final Architecture Diagram
```
                        MarketMemoryRegistry  (DD-030, multi-asset)
                                  │  registry.get(asset)
        ┌───────────── data/ : MarketMemory(asset) ─────────────────┐
 API ──▶│ twelve_data_client ─▶ historical_data_collector ─▶ bootstrap│
 (once) │ candle_clock  data_cache(persist)  data_quality  session    │
 stream▶│ PriceStream ─▶ StreamEvent ─▶ CandleBuilder ─┐              │
        │                                              ▼              │
        │   ┌── TimeframeMemory[M1..D1]  (revision, LIVE|REPLAY) ──┐  │
        │   │  CandleRecord(OHLC,id,seq,source,session,day,meta)   │  │
        │   └───────────────┬───────────────────┬──────────────────┘  │
        │        EventBus (OnNew/Update/Close)   │ MemoryReader        │
        │        DataHealthMonitor               │ snapshot()          │
        └────────────────────┬───────────────────┴─────────────────────┘
                             │  (Memory-First: nothing below calls the API)
        Context ─▶ Signals ─▶ AI ─▶ Decision ─▶ Risk ─▶ Telegram
                             │
                             └▶ [Future] REST/WS API Server ─▶ Mini App · Mobile · Desktop · Web · Chart
```

---

## 21. Director Amendments incorporated (DD-026 … DD-035)
| DD | Decision | Reflected in |
|---|---|---|
| DD-026 | M1 **default ON**; all six TFs (M1,M5,M15,H1,H4,D1) mandatory; optimize elsewhere | §5, §17 |
| DD-027 | Extended candle model (id, seq, source, last_update, session, trading_day, metadata) | §4 |
| DD-028 | Memory Event Bus (OnNewCandle/Update/Close); no polling | §6 |
| DD-029 | Per-TF `revision` versioning; `revision++` per update | §5, §7 |
| DD-030 | `MarketMemory` not singleton → `MarketMemoryRegistry`, multi-asset | §2 |
| DD-031 | Full `MemoryReader` (get_last/closed/forming/series, subscribe, health, snapshot) | §7 |
| DD-032 | Chart support (TradingView/Lightweight/Custom/Replay), Memory-only | §18 |
| DD-033 | Replay mode (LIVE/REPLAY) for AI + Chart | §9 |
| DD-034 | `snapshot()` anytime (debug/AI/export/mobile/API) | §8 |
| DD-035 | Future REST/WS API server; Memory stays internal | §19 |

## 22. Article 12 — New / Extended / Reused
| New | Extended | Reused |
|---|---|---|
| `data_layer/live_data/*`, `candle_builder.py`, `candle_clock.py`, `data_layer/market_memory/*` (registry, market_memory, timeframe_memory, candle_record, memory_events, memory_reader, memory_snapshot), `market_data_manager.py` | `data_layer/market_memory/data_cache.py`, `config.TIMEFRAME_HISTORY` | `twelve_data_client.py`, `market_data.py`, `historical_data_collector.py`, `historical_validator.py`, `data_quality.py`, `api_error_classifier.py`, `session_filter.py`, `monitoring/` |

## 23. Acceptance-criteria mapping
| Director criterion | Satisfied by |
|---|---|
| Historical once per TF | §10 + `_check_api_limit` |
| Live stream updates Memory continuously | §11 |
| No high-level module calls Twelve Data directly | §7 Memory-First `MemoryReader` |
| Single Memory = shared source for all platforms | §2, §7, §19 |
| Extensible to all platforms without change | §7, §18, §19, multi-asset §2 |

## 24. Risk Analysis
| Risk | Sev | Mitigation |
|---|---|---|
| No true WS/tick for XAUUSD | High | transport-agnostic stream; quote→OHLC builder |
| Memory-First refactor is pipeline-adjacent | High | re-read `AUDIT_REPORT.md`; flag + fallback; no signal/risk/decision change |
| Thread-safety (race/torn read) | High | single-writer/TF + copy-on-read + fixed lock order + revision |
| M1 volume (memory/CPU) | Med | bounded ring buffer; M1 built in-RAM (no extra API); tuned depth |
| Duplicating `data_cache`/`market_data` | Med | explicit REUSE/EXTEND (§1) |
| Multi-asset scope creep | Med | registry is a thin indirection; only XAUUSD wired first, others config-added |
| Event bus back-pressure | Med | bounded queue / off-write-path dispatch (§6) |

## 25. Phasing (implementation, later — after this doc merges)
1. Memory core: `candle_record`, `timeframe_memory` (+revision), `market_memory`, `registry`.
2. `candle_clock` (extract) + `candle_builder`.
3. `stream/` + `market_data_manager` (bootstrap → live), behind a flag.
4. `memory_reader` + event bus + snapshot.
5. Memory-First wiring of the pipeline data stage (fallback retained).
6. Health monitor integration; recovery paths.
7. (Future phases) chart adapters, replay driver, REST/WS API server.

## 26. References
- `data/README.md`, `docs/ARCHITECTURE.md`, `docs/architecture/DATA_FLOW.md`,
  `docs/DATA_QUALITY.md`, `docs/AUDIT_REPORT.md` (pipeline safety).
- `docs/governance/director/DD-026.md … DD-035.md` — the amendments.
- `config.TIMEFRAME_HISTORY` — timeframe depths.
