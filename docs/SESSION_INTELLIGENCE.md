# Session Intelligence Foundation (Phase A6)

## Purpose

Classifies which trading session (Asia, London, New York, the London/
New York overlap, or off-hours) a candle falls into, and derives two
real, data-backed statistics from that classification per session:
average range (a volatility proxy) and liquidity-sweep activity.
**Session Intelligence is context, not a decision.** It never
generates a signal and is not a strategy — see `context/README.md`
for what it does not do.

This phase exists because the roadmap named "WHEN?" (which session)
as the last major missing piece of market context — GoldBot already
knew Structure, Liquidity, Wyckoff phase, and HTF trend, but nothing
described which part of the trading day a candle belonged to.

## Architecture

Like Wyckoff (Phase A5) and unlike HTF Bias (Phase A2), Session
Intelligence needed **no `core/pipeline.py` change**. Session
classification depends only on a candle's own timestamp — the same
execution-timeframe candles every other `context/` detector already
receives, not a separate multi-timeframe fetch. It is the 7th
detector inside `ContextEngine.build()`:

```
Candles
  -> ... (Structure, BOS/CHoCH, Liquidity, OB, FVG, AMD, Wyckoff)
  -> Session Events           (context_layer/session/session.py, Phase A6)
  -> ContextSnapshot          (..., wyckoff_events, session_events)
```

`ContextSnapshot` gains an 11th field, `session_events`. Every
existing field keeps its exact name and meaning. Both real
construction sites (`ContextEngine.build()`, and the two tests that
build a `ContextSnapshot` by hand) were updated to supply it,
preserving the dataclass's "every field required, no silent defaults"
convention — same handling as Phase A5's `wyckoff_events` addition.

**Distinct from `data_layer/live_data/session_filter.py`.** That module's
`is_trading_time()` answers a different question — "is it trading
time right now" (wall-clock `datetime.now()`, Tashkent time, a binary
gate for whether the pipeline should run at all) — not "which session
was this candle in" (any candle's own UTC timestamp, a five-way
classification for describing context after the fact). This module
does not read, call, or duplicate `session_filter.py`'s logic; the two
serve unrelated purposes and use unrelated time conventions (UTC here,
Tashkent there).

**Reuse, not duplication**: `compute_session_liquidity_activity()`
reads `context.liquidity.LiquiditySweepEvent` — already detected,
unchanged — grouping existing sweep timestamps by session rather than
detecting anything new.

## Inputs

- `classify_session(timestamp)` — any `datetime`.
- `detect_session_events(candles)` — `Sequence[Candle]`, the same
  execution-timeframe candles every other detector receives.
- `compute_session_volatility(candles)` — same.
- `compute_session_liquidity_activity(liquidity_sweeps)` —
  `Sequence[LiquiditySweepEvent]` (already computed by
  `context_orchestrator.py`).

## Outputs

**`Session`** (enum): `ASIA` / `LONDON` / `LONDON_NEW_YORK_OVERLAP` /
`NEW_YORK` / `OFF_HOURS`. Standard, widely-cited approximate UTC hour
ranges — not official broker/exchange cutoffs (real session activity
ramps up/down gradually, not at a hard clock instant). Deliberately
simplified to non-overlapping hour blocks for this foundation phase,
with the one deliberate exception being the named London/New York
overlap window:

| Session | UTC hours |
|---|---|
| `ASIA` | 00:00–08:00 |
| `LONDON` | 08:00–13:00 |
| `LONDON_NEW_YORK_OVERLAP` | 13:00–16:00 |
| `NEW_YORK` | 16:00–21:00 |
| `OFF_HOURS` | 21:00–24:00 |

**`SessionEvent`** (`ContextSnapshot.session_events`): `index`,
`timestamp`, `session` — emitted only at transitions (sparse, matching
`BosEvent`/`ChochEvent`/etc.'s convention of firing only on a
meaningful change, not every candle).

**`compute_session_volatility(candles) -> Dict[Session, float]`**:
average `(high - low)` range per session, computed directly from real
OHLC data in the provided window — not a fabricated statistic. A
session absent from the window is absent from the result (no `0.0`
placeholder), so a caller can distinguish "no data" from "measured
zero volatility."

**`compute_session_liquidity_activity(liquidity_sweeps) ->
Dict[Session, int]`**: count of already-detected liquidity sweeps per
session — a real, data-backed answer to "which session tends to sweep
liquidity in this window." Same absent-if-empty convention.

Both statistic functions are standalone (not `ContextSnapshot`
fields) — their `Dict[Session, ...]` shape doesn't match the other
per-candle event-list fields, the same reasoning `data_layer/live_data/market_data.py`'s
`MarketSnapshot.quality: Dict[str, str]` already established for a
dict-shaped result living outside a list-of-events contract.

## What was asked but is NOT included in this phase

The roadmap named "volatility," "liquidity probability," and "setup
quality" per session. This phase delivers the first two honestly
(real average range, real sweep counts) and deliberately does **not**
fabricate the third:

- **"Liquidity probability"** would need statistical analysis across
  many historical days to mean anything ("how often does London sweep
  liquidity") — a single pipeline cycle's candle window doesn't carry
  that history. `compute_session_liquidity_activity()`'s per-window
  *count* is the honest building block; a probability derived from it
  needs a backtesting/historical-aggregation layer this phase does not
  build.
- **"Setup quality" per session** is Signal Quality Score's job
  (Phase A4), not a new concept here — see `docs/SIGNAL_QUALITY.md`'s
  Future Expansion section, which already named a `SESSION_ALIGNED`
  criterion as the mechanism. Not wired in this phase (see "What this
  does NOT do" below).

## What this does NOT do

- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — no `strategies/*.py` file reads `Session`/`SessionEvent`.
- Does not add a `SESSION_ALIGNED` criterion to
  `signals/signal_quality.py` — that remains a distinct, separate,
  not-yet-done future step, the same "compute now, connect later"
  posture HTF Bias had between Phase A2 and Phase A3.
- Does not modify `data_layer/live_data/session_filter.py` — different purpose,
  different time convention, left untouched.
- Does not change any existing `ContextSnapshot` field's name or
  meaning — only adds `session_events`.
- Does not write to the database — no schema change, no new table.
- Does not block, delay-gate, or filter the pipeline in any way.

## Future expansion

- **`SESSION_ALIGNED` in Signal Quality Score** — the mechanism is
  already documented in `docs/SIGNAL_QUALITY.md`; wiring it is a
  distinct future step now unblocked by this phase.
- **Historical liquidity probability** — once a backtesting/historical-
  aggregation layer exists, `compute_session_liquidity_activity()`'s
  per-window counts could be aggregated across many windows into a
  real probability, rather than fabricated now.
- **DST-aware session boundaries** — the UTC hour ranges above are a
  deliberate simplification; London/New York's real session hours
  shift with daylight saving in their local time zones. Not addressed
  in this foundation phase.
