# Pre-Phase 59 Architecture Readiness Review

Requested by the Director after Phase A19, before Phase 59 (Real
Market Validation) begins. The Director's own audit listed nine
concerns (AC-01 through AC-07, plus Session Intelligence and Data
Quality) as `🟡` needing foundation work. **A verification pass against
the real codebase found six of the nine already fully built** (across
Phases A2, A5, A6, A7, A8, A9, A11, A12), one partially built (AC-02,
now completed), and one genuinely unwired (AC-03, now wired). This
document is that verification, plus the two pieces of real work this
review added.

## Summary

| Item | Director's assessment | Verified status |
|---|---|---|
| AC-01 HTF Bias | 🟡 needs foundation | ✅ Already built (Phase A2), already wired into Decision Engine (Phase A3) |
| AC-02 Wyckoff/AMD | 🟡 needs verification | 🟡→✅ Wyckoff/AMD detection already built; the requested 5-state `MarketPhase` model did not exist — **built in this review** |
| AC-03 Signal + Context Historical Link | ⭐⭐⭐ most important | ❌→✅ `SignalSchema`/`ContextSnapshotSchema` (A15/A16) existed but were never wired together — **wired in this review** |
| AC-04 Asset Foundation | 🟡 needs foundation | ✅ Already built (Phase A12) |
| AC-05 Strategy Lifecycle | 🟡 mandatory | ✅ Already built (Phase A11) |
| AC-06 Session Intelligence | 🟡 needs verification | ✅ Already built (Phase A6) |
| AC-07 Data Quality (API errors) | 🟡 mandatory | 🟡→✅ Candle/duplicate/timeframe checks already built (Phase A8); API-error classification did not exist — **built in this review** |
| Performance Analytics vs. A19 | must not be confused | ✅ Already correctly distinguished — A19's own docs already state this |
| Explainability | — | 🟢 Confirmed — already built (Phase A9), matches the Director's own bar |

## AC-01 — HTF Bias Foundation Audit

**Verified: already exists, already wired.**

`context/htf_bias.py` (Phase A2) defines:

```python
@dataclass(frozen=True)
class HTFBiasResult:
    bias: HTFBias
    confidence: float
    timeframes: Sequence[str]
    quality_score: float
```

`compute_htf_bias()` classifies Daily/H4/H1 (`SUPPORTED_HTF_TIMEFRAMES`)
into a `bias` (`BULLISH`/`BEARISH`/`NEUTRAL`/`UNKNOWN`) with a
`confidence` — exactly the "Bozor yo'nalishi qanday?" question this
AC item asked for, and exactly the field shape the Director's own
`HTFBiasSnapshot` example named (`trend`/`timeframe`/`structure`/
`confidence` map onto `bias`/`timeframes`/the swing/structure
functions it reuses/`confidence`). It generates no signal — see
`context/htf_bias.py`'s own module docstring and
`contracts/context_contract.md`.

`decision/decision_engine.py` already imports `HTFBias`/`HTFBiasResult`
and uses it as one of Decision Engine v2's four weighted inputs (Phase
A3) — `core/pipeline.py`'s `evaluate(candidate, ai_result, htf_bias)`
call. No further work needed.

## AC-02 — Wyckoff + AMD Audit

**Verified: detection exists; the requested output model did not — built in this review.**

`context/wyckoff.py` (Phase A5) and `context/amd.py` (pre-existing)
both detect real events:

