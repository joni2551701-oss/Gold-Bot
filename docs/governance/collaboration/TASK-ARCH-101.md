# TASK-ARCH-101 — Canonical Live Data Completion

Branch: `claude/collaboration`. Priority: CRITICAL. Owner-APPROVED.
Status: **Parts 1 & 2 DONE; Part 3 resolved (MarketProjection is
upper-layer, not Data Layer) + PART-03 proposal delivered (Owner
approved Option 3A's source pattern; location L1/L2/L3 awaiting Owner
pick; NO projection code written per the proposal-first order);
`stream/` flipped to DEPRECATED, `market/` LEGACY — both no-delete,
no-feature-loss. See PART-03 at the bottom.**

Governed by `TASK-GOV-001.md` Laws 1–12, Constitution Article 7 (Reuse
Principle — mandatory for this task per the Owner's own rule), and the
Owner's Final Instruction: the goal is to feature-complete the
canonical Data Layer with **zero feature loss**, NOT to delete; legacy
moves to DEPRECATED only after full migration AND Owner approval.

## Owner Decisions (all APPROVED)

1. Add a **canonical StreamValidator** in `data_layer/live_data/` — migrate the
   legacy `stream/StreamValidator` features, no duplicate, integrate
   with existing architecture.
2. Add a **canonical MarketCalendar** (clearer name than `StreamMode`)
   in `data_layer/live_data/` — Forex 24×5 sessions, weekend/open/close,
   gating when the live stream runs. Part of Data Layer → Live Data.
3. **Keep `market/`'s projection but migrate it** onto the canonical
   `MemoryReader` (MarketMemory → MemoryReader → Market Projection →
   Consumers), consistent with Single Source of Truth.

## Part 1 — Canonical StreamValidator (DONE)

New: `data_layer/live_data/stream_validator.py` — `StreamValidator` +
`ValidationResult(valid, code, reason)`, validating the canonical
`data_layer.live_data.stream_event.StreamEvent` (a price TICK). Checks migrated
from the legacy validator: `empty`, `asset` mismatch, `price`
integrity (missing/non-finite/non-positive/negative-volume),
`timestamp` (future beyond 5-min skew tolerance), `duplicate`,
`sequence`. Never raises.

**Reuse-First / no-duplication (Constitution Article 7):** the legacy
validator also did OHLC-candle integrity checks because the legacy
`StreamEvent` carried OHLC. The canonical `StreamEvent` is a single
tick (no OHLC), so OHLC validation is **not** re-implemented here — it
already exists at its correct canonical layer (`data_layer.live_data.market_data`'s
`_validate_and_clean` + `data_layer.data_validation.data_quality.assess_data_quality`). Only
the tick-level checks that had no canonical home were migrated. No
feature is lost: OHLC validation is preserved, at the candle layer;
tick validation is now present, at the tick layer.

**Integration (additive, non-breaking):** `data_layer/live_data/price_stream.py`
`PriceStream` gained an optional `validator=None` constructor param.
When supplied, `_forward_ordered` drops any event failing validation
(new `dropped_invalid` stat), fully fail-safe (a validator exception
is logged and treated as valid — it never blocks the stream). Default
`None` → existing behavior and all pre-existing PriceStream tests
unchanged. `PriceStreamService.register_source(..., validator=None)`
threads it through; the Phase-3 `CurrentPriceProvider` default path is
untouched (it passes no validator).

Tests: `tests/data_layer/live_data/test_canonical_stream_validator.py` (13) +
2 PriceStream integration tests.

## Part 2 — Canonical MarketCalendar (DONE)

New: `data_layer/live_data/market_calendar.py` — `ForexMarketCalendar` +
module-level `is_weekend()` / `is_market_open()` (same names/semantics
as the legacy `stream/stream_mode.py`).

**Reuse-First win:** `data_layer/live_data/price_stream.py` already defined the
`MarketCalendar` Protocol (`is_open(now)` / `next_open(now)`) and an
`AlwaysOpenCalendar` (24/7 crypto). `ForexMarketCalendar` is the
missing **concrete** Forex implementation of that **existing**
protocol — not a new abstraction. A `PriceStream(calendar=
ForexMarketCalendar())` gets the legacy `StreamMode`'s
weekend/market-closed behavior for free through PriceStream's existing
waiting-mode machinery (DD-047): market-closed → disconnect, no
provider calls, idle, auto-resume on reopen. The legacy `StreamMode`
enum (ACTIVE/WEEKEND_WAIT/…) maps onto PriceStream's existing
`StreamState` (STREAMING/WAITING_FOR_MARKET/…) — no parallel mode enum
is introduced. Forex session: Sun 22:00 UTC → Fri 22:00 UTC (same
coarse clock as legacy; not a holiday calendar).

Threaded through `PriceStreamService.register_source(..., calendar=
None)`; default unchanged.

Tests: `tests/data_layer/live_data/test_market_calendar.py` (10).

## Part 3 — Market Projection → MemoryReader (DESIGN + one question; NOT executed)

The Owner's target chain is `MarketMemory → MemoryReader → Market
Projection → Consumers`. Auditing `market/` for the migration surfaced
a real design question that Reuse First and STOP → AUDIT → Owner
Decision say I must raise rather than guess:

**`market/`'s projections do not read candles — they read
`context/`'s structure output.** Every `market/` state module
(`trend_state`, `liquidity_state`, `session_state`, `volatility_state`,
`regime_state`, `market_structure`) projects a
`context.snapshot.ContextSnapshotSchema` (BOS/CHoCH/OB/FVG/liquidity/
regime/session — computed by the FROZEN `context/` engine), plus a
current price. `MemoryReader` (MA-002) exposes **candles and price from
`MarketMemory`** — it does **not** expose `context/`'s structure
output. So `MemoryReader → Projection` alone cannot supply what the
projection needs; the structure input must still come from `context/`.

**Three ways to honor the Owner's intent — an Owner decision, not a
Worker one:**

- **3A (recommended):** the canonical projection reads **price/candles
  from `MemoryReader`** (replacing its legacy `stream/CurrentPrice`
  dependency) **and structure from `context/`'s public
  `ContextSnapshotSchema`** (unchanged — that is already the canonical
  context contract). The Owner's chain becomes
  `MemoryReader (price) + ContextSnapshotSchema (structure) →
  Projection → Consumers`. Lowest risk, no change to MA-002 or
  `context/`, preserves every projection feature; only the price source
  is re-homed off legacy `stream/`.
- **3B:** extend `MemoryReader` (MA-002, a Director-accepted frozen
  module) to also surface context structure, so the projection reads
  everything through one reader. Bigger — touches a frozen module and
  couples memory to context.
- **3C:** the canonical projection covers only the price/candle part via
  `MemoryReader`, and structure projection stays separate. Splits a
  capability that is currently one coherent facade.

**New location** (all options): a new canonical package (proposed
`data/projection/` or `market_view/` under the Data Layer, or a
consumer module beside `data_layer/market_memory/`). Naming/placement is part of the
same Owner decision. **Nothing in `market/` was moved or changed for
Part 3** — it stays in place, not deleted, not deprecated, until the
Owner rules.

### Part 3 — RESOLVED by Owner ruling (all three options WITHDRAWN)

The Owner's ruling supersedes the 3A/3B/3C options above — and does so
by rejecting the premise all three shared:

> "MarketProjection Data Layer tarkibiga kirmaydi. U Data Layer va
> GoldBot Core natijalarini iste'mol qiluvchi yuqori qatlam komponenti
> hisoblanadi. Data Layer faqat xom bozor ma'lumotlari (raw market data)
> bilan ishlaydi va Context, Strategy yoki Decision obyektlarini
> bilmaydi."

**MarketProjection is NOT a Data Layer component.** It is an
upper-layer component that consumes Data Layer output (raw price) and
GoldBot Core output (`context/` structure). The Data Layer works only
with raw market data and does not know Context/Strategy/Decision
objects.

This makes 3A/3B/3C all wrong: each would have placed the projection
(which reads `context/`'s `ContextSnapshotSchema`) inside `data/`,
forcing the Data Layer to depend on Context — the exact boundary the
Owner is protecting. (This is why Part 3 was raised as a question, not
executed — 3A would have imported `context/` from a Data-Layer module.)

**Verified in code (this ruling already holds today):**
- `data/` imports nothing from `context/`, `strategies/`, `decision/`,
  `signals/`, or `risk/` (grep: zero) — the Data Layer is raw-market-
  data-only, as the ruling requires.
- `data/` imports nothing from `market/` or `stream/` (zero) — correct
  dependency direction (lower never depends on upper).
- `market/` DOES read `context.snapshot.ContextSnapshotSchema` — which
  is precisely why it belongs above the Data Layer, not in it.

**Resolution / actions taken (documentation only, no code logic):**
- Part 3's "migrate the projection into the Data Layer / onto
  `MemoryReader`" plan is **WITHDRAWN**. `market/` is **not** folded
  into `data/`.
- `market/` is **reclassified**: from the earlier (mistaken)
  "Data Layer legacy duplicate" to an **upper-layer Market View /
  Projection component** (maps to the ecosystem's Application Services /
  market-view tier — see `04_Application_Services.md` / `01`'s layer
  map). Its `__init__`/README markers were corrected accordingly.
- `market/` remains: not deleted, not deprecated, out of the Data Layer
  canonical migration scope. The **only** Data-Layer-migration-relevant
  item left about it is that it currently reads price from the LEGACY
  `stream/CurrentPrice`; re-pointing that one dependency to the
  canonical current-price source (`data_layer.live_data.current_price_provider`) is a
  small, separate, future item — it does not require moving the
  projection anywhere.
- The Data Layer boundary principle ("Data Layer = raw market data only;
  never knows Context/Strategy/Decision; Market Projection is an
  upper-layer consumer") is recorded in `02_Data_Layer.md` so future
  tasks don't repeat the mis-classification.

This resolved the *placement* question (the projection does NOT go into
`data/`). **Follow-up Owner decision (PART-03, this document's bottom
section):** the Owner then APPROVED Option 3A's *data-source pattern* —
the (upper-layer) projection reads market data from `MemoryReader` and
context from `ContextSnapshotSchema`, with `MemoryReader` not extended
and `ContextSnapshotSchema` not moved into `data/`. So there IS a
migration after all, but to a canonical **upper-layer** home, not into
the Data Layer — the two rulings are consistent. The full proposal (7
deliverables, location options L1/L2/L3, diagrams, migration plan, risk,
feature preservation) is in **PART-03** at the bottom of this document,
and no projection code is written until the Owner selects a location.

## Part 4 — Prepare legacy for DEPRECATED (partial)

- **`stream/`:** with Parts 1 & 2 landed, every `stream/` capability now
  has a canonical equivalent (see the mapping in `TASK-ARCH-100.md`
  Step 2 + Parts 1/2 above). `stream/`'s status marker is updated to
  **CANONICAL-FEATURE-COMPLETE, READY FOR DEPRECATION REVIEW** — but is
  deliberately **NOT** flipped to DEPRECATED here: that transition
  needs explicit Owner confirmation (a Worker does not self-approve
  migrate→deprecate). Ready when the Owner says so.
- **`market/`:** blocked on Part 3 — stays LEGACY, unchanged. Cannot be
  prepared for deprecation until its projection is migrated (Part 3)
  and Owner-approved.

## Feature Preservation (verified)

| Legacy feature | Canonical home (this task) | Verified |
|---|---|---|
| Tick validation (`ValidationResult` contract) | `data_layer/live_data/stream_validator.py` | ✅ 13 tests |
| OHLC-candle validation | already canonical (`data_quality`/`_validate_and_clean`) — not duplicated | ✅ existing tests |
| Forex 24×5 weekend/open/close clock | `data_layer/live_data/market_calendar.py` | ✅ 10 tests |
| Waiting/pause on market-closed | PriceStream waiting-mode + `ForexMarketCalendar` | ✅ existing + integration tests |
| market/ projection facade | **not yet — Part 3 pending Owner** | n/a |

No feature was removed. Nothing was deleted.

## Validation

- `pyflakes` clean; `compileall` OK.
- **`pytest`: 5400 passed** (was 5375 — +25 new tests; **no coverage
  loss**, Acceptance Criterion met).
- `python main.py`: unchanged pipeline output.
- 659 modules import clean; **0 broken imports**.
- Forbidden list respected: no Core/Decision/Risk/Strategy/AI/Platform/
  Business/Learning/Media logic touched. `.py` changes confined to
  `data_layer/live_data/` (2 new modules + 2 additive param wirings) and
  status-only markers.

## Known Issues / Next

1. Part 3 — RESOLVED by Owner ruling (MarketProjection is upper-layer,
   not Data Layer; no migration into `data/`). `market/` reclassified,
   out of Data Layer scope. Remaining small item: re-point `market/`'s
   price source from legacy `stream/` to canonical
   `data_layer.live_data.current_price_provider` — a separate future task, not blocking.
2. `stream/` is ready for the DEPRECATED flip on Owner confirmation
   (its two canonical gaps are closed by Parts 1 & 2).
3. Pre-existing unrelated `DeprecationWarning` (`\-` escape) in
   `market/__init__.py` docstring — untouched, out of scope.

## Status

```
TASK-ID:    TASK-ARCH-101 (Canonical Live Data Completion)
Status:     Parts 1 & 2 DONE; Part 3 RESOLVED by Owner ruling; Part 4
            partial (stream/ ready for deprecation review).
Done:       Canonical StreamValidator + PriceStream integration;
            Canonical ForexMarketCalendar (impl of existing protocol);
            Part 3 resolved -- MarketProjection reclassified as an
            upper-layer component, NOT Data Layer, no migration into
            data/; market/ markers corrected; Data Layer boundary
            principle recorded in 02_Data_Layer.md; stream/ marked
            canonical-feature-complete / deprecation-ready.
Not done:   The stream/ DEPRECATED flip (needs Owner confirmation);
            re-pointing market/'s price source off legacy stream/ (small
            separate future item, non-blocking).
