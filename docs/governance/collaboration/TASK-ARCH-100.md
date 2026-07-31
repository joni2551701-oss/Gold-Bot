# TASK-ARCH-100 — PHASE-01: Data Layer Migration

Branch: `claude/collaboration`. Priority: CRITICAL. Status: **Steps
1–4 delivered (audit/mapping only); Step 5+ (actual code refactoring)
NOT started — see "STOP before Step 5" below.**

This is a code-bearing task (the brief explicitly permits move/rename/
merge/split under Step 5), governed by `TASK-GOV-001.md` Laws 1–12
(referenced, not restated) plus this task's own Reuse First addendum:
*"Har qanday refactoring yoki modul ko'chirishdan oldin worker mavjud
kodni maksimal darajada qayta ishlatishi shart... Reuse First —
majburiy qoida."* Steps 1–4 (Repository Audit, Responsibility Audit,
Folder Audit, Architecture Mapping) are audit-only by the brief's own
structure — no code touched to produce them. What that audit found
changes how Step 5 must proceed, which is why this document stops
there and asks rather than executes.

## Step 1 — Repository Audit

Per the brief's own candidate list (`data/`, `context/`, `provider/`,
`memory/`, `stream/`, `cache/`, `bootstrap/`, `recovery/`,
`historical/`, `validator/`, current price, event, snapshot,
collector): a full top-level directory sweep found **no stray
top-level `provider/`, `memory/`, `cache/`, `bootstrap/`, `recovery/`,
`historical/`, or `validator/` directory** — those responsibilities
already live entirely under `data/`'s own subpackages
(`data/providers/`, `data/memory/`, `data/bootstrap/`, etc.). `context/`
exists but is the Context Engine (a distinct GoldBot Core layer per
`03_GoldBot_Core.md`), not Data Layer — out of this task's scope
(Forbidden: "Core logikasini o'zgartirmaydi").

**Two top-level directories do belong to this audit and were not
mentioned by name in the brief's own candidate list:**

- **`stream/`** (8 modules + README) — TASK-CORE-004, a real-time
  market data-flow layer: `price_stream.py` (`PriceStream`),
  `stream_event.py`, `stream_validator.py`, `stream_state.py`,
  `current_price.py` (`CurrentPrice`), `stream_mode.py`,
  `stream_router.py`, `stream_subscriber.py`.
- **`market/`** (13 modules + README) — TASK-CORE-005, a read-only
  market facade: `market_manager.py`, `market_data.py`
  (`MarketData`/`MarketSnapshot`), `market_structure.py`,
  `trend_state.py`, `liquidity_state.py`, `session_state.py`,
  `volatility_state.py`, `regime_state.py`, `candle.py`, `ticker.py`,
  `orderbook.py`, `current_price.py` (`MarketPrice`).

Both are documented ("Status: Foundation only — nothing here is wired
into `core/pipeline.py`"), both are tested (108 passing tests combined,
`tests/stream/` + `tests/market/`), and **neither is imported by
`telegram/`, `core/`, or any other consumer anywhere in the
repository** — confirmed by a full-repo import grep. They are real,
maintained, isolated foundation, not dead/orphaned code in the
"unused import" sense — but they are architecturally isolated from
everything this session's `TASK-DATA-001..004` work built in `data/`.

Full `data/` inventory (70 files across 10 subpackages: top-level,
`bootstrap/`, `events/`, `memory/`, `normalization/`, `persistence/`,
`providers/`, `replay/`, `snapshots/`, `stream/`) was already produced
in `TASK-ARCH-001`'s own Data Layer audit and is not reproduced here
verbatim — see `02_Data_Layer.md` and this document's Step 2 for the
delta that matters: the `stream/`+`market/` vs. `data/` overlap.

## Step 2 — Responsibility Audit

Grouped by responsibility (not one row per file — ~90 files total
across the three trees; full per-file detail available on request).
**Bold** rows are the direct name/responsibility collisions found.

