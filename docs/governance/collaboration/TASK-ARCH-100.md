# TASK-ARCH-100 — PHASE-01: Data Layer Migration

Branch: `claude/collaboration`. Priority: CRITICAL.

**Status: Phase-01 audit (Steps 1–4) delivered; STEP-05 Owner-approved
and PARTIAL-DONE — see the "STEP-05" section at the bottom of this
document for what was executed (MarketSnapshot collision resolved;
legacy packages marked) and what is proposed for follow-up sub-tasks
(the two feature-migration gaps + the market/ projection migration).
The "STOP before Step 5" section below is the original Phase-01 record;
the Owner subsequently ruled on its open decision, which STEP-05
executes.**

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
(`data_layer/providers/`, `data_layer/market_memory/`, `data_layer/historical_data/`, etc.). `context/`
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
| `data_layer/providers/` | Vendor adapters (TwelveData real; MT5/Binance/Bitget/FRED stubs) | Historical + live provider access | **Historical Providers** + **Live Providers** | No | Yes | Keep |
| `data_layer/historical_data/` | Historical bootstrap orchestration, gap recovery | Historical load + recovery | **Bootstrap**, **Recovery** | No | Yes | Keep |
| `data_layer/historical_data/historical_data_collector.py`, `historical_validator.py` | Historical range collection + validation | Historical collection/validation | **Historical Data → Data Validation** | No | Yes | Keep, maybe rename for clarity (Step 3) |
| `data_layer/live_data/market_data.py` (`MarketDataNormalizer`) | Fetch/validate/dedupe candles, the pipeline's real data source | Live fetch (despite the name, not history-only) | **HistoricalDataService** input OR its own thing — see Conflict below | Partial (name vs. `data_layer/live_data/market/market_data.py`) | Yes | Keep; **rename collision with `data_layer/live_data/market/market_data.py` flagged, not resolved** |
| `data_layer/live_data/market_data_service.py` (`MarketDataService`, TASK-DATA-001/002/004) | Facade: candles/snapshot/history + optional MarketMemory hydrate | Wired into `core/pipeline.py` today | **HistoricalDataService** (closest real match to the target box) | No | Yes | Keep — this is the target's `HistoricalDataService`, just not yet renamed to match |
| **`data_layer/live_data/` (TASK-DATA-001, this session)** | `PriceStreamService`, `PriceCache`, `PriceTick`, `PriceProvider`, `PriceStream`, `StreamManager`, vendor adapters | Live tick API, not wired into pipeline | **Live Data → PriceStreamService** | **YES — vs. `stream/`** | Yes | Keep as primary candidate — see Conflict below |
| **`stream/` (TASK-CORE-004, pre-existing)** | `PriceStream`, `StreamEvent`, `CurrentPrice`, `StreamValidator`, `StreamRouter`, `StreamMode` | Live tick flow, zero consumers anywhere | **Live Data → PriceStreamService** (same target box as `data_layer/live_data/`) | **YES — vs. `data_layer/live_data/`** | Partial (real, tested, but unconsumed) | **Do not touch without Owner decision** — see Conflict |
| `data_layer/market_memory/` (MA-001, Director-accepted) | `MarketMemory`, `TimeframeMemory`, `MemoryReader`, `MarketMemoryRegistry` | Candle Single Source of Truth, not yet the pipeline's read path | **MarketMemory** | No | Yes | Keep — this is the canonical, Constitution/MA-001-governed target |
| `data_layer/live_data/candle_builder.py` | Aggregates ticks into OHLC, single writer into `MarketMemory` | Foundation, wired to `data_layer/live_data/price_stream_service.py`'s optional memory path | **CandleBuilder** | No | Yes | Keep |
| **`market/` (TASK-CORE-005, pre-existing)** | Read-only facade over `context/` + `data_layer/live_data/stream/current_price.py`; `MarketData`/`MarketSnapshot`, structure/trend/liquidity/session/volatility/regime projections | Zero consumers anywhere | Not named in the target diagram at all (Historical Data / Live Data split has no "read facade" box) | **Partial — vs. `data_layer/live_data/market_data_service.py`'s `MarketSnapshot` name, and conceptually vs. what `MemoryReader` (MA-002) is meant to become** | Partial | **Do not touch without Owner decision** — see Conflict |
| `data_layer/live_data/current_price_provider.py` (Phase 1/3) | `CurrentPriceProvider`, the real Telegram-facing current-price seam, now backed by `PriceStreamService` | **Wired — Telegram's actual live path** | **Live Data → CurrentPriceProvider** | **YES — vs. `data_layer/live_data/stream/current_price.py`'s `CurrentPrice`** | Yes | Keep — this is the one with a real consumer |
| `data_layer/event_system/` | `EventBus`, `Event`/`EventType`, bridges, metrics | Central pub/sub, foundation only | **EventBus** | No | Yes | Keep |
| `data_layer/market_memory/persistence/`, `data_layer/snapshots/`, `backtesting_layer/replay_engine/` | Durable storage, snapshot lifecycle, replay | Foundation only, not in target diagram explicitly | Supporting infra for **Historical Database** / **MarketMemory** persistence | No | Yes | Keep |
| `data_layer/normalization/` | Candle/symbol/timeframe mapping helpers | Used by provider path | Supporting infra for **Historical Providers** | No | Yes | Keep |
| `data_layer/market_memory/data_cache.py` (`SmartDataCache`) | Cache-hit/miss orchestration over `MarketDataNormalizer`, not wired | Foundation, documented "not yet wired into the pipeline" since before this session | **Data Validation** / caching layer under Historical Data | No (unique cache-hit/miss logic, not duplicated elsewhere) | Yes | Keep — flagged in `TASK-DATA-003` of the Owner's own roadmap as needing its own audit ("kerakmi yoki olib tashlanadimi") |
| `data_layer/providers/api_error_classifier.py`, `data_layer/data_validation/data_quality.py`, `data_layer/live_data/session_filter.py`, `data_layer/providers/provider_comparison.py`, `data_layer/live_data/market_data_snapshot.py` | Small, single-purpose observational/utility modules, mostly wired or foundation | Various | **Data Validation** support | No | Yes | Keep |

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
│   ├── HistoricalDataService   -> data_layer/live_data/market_data_service.py (rename candidate)
│   ├── Bootstrap                -> data_layer/historical_data/
│   ├── Recovery                 -> data_layer/historical_data/gap_recovery.py
│   ├── Historical Providers     -> data_layer/providers/
│   ├── Data Validation          -> data_layer/data_validation/data_quality.py, data_layer/data_validation/historical_validator.py, data_layer/market_memory/data_cache.py
│   └── Historical Database      -> database_layer/market_repository/raw_candle_repository.py + data_layer/market_memory/persistence/
│
└── Live Data
    ├── PriceStreamService        -> data_layer/live_data/price_stream_service.py  (CONFLICT: data_layer/live_data/stream/price_stream.py)
    ├── CurrentPriceProvider      -> data_layer/live_data/current_price_provider.py       (CONFLICT: data_layer/live_data/stream/current_price.py)
    ├── CandleBuilder             -> data_layer/live_data/candle_builder.py
    ├── MarketMemory               -> data_layer/market_memory/  (MA-001, unconflicted)
    ├── EventBus                   -> data_layer/event_system/
    └── Live Providers             -> data_layer/providers/, data_layer/live_data/twelve_data_provider.py, data_layer/live_data/bitget_price_source.py
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
| `data_layer/live_data/market_data_service.py` | → | Data Layer → Historical Data → HistoricalDataService |
| `data_layer/historical_data/` | → | Data Layer → Historical Data → Bootstrap |
| `data_layer/historical_data/gap_recovery.py` | → | Data Layer → Historical Data → Recovery |
| `data_layer/providers/` | → | Data Layer → Historical Data → Historical Providers |
| `data_layer/data_validation/data_quality.py`, `historical_validator.py` | → | Data Layer → Historical Data → Data Validation |
| `database_layer/market_repository/raw_candle_repository.py` + `data_layer/market_memory/persistence/` | → | Data Layer → Historical Data → Historical Database |
| `data_layer/live_data/price_stream_service.py` **or** `data_layer/live_data/stream/price_stream.py` | → | Data Layer → Live Data → PriceStreamService (CONFLICT) |
| `data_layer/live_data/current_price_provider.py` **or** `data_layer/live_data/stream/current_price.py` | → | Data Layer → Live Data → CurrentPriceProvider (CONFLICT) |
| `data_layer/live_data/candle_builder.py` | → | Data Layer → Live Data → CandleBuilder |
| `data_layer/market_memory/` | → | Data Layer → Live Data → MarketMemory |
| `data_layer/event_system/` | → | Data Layer → Live Data → EventBus |
| `data_layer/live_data/twelve_data_provider.py`, `bitget_price_source.py` | → | Data Layer → Live Data → Live Providers |
| `market/` (entire package) | → | **No target box exists.** Closest conceptual match is `MemoryReader` (MA-002, `data_layer/market_memory/memory_reader.py`) — a read-only projection layer — but `market/` projects `context/` + `stream/`, not `MarketMemory`. Not force-mapped here. |

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