Verified:   5400 tests pass (no coverage loss), 0 broken imports across
            659 modules, main.py unchanged, Forbidden list respected;
            Data-Layer-independence principle verified in code (data/
            imports no context/strategies/decision/signals/risk).
Next step:  Owner confirms flipping stream/ to DEPRECATED. The market/
            price-source re-point can be its own small task when wanted.
```

═══════════════════════════════════════════════════════════════════════

# TASK-ARCH-101 PART-03 — Canonical Market Projection: Architecture Proposal

Owner-APPROVED Option 3A and ordered a proposal-first workflow: **no
projection code is written** until the Owner selects the canonical
location. This section is that proposal (the 7 required deliverables).
Also records the two status flips the Owner ordered this turn:
`stream/` → DEPRECATED, `market/` → LEGACY (both no-delete, no-feature-
loss; markers updated in `stream/`+`market/` `__init__.py`/README).

Binding constraints (Owner): Data Layer never gains Context/Strategy/
Decision; `MemoryReader` is NOT extended; `ContextSnapshotSchema` is
NOT moved into the Data Layer; dependency flows top→down only
(DATA LAYER → GOLDBOT CORE → APPLICATION SERVICES → PLATFORM); no new
dependency without Owner approval; if any step would break a layer
boundary in `01_Ecosystem_Architecture.md`, STOP and return to Owner.

## 1. Market Projection Architecture Proposal

Market Projection is an **Application-Services-tier** read-only
component. It produces a market-*state* view (trend, liquidity,
session, volatility, regime, structure presence + current price) by
**projecting** two already-computed, canonical inputs — it computes no
market structure of its own (that is `context/`, FROZEN):

- **Market data** (current price / latest candle) ← `data_layer/market_memory/`
  `MemoryReader` (MA-002), the canonical Data Layer read surface. Used
  as-is; not extended (Owner constraint).
- **Context results** (BOS/CHoCH/OB/FVG/liquidity/regime/session) ←
  `context.snapshot.ContextSnapshotSchema`, the canonical public Core
  contract. Read as-is; not moved into the Data Layer (Owner
  constraint).

Output: the existing read models (`MarketStateSnapshot` + per-aspect
view states), unchanged in shape — only their *price input source*
changes from the legacy `stream.CurrentPrice` to `MemoryReader`, and
their *weekend clock* from `stream.stream_mode.is_weekend` to the
canonical `data_layer.live_data.market_calendar.is_weekend` (already built,
TASK-ARCH-101 Part 2).

This is Option 3A exactly: Projection = f(MemoryReader market data,
ContextSnapshotSchema context) — no Data-Layer/Core boundary crossed,
because Projection sits ABOVE both and depends downward on each.

## 2. Canonical Location — recommendation (Owner selects)

Constitution Article 7: a new top-level package is the highest-cost
option; prefer reusing/relocating an existing one.

- **L1 (RECOMMENDED) — keep the top-level `market/` package as the
  canonical Market Projection home; only re-point its two legacy
  `stream/` couplings to canonical.** `market/` is already a distinct,
  top-level, Application-Services-tier component in the correct
  dependency position (it reads Core's `ContextSnapshotSchema` + Data
  Layer price; nothing in Data Layer or Core imports it). The only
  non-canonical thing about it is *what it reads price from*. So the
  "migration" is: swap `stream.CurrentPrice` → `MemoryReader` and
  `stream.stream_mode.is_weekend` → `data_layer.live_data.market_calendar`. No
  folder move, no new package (lowest cost, Article 7-aligned). The
  package could optionally be renamed `market_view/` or
  `market_projection/` for clarity, but that is cosmetic and separable.
- **L2 — new top-level `market_projection/` (or `market_view/`)
  package**, relocate the projection modules there, retire `market/`.
  Cleaner name, but a new top-level package (highest cost) and a larger
  move (every projection module + its tests) for no functional gain
  over L1.
- **L3 — under a new `application/` (or `services/`) grouping** that
  would also house future Application-Services components. Most
  structurally "correct" long-term, but requires establishing a new
  top-level tier folder now, before other Application-Services members
  exist — premature per Article 13 (Future First designs for it,
  doesn't build the container before there are ≥2 occupants).

**Recommendation: L1** (re-point in place; optional cosmetic rename
later). It preserves every feature, moves no files, creates no new
package, and fully satisfies Option 3A. **Owner selects L1/L2/L3.**

## 3. Dependency Diagram

```
              APPLICATION SERVICES tier
         ┌─────────────────────────────────┐
         │        Market Projection        │   (market/, L1)
         │  (MarketManager / *_state views │
         │   / MarketStateSnapshot)        │
         └───────┬───────────────┬─────────┘
                 │ reads         │ reads
                 ▼ (market data) ▼ (context results)
      ┌────────────────────┐   ┌───────────────────────────┐
      │  data_layer/market_memory/      │   │ context.snapshot.         │
      │  MemoryReader      │   │ ContextSnapshotSchema     │
      │  (DATA LAYER, MA-2)│   │ (GOLDBOT CORE public      │
      └─────────┬──────────┘   │  contract)                │
                │              └───────────────────────────┘
                ▼
      ┌────────────────────┐
      │  data_layer/market_memory/      │
      │  MarketMemory(MA-1) │
      └────────────────────┘
