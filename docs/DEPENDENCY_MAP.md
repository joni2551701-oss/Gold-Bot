# GoldBot Dependency Map (Phase A1)

Real, grepped import graph — every edge below was verified by reading
the actual `from X import Y` / `import X` lines in the source this
phase (`grep -rhoE "^(from|import) ..."` per package, then the
suspicious/cross-layer hits individually re-read in full), not
inferred from `docs/ARCHITECTURE.md`'s prose. Standard-library imports
(`os`, `sys`, `datetime`, `typing`, `dataclasses`, `enum`, `sqlite3`,
`asyncio`, `logging`, etc.) and third-party imports (`aiogram`) are
omitted from the graph — only project-internal package edges are
shown.

## Package-level graph

```
data/          -> core/
context/       -> core/, data/
strategies/    -> context/, signals/            *
signals/       -> context/, strategies/         *
ai/            -> context/, core/
decision/      -> ai/, signals/
risk/          -> decision/, signals/
execution/     -> risk/                          (never imported externally)
monitoring/    -> core/, database/                (never imported externally)
database/      -> config, core/, signals/, decision/, risk/   †
telegram/      -> ai/, core/, database/, decision/, risk/, signals/  ‡
core/pipeline.py -> data/, context/, signals/, ai/, decision/, risk/, telegram/, database/, core/
```

`*` — see "Circular Dependency" below.
`†` — via `database_layer/trade_repository/signal_record.py` only, not any `*_repository.py`.
`‡` — via `platform_layer/telegram/signal_formatter.py` only, not `platform_layer/telegram/handlers.py`.

## Edge-by-edge detail

| From | To | File(s) | Nature |
|---|---|---|---|
| `context/` | `core/` | `context_orchestrator.py` and others | logger, expected |
| `context/` | `data/` | multiple | `Candle` type, expected (context consumes candles) |
| `strategies/` | `context/` | all 3 strategy files | `ContextSnapshot` input, expected |
| `strategies/` | `signals/` | `amd_strategy.py`, `fvg_strategy.py`, `liquidity_strategy.py`, `strategy_manager.py` | `signal_layer.signal_builder.models.SignalCandidate`/`SignalType` — output type |
| `signals/` | `context/` | `signal_engine.py` (via `ContextSnapshot` param) | expected |
| `signals/` | `strategies/` | `signal_engine.py` | `strategy_layer.strategy_manager.strategy_manager.StrategyManager` — orchestration call |
| `ai/` | `context/` | `ai_analyzer.py`, `ai_prompt.py`, `confidence_model.py` | `ContextSnapshot` input, expected |
| `ai/` | `core/` | `ai_analyzer.py` | logger, expected |
| `decision/` | `ai/` | `decision_engine.py`, `models.py` | `AIAnalysisResult` input — `decision_engine.py`'s is `TYPE_CHECKING`-only |
| `decision/` | `signals/` | `decision_engine.py` | `SignalCandidate` input — `TYPE_CHECKING`-only |
| `risk/` | `decision/` | `risk_manager.py` | `TradeDecision`/`DecisionAction` input, expected |
| `risk/` | `signals/` | `risk_manager.py` | expected |
| `execution/` | `risk/` | `execution_engine.py` | `RiskResult` type only — **file has zero external importers** (confirmed by repo-wide grep this phase) |
| `monitoring/` | `core/` | both files | logger, expected |
| `monitoring/` | `database/` | `performance.py` only | `SignalRepository` — **not** `signal_monitor.py`, whose own docstring claims package-wide database isolation (see Architecture Audit) |
| `database/` | `config`, `core/` | throughout | expected, cross-cutting |
| `database/` | `signals/`, `decision/`, `risk/` | **`signal_record.py` only** | type-borrowing for the persistence wrapper — no `*_repository.py` file does this |
| `telegram/` | `ai/`, `decision/`, `risk/`, `signals/` | **`signal_formatter.py` only** | formats a `SignalCandidate`+`AIAnalysisResult`+`TradeDecision`+`RiskResult` into a message — consistent with Telegram's documented downstream position |
| `telegram/` | `database/` | `telegram/*_service.py` files only, never `handlers.py` | correct per stated rule, re-confirmed this phase |
| `telegram/` | `core/` | throughout | expected |
| `core/pipeline.py` | every layer | one file | the documented orchestrator exception |

