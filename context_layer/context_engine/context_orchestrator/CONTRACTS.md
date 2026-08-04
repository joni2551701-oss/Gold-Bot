# CONTRACTS.md — context_layer/context_engine/context_orchestrator

## Public API

- `dataclass`
- `List`
- `Optional`
- `Sequence`
- `TYPE_CHECKING`
- `Candle`
- `ContextConfig`
- `detect_swing_points`
- `classify_structure`
- `SwingPoint`
- `StructurePoint`
- `detect_bos`
- `BosEvent`
- `detect_choch`
- `ChochEvent`
- `detect_equal_levels`
- `detect_sweeps`
- `LiquidityZone`
- `LiquiditySweepEvent`
- `detect_order_blocks`
- `OrderBlock`
- `detect_fvg`
- `FairValueGap`
- `detect_amd_events`
- `AmdEvent`
- `detect_wyckoff_events`
- `WyckoffEvent`
- `detect_session_events`
- `SessionEvent`
- `compute_market_regime`
- `MarketRegimeResult`
- `setup_logger`
- `logger`
- `ContextSnapshot`
- `ContextEngine`
- `build_context_snapshot`

## Ownership

Canonical module `context_layer/context_engine/context_orchestrator`.

## Runtime Rules

Behaviour unchanged from the pre-GEL-001 flat module.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `context_orchestrator.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
