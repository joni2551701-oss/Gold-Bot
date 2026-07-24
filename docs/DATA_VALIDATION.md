# Data Validation

How a collected historical candle archive is audited for integrity
(Phase 59.5: Historical Data Collection & Validation Foundation).
Companion to `docs/DATASET_COLLECTION.md` (how the archive is built).

## Scope

Read-only auditing. Nothing here repairs, drops, or corrects a
candle — a validator that found an issue only reports it; fixing a gap
means re-running `data/historical_data_collector.py`'s collection over
that window, a separate, explicit step.

## `data/historical_validator.py`

`validate_historical_candles(candles, timeframe=None,
expected_provider=None) -> ValidationReport` checks a
`List[database.raw_candle_models.RawCandle]` for:

| Check | What it means |
|---|---|
| Missing candles | A gap larger than the timeframe's expected step between two adjacent (sorted) candles. Counted per gap event, not per missing timestamp — see `analytics/gap_report.py` for a per-timestamp enumeration. |
| Duplicate candles | A timestamp appearing more than once in the input. |
| Timestamp ordering | An adjacent pair (in the order given, not re-sorted) where the later element isn't strictly after the earlier one. |
| Future timestamps | A candle timestamped after "now". |
| Timezone mismatch | A candle with a timezone-naive timestamp — every `RawCandle.timestamp` in this codebase is expected timezone-aware. |
| Invalid OHLC | `high < max(open, close)` or `low > min(open, close)` — a geometrically impossible candle. |
| Provider mismatch | A candle's `.provider` differs from a caller-supplied `expected_provider` (skipped entirely — always 0 — when no `expected_provider` is given). |

`ValidationReport.valid` is `True` only when every count above is
zero. Never raises: an empty candle list is a valid, trivial input,
not an exception.

### Relationship to `data/data_quality.py` (Phase A8)

`data_quality.py`'s `assess_data_quality()` is a different tool for a
different job: it scores a single, already-fetched, in-memory
`List[data.twelve_data_client.Candle]` (no symbol/timeframe/provider
of its own) for the live trading pipeline's own `market_data` stage,
producing one 0-100 score per pipeline cycle. `historical_validator.py`
audits a persisted, multi-symbol/multi-timeframe/multi-provider
archive (`database.raw_candle_models.RawCandle`) for an offline
dataset review, producing structured per-issue-type counts. Two checks
(invalid OHLC, gap detection) are intentionally re-implemented
independently rather than imported from `data_quality.py` — the same
"small, disclosed duplication of intent, not code" precedent that
module's own docstring already established for `market_data.py`. The
one piece safely reused is `data_quality.INTERVAL_DELTAS` — a public,
same-package module constant, not a private method.

## `analytics/gap_report.py`

Where `historical_validator.py` answers "how many gap events/
duplicates exist", `gap_report.py`'s `build_gap_report(candles,
symbol, timeframe) -> GapReport` answers "which exact timestamps" —
one `GapEntry(timestamp, gap_type)` per individual missing timestamp
(enumerated at the timeframe's own step, capped at
`MAX_GAP_ENTRIES = 1000` to avoid enumerating an absurdly large gap)
and one per distinct duplicated timestamp. `format_gap_report()`
renders the exact shape this phase's own brief names:

```
XAUUSD
M15
2026-07-01
02:15 missing
04:30 missing
17:45 duplicate
```

## `analytics/dataset_report.py`

A dataset-wide overview, not a single-timeframe audit:
`build_dataset_report(candles) -> DatasetReport` groups a mixed
`List[RawCandle]` by `(symbol, timeframe)`, runs
`historical_validator.validate_historical_candles()` per group
(reused, not reimplemented) and sums the duplicate/missing/invalid
counts across every group, plus computes `coverage_pct` — the mean,
across every group, of `(actual candle count / expected candle count
for that group's own span) * 100`, capped at 100 per group. This mean
is a simple, unweighted average across groups (disclosed, not hidden —
see the module's own docstring) — a thin, mostly-empty group counts
equally toward it as a dense, complete one.

`format_dataset_report()` renders:

```
Provider: twelvedata
Symbols: XAUUSD
Timeframes: M15
Candles: 4032
Oldest candle: 2026-06-24T00:00:00+00:00
Newest candle: 2026-07-01T00:00:00+00:00
Coverage %: 98.5
Duplicates: 0
Missing: 3
Invalid: 0
```

## `data/provider_comparison.py`

Cross-provider validation, foundation only: `compare_providers(
candles_a, candles_b, tolerance=0.5) -> List[ProviderComparison]`
matches two providers' candle lists by timestamp and reports
close/high/low/spread differences for every timestamp both sides
have. **No auto-correction happens anywhere** — this module never
merges, overwrites, or picks a "winning" provider; it only reports
what it observed. A future reconciliation policy (e.g. "prefer
provider X on disagreement") is explicitly out of scope for this
foundation phase.

## Owner visibility (foundation only)

`telegram/owner/dataset_commands.py`'s `get_dataset_status()` and
`get_provider_compare()` surface these reports as text. Neither is
wired into the live Telegram bot; see `telegram/owner/README.md`.
