# Performance Metrics Foundation (Phase A19)

## Purpose

Builds the ability to **measure** GoldBot before trying to make it
faster. Today, nobody knows which module takes the longest, where the
pipeline slows down, how long an API call takes, how long a database
query takes, or where a future optimization would actually help.
`performance/` answers "how long did this take, and did it succeed,"
in one standard, serializable shape — nothing more. **This phase does
not speed anything up.**

## Not what it sounds like — two pre-existing, unrelated concepts

The word "performance" already means two different things elsewhere
in this codebase. Neither is touched by this phase, and neither is
what this new package is:

| | Purpose | Question it answers |
|---|---|---|
| `monitoring/performance.py`'s `PerformanceTracker`/`PerformanceResult` (pre-existing) | Historical **trade outcome** statistics — win rate, per-strategy breakdown, confidence-bucket accuracy, computed from the `signals` database table. | "How well did GoldBot's signals actually perform?" |
| `core/pipeline.py`'s own `_log_stage()` (pre-existing) | Logs each pipeline stage's real duration today, with a slow-operation warning threshold. | "How long did *this specific pipeline run's* stages take?" |
| `performance/` (this phase, new) | A standalone, reusable timing/metrics foundation — a data model, a collector, a timer/decorator. | "How do I *measure* any block of code, anywhere, in a standard way?" |

`docs/PERFORMANCE.md` (Phase 53) is a separate, one-time benchmark
*report* (real numbers measured once, written up) — not this ongoing
measurement *infrastructure*. This document is about the tool;
`docs/PERFORMANCE.md` is about a specific measurement taken with an
earlier, ad-hoc version of that idea.

## Architecture

```
Module
  |
  v
PerformanceTimer
  |
  v
Metric Collector
  |
  v
Logger / Future Database
```

`PerformanceTimer` (a context manager, or its `@measure_performance`
decorator form) wraps a block of code, measures its wall-clock
duration via `time.perf_counter()` (the same monotonic primitive
`core/pipeline.py`'s own `_log_stage()` already uses), and always
logs a `PERFORMANCE` line. If given a `PerformanceCollector`, it also
records a `PerformanceMetric` into it. Nothing writes to the database
in this phase — "Future Database" is drawn as a not-yet-implemented
future stage.

## Zero pipeline wiring

`core/pipeline.py` is entirely unmodified — no existing stage
(`market_data`, `context`, `signal`, `ai`, `decision`, `risk`, etc.)
constructs a `PerformanceTimer` or a `PerformanceCollector` in this
phase. `performance/` exists as a standalone, importable foundation a
future, separately-approved phase could wire into the pipeline (or
into `strategies/`, `ai/`, `database/`) — matching every other Phase
A foundation module's "zero pipeline wiring" posture.

## Model

```python
@dataclass(frozen=True)
class PerformanceMetric:
    name: str
    module: str
    duration_ms: float
    metric_id: str = field(default_factory=generate_metric_id)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "success"
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_code: Optional[str] = None
```

`name`/`module`/`duration_ms` are required — matching this phase's
own brief, which shows `PerformanceMetric(name=..., module=...,
duration_ms=...)` with nothing else supplied. Every other field has a
sensible default (`metric_id` auto-generated, `timestamp` "now",
`status="success"`, `metadata={}`, `error_code=None`) — a deliberate
difference from `signals.schema.SignalSchema`/
`context.snapshot.ContextSnapshotSchema` (Phase A15/A16), whose
identity fields are always required with no default, because *this*
phase's own brief explicitly demonstrates the shorter, default-heavy
construction form.

## Metric categories

| Category | Standard `name` |
|---|---|
| Pipeline | `pipeline_total_time` |
| Market Data | `market_data_fetch_time` |
| Context | `context_build_time` |
| Strategy | `strategy_execution_time` |
| AI | `ai_analysis_time` |
| Decision | `decision_time` |
| Database | `database_query_time` |

Named as constants in `performance/metrics.py`
(`METRIC_PIPELINE_TOTAL_TIME`, etc.) — a convention, not an enforced,
closed vocabulary; `validate_metric()` does not reject an unlisted
name.

## Collector

`PerformanceCollector` (`register()`/`get()`-style interface, named
`record()`/`get_metrics()`/`get_by_module()`/`clear()` per this
phase's own brief) is a plain in-memory list — not a singleton, same
convention as `strategies.lifecycle.strategy_registry.StrategyRegistry`/
`assets.asset_registry.AssetRegistry`: each instance is independent.

## Timer and decorator

```python
with PerformanceTimer("context_build", module="ContextEngine", collector=collector):
    build_context()
```

```python
@measure_performance("strategy_execution", module="StrategyEngine", collector=collector)
def run_strategy():
    ...
```

Both forms measure start time, end time, and duration automatically,
and never swallow an exception raised inside — the original exception
always propagates after the metric is recorded with
`status="failed"`.

## Phase A18 integration

If the exception raised inside a `PerformanceTimer`/
`measure_performance` block is a `core.errors.base.GoldBotError` (or
any of its nine subclasses — Phase A18), its `.code` is captured as
the metric's `error_code`, exactly matching this phase's own
error-integration example:

```python
{
    "name": "strategy_execution",
    "status": "failed",
    "duration_ms": 150,
    "error_code": "STRATEGY_001",
}
```

This is an `isinstance(exc_val, GoldBotError)` check — never guessed
or fabricated for a non-`GoldBotError` exception, which leaves
`error_code=None`.

## Logging integration

Existing logging (`core/logger.py`'s `setup_logger()`) is unchanged.
Every `PerformanceTimer`/`measure_performance` completion logs one
line:

```
PERFORMANCE module=DecisionEngine name=decision_time duration_ms=82.0 status=SUCCESS
```

Always logged, regardless of whether a `PerformanceCollector` was
supplied — visibility into a measured block's duration doesn't
require opting into collection.

## Serialization

`PerformanceMetric.to_dict()`/`.to_json()` — `timestamp` rendered as
an ISO-8601 string, everything else already a JSON-native primitive.
Future consumers (not implemented in this phase): Telegram alerts, a
monitoring pipeline, a dashboard — the same "standard shape now, real
consumer later" pattern every Phase A foundation module has followed.

## Rules

- Performance metrics are not business logic — `performance/` never
  reads `ContextSnapshot`, `SignalCandidate`, or any trading-domain
  type; it only measures a block of code's duration.
- The metric collector does not generate a signal.
- The metric collector does not make a decision.
- It only measures.

## What this phase does NOT do

- Does not add caching.
- Does not optimize the API layer, the database layer, or anything
  else — this phase only builds the ability to *measure*, per its own
  stated purpose.
- Does not change `core/pipeline.py`'s existing `_log_stage()`
  mechanism, `monitoring/performance.py`, any strategy, signal logic,
  or AI logic.
- Does not migrate the database schema.
- Does not wire `PerformanceTimer`/`PerformanceCollector` into any
  existing module.

## Future usage

- **Phase 53 Optimization** (a future, separately-approved phase):
  `Metrics -> Analysis -> Optimization` — once real metrics exist,
  identifying and fixing an actual bottleneck becomes possible;
  neither analysis nor optimization is implemented here.
- **Analytics**: `Performance data -> Dashboard` — a future consumer
  of `PerformanceCollector.get_metrics()`/`to_dict()`.
- **AI**: `Pipeline metrics -> AI diagnosis` — a future real AI
  provider (v0.4) reading collected metrics to help diagnose a
  slowdown, not implemented here.