| Module / Group | Purpose | Current Responsibility | Target (per `01_Ecosystem_Architecture.md`) | Duplicate | Reusable | Action |
|---|---|---|---|---|---|---|
| `data/providers/` | Vendor adapters (TwelveData real; MT5/Binance/Bitget/FRED stubs) | Historical + live provider access | **Historical Providers** + **Live Providers** | No | Yes | Keep |
| `data/bootstrap/` | Historical bootstrap orchestration, gap recovery | Historical load + recovery | **Bootstrap**, **Recovery** | No | Yes | Keep |
| `data/historical_data_collector.py`, `historical_validator.py` | Historical range collection + validation | Historical collection/validation | **Historical Data → Data Validation** | No | Yes | Keep, maybe rename for clarity (Step 3) |
| `data/market_data.py` (`MarketDataNormalizer`) | Fetch/validate/dedupe candles, the pipeline's real data source | Live fetch (despite the name, not history-only) | **HistoricalDataService** input OR its own thing — see Conflict below | Partial (name vs. `market/market_data.py`) | Yes | Keep; **rename collision with `market/market_data.py` flagged, not resolved** |
| `data/market_data_service.py` (`MarketDataService`, TASK-DATA-001/002/004) | Facade: candles/snapshot/history + optional MarketMemory hydrate | Wired into `core/pipeline.py` today | **HistoricalDataService** (closest real match to the target box) | No | Yes | Keep — this is the target's `HistoricalDataService`, just not yet renamed to match |
| **`data/stream/` (TASK-DATA-001, this session)** | `PriceStreamService`, `PriceCache`, `PriceTick`, `PriceProvider`, `PriceStream`, `StreamManager`, vendor adapters | Live tick API, not wired into pipeline | **Live Data → PriceStreamService** | **YES — vs. `stream/`** | Yes | Keep as primary candidate — see Conflict below |
| **`stream/` (TASK-CORE-004, pre-existing)** | `PriceStream`, `StreamEvent`, `CurrentPrice`, `StreamValidator`, `StreamRouter`, `StreamMode` | Live tick flow, zero consumers anywhere | **Live Data → PriceStreamService** (same target box as `data/stream/`) | **YES — vs. `data/stream/`** | Partial (real, tested, but unconsumed) | **Do not touch without Owner decision** — see Conflict |
| `data/memory/` (MA-001, Director-accepted) | `MarketMemory`, `TimeframeMemory`, `MemoryReader`, `MarketMemoryRegistry` | Candle Single Source of Truth, not yet the pipeline's read path | **MarketMemory** | No | Yes | Keep — this is the canonical, Constitution/MA-001-governed target |
| `data/candle_builder.py` | Aggregates ticks into OHLC, single writer into `MarketMemory` | Foundation, wired to `data/stream/price_stream_service.py`'s optional memory path | **CandleBuilder** | No | Yes | Keep |
| **`market/` (TASK-CORE-005, pre-existing)** | Read-only facade over `context/` + `stream/current_price.py`; `MarketData`/`MarketSnapshot`, structure/trend/liquidity/session/volatility/regime projections | Zero consumers anywhere | Not named in the target diagram at all (Historical Data / Live Data split has no "read facade" box) | **Partial — vs. `data/market_data_service.py`'s `MarketSnapshot` name, and conceptually vs. what `MemoryReader` (MA-002) is meant to become** | Partial | **Do not touch without Owner decision** — see Conflict |
| `data/current_price_provider.py` (Phase 1/3) | `CurrentPriceProvider`, the real Telegram-facing current-price seam, now backed by `PriceStreamService` | **Wired — Telegram's actual live path** | **Live Data → CurrentPriceProvider** | **YES — vs. `stream/current_price.py`'s `CurrentPrice`** | Yes | Keep — this is the one with a real consumer |
| `data/events/` | `EventBus`, `Event`/`EventType`, bridges, metrics | Central pub/sub, foundation only | **EventBus** | No | Yes | Keep |
| `data/persistence/`, `data/snapshots/`, `data/replay/` | Durable storage, snapshot lifecycle, replay | Foundation only, not in target diagram explicitly | Supporting infra for **Historical Database** / **MarketMemory** persistence | No | Yes | Keep |
| `data/normalization/` | Candle/symbol/timeframe mapping helpers | Used by provider path | Supporting infra for **Historical Providers** | No | Yes | Keep |
| `data/data_cache.py` (`SmartDataCache`) | Cache-hit/miss orchestration over `MarketDataNormalizer`, not wired | Foundation, documented "not yet wired into the pipeline" since before this session | **Data Validation** / caching layer under Historical Data | No (unique cache-hit/miss logic, not duplicated elsewhere) | Yes | Keep — flagged in `TASK-DATA-003` of the Owner's own roadmap as needing its own audit ("kerakmi yoki olib tashlanadimi") |
| `data/api_error_classifier.py`, `data/data_quality.py`, `data/session_filter.py`, `data/provider_comparison.py`, `data/market_data_snapshot.py` | Small, single-purpose observational/utility modules, mostly wired or foundation | Various | **Data Validation** support | No | Yes | Keep |

## Step 3 — Folder Audit

