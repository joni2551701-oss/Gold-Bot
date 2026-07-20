"""
Monitoring Layer — Owner Snapshot model (GoldBot Core Owner Snapshot
Reporter Alpha, TASK 1; extended by the v1.1 Operational Intelligence
Upgrade, TASK 1-8).

Pure data model only -- no AI, no trading logic, no I/O. Every field
is sourced from an existing monitoring/* function by
monitoring/snapshot_collector.py; this module only defines the shape.
See docs/PHASE_OWNER_SNAPSHOT_AUDIT.md for the Alpha phase's reuse
audit, docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md for v1.1's, and
docs/OWNER_SNAPSHOT_REPORTER.md for what `telegram_status`/
`uptime_info` (and every v1.1 Proxy-classified field below) honestly
do and do not mean in a GitHub-Actions, one-shot-process context.

Every v1.1 field below is additive with a default (LOCK Policy
explicitly permits "yangi snapshot field") -- no existing field was
renamed, moved, or removed.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OwnerSnapshot:
    timestamp: str
    status: str
    core_status: str
    database_status: str
    telegram_status: str
    market_data_status: str
    last_signal: Optional[str]
    error_count: int
    uptime_info: str
    # Additive field (LOCK Policy explicitly permits "yangi snapshot
    # field") -- needed to honor TASK 3's own "Signals Today: 3"
    # format example, which TASK 1's original field list omitted.
    signals_today: int = 0

    # v1.1 TASK 1 -- Pipeline Activity. Proxy: sourced from the
    # `signals` table (the only real, wired per-cycle decision
    # record -- see docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md's TASK 1
    # finding), not a literal GitHub Actions execution count.
    # `pipeline_last_status` is "SUCCESS" (today has at least one
    # persisted decision), "NO_RUNS_TODAY" (none yet), or "UNKNOWN"
    # (the read itself failed) -- never a fabricated per-run exit code.
    pipeline_runs_today: int = 0
    pipeline_last_at: Optional[str] = None
    pipeline_last_status: str = "UNKNOWN"

    # v1.1 TASK 2 -- Signal Intelligence. Real: aggregated from the
    # same `signals` table rows already read for `signals_today`.
    signals_approved: int = 0
    signals_rejected: int = 0
    # Pre-formatted text (e.g. "FVG: 2, AMD: 3") -- kept a plain str,
    # not a dict, to match every other field's primitive-only shape
    # (this model's own docstring convention).
    strategy_breakdown: str = ""
    last_signal_score: Optional[int] = None

    # v1.1 TASK 3 -- Decision Engine Snapshot (read-only). Same source
    # as TASK 2 -- this layer maintains no second, independent
    # decision dataset (none exists). `decision_risk_pass_rate_pct` is
    # the honest substitute for the brief's "Average Risk Score": no
    # numeric risk score is persisted anywhere, only a PASSED/BLOCKED
    # `risk_status` string -- see the audit doc's TASK 3 finding.
    decision_total: int = 0
    decision_approved: int = 0
    decision_rejected: int = 0
    decision_avg_confidence_pct: float = 0.0
    decision_risk_pass_rate_pct: float = 0.0

    # v1.1 TASK 4 -- AI Layer Monitoring. Unavailable by design: AI
    # request/response logs are in-memory only (ai/audit/*.py), never
    # persisted, so a fresh one-shot process always sees zero AI
    # activity from a *different* process. Always "NO_DATA"/0 today --
    # never fabricated, exactly the brief's own anticipated fallback.
    ai_requests_today: int = 0
    ai_status: str = "NO_DATA"

    # v1.1 TASK 5 -- Market Data Monitoring Upgrade. Real
    # provider/symbol/timeframe/configured-candle-count -- the single
    # timeframe (`M15`) the live pipeline actually fetches today, not
    # the brief's three-timeframe example (see audit doc).
    market_provider: str = ""
    market_symbol: str = ""
    market_timeframe: str = ""
    market_candles_configured: int = 0

    # v1.1 TASK 6 -- Error Intelligence. Real: aggregated from
    # ErrorMonitor.get_recent_errors()'s already-returned severity/
    # module/timestamp fields.
    errors_critical: int = 0
    errors_warning: int = 0
    last_error_module: Optional[str] = None
    last_error_time: Optional[str] = None

    # v1.1 TASK 7 -- System Runtime Metrics. Self-measured: this
    # run's own collect->format->send duration (a real,
    # time.perf_counter()-measured number, never estimated -- same
    # convention monitoring/provider_health.py's latency_ms already
    # uses). `runtime_next_check` is a deterministic computation from
    # the known 15-minute cron schedule.
    runtime_execution_seconds: float = 0.0
    runtime_next_check: Optional[str] = None

    # v1.1 TASK 8 -- Database Statistics. Real row counts, "today"
    # scoped to match every other v1.1 field. `db_pipeline_events_total`
    # reads 0 today for the same reason as `pipeline_runs_today`'s own
    # caveat: monitoring_decision_pipeline has no production writer yet.
    db_signals_total: int = 0
    db_errors_total: int = 0
    db_pipeline_events_total: int = 0
