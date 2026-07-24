# performance/

## Purpose
Performance Metrics foundation (Phase A19) — the ability to
**measure** GoldBot before trying to make it faster. A data model
(`PerformanceMetric`), a collector (`PerformanceCollector`), and a
timer/decorator (`PerformanceTimer`/`measure_performance`). Not a
speed-up: no caching, no API/database optimization, no pipeline
change. See `docs/PERFORMANCE_METRICS.md` for the full contract,
including how this differs from the two pre-existing, similarly-named
concepts (`monitoring/performance.py`'s trade-outcome statistics and
`core/pipeline.py`'s own `_log_stage()` timing).

## Usage
```python
from performance.collector import PerformanceCollector
from performance.timer import PerformanceTimer, measure_performance

collector = PerformanceCollector()

with PerformanceTimer("context_build", module="ContextEngine", collector=collector):
    build_context()

@measure_performance("strategy_execution", module="StrategyEngine", collector=collector)
def run_strategy():
    ...

for metric in collector.get_metrics():
    print(metric.to_json())
```

## Module layout
- `metrics.py` — `PerformanceMetric` (`name`/`module`/`duration_ms`
  required; `metric_id`/`timestamp`/`status`/`metadata`/`error_code`
  default), `validate_metric()`, `generate_metric_id()`, the
  `METRIC_*` standard-name constants.
- `collector.py` — `PerformanceCollector`
  (`record()`/`get_metrics()`/`get_by_module()`/`clear()`), not a
  singleton.
- `timer.py` — `PerformanceTimer` (a context manager) and
  `measure_performance()` (its decorator form). Integrates with Phase
  A18: a `core.errors.base.GoldBotError` raised inside is captured as
  the metric's `error_code`.

## What this does NOT do
- Does not speed anything up — no caching, no API optimization, no
  database refactor.
- Does not change `core/pipeline.py`, any strategy, signal logic, or
  AI logic.
- Does not migrate the database schema — no metric is persisted in
  this phase.
- Does not generate a signal or make a decision — it only measures.
- Is not wired into any existing module in this phase.

## Dependencies
`core/errors/` (for the optional `GoldBotError` integration in
`timer.py`) and `core/logger.py` (for the `PERFORMANCE` log line) —
both cross-cutting, same as every layer's existing access to `core/`.
No dependency on `context/`, `strategies/`, `signals/`, `ai/`,
`decision/`, `risk/`, `execution/`, `telegram/`, or `database/`.

## Future extension
See `docs/PERFORMANCE_METRICS.md`'s "Future usage" section — Phase 53
Optimization (`Metrics -> Analysis -> Optimization`), an Analytics
dashboard, and AI-assisted pipeline diagnosis are all named, explicit
future steps, none implemented in this phase.
