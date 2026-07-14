# Wyckoff Engine Foundation (Phase A5)

## Purpose

A knowledge layer inside the Context Engine — detects Spring and
Upthrust events (the "test of support/resistance" patterns Wyckoff
theory is most identified by) from already-detected liquidity sweeps
and structural breaks. **Wyckoff is context, not a decision or a
strategy.** It never generates a `BUY`/`SELL` signal and is not
consumed by any `strategies/*.py` file — wiring one is a future,
separately-approved phase.

This phase exists because Phase A1's architecture audit found zero
Wyckoff code anywhere in the codebase — `context/amd.py`'s
Accumulation-Manipulation-Distribution cycle detector uses overlapping
vocabulary but is a distinct, narrower SMC concept (see "Relationship
to AMD" below).

## Architecture

Unlike HTF Bias (Phase A2) and Signal Quality Score (Phase A4), Wyckoff
needed **no `core/pipeline.py` change at all**. It is a sixth detector
inside `ContextEngine.build()`, following the exact same pattern as
`amd_events`:

```
Candles
  -> SwingPoints / StructurePoints
  -> BOS / CHoCH
  -> Liquidity Zones / Sweeps
  -> Order Blocks / Fair Value Gaps
  -> AMD Events
  -> Wyckoff Events          (context/wyckoff.py, Phase A5)
  -> ContextSnapshot         (candles, ..., amd_events, wyckoff_events)
```

`ContextSnapshot` gains a 10th field, `wyckoff_events`. Every existing
field keeps its exact name and meaning — only a new one was added.
Both real construction sites (`context/context_orchestrator.py`'s
`ContextEngine.build()`, and every test that builds a `ContextSnapshot`
by hand) were updated to supply it, preserving this dataclass's
existing "every field is required, no silent defaults" convention
(stated in `tests/test_generate_signals.py`'s own docstring) rather
than adding a default value that would have broken that convention.

**Reuse, not duplication** (per `CLAUDE.md`'s "No duplicate logic"
rule):
- `context.liquidity.LiquiditySweepEvent`, `context.bos.BosEvent`,
  `context.choch.ChochEvent` — all unchanged. `detect_wyckoff_events()`
  correlates already-detected sweeps and breaks; it does not detect
  either from scratch.

## Relationship to AMD

`context/amd.py`'s `detect_amd_events()` already correlates a
liquidity sweep (its `MANIPULATION` event) with a subsequent
structural break (its `DISTRIBUTION` event) — a general pattern.
Wyckoff's Spring/Upthrust are a **narrower, more specific**
correlation of the same underlying idea (a sweep followed by the
*nearest* same-direction break), so the vocabulary overlaps, but this
module does not import, wrap, or reuse `context/amd.py`'s function
directly. Two reasons:

1. `context/amd.py` already feeds a live, tested strategy
   (`strategies/amd_strategy.py`). Touching it to share logic with a
   brand-new, unwired module would raise the blast radius of this
   foundation phase for no functional benefit — CLAUDE.md's "no
   unnecessary refactor" principle weighed against "no duplicate
   logic" here, and the safer, more conservative choice for a
   strategy-feeding file won.
2. Spring/Upthrust deliberately differ from AMD's correlation in one
   concrete way: AMD takes *any* future break regardless of distance;
   Wyckoff's `_confirming_break()` also takes the nearest one — same
   selection rule, independently implemented. This is a small, known,
   accepted duplication between `_build_amd`'s reasoning and
   `_confirming_break()`, flagged here rather than silently
   introduced. A future cleanup phase could extract a shared "nearest
   same-direction break after index N" helper covering both
   `context/order_block.py` (which has the identical pattern a third
   time) and this module — not done in this phase.

**Manipulation is not a third, separate Wyckoff event type.** It is
the `sweep` field already present on every `WyckoffEvent` — the
liquidity sweep that sets up a Spring/Upthrust *is* the manipulation
leg of that cycle. Modeling it as an independent detector would
re-describe what `AmdEventType.MANIPULATION` already names.

## Inputs

`detect_wyckoff_events(candles, liquidity_sweeps, bos_events,
choch_events)` — all four already computed by
`context_orchestrator.py` before this stage runs; no new fetch or
detection.

## Outputs

`WyckoffEvent` (immutable dataclass), one per confirmed Spring/Upthrust:

| Field | Type | Meaning |
|---|---|---|
| `type` | `WyckoffEventType` | `SPRING` or `UPTHRUST`. |
| `phase` | `WyckoffPhase` | `ACCUMULATION` (Spring) or `DISTRIBUTION` (Upthrust) — currently a direct function of `type`, exposed separately so a caller can query by phase without knowing the type mapping, and so a future event type sharing a phase doesn't require a breaking change. |
| `index` / `confirming_break_index` | `int` | The confirming BOS/CHoCH's candle index (not the sweep's) — same convention `context/order_block.py` uses. |
| `timestamp` | `datetime` | The confirming break's timestamp. |
| `sweep` | `LiquiditySweepEvent` | The sweep that set up this event — the Manipulation leg (see above). |
| `volume_confirmed` | `Optional[bool]` | Always `None` today — see "Volume confirmation hook" below. |

## Detection rule

For each `LiquiditySweepEvent`:
- **`SSL` (sell-side liquidity, a support/equal-lows zone swept)** →
  looks for the nearest subsequent `BULLISH` `BosEvent` or `ChochEvent`
  → if found, emits a `SPRING` (`phase=ACCUMULATION`).
- **`BSL` (buy-side liquidity, a resistance/equal-highs zone swept)**
  → looks for the nearest subsequent `BEARISH` break → if found, emits
  an `UPTHRUST` (`phase=DISTRIBUTION`).
- No matching break (of any distance) after a sweep → no event for
  that sweep. Never raises.

## Volume confirmation hook

Wyckoff theory conventionally looks for climactic/declining volume
around a Spring or Upthrust to fully confirm the test. **This codebase
has no volume data source at all** — `data/twelve_data_client.py`'s
`Candle` is OHLC-only (confirmed in Phase A1's architecture audit,
re-confirmed by reading the file this phase; Twelve Data's response is
never asked for volume). `context/wyckoff.py`'s `_volume_confirms()`
is a named, documented, functionally-inert hook — it always returns
`None` ("not checked"), never fabricates `True`/`False`. Wiring in
real volume confirmation is a future, separately-approved phase's job;
only `_volume_confirms()`'s body would need to change, nothing else in
this module.

## What this does NOT do

- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — no `strategies/wyckoff_strategy.py` was created, and no
  existing `strategies/*.py` file was modified to read
  `WyckoffEvent`.
- Does not implement full Wyckoff phase theory (Phase A/B/C/D/E
  boundaries within Accumulation/Distribution) — only the Spring/
  Upthrust test events, the most concrete, directly-detectable pieces
  of the theory given this codebase's existing primitives.
- Does not modify `context/amd.py`, `context/order_block.py`, or any
  other existing detector — see "Relationship to AMD" above for why.
- Does not change any existing `ContextSnapshot` field's name or
  meaning — only adds `wyckoff_events`.
- Does not write to the database — no schema change, no new table.
- Does not block, delay-gate, or filter the pipeline in any way —
  `wyckoff_events` is simply part of `ContextSnapshot`, computed
  alongside every other detector, consumed by nothing downstream yet.

## Future expansion

- **A `strategies/wyckoff_strategy.py`** (a future, separately-
  approved phase) — registering it in `StrategyManager.__init__`'s
  strategy list is the natural next step once a Spring/Upthrust-based
  entry rule is explicitly scoped.
- **Real volume confirmation** — once a volume data source exists in
  `data/`, only `_volume_confirms()`'s body needs to change.
- **Shared sweep-then-break helper** — a future cleanup phase could
  extract the "nearest same-direction break after index N" pattern
  duplicated (independently, not copy-pasted) across
  `context/order_block.py`, `context/amd.py`, and this module — not
  done here to avoid touching two already-tested,
  strategy-feeding files in a foundation-only phase.
- **Signal Quality Score integration** — `signals/signal_quality.py`
  (Phase A4) could gain a `WYCKOFF_ALIGNED` criterion once a strategy
  consumes `WyckoffEvent`, following the exact extension mechanism
  `docs/SIGNAL_QUALITY.md` already documents for Session/Volume.
