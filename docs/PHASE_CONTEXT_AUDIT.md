# TASK-CORE-006 — context/ Foundation Reuse Audit

**Scope decision (Director):** *Audit + gap-fill only.* `context/` is
recognized as **production-complete** for every market-analysis
capability TASK-CORE-006 lists. No new modules are created, and the
**frozen, live detection logic is not modified**. This task adds the
missing *documentation* (this file) and the missing *dedicated unit
tests* for the core Smart-Money-Concepts detectors, exercising the
existing detectors read-only.

## Why not "create/extend the listed files"

`context/` is the **live market-analysis brain** of the pipeline
(`core/pipeline.py`: Data → **Context** → Signal → AI → Decision → Risk →
Telegram). Under CLAUDE.md **Trading Safety**, its signal-affecting
detection logic (structure / liquidity / order-block / FVG / regime)
must not be modified without explicit per-change approval. The task's
own **Reuse rule** says the same: *"agar logic allaqachon mavjud bo'lsa —
qayta ishlatiladi; to'liq qayta yozilmaydi; duplicate package
yaratilmaydi."* Every capability already exists, so the correct outcome
is reuse, not rewrite.

## Capability → existing implementation map

| TASK-CORE-006 asked | Already implemented in | Public API | Live in pipeline |
|---|---|---|---|
| context_manager.py (orchestration) | `context_layer/context_engine/context_orchestrator.py` | `ContextEngine.build()` / `build_context_snapshot()` | ✅ |
| snapshot.py (container) | `context_layer/context_engine/context_orchestrator.py` + `context_layer/context_engine/snapshot.py` | `ContextSnapshot` (internal) / `ContextSnapshotSchema` (public contract) | ✅ |
| market_structure.py (HH/HL/LH/LL, swing) | `context_layer/market_structure/market_structure.py` | `detect_swing_points()`, `classify_structure()`, `StructureType` | ✅ |
| BOS | `context_layer/market_structure/bos.py` | `detect_bos()`, `BosEvent`, `BosDirection` | ✅ |
| CHoCH | `context_layer/market_structure/choch.py` | `detect_choch()`, `ChochEvent`, `ChochDirection` | ✅ |
| liquidity.py (BSL/SSL, sweep, zone) | `context_layer/liquidity/liquidity.py` | `detect_equal_levels()`, `detect_sweeps()`, `LiquidityType` | ✅ |
| order_block.py (bull/bear) | `context_layer/order_block/order_block.py` | `detect_order_blocks()`, `OrderBlock`, `OrderBlockType` | ✅ |
| fvg.py (imbalance) | `context_layer/fair_value_gap/fvg.py` | `detect_fvg()`, `FairValueGap`, `FvgType` | ✅ |
| trend.py / bias.py | `context_layer/market_structure/market_structure.py` + `context_layer/trend/htf_bias.py` | `most_recent_bias()` (BULLISH/BEARISH/None), `HTFBiasResult` | ✅ |
| regime.py (trending/range/…) | `context_layer/trend/market_regime.py` | `compute_market_regime()`, `MarketRegime` | ✅ |
| session.py (Asia/London/NY/Off) | `context_layer/session/session.py` | `classify_session()`, `detect_session_events()`, `Session` | ✅ |
| volatility.py (low/normal/high) | `context_layer/trend/market_regime.py` (HIGH/LOW_VOLATILITY) + `context_layer/session/session.py` `compute_session_volatility()` | — | ✅ |
| helpers/ | `context_layer/context_engine/candle.py` (`is_bullish`/`is_bearish`/`body_ratio`/…) + inline | — | ✅ |

Extra detectors already present beyond the task list: `context_layer/amd/amd.py`
(Accumulation-Manipulation-Distribution), `context_layer/wyckoff/wyckoff.py`
(Spring/Upthrust), `context_layer/trend/market_phase.py` (5-state phase),
`context_layer/fundamental/fundamental_context.py` / `economic_events.py` /
`fundamental_scoring.py` (fundamental layer).

