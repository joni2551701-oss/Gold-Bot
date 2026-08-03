"""
Monitoring Layer — Foundation Models (GoldBot Core Owner Monitoring
Alpha, TASK 1; extended by Phase B.0's own genuine-gaps set --
`HealthStatus`, `ResourceSnapshot`, `PerformanceCounters`, and
`DecisionPipelineEntry.stage_durations_ms` -- see
`docs/PHASE_B0_AUDIT.md`).

Every field is a primitive (`str`/`float`/`int`/`bool`) or an enum
defined in this same file -- no Trading Core object reference of any
kind (`decision_layer.decision_engine.models.TradeDecision`, `risk_layer.risk_engine.risk_manager.RiskResult`,
`signal_layer.signal_scoring.signal_quality.SignalQualityResult`, etc.). Monitoring never
imports `decision/`, `risk/`, or `execution/` (this brief's own TASK 8
isolation list); `SystemHealth`/`MarketHealth`/`SignalHealth` are
computed live from already-existing sources (see
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s TASK 9 conclusion -- no new
persistence for these three, only for `ErrorEvent`/
`DecisionPipelineEntry`).

Fields the underlying data source cannot honestly supply are
`Optional` and left `None` rather than fabricated -- e.g.
`MarketHealth.last_price`/`.last_update` (no data-freshness concept
exists anywhere in `data_layer/providers/` today, per the audit's own
"data_layer/providers/" section).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence, Tuple


@dataclass(frozen=True)
class SystemHealth:
    """
    status: a short label ("RUNNING"/"DEGRADED"/etc.), caller-supplied
        or derived by `system_monitor.get_health()` -- never a
        Trading Core operating-mode object.
    uptime_seconds: how long this monitoring session has observed the
        process for -- an in-memory duration tracked by
        `system_monitor.SystemMonitor` itself (this Foundation holds
        no persisted "process started at" timestamp anywhere else).
    last_scan: an optional, caller-supplied timestamp string for the
        most recent pipeline activity `SystemMonitor.record_scan()`
        was told about -- `None` ("N/A") until a caller reports one;
        never inferred from `core/pipeline.py` (untouched, per Strict
        Rules).
    last_error: the most recent `ErrorEvent.message`, when the error
        monitor has captured one -- `None` otherwise.
    data_connection: a short label summarizing provider registry
        health (e.g. "2/4 ONLINE").
    database_status: relayed directly from
        `telegram.admin_service.AdminService.get_system_status().database`.
    """

    status: str
    uptime_seconds: float
    data_connection: str
    database_status: str
    last_scan: Optional[str] = None
    last_error: Optional[str] = None


@dataclass(frozen=True)
class MarketHealth:
    """
    symbol: the instrument this snapshot describes.
    last_price/last_update: optional, caller-supplied -- this package
        has no live price feed of its own; `None` when the caller
        supplies nothing (never fabricated).
    latency: relayed from `monitoring.provider_health.ProviderHealthReport.latency_ms`.
    data_source_status: relayed from
        `monitoring.provider_health.ProviderHealthStatus.value`.
    """

    symbol: str
    data_source_status: str
    last_price: Optional[float] = None
    last_update: Optional[str] = None
    latency_ms: Optional[float] = None


@dataclass(frozen=True)
class SignalHealth:
    """
    total_signals/buy_count/sell_count/none_count: today's activity
        counts, aggregated from `database.signal_repository.SignalRepository`
        rows -- relayed counts, never estimated.
    average_confidence: mean of `confidence_score` across today's
        signal rows, 0.0 when there are none (never a fabricated
        default like 0.5).
    """

    total_signals: int
    buy_count: int
    sell_count: int
    none_count: int
    average_confidence: float


class ErrorSeverity(Enum):
    """TASK 6's own exact vocabulary -- caller-supplied when `ErrorMonitor.capture()` is called."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class ErrorEvent:
    """
    TASK 1's own exact field list: `timestamp`, `module`, `error_type`,
    `message`, `severity`. Persisted via
    `database.monitoring_repository.MonitoringRepository` (TASK 9) --
    the one genuinely new persistence this phase adds (no existing
    error-capture mechanism anywhere in the codebase, per the audit's
    own `core_layer/logger/logger.py` section).
    """

    timestamp: str
    module: str
    error_type: str
    message: str
    severity: ErrorSeverity


