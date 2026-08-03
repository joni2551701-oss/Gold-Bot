# GoldBot — Trading Architecture

Governed by `docs/constitution/CONSTITUTION.md` Article 1/2. This is
the Trading-Engine-specific view of `docs/architecture/DATA_FLOW.md`'s
real, grep-verified 16-stage `core/pipeline.py` order — restated here
scoped to the trading-only stages, since `docs/trading/` groups
Decision/Risk/Execution documentation together. The full 16-stage
order with every stage's responsibility remains
`docs/architecture/DATA_FLOW.md`; this document does not repeat it,
only the trading-relevant subset.

## The trading-relevant stage order

```
Market Data     data/
    │
    ▼
Context          context_layer/context_engine/context_orchestrator.py
    │
    ▼
Strategy           strategy_layer/strategy_manager/strategy_manager.py
    │
    ▼
Signal                signal_layer/signal_engine/signal_engine.py
    │
    ▼
AI Analysis              ai/ai_analyzer.py — advisory only, produces
                          AIAnalysisResult, never itself decides
                          (Constitution Article 1)
    │
    ▼
Decision                    decision_layer/decision_engine/decision_engine.py
    │
    ▼
Risk                           risk_layer/risk_engine/risk_manager.py
    │
    ▼
Execution                          execution_layer/execution_engine/execution_engine.py
                                    (intentionally inert — no live
                                    MT5 order calls exist yet)
    │
    ▼
Monitoring                            trade_monitoring_layer/paper_trading/paper_trade_monitor.py
```

This matches the Director's own brief order exactly — unlike
`docs/architecture/DATA_FLOW.md`'s finding in Phase 62.1b (where an
earlier sketch had misplaced AI Analysis relative to Decision/Risk),
this trading-scoped view and the real code agree.

## The one rule this whole document exists to protect

Constitution Article 1: the AI layer produces a *value*
(`AIAnalysisResult`) that `decision_layer/decision_engine/decision_engine.py` accepts as one
input among several — it never calls `decision/`, `risk/`, or
`execution/` itself. See `docs/trading/DECISION_ENGINE.md` for exactly
how that value is blended, and `docs/architecture/IMPORT_RULES.md` for
the mechanically-verified import boundary.

## Related

- `docs/architecture/DATA_FLOW.md` — the full 16-stage pipeline order.
- `docs/trading/MARKET_CONTEXT.md`, `DECISION_ENGINE.md`,
  `RISK_SYSTEM.md`, `EXECUTION_SYSTEM.md` — each stage above, in depth.
- `docs/ARCHITECTURE.md` — the original full pipeline diagram.
