# STEP-08 Upstream Freeze

Per the STEP-08 directive ("signals/ boshlanishidan oldin arxitekturani
o'zgartirmaslik kerak … config/providers/stream/market/context/strategies/
architecture qatlamlarini haqiqiy FROZEN holatiga o'tkazing"), the following
layers are declared **FROZEN** as of the STEP-08 / TASK-CORE-008 commit.

## Frozen layers and their public contracts

| Layer | Public contract (frozen) | Prior freeze basis |
|---|---|---|
| `config.py` | config values / feature flags read via `core/secrets` | — |
| `data_layer/providers/` | provider adapters → raw candles / `FundamentalSnapshot`; `base_provider` ABC | Phase 59.1–59.2 |
| `stream/` | `StreamEvent`, current price, `StreamState` (data-flow only) | — |
| `market/` | `MarketStructureView.from_context()` + `*State` façade DTOs (read-only projection) | TASK-CORE-005 |
| `context/` | `ContextSnapshot` (structure/liquidity/OB/FVG/trend/bias/session/volatility/regime) | TASK-CORE-006 |
| `strategies/` | live `analyze() → SignalCandidate` (frozen) + additive `StrategyResult` setup layer | TASK-CORE-007 |

## What "frozen" means here

- **No change** to these layers' public contracts, computations, or file
  structure without **explicit Director approval** for that specific change.
- The STEP-08 signals/ work consumes `strategies.result.StrategyResult` (read
  only) and `context.ContextSnapshot` (read only) — it modifies none of the
  frozen layers.
- The live trading pipeline
  (`config → … → strategies → signal_engine → decision → risk`) is unchanged;
  `signal_engine.SignalEngine → SignalCandidate` remains the live path and is
  itself frozen (CLAUDE.md Trading Safety).

## Verification at freeze time

- Architecture boundary audits `docs/PHASE_ARCH_001_AUDIT.md` and
  `docs/PHASE_ARCH_002_AUDIT.md` confirmed these layers already hold their
  single-responsibility boundaries (no cross-layer leakage, no duplicate
  detectors) — the precondition for a clean freeze.
- STEP-08 adds only the `signals/` canonical layer downstream of the freeze
  line; full test suite + CI green on the freeze commit.

This document is the reference for "is layer X frozen?" from STEP-08 onward.