@dataclass(frozen=True)
class DecisionPipelineEntry:
    """
    TASK 5's own "AI keyinchalik o'rganishi uchun" (for AI to learn
    from later) datasource -- the future `66.5`/`66.6` Performance/
    Strategy Intelligence input this brief's own closing section names.

    criteria_met/criteria_total mirror
    `signal_layer.signal_scoring.signal_quality.SignalQualityResult`'s own shape exactly
    (e.g. `criteria_met=("STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT")`,
    `criteria_total=5`) -- relayed as primitive values only, this
    module never imports `signal_layer.signal_scoring.signal_quality.SignalQualityResult`
    itself (see `docs/PHASE_CORE_MONITORING_AUDIT.md`'s own
    "signals/ and context/" section for why: a primitive-only contract
    boundary, not an object reference).
    decision: the already-made decision label (e.g. "NO TRADE",
        "BUY") -- relayed only, never computed by this package.
    stage_durations_ms: Phase B.0's own genuine gap (TASK 5 -- "Har
        bosqich vaqtini yozadi", each stage records its own time) --
        an ordered `(stage_name, duration_ms)` sequence, e.g.
        `(("context", 4.2), ("signal", 1.1), ("ai", 812.0),
        ("decision", 0.3), ("risk", 0.2))`. Caller-supplied only, this
        module never measures a stage's duration itself. Defaults to
        `()` -- entries logged before Phase B.0 (or by a caller that
        doesn't measure stages) remain valid.
    """

    timestamp: str
    symbol: str
    timeframe: str
    criteria_met: Sequence[str]
    criteria_total: int
    decision: str
    reason: str = ""
    stage_durations_ms: Sequence[Tuple[str, float]] = field(default_factory=tuple)


class HealthStatus(Enum):
    """Phase B.0 TASK 6's own exact vocabulary -- a deterministic classification of already-known facts, never a fabricated grade."""

    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class ResourceSnapshot:
    """
    Phase B.0 TASK 2's own genuine gap -- process-level resource
    metrics, distinct from `SystemHealth` (which covers
    database/data-connection/scan-activity, not CPU/RAM/threads).

    cpu_time_seconds/max_rss_kb: from `resource.getrusage(RUSAGE_SELF)`
        (stdlib, POSIX-only) -- `None` on a platform where the
        `resource` module is unavailable, never fabricated.
    thread_count: `threading.active_count()` at snapshot time.
    restart_count: how many times this process has started, persisted
        via `database.monitoring_repository.MonitoringRepository`
        (the one fact in this snapshot that cannot be tracked
        in-memory, since a restart is by definition a new process).
    uptime_seconds: relayed from the already-existing
        `monitoring.system_monitor.SystemMonitor.uptime_seconds()` --
        never a second, competing uptime tracker.
    heartbeat_at: an ISO-8601 timestamp stamped at snapshot time --
        proof this process answered the call, not a background
        scheduler (Rule 3: passive observation only).
    """

    cpu_time_seconds: Optional[float]
    max_rss_kb: Optional[int]
    thread_count: int
    restart_count: int
    uptime_seconds: float
    heartbeat_at: str


@dataclass(frozen=True)
class PerformanceCounters:
    """
    Phase B.0 TASK 7's own genuine gap -- "Hozircha faqat yig'adi.
    Hisoblamaydi" (for now, only collects, does not compute). Plain
    tallies only -- no win-rate, no average, no derived metric of any
    kind (that is `monitoring.performance.PerformanceTracker`'s own,
    separate, already-existing concern). Every count starts at 0 and
    is incremented one at a time by `monitoring.performance_collector.PerformanceCollector`.
    """

    signal_count: int = 0
    decision_count: int = 0
    trade_count: int = 0
    reject_count: int = 0
    error_count: int = 0
    reconnect_count: int = 0
    runtime_seconds: float = 0.0