## How the pipeline works (verified, unchanged)

`ContextEngine.build(candles, htf_bias)` runs a deterministic, stateless
8-stage pipeline and returns one immutable `ContextSnapshot`:

```
Candles
  → SwingPoints            detect_swing_points   (market_structure.py)
  → StructurePoints HH/HL/LH/LL   classify_structure
  → BOS / CHoCH            detect_bos / detect_choch
  → Liquidity Zones+Sweeps detect_equal_levels / detect_sweeps
  → Order Blocks / FVGs    detect_order_blocks / detect_fvg
  → AMD / Wyckoff          detect_amd_events / detect_wyckoff_events
  → Session Events         detect_session_events
  → Market Regime          compute_market_regime   (incl. volatility)
  → ContextSnapshot
```

- **Trend / bias:** `most_recent_bias(structure)` returns `"BULLISH"`
  for the most recent HH/HL, `"BEARISH"` for LH/LL, `None` if nothing
  classified yet. `htf_bias.py` layers the multi-timeframe read.
- **Liquidity / OB / FVG:** liquidity zones come from equal-level swing
  clustering; sweeps are wick-through-then-close-back events; an Order
  Block is the last opposing candle before a sweep-induced BOS/CHoCH; an
  FVG is a 3-candle imbalance. All read-only analysis — no order/decision.
- **Snapshot assembly:** every field is required (no silent gaps);
  `context.snapshot.from_context_snapshot()` projects the internal
  `ContextSnapshot` into the flat public `ContextSnapshotSchema` (the
  contract `market/` and future AI consume).

## Consumers (unchanged)

`context/` feeds `signals/` (signal quality/generation), `decision/`,
`ai/context/` (AI context builder), `market/` (the read-only facade,
TASK-CORE-005), `analytics/context_report.py`, and monitoring — as
data only. It does **not** emit signals or trade decisions.

## Security (verified)

`context/` reads no `.env`, holds no API key, logs no secret — it works
purely on already-normalized candle data and its own computed state.

## What this task added (gap-fill)

Before this task, the core detectors had **no dedicated unit-test
files** (they were exercised only indirectly through snapshot/signal/
integration tests). Added dedicated, read-only detector tests under
`tests/context/` — they call the existing frozen detectors and assert
their documented behavior; **no detector code changed**:

- `test_market_structure.py` — swing detection, HH/HL/LH/LL
  classification, `most_recent_bias` (trend/bias), empty & invalid input.
- `test_bos.py` — bullish/bearish BOS + no-structure input.
- `test_choch.py` — bullish/bearish CHoCH + no-structure input.
- `test_liquidity.py` — BSL/SSL equal-level zones, sweeps, empty input.
- `test_order_block.py` — bullish/bearish OB + no-sweep input.
- `test_fvg.py` — bullish/bearish FVG + fewer-than-3-candles input.
- `test_context_engine.py` — full `ContextEngine.build()` snapshot,
  empty-candle input, and non-ascending (invalid) candle order.

(Regime, session, snapshot already had dedicated tests:
`test_market_regime.py`, `test_session.py`, `test_snapshot.py`,
`test_serialization.py`, `test_snapshot_validation.py`.)

## Deferred to next stage

`strategies/` — the next layer up. `context/` now provides the verified,
tested analytical foundation it will consume. No `context/` change is
required for that; consumers read the existing contracts.

## Acceptance

- ✅ context/ gives full market analysis (HH/HL/LH/LL, BOS, CHoCH,
  liquidity, OB, FVG, trend/bias, regime, session, volatility).
- ✅ No signal/decision logic mixed in.
- ✅ No secret read or logged.
- ✅ Frozen detection logic untouched; only tests + this doc added.
- ✅ Provides a tested foundation for `strategies/`.