- `WyckoffPhase`: `ACCUMULATION`/`DISTRIBUTION` (tied to Spring/
  Upthrust events only — a narrower 2-state model, by design, see
  `context/wyckoff.py`'s own module docstring).
- `AmdEventType`: `MANIPULATION`/`DISTRIBUTION`.

Neither produces the Director's requested standard output —
`MarketPhase(ACCUMULATION/MANIPULATION/DISTRIBUTION/MARKUP/MARKDOWN)`
— a genuine gap. This review adds `context/market_phase.py`:

```python
class MarketPhase(Enum):
    ACCUMULATION = "ACCUMULATION"
    MANIPULATION = "MANIPULATION"
    DISTRIBUTION = "DISTRIBUTION"
    MARKUP = "MARKUP"
    MARKDOWN = "MARKDOWN"
    UNKNOWN = "UNKNOWN"  # a safe fallback the Director's own 5-value list didn't include, matching every other classification enum in this codebase (HTFBias, MarketRegime, ...)
```

`compute_market_phase(context)` classifies from data **already on**
`ContextSnapshot` (`wyckoff_events`, `amd_events`, `market_regime`) —
no new detection logic; `context/wyckoff.py` and `context/amd.py` are
both unmodified. Priority order (most specific first, mirroring
`context/market_regime.py`'s own established pattern):

1. Most recent Wyckoff Spring/Upthrust → `ACCUMULATION`/`DISTRIBUTION`
   (narrowest, most specific signal).
2. Else, most recent AMD event → `MANIPULATION`/`DISTRIBUTION`.
3. Else, a confirmed `TRENDING` Market Regime → `MARKUP` (bullish) or
   `MARKDOWN` (bearish).
4. Else → `UNKNOWN` (never fabricated).

Wired into `core/pipeline.py` as a new `market_phase` stage
(computed once per cycle, right after `context`), returned in
`run()`'s result dict (`"market_phase"`) — advisory only, not
consumed by any strategy, AI, Decision, or Risk. This is exactly the
"AI explanation" and "Education" readiness the Director named.

## AC-03 — Signal + Context Historical Link ⭐⭐⭐

**Verified: the two schemas existed independently; the link did not — wired in this review. This was the real gap.**

Before this review: `signals/schema.py`'s `SignalSchema.context_id`
(Phase A15) and `context/snapshot.py`'s `ContextSnapshotSchema` (Phase
A16) both existed as complete, tested, documented models — but
nothing in production code ever set `context_id` to a real value.
Grepping the codebase confirmed `context_id` was populated only in
test files; the one production call site (`signals/adapter.py`)
simply passed through a caller-supplied parameter that defaulted to
(and always was) `None`.

This review wires the two together in `core/pipeline.py`, adding a new
`signal_history` stage (after `risk`, before `telegram_format`):

1. One `ContextSnapshotSchema` is built per cycle:
   `from_context_snapshot(context, symbol=self.symbol, timeframe=self.interval)`.
2. One `SignalSchema` is built per candidate:
   `from_signal_candidate(candidate, ..., context_id=context_snapshot.snapshot_id, quality=quality, decision=decision, decision_id=str(uuid.uuid4()))`.

This closes exactly the linkage the Director's diagram named:

```
Signal
 |
 +-- context_id     -- the cycle's real ContextSnapshotSchema.snapshot_id
 |
 +-- snapshot_id    -- (same value; the Director's diagram names the
 |                      reference on Signal "context_id" and the
 |                      referenced object's own identity "snapshot_id"
 |                      -- one linkage, not two separate fields)
 |
 +-- strategy_id    -- SignalSchema.strategy_name already carries this
 |                      (the real value, e.g. "LIQUIDITY_SWEEP_STRATEGY",
 |                      matching strategies.lifecycle.strategy_registry
 |                      .StrategyDefinition.id, Phase A11) -- no new
 |                      field needed
 |
 +-- decision_id    -- a new SignalSchema field (this review), a
                        fresh id generated per TradeDecision
                        (decision.models.TradeDecision has no id
                        field of its own; core/pipeline.py generates
                        this one, not TradeDecision)
```

**Not persisted to the database in this review** — every prior
foundation phase (A15 through A19) explicitly excluded database
migration, and this review does not introduce one either. The link
now exists and is returned in `run()`'s result dict
(`"context_snapshot"`, `"signal_history"`), ready for a future,
separately-approved persistence phase — the Director's own stated
reason for this AC item ("Kelajak: AI: 'Nega bu signal ishladi?' deb
javob berishi uchun") is served by the link *existing*, not
necessarily by it being in a database table yet.

Verified end to end with a real (mocked-fetch-layer-only) pipeline run
in `tests/integration/test_signal_context_link.py`: `context_id`
matches the cycle's `snapshot_id`, each candidate gets its own
`decision_id`, all candidates in one cycle share one `context_id`, and
`strategy_name` reflects the real candidate.

## AC-04 — Asset Intelligence Foundation

**Verified: already exists.**

`assets/` (Phase A12): `AssetDefinition` has `asset_type: AssetType`
and explicit `None`-valued hooks for exactly the fields the Director's
example named — `trading_session`/`volatility_class: Optional[str] =
None`, plus `session_profile`/`risk_profile`/`news_profile`/
`fundamental_profile`. `GOLD_ASSET` (`assets/profiles/gold.py`) is the
real XAUUSD profile. Strategy logic does not import `assets/` — see
`docs/ASSET_INTELLIGENCE.md`'s "Strategy Lifecycle relationship
(documentation only)" section, matching the Director's own "Strategy
ichiga asset logic kiritilmaydi" instruction exactly. No further work
needed.

## AC-05 — Strategy Lifecycle Foundation

**Verified: already exists.**

`strategies/lifecycle/` (Phase A11): `StrategyDefinition(id, name,
version, status, ...)`, `StrategyStatus(TESTING/ACTIVE/DISABLED/
DEPRECATED)` — exactly the fields and states the Director's example
named. `StrategyRegistry.active()` already supports the "which
strategies are live" query a future analytics module (e.g. "Liquidity
Sweep v1 vs v2 win rate") would build on. No further work needed.

## AC-06 — Session Intelligence Verification

**Verified: already exists.**

`context/session.py` (Phase A6): `Session(ASIA/LONDON/
LONDON_NEW_YORK_OVERLAP/NEW_YORK/OFF_HOURS)`, classified per candle by
`classify_session()`. Already part of `ContextSnapshot`
(`session_events`), already read by Signal Quality, Explainability,
Feature Engineering, and (as of this review) `ContextSnapshotSchema`/
`SignalSchema`'s `session` field. No further work needed — this
review's AC-03 wiring additionally threads the current session into
every `SignalSchema` record for free, since `ContextSnapshotSchema`
already computes it.

## AC-07 — Data Quality Verification (API errors)

**Verified: three of four checks existed; API-error classification did not — built in this review.**

`data/data_quality.py` (Phase A8) already checks missing candles,
duplicate timestamps, invalid OHLC, and timeframe consistency. It had
no classification for API-layer failures (timeout, rate limit,
connection failure) — those were caught and logged as free-text
strings in `data/market_data.py`'s `MarketDataNormalizer.get_candles()`,
with no structured code.

This review adds `data/api_error_classifier.py`'s
`classify_api_error(exception) -> ExternalAPIError` — a pure,
additive classification helper using Phase A18's error hierarchy
(`API_001` for a timeout/connection failure, `API_002` for anything
else — rate limit, malformed response, missing key). Wired into
`MarketDataNormalizer.get_candles()`'s existing `except` block as
**one additional `logger.error()` call only** — the existing
degrade-to-`[]` return value and control flow are byte-for-byte
unchanged; `data/twelve_data_client.py`'s own retry/backoff logic is
untouched. Verified explicitly:
`tests/data/test_market_data.py::test_get_candles_still_returns_empty_list_on_fetch_failure`
and `::test_get_candles_still_works_normally_when_fetch_succeeds`
confirm the pre-existing contract is unchanged.

## Performance Analytics vs. Phase A19

**Verified: already correctly distinguished.** `performance/`
(Phase A19) measures system timing (`pipeline_total_time`,
`api_response_time`, etc.); `monitoring/performance.py` (pre-existing)
computes trade-outcome statistics (win rate, strategy breakdown).
`performance/README.md` already states this distinction explicitly.
The Director's own `analytics/` package (`signal_performance.py`,
`strategy_report.py`, `confidence_report.py`) is correctly deferred to
Phase 59, per the Director's own instruction — not added in this
review.

## Explainability — confirmed 🟢

`signals/explainability.py` (Phase A9) already produces exactly the
shape the Director's example showed: `direction`, `reasons` (a list —
"H4 bullish structure", "Liquidity sweep", "FVG reaction", session
context, Market Regime), `quality`, `confidence`. Matches the
Director's own bar without any further work.

## What this review does NOT do

- Does not persist `SignalSchema`/`ContextSnapshotSchema` to the
  database — no schema migration in this review.
- Does not change any Decision Engine threshold, confidence-blending
  weight, or approval logic.
- Does not change any strategy's detection algorithm — Wyckoff/AMD/
  Session/HTF Bias detection code is entirely unmodified.
- Does not build the `analytics/` package the Director named for
  Phase 59 — explicitly out of scope per the Director's own
  instruction ("Hozir v0.3.5 ga qo'shish shart emas").
- Does not add caching, API optimization, or a database refactor.

## Verification

- `python -m compileall .`: OK
- `python -m pyflakes` (all tracked + new files): clean
- Full test suite: see the closing commit message for the exact
  before/after count — no regression, every new module at 100%
  coverage.
- Full module import sweep: OK
- `python main.py` smoke test: exit 0, new `market_phase`/
  `signal_history` stages log correctly, existing stage order
  otherwise unchanged.

## Result

```
v0.3.5 Architecture Completion (A13-A19)
        |
        v
Pre-Phase 59 Architecture Readiness Review (this document)
        |
        v
v0.3.5 COMPLETE
        |
        v
Phase 59 — Real Market Validation
```
