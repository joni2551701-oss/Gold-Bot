# Strategy Lifecycle Management Foundation (Phase A11)

## Purpose

Builds a standard metadata and status-management layer for
strategies — `StrategyDefinition`, `StrategyStatus`,
`StrategyRegistry` — entirely separate from strategy execution. **This
is a metadata layer, not a signal-generation layer.** It does not
detect anything, does not run a strategy, and does not change what
`strategies/strategy_manager.py`'s `StrategyManager` already does.

This phase exists because Phase 59 (Real Market Validation), Quant
Research, a future AI Assistant, and Analytics will all eventually
need to answer "what strategies exist, what state are they in, what
assets/styles/timeframes do they support" — without a standard
registry, each would independently re-derive that answer from
`strategy_manager.py`'s source code. `StrategyRegistry` is the single,
documented answer, the same "everyone re-reads raw candles" problem
HTF Bias (Phase A2), Signal Quality Score (Phase A4), and Feature
Engineering (Phase A10) already solved for their own narrower
questions.

## Design Rules

1. Strategy Lifecycle does not generate a signal.
2. Strategy Lifecycle does not run a strategy.
3. The registry stores metadata only.
4. It does not compute performance.
5. It does not compute win rate.
6. It does not write to the database.
7. No fake performance value is ever written.
8. Existing strategy code (`strategies/liquidity_strategy.py`,
   `fvg_strategy.py`, `amd_strategy.py`, `strategy_manager.py`) is not
   rewritten.
9. Backward compatibility with `StrategyManager` is preserved — it is
   entirely untouched by this phase.
10. This module is a foundation for Phase 59, Analytics, and a future
    AI Assistant — not a consumer-facing feature itself.

## What Strategy Lifecycle is NOT

Before this phase, no registry, metadata model, or status system
existed anywhere in this codebase for strategies (confirmed by
auditing `strategies/` in full before writing any code — the only
pre-existing "registry"-flavored code in the whole codebase turned out
to be unrelated docstring mentions in `ai/prompts/prompt_manager.py`
and `telegram/command_router.py`, no actual metadata/registry
pattern). `strategies/strategy_manager.py`'s `StrategyManager` is the
only thing that has ever run a strategy, and stays that way.

## Strategy Status

Exactly four states — no others are added:

```python
class StrategyStatus(Enum):
    TESTING = "TESTING"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
```

`StrategyStatus` classifies registry metadata only — it does not
control whether `StrategyManager` actually runs a strategy. A
strategy marked `DISABLED` here still runs in production today unless
a future, separately-approved phase wires this status into
`StrategyManager` itself (not done in this phase — see "What this
does NOT do" below).

## Strategy Model

```python
@dataclass(frozen=True)
class StrategyDefinition:
    id: str
    name: str
    version: str
    status: StrategyStatus
    supported_assets: List[str]
    supported_styles: List[str]
    supported_timeframes: List[str]
    performance: Optional[float] = None
    win_rate: Optional[float] = None
    last_validation: Optional[str] = None
```

Immutable metadata only — no trading logic, no entry/stop-loss/
take-profit calculation, no `analyze()` method.

## Registry

```python
class StrategyRegistry:
    def register(self, definition: StrategyDefinition) -> None: ...
    def get(self, strategy_id: str) -> Optional[StrategyDefinition]: ...
    def list(self) -> List[StrategyDefinition]: ...
    def active(self) -> List[StrategyDefinition]: ...
```

`register()` raises `DuplicateStrategyIdError` (a `ValueError`
subclass) if `id` is already registered — this catches an accidental
double-registration early rather than silently overwriting metadata.
`get()` returns `None` for an unknown id, never raises.
`StrategyRegistry` is not a singleton: each `StrategyRegistry()` or
`build_default_registry()` call produces an independent, in-memory
store — no shared global state, no database.

## Existing strategies

`build_default_registry()` registers exactly the three strategies
`strategies/strategy_manager.py`'s `StrategyManager` already runs in
production — no new strategy is introduced:

| `id` | `name` | Real source |
|---|---|---|
| `LIQUIDITY_SWEEP_STRATEGY` | Liquidity Sweep | `strategies/liquidity_strategy.py` |
| `FVG_STRATEGY` | Fair Value Gap | `strategies/fvg_strategy.py` |
| `AMD_STRATEGY` | AMD (Accumulation-Manipulation-Distribution) | `strategies/amd_strategy.py` |

Each `id` matches the exact `SignalCandidate.strategy_name` string
literal that strategy's own `analyze()` method already produces (see
each file's `candidates.append(SignalCandidate(..., strategy_name=...))`
line) — not a new naming scheme — so a future consumer can join
`StrategyDefinition` metadata against actual `SignalCandidate`/
`SignalRecord` rows without a separate mapping table. All three are
`status=ACTIVE` (they are, today, literally what
`StrategyManager.strategies` runs — no strategy in this codebase is
currently `TESTING`/`DISABLED`/`DEPRECATED`). `version="1.0"` for all
three: no versioning history exists yet.