```

Rules honored: every arrow points DOWN (Application Services → Data
Layer, Application Services → Core). Nothing in `data/` or `context/`
points up at Market Projection (verified: zero imports of `market/`
from `data/` or `context/`). `MemoryReader` unchanged;
`ContextSnapshotSchema` unchanged; no Data-Layer↔Context coupling
introduced (Projection depends on BOTH separately — it does not make
the Data Layer know Context).

## 4. Consumer Diagram

```
                     Market Projection
                           │  (one read-only market-state surface)
   ┌──────────┬────────────┼────────────┬───────────────┐
   ▼          ▼            ▼            ▼               ▼
 Telegram   Chart        AI Layer   Monitoring      Web/Dashboard
 (present)  Service     (explain)   (observe)       (future)
```

All consumers are Application-Services / Platform tier or above — they
read Projection, Projection reads down. No consumer today (Projection
is foundation); the diagram is the intended fan-out. Consumers never
reach into `context/` or `data/` directly for a market-state view —
that is the whole point of the projection (one surface).

## 5. Migration Plan (L1; executed only after Owner selects a location)

Per-file, re-point-only, no logic rewrite:

1. `market/current_price.py` — read latest price from `MemoryReader`
   (`get_last_candle(...).close` / forming candle) instead of
   `stream.current_price.CurrentPrice`. Keep the `MarketPrice`
   output shape.
2. `market/session_state.py` — import `is_weekend` from
   `data_layer.live_data.market_calendar` instead of `stream.stream_mode`.
3. `market/market_manager.py` — its price input already comes via
   `current_price.py`; update the type/source references accordingly.
4. `market/candle.py` — adapt from `MemoryReader`'s `CandleRecord` /
   canonical `data_layer.live_data.StreamEvent` instead of `stream.StreamEvent`.
5. Everything reading `ContextSnapshotSchema` — UNCHANGED (already
   canonical Core contract).
6. Tests (`tests/market/`) — updated to the canonical price/clock
   sources; coverage preserved.
7. Once `market/` no longer imports `stream/`, `stream/` has no
   importers left → it becomes eligible for the later Owner-authorized
   DELETE phase (separate task; not part of this migration).

Sequencing: this runs as its own Owner-approved commit AFTER the
location decision; it does not touch Data Layer or Core.

## 6. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data-Layer/Core boundary accidentally crossed | Low | High | Projection depends DOWN on each input separately; `data/` still imports no `context/` (CI-checkable grep); STOP-and-audit rule if any Data-Layer file would import Context |
| `MemoryReader` current-price semantics differ from `stream.CurrentPrice` | Medium | Medium | Both resolve to "latest known price"; validate with a projection test asserting equal behavior before/after re-point; MemoryReader read is fail-safe (None → UNKNOWN, already the projection's missing-data contract) |
| Feature loss during re-point | Low | High | Re-point only (no logic rewrite); Feature Preservation Report (§7) enumerates every projection field; tests updated not weakened |
| `stream/` deleted too early (still imported by `market/`) | Low | High | DELETE is a separate later phase, explicitly gated on `market/` no longer importing `stream/` (§5.7); `stream/` is DEPRECATED (not deleted) now |
| New top-level package cost (if L2/L3) | — | Medium | L1 recommended precisely to avoid it (Article 7) |

## 7. Feature Preservation Report

Every projection capability, and where it comes from after 3A:

| Projection feature | Source before | Source after (3A) | Preserved? |
|---|---|---|---|
| Current price | `stream.CurrentPrice` | `MemoryReader` (latest candle/forming close) | ✅ re-point |
| Trend state | `ContextSnapshotSchema.structure.trend` | same | ✅ unchanged |
| Liquidity state | `ContextSnapshotSchema.liquidity` | same | ✅ unchanged |
| Session state | context session + `stream.is_weekend` | context session + `data_layer.live_data.market_calendar.is_weekend` | ✅ re-point clock |
| Volatility state | `ContextSnapshotSchema.regime` | same | ✅ unchanged |
| Regime state | `ContextSnapshotSchema.regime` | same | ✅ unchanged |
| Structure view (BOS/CHoCH/OB/FVG) | `ContextSnapshotSchema.structure/zones` | same | ✅ unchanged |
| `MarketStateSnapshot` (serializable summary) | `market/market_data.py` | same (already renamed, Step 8) | ✅ unchanged |
| Candle read model | `stream.StreamEvent` adapter | `MemoryReader` `CandleRecord` / canonical `StreamEvent` adapter | ✅ re-point |

No feature is dropped; only the two Data-Layer input *sources* change
from legacy `stream/` to canonical `MemoryReader`/`market_calendar`.
The context-projection logic — the unique capability — is untouched.

## PART-03 — L1 Migration EXECUTED (Owner selected L1)

The Owner selected **L1** (keep top-level `market/`, re-point only its
legacy `stream/` couplings). Executed exactly as the §5 plan, minimal,
no logic rewrite, all features preserved:

1. `market/session_state.py` — `from stream.stream_mode import
   is_weekend` → `from data_layer.live_data.market_calendar import is_weekend`
   (the canonical clock built in Part 2; identical semantics).
2. `market/current_price.py` — `read_current_price` now reads the
   freshest last candle from a `data_layer.market_memory.MemoryReader` (was a
   duck-typed `stream.CurrentPrice`). Added `MarketPrice.from_candle_record`.
   Fail-safe (unknown asset → None).
3. `market/market_manager.py` — `build_market_data(..., stream_current_price=)`
   → `build_market_data(..., memory_reader=)`; reads price via the
   canonical `MemoryReader`.
4. `market/candle.py` — added `from_candle_record` (MemoryReader
   CandleRecord adapter); `from_stream_event` kept as a generic,
   duck-typed, `stream`-import-free adapter (backward-compatible name).
5. Tests — `tests/market/test_market_current_price.py` rewritten to use
   a real `MemoryReader` (hydrated `MarketMemory`) instead of a
   `stream.CurrentPrice`; all other market tests unchanged.
6. Markers — `market/` flipped **LEGACY → CANONICAL PROJECTION**;
   `stream/` marker notes it now has **zero non-test importers**.

**Result:** `market/` has **zero `stream` imports** (verified by grep);
nothing outside `stream/`+`tests/stream/` imports `stream/` anymore. The
projection reads exactly its two Owner-approved canonical inputs
(`MemoryReader` + `ContextSnapshotSchema`) and nothing else. Every
projection feature preserved; no logic rewritten; no new package; no
Data-Layer↔Context coupling introduced (Application Services → Data
Layer, → Core; strictly downward).

## PART-03 Status

```
TASK-ID:    TASK-ARCH-101 PART-03 (Canonical Market Projection)
Status:     DONE. L1 migration executed; market/ is the Canonical
            Market Projection; stream/ DEPRECATED with zero non-test
            importers.
Done:       market/ decoupled from stream/ (zero stream imports),
            reads MemoryReader + ContextSnapshotSchema only; markers
            LEGACY->CANONICAL PROJECTION; every feature preserved.
Not done:   The stream/ DELETE -- a separate, later, Owner-authorized
            phase (now unblocked: stream/ has no non-test importers).
Verified:   Full suite passes (no coverage loss); market/ has 0 stream
            imports; no logic rewritten; Forbidden list respected (no
            new package, no Data-Layer/Context coupling, no feature
            removed).
Next step:  Owner may, when ready, authorize a separate task to DELETE
            the DEPRECATED stream/ (no importers remain).
```