1. **`data_layer/live_data/` (mine, this session, wired to `data_layer/live_data/current_price_provider.py`
   and `MarketMemory`) vs. `stream/` (TASK-CORE-004, pre-existing, zero
   consumers, has its own `market/` facade built on top of it).** Which
   becomes the Live Data `PriceStreamService`/`CurrentPriceProvider`?
   Options: (a) keep `data_layer/live_data/` as canonical, retire `stream/` +
   `market/` (loses `market/`'s context-projection facade — nothing
   else provides that today); (b) keep `stream/`+`market/` as
   canonical, retire `data_layer/live_data/` (loses `MarketMemory`/`CandleBuilder`
   wiring built in `TASK-DATA-004`, and `data_layer/live_data/current_price_provider.py`'s
   real Telegram consumer would need to point at `stream/` instead);
   (c) merge specific pieces of each (e.g., keep `market/`'s
   context-projection idea as a future consumer of `MarketMemory`
   instead of `stream/`) — the most Reuse-First-aligned option on paper,
   but the most work and the most design judgment, which is exactly why
   it needs Owner sign-off before any code moves.
2. Whatever is retired (`stream/`+`market/`, or `data_layer/live_data/`, or
   neither) — is it **deleted**, or kept as a **documented, explicitly
   superseded/frozen** package? Both `stream/` and `market/` have real,
   passing test suites (108 tests) that this task's own Acceptance
   Criteria ("✓ Testlar o'tgan bo'lsa") would need to account for either
   way.
