# CONTRACTS.md -- strategy_layer/strategy_library

## Input

Not independently specified beyond the module's own code at rollout time -- see `README.md` Public API.

## Output

Not independently specified beyond the module's own code at rollout time -- see `README.md` Public API.

## Events

None documented at rollout time.

## Public API

See `README.md`.

## Internal API

See `MODULE_MAP.md`.

## Ownership

Module `strategy_layer/strategy_library`.

## Dependencies

Cross-layer imports found mechanically in this module's own `.py` files at rollout time:

- `context_layer.amd`
- `context_layer.context_engine`
- `context_layer.fair_value_gap`
- `context_layer.liquidity`
- `context_layer.market_structure`
- `context_layer.order_block`
- `context_layer.wyckoff`
- `signal_layer.signal_builder`
- `strategy_layer.strategy_engine`
- `strategy_layer.strategy_library`
- `strategy_layer.strategy_manager`

## Runtime Rules

None documented beyond what CLAUDE.md's Trading Safety section already states at the repository level.

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Dependencies list is mechanically derived from actual `import` statements, not asserted from design intent.*
