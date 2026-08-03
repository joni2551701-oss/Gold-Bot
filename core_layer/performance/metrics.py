"""
Performance Metrics — data model (Phase A19).

Measures execution time; it does not decide, analyze, or optimize
anything. PerformanceMetric is a pure record of "this named thing, in
this module, took this long, and either succeeded or failed" -- see
docs/PERFORMANCE_METRICS.md for the full contract.

Distinct from two pre-existing, unrelated concepts with a similar
name:
- core_layer/health_monitor/performance.py's PerformanceTracker/PerformanceResult
  compute historical *trade outcome* statistics (win rate, strategy
  breakdown) from the database -- a completely different question
  than "how long did this code take to run."
- core/pipeline.py's own _log_stage() already logs each pipeline
  stage's duration today -- this package does not replace or wrap
  that; it is a new, standalone, not-yet-wired-in foundation (see
  "Zero pipeline wiring" in docs/PERFORMANCE_METRICS.md).
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# The two real statuses this phase's own brief uses in both its
# model example and its error-integration example.
ALLOWED_STATUSES = ("success", "failed")

# Standard metric names (one per category named in this phase's
# brief) -- the conventional value for `name` per category. Not
# enforced by validate_metric(): a caller may record any name: these
# are named constants for consistency, not a closed vocabulary.
METRIC_PIPELINE_TOTAL_TIME = "pipeline_total_time"
METRIC_MARKET_DATA_FETCH_TIME = "market_data_fetch_time"
METRIC_CONTEXT_BUILD_TIME = "context_build_time"
METRIC_STRATEGY_EXECUTION_TIME = "strategy_execution_time"
METRIC_AI_ANALYSIS_TIME = "ai_analysis_time"
METRIC_DECISION_TIME = "decision_time"
METRIC_DATABASE_QUERY_TIME = "database_query_time"


def generate_metric_id() -> str:
    """Same generation convention as signals.schema.generate_signal_id()/context.snapshot.generate_snapshot_id() (str(uuid.uuid4()))."""
    return str(uuid.uuid4())


@dataclass(frozen=True)
class PerformanceMetric:
    """
    name/module/duration_ms are required -- matching this phase's own
    brief, which shows PerformanceMetric(name=..., module=...,
    duration_ms=...) with no other argument. metric_id/timestamp/
    status/metadata/error_code all have sensible defaults
    (auto-generated id, "now" timestamp, "success" status, an empty
    metadata dict, no error code) so that three-argument construction
    works exactly as the brief's own example shows -- a deliberate
    difference from signals.schema.SignalSchema/
    context.snapshot.ContextSnapshotSchema, whose identity fields are
    always required, no default, because this phase's own brief
    explicitly demonstrates the shorter form.

    name: the metric's name (e.g. "context_analysis") -- see the
        METRIC_* constants above for the standard per-category names.
    module: which module/component this measures (e.g.
        "ContextEngine") -- a plain string, not a Python module path.
    duration_ms: elapsed time in milliseconds.
    metric_id: a real, generated identity (generate_metric_id()).
    timestamp: when this metric was recorded (UTC).
    status: "success" or "failed" (ALLOWED_STATUSES).
    metadata: optional extra structured context -- defaults to an
        empty dict, never None.
    error_code: optional, e.g. "STRATEGY_001" -- set when `status`
        is "failed" and the failure was a core_layer.errors.base.GoldBotError
        (see core_layer/performance/timer.py's PerformanceTimer for the one
        place this gets populated automatically). None otherwise --
        never fabricated.
    """
    name: str
    module: str
    duration_ms: float
    metric_id: str = field(default_factory=generate_metric_id)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "success"
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """JSON-safe dict -- timestamp rendered as an ISO-8601 string."""
        return {
            "metric_id": self.metric_id,
            "name": self.name,
            "module": self.module,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "metadata": self.metadata,
            "error_code": self.error_code,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass(frozen=True)
class ValidationResult:
    """Same two-field (valid, errors) shape as every other Phase A foundation module's own independent ValidationResult -- not imported from elsewhere (see docs/PERFORMANCE_METRICS.md)."""
    valid: bool
    errors: List[str] = field(default_factory=list)


def validate_metric(metric: PerformanceMetric) -> ValidationResult:
    """Never raises -- an invalid PerformanceMetric produces ValidationResult(valid=False, errors=[...]), not an exception."""
    errors: List[str] = []

    if not metric.name:
        errors.append("name is required")
    if not metric.module:
        errors.append("module is required")
    if metric.duration_ms is None or metric.duration_ms < 0:
        errors.append("duration_ms must be a non-negative number")
    if metric.status not in ALLOWED_STATUSES:
        errors.append(f"status must be one of {ALLOWED_STATUSES}, got {metric.status!r}")

    return ValidationResult(valid=len(errors) == 0, errors=errors)