3. `data_layer/live_data/market_data.py`'s `MarketSnapshot` vs. `data_layer/live_data/market/market_data.py`'s
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
   `data_layer/live_data/market_data.py` vs. `data_layer/live_data/market/market_data.py` naming collision;
   `market/` has no target box in the brief's own diagram.
10. **Recommendations** — Option (a) in Decision 1 (keep `data_layer/live_data/`
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
            decision on the stream/+market/ vs. data_layer/live_data/ conflict
            before any code is moved, renamed, or merged.
Next step:  Owner rules on Decision 1 (and 2, 3); Worker executes
            Step 5 onward under that ruling, as its own, separately
            validated commit(s) with full test coverage maintained.
```

═══════════════════════════════════════════════════════════════════════

# TASK-ARCH-100 — STEP-05 — Canonical Data Layer Migration (Owner-APPROVED)

The Owner approved Step-05 with four mandatory decisions:
1. **Canonical Data Layer = `data/`.**
2. **Canonical Live Stream = `data_layer/live_data/`.**
3. **Canonical MarketSnapshot = `data_layer.live_data.market_data.MarketSnapshot`** — no
   other `MarketSnapshot` *class* may remain.
4. **DELETE forbidden.** Only Migration / Compatibility / Refactoring /
   Wrapper / Adapter. A legacy module reaches DEPRECATED only after its
   functionality is fully migrated to canonical AND the Owner approves;
   only a later phase may DELETE.

Governing lens (Owner's Final Instruction): the goal is unification
under one canonical architecture with **zero feature loss**, not code
reduction.

## What was executed this turn (concrete, reversible, no feature loss)

### Step 8 — MarketSnapshot Refactor (DONE)
`data_layer/live_data/market/market_data.py`'s projection-snapshot class (a market-*state*
summary: trend/liquidity/session/volatility/regime/structure primitives)
was **renamed** `MarketSnapshot` → `MarketStateSnapshot`, with a
backward-compatible `MarketSnapshot = MarketStateSnapshot` alias kept in
the module. Result:
- The only class in the repository literally *defined* as
  `class MarketSnapshot` is now the canonical
  `data_layer.live_data.market_data.MarketSnapshot` (a multi-timeframe candle container
  — a genuinely different shape) — satisfies Owner decision 3.
- No delete; the projection class and every field/method are intact —
  satisfies decision 4 and feature preservation.
- `market/__init__.py` and `data_layer/live_data/market/market_manager.py` updated to the new
  canonical name; the `MarketSnapshot` alias is still exported.
- The three `tests/market/*` suites that import `MarketSnapshot` from
  `data_layer.live_data.market.market_data` were deliberately left importing via the alias —
  so they now actively **prove** the backward-compat shim works. All 108
  `tests/market/` + `tests/stream/` tests pass unchanged.

### Legacy status markers (DONE — status only, no behavior change)
`stream/` and `market/` (both `__init__.py` docstrings + `README.md`)
now carry a **LEGACY (NON-CANONICAL)** banner recording Owner decisions
1 & 2. They are explicitly marked **NOT DEPRECATED** (per the Owner's
staging rule) and **NOT deleted**. `market/`'s banner additionally
records that its projection facade is a unique capability under an OPEN
Migration Proposal (Step 7) that must not be moved without approval.

## Step 1 — Legacy Module Audit

| Module | Purpose | Consumer | Producer | Tests | Docs | Status |
|---|---|---|---|---|---|---|
| `data_layer/live_data/stream/price_stream.py` (`PriceStream`) | Composition root: ingest/poll → validate → state → route | none (only `tests/stream/`) | `data_layer/providers` (via poll) | `tests/stream/` | `stream/README.md` | LEGACY |
| `data_layer/live_data/stream/stream_event.py` (`StreamEvent`) | Transport shape + `from_candle()` | `stream/` internals | — | yes | README | LEGACY |
| `data_layer/live_data/stream/stream_validator.py` (`StreamValidator`) | `validate()`→`ValidationResult` (empty/OHLC/future ts/dup/out-of-seq) | `data_layer/live_data/stream/price_stream.py` | — | yes | README | LEGACY — **unique validation contract** (see Step 3) |
| `data_layer/live_data/stream/stream_state.py` (`StreamState`) | Last price/event/ts/provider/mode runtime state | `data_layer/live_data/stream/price_stream.py` | — | yes | README | LEGACY |
| `data_layer/live_data/stream/current_price.py` (`CurrentPrice`) | Fast single-value latest-price read | `stream/`, `data_layer/live_data/market/current_price.py` | — | yes | README | LEGACY (canonical: `data_layer.live_data.current_price_provider.CurrentPrice`) |
| `data_layer/live_data/stream/stream_mode.py` (`StreamMode`) | Forex 24×5 weekend/market-closed clock + `resolve_mode()` | `stream/`, `data_layer/live_data/market/session_state.py` | — | yes | README | LEGACY — **unique Forex clock** (see Step 3) |
| `data_layer/live_data/stream/stream_router.py` (`StreamRouter`) | Fan-out to subscribers, per-subscriber fault isolation | `data_layer/live_data/stream/price_stream.py` | — | yes | README | LEGACY (canonical: `data_layer.event_system.EventBus`) |
| `data_layer/live_data/stream/stream_subscriber.py` (`StreamSubscriber`) | Subscriber ABC + `CallbackSubscriber` | `stream/` | — | yes | README | LEGACY (canonical: `EventBus` subscription) |
| `data_layer/live_data/market/market_manager.py` (`MarketManager`) | Facade entry: build/store current market view | none (only `tests/market/`) | `context/` snapshot + `stream/CurrentPrice` | `tests/market/` | `market/README.md` | LEGACY — **unique projection facade** |
| `data_layer/live_data/market/market_data.py` (`MarketData`, `MarketStateSnapshot`) | Aggregated read container + immutable projection snapshot | `market/` | — | yes | README | LEGACY; snapshot renamed (Step 8) |
| `data_layer/live_data/market/market_structure.py`, `trend_state.py`, `liquidity_state.py`, `session_state.py`, `volatility_state.py`, `regime_state.py` | Read-only projections of `context/` snapshot into typed view models | `data_layer/live_data/market/market_manager.py` | `context.snapshot.ContextSnapshotSchema` | yes | README | LEGACY — **unique projection capability** |
| `data_layer/live_data/market/candle.py`, `ticker.py`, `orderbook.py`, `current_price.py` (`MarketPrice`) | Read models + adapters | `market/` | `stream/` / `data_layer.providers` | yes | README | LEGACY |

`data/` canonical modules (already inventoried in `02_Data_Layer.md` and
Step 2 of this document's Phase-01 audit) are unchanged by this step.

## Step 2 — Canonical Mapping

| Legacy | Canonical equivalent | Relationship |
|---|---|---|
| `data_layer/live_data/stream/price_stream.py` `PriceStream` | `data_layer/live_data/price_stream.py` `PriceStream` + `price_stream_service.py` | canonical is the lifecycle state machine + service |
| `data_layer/live_data/stream/current_price.py` `CurrentPrice` | `data_layer/live_data/current_price_provider.py` `CurrentPrice` (wired to Telegram) | canonical has the real consumer |
| `data_layer/live_data/stream/stream_state.py` `StreamState` | `data_layer/live_data/price_cache.py` `PriceCache` | last-value runtime store |
| `data_layer/live_data/stream/stream_router.py` + `stream_subscriber.py` | `data_layer/event_system/event_bus.py` `EventBus` (`PRICE.UPDATED`) | canonical uses pub/sub instead of router/subscriber |
| `data_layer/live_data/stream/stream_mode.py` `StreamMode` | `data_layer/live_data/price_stream.py` `MarketCalendar`/waiting-mode (DD-047) | **partial** — see Step 3 gap |
| `data_layer/live_data/stream/stream_validator.py` `StreamValidator` | `data_layer/live_data/market_data.py` `_validate_and_clean` + `data_layer/data_validation/data_quality.py` | **partial** — see Step 3 gap |
| `data_layer/live_data/stream/stream_event.py` `StreamEvent` | `data_layer/live_data/stream_event.py` `StreamEvent` | same concept |
| `market/*` projection facade | **none** | **no canonical equivalent — Step 7 proposal** |
| `data_layer/live_data/market/market_data.py` `MarketSnapshot` | `data_layer.live_data.market_data.MarketSnapshot` (canonical) | resolved via rename+alias (Step 8) |

## Step 3 — Feature Comparison (no feature may be lost)

| Feature | Legacy home | Canonical equivalent | Gap? |
|---|---|---|---|
| Live tick ingest + lifecycle | `stream/PriceStream` | `data_layer/live_data/PriceStream`+service | none |
| Latest-price single read | `stream/CurrentPrice` | `data_layer/live_data/current_price_provider` | none |
| Fan-out to consumers | `stream/StreamRouter`+`Subscriber` | `data_layer/event_system/EventBus` | none (different shape, equivalent capability) |
| Transport event shape | `stream/StreamEvent` | `data_layer/live_data/StreamEvent` | none |
| **Tick validation contract** (`validate()`→`ValidationResult`: empty/OHLC/future-ts/duplicate/out-of-sequence, never raises) | `stream/StreamValidator` | `data/`'s validation is candle-list cleaning in `market_data._validate_and_clean` + `data_quality`; **no standalone stream-tick validator with this exact contract** | **PARTIAL GAP** — capability must be added to canonical before `stream/` can be deprecated |
| **Forex 24×5 market clock** (`is_weekend`/`is_market_open`, Sun 22:00–Fri 22:00 UTC) | `stream/StreamMode` | `data_layer/live_data/` has a `MarketCalendar` protocol + `AlwaysOpenCalendar`; **no concrete Forex-session clock** | **PARTIAL GAP** — a concrete Forex `MarketCalendar` must exist in canonical before `stream/` can be deprecated |
| **context→market-state projection** (trend/liquidity/session/volatility/regime/structure read models over a `ContextSnapshotSchema`) | `market/` (whole package) | **none** | **FULL GAP** — Step 7 Migration Proposal |

No feature was removed this turn. The three gaps above are the exact
work that must land in canonical *before* the corresponding legacy
package may move to DEPRECATED (Owner's staging rule) — none of that is
done here; it is proposed (Step 4/7) for separate, Owner-approved tasks.

## Step 4 — Migration Plan (per legacy area)

1. **`stream/` core (event/state/current-price/router/subscriber/price-stream):**
   already have canonical equivalents → migration is **re-point + retire**,
   no new code. Action when approved: none required in canonical; mark
   these `stream/` modules DEPRECATED once the two PARTIAL gaps below are
   closed (so the *whole* package can retire together, not piecemeal).
2. **`stream/StreamValidator`:** ADD a canonical stream-tick validator
   (new file in `data_layer/live_data/`, reusing `data_quality`'s existing checks
   where possible — Reuse First) that reproduces the `ValidationResult`
   contract. Then `stream/StreamValidator` → DEPRECATED.
3. **`stream/StreamMode`:** ADD a concrete Forex `MarketCalendar`
   implementation in `data_layer/live_data/` (the protocol already exists — this
   is extending, not creating a new abstraction). Then `stream/StreamMode`
   → DEPRECATED.
4. **`market/` projection facade:** Step 7 Migration Proposal — do NOT
   move without Owner approval.
5. **`MarketSnapshot` collision:** DONE this turn (Step 8).

Each of 2/3/4 is its own future Owner-approved sub-task with full tests;
none is executed here.

## Step 6 — Feature Preservation (verified this turn)

| Feature | Migrated? | Verified? |
|---|---|---|
| `MarketSnapshot` (canonical candle container) | unchanged | ✅ 5375 tests pass |
| `market/` projection snapshot (now `MarketStateSnapshot`) | preserved (renamed only) | ✅ 108 market/stream tests pass via alias |
| Backward-compat `data_layer.live_data.market.market_data.MarketSnapshot` import | preserved (alias) | ✅ tests import via alias and pass |
| All `stream/` + `market/` behavior | preserved (status-only markers) | ✅ unchanged, tests pass |

Nothing was migrated *away* this turn, so nothing could be lost. The
gaps in Step 3 are documented as pre-conditions for future deprecation.

## Step 7 — Market Projection Audit (Migration PROPOSAL — needs Owner approval)

- **Capability:** read-only projection of an already-computed
  `context.snapshot.ContextSnapshotSchema` (+ current price) into typed
  view models (trend/liquidity/session/volatility/regime/structure) and
  an immutable `MarketStateSnapshot`. No structure math (that is
  `context/`, FROZEN) — pure projection.
- **Responsibility:** give future consumers (chart/AI/telegram/monitoring)
  one read surface, so none reach into `context/` internals.
- **Dependencies:** `context_layer.context_engine.snapshot` (public contract only),
  `stream/current_price` (legacy — would re-point to canonical
  `data_layer.live_data.current_price_provider`).
- **Consumer:** none today.
- **Future location (proposed):** a new read-facade under the canonical
  Data Layer or as a consumer of `data_layer/market_memory/MemoryReader` (MA-002),
  which is the canonical read-only surface — the projection would read
  the canonical snapshot + `MemoryReader` instead of `stream/`. This is
  the Reuse-First-aligned target (build on MA-002, don't duplicate it).
- **Proposal:** migrate `market/`'s projection to read canonical
  (`MemoryReader` + `ContextSnapshotSchema`) as its own Owner-approved
  sub-task; until then `market/` stays in place, LEGACY, not deleted,
  not deprecated. **Not moved this turn.**

## Step 9 — Import Report

- Broken imports after this step: **0** (verified — all 657 modules
  import cleanly; full suite green).
- `data_layer.live_data.market.market_data.MarketSnapshot` importers: still resolve (alias).
- Canonical `data_layer.live_data.market_data.MarketSnapshot` importers (`core/pipeline.py`,
  `context_layer/trend/htf_bias.py`, `backtesting/`, many tests): unaffected — that
  class was never touched.

## Step 13 — Module Status

| Status | Modules |
|---|---|
| **Canonical** | all of `data/` (incl. `data_layer/live_data/`, `data_layer/market_memory/`, `data_layer/event_system/`, `data_layer/live_data/current_price_provider.py`, `data_layer/live_data/market_data.py`) |
| **Legacy (non-canonical, active, not deprecated)** | all of `stream/`, all of `market/` |
| **Deprecated** | none (Owner staging rule — nothing migrated-and-approved yet) |
| **Frozen** | `data_layer/providers/` (per its own docs), `data_layer/market_memory/` (MA-001), `context/` (Core layer) |
| **Deleted** | none (DELETE forbidden) |

## Repository Tree (Data-Layer-relevant, after this step)

```
data/                     CANONICAL Data Layer
  ├── stream/             CANONICAL live stream
  ├── memory/             CANONICAL MarketMemory (MA-001)
  ├── events/             CANONICAL EventBus
  ├── providers/          Historical + Live providers (FROZEN)
  ├── bootstrap/          Bootstrap + Recovery
  ├── persistence/ snapshots/ replay/ normalization/
  ├── market_data.py      CANONICAL MarketSnapshot lives here
  ├── market_data_service.py   HistoricalDataService (target name)
  └── current_price_provider.py  CANONICAL CurrentPriceProvider (Telegram-wired)
stream/                   LEGACY (non-canonical) — retire after gap-close
market/                   LEGACY (non-canonical) — projection = OPEN proposal
```

## Known Issues

1. Two PARTIAL feature gaps (StreamValidator contract; concrete Forex
   `MarketCalendar`) must land in canonical before `stream/` can be
   deprecated — Step 3/4. **(CLOSED by TASK-ARCH-101 Parts 1 & 2.)**
2. ~~`market/`'s projection facade has no canonical home yet — Step 7
   proposal.~~ **CORRECTED (TASK-ARCH-101 Part 3, Owner ruling):
   `market/` is NOT a Data Layer component and is NOT migrated into
   `data/` — it is an upper-layer component consuming Data Layer + Core.
   This Step-05 audit's treatment of `market/` as a Data-Layer
   migration target was a mis-classification; see `TASK-ARCH-101.md`
   Part 3 and `02_Data_Layer.md`'s "Data Layer boundary" section.**
3. Pre-existing, unrelated `DeprecationWarning: invalid escape sequence
   '\-'` in `market/__init__.py` line 1 (a docstring backslash) —
   noted, not fixed (out of this step's scope; touching it is optional
   cleanup, not migration).

## Recommendations

1. Approve the two small canonical additions (StreamValidator, Forex
   `MarketCalendar`) as one focused sub-task — they are the only things
   standing between `stream/` and a clean, whole-package deprecation.
2. Approve the Step 7 projection migration target (recommend: rebuild
   `market/`'s projection as a consumer of `MemoryReader` (MA-002) +
   `ContextSnapshotSchema`, not a copy) as its own sub-task.
3. Keep `stream/`/`market/` LEGACY (not deprecated) until 1 & 2 land and
   are verified feature-complete — exactly the Owner's staging rule.

## Status

```
TASK-ID:    TASK-ARCH-100 STEP-05 (Canonical Data Layer Migration)
Status:     STEP-05 PARTIAL-DONE, REVIEW.
Done:       MarketSnapshot collision resolved (Step 8, rename+alias, no
            delete, backward compatible); stream/ + market/ marked
            LEGACY (non-canonical, NOT deprecated); full audit/plan/
            proposals (Steps 1-4, 6, 7, 9, 13) delivered.
Not done:   The two canonical feature additions (StreamValidator, Forex
            MarketCalendar) and the market/ projection migration -- each
            proposed for its own Owner-approved sub-task, per the Owner's
            "migrate-then-deprecate, never delete" staging rule.
Verified:   5375 tests pass (no coverage loss), 0 broken imports across
            657 modules, python main.py unchanged, no .py logic in
            Core/Decision/Risk/Strategy/AI/Platform touched.
Next step:  Owner approves the two feature-migration sub-tasks and the
            Step 7 projection target; Worker executes each as its own
            validated commit; only then do stream/ + market/ move to
            DEPRECATED.
```
