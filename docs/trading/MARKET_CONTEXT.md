# GoldBot — Market Context

Governed by `docs/constitution/CONSTITUTION.md` Article 2. `context/`
(Layer 1, `docs/architecture/SYSTEM_LAYERS.md`) — verified directly
against the package's real file listing.

## Real structure

```
context/
  context_orchestrator.py   the entry point core/pipeline.py calls
  context_config.py         configuration for context building
  snapshot.py                the ContextSnapshot shape decision/ etc. read
  htf_bias.py                 higher-timeframe bias computation
  market_phase.py              5-state market phase classifier
  market_regime.py              regime detection
  market_structure.py            structure analysis
  session.py                      trading-session detection
  fundamental_context.py           fundamental data composition
  fundamental_scoring.py            fundamental scoring engine (Phase 60.5)
  economic_events.py                EconomicEvent model (Phase 60.5)
  candle.py, wyckoff.py, amd.py,
  bos.py, choch.py, fvg.py,
  liquidity.py, order_block.py       pattern/structure detectors
                                      context_orchestrator.py composes
```

## What Context can and cannot do

- **CAN**: build a market context snapshot from raw data, feed the
  Strategy Engine a consistent view of current conditions.
- **CANNOT**: generate a trading signal, evaluate risk, talk to
  Telegram (`docs/architecture/ARCHITECTURE_MASTER.md`'s own Context
  Engine entry, restated here for the trading-scoped reader).
- **Depends on**: `data/` only.

## Where AI reads this

`ai/context/context_adapter.py`'s `market_context_from_snapshot()`
converts a `ContextSnapshotSchema` into the AI layer's own
`MarketContext` shape, type-only — see `docs/ai/AI_PIPELINE.md`.

## Related

- `docs/trading/TRADING_ARCHITECTURE.md` — Context's place in the
  trading-scoped pipeline order.
- `docs/ai/AI_PIPELINE.md` — how the AI layer reads this package's
  output.
- `docs/FUNDAMENTAL_INTELLIGENCE.md`, `docs/MARKET_REGIME.md`,
  `docs/HTF_BIAS.md`, `docs/WYCKOFF.md` — per-detector detail.
