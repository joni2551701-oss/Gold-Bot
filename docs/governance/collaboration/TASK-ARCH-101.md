# TASK-ARCH-101 — Canonical Live Data Completion

Branch: `claude/collaboration`. Priority: CRITICAL. Owner-APPROVED
(three decisions). Status: **Parts 1 & 2 DONE; Part 3 RESOLVED by Owner ruling
(MarketProjection is upper-layer, not Data Layer — no migration into
`data/`); Part 4 partial (stream/ ready for deprecation review).**

Governed by `TASK-GOV-001.md` Laws 1–12, Constitution Article 7 (Reuse
Principle — mandatory for this task per the Owner's own rule), and the
Owner's Final Instruction: the goal is to feature-complete the
canonical Data Layer with **zero feature loss**, NOT to delete; legacy
moves to DEPRECATED only after full migration AND Owner approval.

## Owner Decisions (all APPROVED)

1. Add a **canonical StreamValidator** in `data/stream/` — migrate the
   legacy `stream/StreamValidator` features, no duplicate, integrate
   with existing architecture.
2. Add a **canonical MarketCalendar** (clearer name than `StreamMode`)
   in `data/stream/` — Forex 24×5 sessions, weekend/open/close,
   gating when the live stream runs. Part of Data Layer → Live Data.
3. **Keep `market/`'s projection but migrate it** onto the canonical
   `MemoryReader` (MarketMemory → MemoryReader → Market Projection →
   Consumers), consistent with Single Source of Truth.

## Part 1 — Canonical StreamValidator (DONE)

New: `data/stream/stream_validator.py` — `StreamValidator` +
`ValidationResult(valid, code, reason)`, validating the canonical
`data.stream.stream_event.StreamEvent` (a price TICK). Checks migrated
from the legacy validator: `empty`, `asset` mismatch, `price`
integrity (missing/non-finite/non-positive/negative-volume),
`timestamp` (future beyond 5-min skew tolerance), `duplicate`,
`sequence`. Never raises.

**Reuse-First / no-duplication (Constitution Article 7):** the legacy
validator also did OHLC-candle integrity checks because the legacy
`StreamEvent` carried OHLC. The canonical `StreamEvent` is a single
tick (no OHLC), so OHLC validation is **not** re-implemented here — it
already exists at its correct canonical layer (`data.market_data`'s
`_validate_and_clean` + `data.data_quality.assess_data_quality`). Only
the tick-level checks that had no canonical home were migrated. No
feature is lost: OHLC validation is preserved, at the candle layer;
tick validation is now present, at the tick layer.

**Integration (additive, non-breaking):** `data/stream/price_stream.py`
`PriceStream` gained an optional `validator=None` constructor param.
When supplied, `_forward_ordered` drops any event failing validation
(new `dropped_invalid` stat), fully fail-safe (a validator exception
is logged and treated as valid — it never blocks the stream). Default
`None` → existing behavior and all pre-existing PriceStream tests
unchanged. `PriceStreamService.register_source(..., validator=None)`
threads it through; the Phase-3 `CurrentPriceProvider` default path is
untouched (it passes no validator).

Tests: `tests/data/stream/test_canonical_stream_validator.py` (13) +
2 PriceStream integration tests.

## Part 2 — Canonical MarketCalendar (DONE)

New: `data/stream/market_calendar.py` — `ForexMarketCalendar` +
module-level `is_weekend()` / `is_market_open()` (same names/semantics
as the legacy `stream/stream_mode.py`).

**Reuse-First win:** `data/stream/price_stream.py` already defined the
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

Tests: `tests/data/stream/test_market_calendar.py` (10).

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
consumer module beside `data/memory/`). Naming/placement is part of the
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
  canonical current-price source (`data.current_price_provider`) is a
  small, separate, future item — it does not require moving the
  projection anywhere.
- The Data Layer boundary principle ("Data Layer = raw market data only;
  never knows Context/Strategy/Decision; Market Projection is an
  upper-layer consumer") is recorded in `02_Data_Layer.md` so future
  tasks don't repeat the mis-classification.

Part 3 is therefore **DONE** (resolved by ruling); no code migration was
needed or performed.

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
| Tick validation (`ValidationResult` contract) | `data/stream/stream_validator.py` | ✅ 13 tests |
| OHLC-candle validation | already canonical (`data_quality`/`_validate_and_clean`) — not duplicated | ✅ existing tests |
| Forex 24×5 weekend/open/close clock | `data/stream/market_calendar.py` | ✅ 10 tests |
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
  `data/stream/` (2 new modules + 2 additive param wirings) and
  status-only markers.

## Known Issues / Next

1. Part 3 — RESOLVED by Owner ruling (MarketProjection is upper-layer,
   not Data Layer; no migration into `data/`). `market/` reclassified,
   out of Data Layer scope. Remaining small item: re-point `market/`'s
   price source from legacy `stream/` to canonical
   `data.current_price_provider` — a separate future task, not blocking.
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