## Circular Dependencies

**One found: `strategies/` ↔ `signals/` (package level).**

```
strategies/*.py  --imports-->  signal_layer/signal_builder/models.py
signal_layer/signal_engine/signal_engine.py  --imports-->  strategy_layer/strategy_manager/strategy_manager.py
```

This is a **package-level** cycle, not a **module-level** one — the
two specific submodules that get imported (`signal_layer/signal_builder/models.py`,
`strategy_layer/strategy_manager/strategy_manager.py`) do not import each other, so Python
resolves both import statements without a runtime `ImportError` today
(re-verified this phase: the full 88-module import sweep passes
clean). It is nonetheless a real mutual dependency between the two
packages as a whole, and `docs/ARCHITECTURE.md`'s Data Flow diagram
presents Strategies → Signal Generation as strictly one-directional,
which is only true at the module level, not the package level. See
`docs/ARCHITECTURE_AUDIT.md`'s Architecture Improvement
Recommendations #1 for the proposed documentation fix (no code change
recommended).

No other cycle was found. The full dependency graph above is
otherwise a DAG.

## Tight Coupling

- **`decision/` ↔ `signals/`/`ai/` via `TYPE_CHECKING`-only imports.**
  `decision_engine.py` imports `SignalCandidate` and `AIAnalysisResult`
  only under `if TYPE_CHECKING:` — meaning at runtime `decision/` has
  **zero** hard dependency on `signals/`/`ai/`, only a static-typing-
  time one. This is the loosest coupling in the entire graph and is
  worth calling out as a positive pattern other modules don't
  currently follow (e.g. `risk_layer/risk_engine/risk_manager.py` imports
  `decision_layer.decision_engine.models` at runtime, not `TYPE_CHECKING`-gated).
- **`database_layer/trade_repository/signal_record.py`** is tightly coupled to three upstream
  layers' concrete types (`SignalCandidate`, `TradeDecision`,
  `RiskResult`) at runtime, not `TYPE_CHECKING`-gated — a schema
  change to any of those three dataclasses is a potential breaking
  change to `signal_record.py` without any test currently asserting
  the field-by-field mapping stays valid beyond what
  `tests/test_database.py`/`tests/integration/test_database_flow.py`
  happen to exercise.
- **`platform_layer/telegram/signal_formatter.py`** is similarly coupled to four
  upstream types at runtime — expected for a formatter, but means any
  of `signals/`, `ai/`, `decision/`, or `risk/`'s public dataclasses
  changing shape has exactly one ripple point to check.

## Future Problems (if left unaddressed)

1. The `strategies/`↔`signals/` package cycle: safe today because no
   submodule imports the other package's orchestration module *and*
   is itself imported by that same orchestration module. A future
   strategy that needs something from `signal_engine.py` (not just
   `signal_layer/signal_builder/models.py`) would create a real, hard circular import and
   fail at process start — this would surface immediately (not
   silently), but is worth pre-empting via the documentation fix in
   Architecture Audit recommendation #1 before it happens rather than
   after.
2. `database_layer/trade_repository/signal_record.py`'s three-layer-upward type dependency
   means any of `signals/`, `decision/`, or `risk/`'s dataclasses
   changing a field name breaks persistence silently at the type level
   (Python won't error until the specific field access happens) unless
   caught by a test. Current test coverage on `signal_record.py`
   (92%) is good but not 100% — the 3 uncovered lines are worth a
   look during v0.3.5 (out of scope to fix in this documentation-only
   phase).
3. `core_layer/health_monitor/performance.py`'s direct `database/` import, combined
   with zero external callers, means the module currently carries the
   *cost* of the dependency (it must be kept in sync with
   `SignalRepository`'s interface) without any of the *benefit* (it's
   never actually invoked at runtime). Low risk today; worth resolving
   one way or the other (wire it in, or document why it stays dormant)
   before v0.3.5 adds new database-adjacent monitoring.
