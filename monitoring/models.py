"""
Monitoring Layer — Foundation Models (GoldBot Core Owner Monitoring
Alpha, TASK 1).

Every field is a primitive (`str`/`float`/`int`/`bool`) or an enum
defined in this same file -- no Trading Core object reference of any
kind (`decision.models.TradeDecision`, `risk.risk_manager.RiskResult`,
`signals.signal_quality.SignalQualityResult`, etc.). Monitoring never
imports `decision/`, `risk/`, or `execution/` (this brief's own TASK 8
isolation list); `SystemHealth`/`MarketHealth`/`SignalHealth` are
computed live from already-existing sources (see
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s TASK 9 conclusion -- no new
persistence for these three, only for `ErrorEvent`/
`DecisionPipelineEntry`).

Fields the underlying data source cannot honestly supply are
`Optional` and left `None` rather than fabricated -- e.g.
`MarketHealth.last_price`/`.last_update` (no data-freshness concept
exists anywhere in `data/providers/` today, per the audit's own
"data/providers/" section).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence


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
    own `core/logger.py` section).
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
    `signals.signal_quality.SignalQualityResult`'s own shape exactly
    (e.g. `criteria_met=("STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT")`,
    `criteria_total=5`) -- relayed as primitive values only, this
    module never imports `signals.signal_quality.SignalQualityResult`
    itself (see `docs/PHASE_CORE_MONITORING_AUDIT.md`'s own
    "signals/ and context/" section for why: a primitive-only contract
    boundary, not an object reference).
    decision: the already-made decision label (e.g. "NO TRADE",
        "BUY") -- relayed only, never computed by this package.
    """

    timestamp: str
    symbol: str
    timeframe: str
    criteria_met: Sequence[str]
    criteria_total: int
    decision: str
    reason: str = ""