`supported_assets=["XAUUSD"]` and `supported_timeframes=["M15"]` use
the real symbol/interval constants this codebase runs today (see
`main.py`'s `TradingPipeline(symbol="XAUUSD", interval="M15", ...)`
and `telegram/signal_service.py`'s `DEFAULT_SYMBOL`) — not the
Director brief's illustrative `"GOLD"` label, since `"XAUUSD"` is the
value that actually appears everywhere else in this codebase.
`supported_styles=["INTRADAY"]` is descriptive metadata, matching the
brief's own example.

## Future hooks — never fabricated

`performance`, `win_rate`, and `last_validation` are always `None` on
every `DEFAULT_STRATEGIES` entry. This codebase does not compute
per-strategy performance or win rate anywhere today —
`monitoring/performance.py` aggregates *closed signals* by
`strategy_name` from the database (a different, pre-existing,
unrelated concern `lifecycle/` does not read from or duplicate).
Wiring a real value into these three fields is Phase 59 Validation's
job, not this phase's — until then, they are explicit, honest
placeholders, never a synthetic estimate.

## What this does NOT do

- Does not generate a `BUY`/`SELL` signal and is not itself a
  strategy.
- Does not instantiate, call, or modify `LiquidityStrategy`/
  `FVGStrategy`/`AMDStrategy`/`StrategyManager` — all four are
  untouched by this phase.
- Does not gate or filter which strategies `StrategyManager` runs —
  `StrategyStatus.DISABLED`/`DEPRECATED` are metadata-only in this
  phase; wiring status into `StrategyManager.run_all_strategies()`
  (e.g. skipping a `DISABLED` strategy) is a distinct, not-yet-done
  future step.
- Does not compute performance or win rate.
- Does not persist anything — no database table, no schema change.
- Is not consumed by `signals/`, `ai/`, `decision/`, `risk/`,
  `database/`, or `telegram/` in this phase — `core/pipeline.py` does
  not construct or read a `StrategyRegistry` anywhere in this phase.

## Future usage

- **Phase 59 Real Market Validation**: populates `performance`/
  `win_rate`/`last_validation` per strategy from real trade outcomes —
  not implemented here.
- **Quant Research / Backtesting**: reads `StrategyRegistry.list()`/
  `.active()` to know which strategies to replay, and their
  `supported_assets`/`supported_timeframes`, without re-reading
  `strategy_manager.py`'s source.
- **AI Integration**: a future AI Assistant could query
  `StrategyRegistry.active()` to describe available strategies to a
  user, or reason about a strategy's `status`/`version` — not wired
  into `ai/ai_analyzer.py` in this phase.
- **Analytics**: joins `StrategyDefinition.id` against
  `SignalRecord.strategy_name` (both use the exact same string) to
  group results by strategy metadata (status, version) without a
  separate mapping table.