**Current reality:** three separate top-level trees hold Data-Layer-
adjacent responsibility — `data/` (10 subpackages, the active/
consumed lineage), `stream/` (8 files, isolated), `market/` (13
files, isolated). No other stray locations found (confirmed against
the brief's own candidate list in Step 1).

**Target** (per the brief's Architecture Target diagram):

```
DATA LAYER
├── Historical Data
│   ├── HistoricalDataService   -> data/market_data_service.py (rename candidate)
│   ├── Bootstrap                -> data/bootstrap/
│   ├── Recovery                 -> data/bootstrap/gap_recovery.py
│   ├── Historical Providers     -> data/providers/
│   ├── Data Validation          -> data/data_quality.py, data/historical_validator.py, data/data_cache.py
│   └── Historical Database      -> database/raw_candle_repository.py + data/persistence/
│
└── Live Data
    ├── PriceStreamService        -> data/stream/price_stream_service.py  (CONFLICT: stream/price_stream.py)
    ├── CurrentPriceProvider      -> data/current_price_provider.py       (CONFLICT: stream/current_price.py)
    ├── CandleBuilder             -> data/candle_builder.py
    ├── MarketMemory               -> data/memory/  (MA-001, unconflicted)
    ├── EventBus                   -> data/events/
    └── Live Providers             -> data/providers/, data/stream/twelve_data_provider.py, data/stream/bitget_price_source.py
```

Every target box has a real, working module to map to **except** where
flagged CONFLICT above — those two boxes each have **two** candidate
implementations, and the target diagram doesn't say which wins, nor
does it mention `market/`'s read-facade responsibility at all (no box
for it). This is not a folder-naming cleanup question; it's an
architecture decision. Not resolved in this document.

## Step 4 — Architecture Mapping

| Real module | → | `01_Ecosystem_Architecture.md` subsystem |
|---|---|---|
| `data/market_data_service.py` | → | Data Layer → Historical Data → HistoricalDataService |
| `data/bootstrap/` | → | Data Layer → Historical Data → Bootstrap |
| `data/bootstrap/gap_recovery.py` | → | Data Layer → Historical Data → Recovery |
| `data/providers/` | → | Data Layer → Historical Data → Historical Providers |
| `data/data_quality.py`, `historical_validator.py` | → | Data Layer → Historical Data → Data Validation |
| `database/raw_candle_repository.py` + `data/persistence/` | → | Data Layer → Historical Data → Historical Database |
| `data/stream/price_stream_service.py` **or** `stream/price_stream.py` | → | Data Layer → Live Data → PriceStreamService (CONFLICT) |
| `data/current_price_provider.py` **or** `stream/current_price.py` | → | Data Layer → Live Data → CurrentPriceProvider (CONFLICT) |
| `data/candle_builder.py` | → | Data Layer → Live Data → CandleBuilder |
| `data/memory/` | → | Data Layer → Live Data → MarketMemory |
| `data/events/` | → | Data Layer → Live Data → EventBus |
| `data/stream/twelve_data_provider.py`, `bitget_price_source.py` | → | Data Layer → Live Data → Live Providers |
| `market/` (entire package) | → | **No target box exists.** Closest conceptual match is `MemoryReader` (MA-002, `data/memory/memory_reader.py`) — a read-only projection layer — but `market/` projects `context/` + `stream/`, not `MarketMemory`. Not force-mapped here. |

## STOP before Step 5 — Owner Decision Required

Per this task's own Reuse First addendum and `TASK-GOV-001.md` Law 2
(Reuse First) / Law 4 (No hidden refactor), and Constitution Article 8
(STOP → AUDIT → Owner Decision): **Step 5 (code refactoring — move,
rename, merge, split, dependency cleanup) is not started.** The audit
surfaced a real architectural decision the brief's own target diagram
does not resolve, and executing Step 5 before that decision is made
would mean this Worker unilaterally choosing a winner between two
real, tested, differently-shaped implementations — exactly what Reuse
First and Law 4 exist to prevent.

**The decision needed:**

1. **`data/stream/` (mine, this session, wired to `data/current_price_provider.py`
   and `MarketMemory`) vs. `stream/` (TASK-CORE-004, pre-existing, zero
   consumers, has its own `market/` facade built on top of it).** Which
   becomes the Live Data `PriceStreamService`/`CurrentPriceProvider`?
   Options: (a) keep `data/stream/` as canonical, retire `stream/` +
   `market/` (loses `market/`'s context-projection facade — nothing
   else provides that today); (b) keep `stream/`+`market/` as
   canonical, retire `data/stream/` (loses `MarketMemory`/`CandleBuilder`
   wiring built in `TASK-DATA-004`, and `data/current_price_provider.py`'s
   real Telegram consumer would need to point at `stream/` instead);
   (c) merge specific pieces of each (e.g., keep `market/`'s
   context-projection idea as a future consumer of `MarketMemory`
   instead of `stream/`) — the most Reuse-First-aligned option on paper,
   but the most work and the most design judgment, which is exactly why
   it needs Owner sign-off before any code moves.
2. Whatever is retired (`stream/`+`market/`, or `data/stream/`, or
   neither) — is it **deleted**, or kept as a **documented, explicitly
   superseded/frozen** package? Both `stream/` and `market/` have real,
   passing test suites (108 tests) that this task's own Acceptance
   Criteria ("✓ Testlar o'tgan bo'lsa") would need to account for either
   way.
3. `data/market_data.py`'s `MarketSnapshot` vs. `market/market_data.py`'s
   `MarketSnapshot` — same name, different shape, in whichever of the
   two trees survives decision 1, this naming collision needs its own
   resolution (rename one, or it stops being a collision once one tree
   is retired).

**What this task delivers now, pending that decision:** the audit
above (Steps 1–4, this document's Handover items 1–2 and 4–7 below).
Step 5 onward (refactoring, doc updates beyond this record, dependency/
import cleanup, test updates, performance audit, data-flow validation,
final structure, final report) all depend on decision 1 and are not
executed here.

## Handover

1. **Data Layer Audit** — Steps 1–4 above.
2. **Refactoring Summary** — not applicable yet; no refactoring executed.
3. **Migration Report** — not applicable yet.
4. **Updated Folder Structure** — Step 3's target table, pending
   decision 1's resolution of the two CONFLICT rows.
5. **Updated Module Map** — Step 4's table.
6. **Dependency Diagram** — not produced; blocked on decision 1 (a
   dependency diagram drawn before knowing which `PriceStream`/
   `CurrentPrice` survives would need redrawing).
7. **Data Flow Diagram** — the target (`Provider → Validation → Market
   Memory → CurrentPrice → CandleBuilder → Core`) is stated in the
   brief itself (Step 11) and matches `data/`'s real, wired path today
   (`MarketDataNormalizer → data_quality → [MarketMemory not yet the
   read path, per `TASK-ARCH-001`'s own Gap Analysis] → context/ →
   ...`) — already documented in `02_Data_Layer.md`, `05_Complete Data
   Flow` (`01_Ecosystem_Architecture.md` §5), and
   `docs/architecture/DATA_FLOW.md`. `stream/`+`market/`'s parallel
   flow (`Provider → stream/ → context/ → market/`) is real but
   disconnected from this one — see the Conflict.
8. **Test Report** — no test was changed; `tests/stream/` + `tests/market/`
   (108 passing) and the full `data/` test suite (part of the 5375
   passing suite as of the last commit) both currently pass, unaffected
   by an audit-only task.
9. **Known Issues** — the three CONFLICT rows in Step 2/3/4 above; the
   `data/market_data.py` vs. `market/market_data.py` naming collision;
   `market/` has no target box in the brief's own diagram.
10. **Recommendations** — Option (a) in Decision 1 (keep `data/stream/`
    as canonical) is the lowest-risk path given it already has the real
    Telegram consumer and the `MarketMemory`/`CandleBuilder` wiring this
    session built under explicit Owner approval (`TASK-DATA-001..004`);
    but `market/`'s context-projection facade is a real capability
    `data/` has no equivalent for today, so outright deleting `market/`
    would be a genuine capability loss, not just a cleanup. This is a
    recommendation, not a decision — flagged per this task's own rule
    that the Worker does not resolve an architecture conflict alone.

## Status

```
TASK-ID:    TASK-ARCH-100 (PHASE-01: Data Layer Migration)
Goal:       Migrate Data Layer to 100% match 01_Ecosystem_Architecture.md.
Rules:      TASK-GOV-001.md Laws 1-12; Reuse First addendum (this
            task's own rule); Constitution Article 7/8.
Forbidden:  Core/Strategy/Decision/Risk/Telegram/AI/Platform/Business/
            Learning/Media code; resolving the Step 5 conflict
            unilaterally.
Allowed:    Data Layer audit (Steps 1-4, delivered); Data Layer code
            refactoring (Step 5+, NOT yet authorized to proceed).
Input:      TASK-ARCH-100 brief (Owner instruction).
Output:     This audit document.
Owner:      Worker (this session) -- task-assignee sense.
Status:     BLOCKED -- Steps 1-4 delivered; Step 5 requires an Owner
            decision on the stream/+market/ vs. data/stream/ conflict
            before any code is moved, renamed, or merged.
Next step:  Owner rules on Decision 1 (and 2, 3); Worker executes
            Step 5 onward under that ruling, as its own, separately
            validated commit(s) with full test coverage maintained.
```
