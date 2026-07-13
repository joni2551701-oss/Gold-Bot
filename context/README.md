# context/

## Purpose
Pure Smart Money Concepts (SMC) market-structure detection.

## Responsibilities
Swing points, BOS/CHoCH, liquidity sweeps, order blocks, fair value
gaps, and AMD (Accumulation-Manipulation-Distribution) cycle
detection — all as stateless functions over a candle sequence.

## Input
`Sequence[Candle]` (from `data/`).

## Output
`ContextSnapshot` (`context_orchestrator.py`) — an immutable, fully
resolved snapshot of every detector's output for one candle series.

## Dependencies
`data/` (for the `Candle` type) only. No dependency on `strategies/`,
`signals/`, `ai/`, `database/`, or `telegram/`.

## Future Roadmap
None planned — this layer's SMC formulas are stable and explicitly
out of scope for casual change (see `CLAUDE.md`'s Trading Safety
rules).
