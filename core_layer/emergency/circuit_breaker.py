"""
Core Layer — Circuit Breaker Foundation (Phase 59.9: Emergency Safety
Layer Foundation, TASK 4).

A pure decision function: given a snapshot of loss/drawdown/api/error
signals, returns a CircuitDecision (ALLOW/BLOCK/WARNING) and a
human-readable reason. Deliberately stateless and side-effect-free --
it does not read or write core_layer.emergency.emergency_manager.EmergencyManager,
does not persist anything, and is never called from
core/pipeline.py/decision/risk/execution/ in this phase ("executionga
ulanmaydi. Faqat qaror beradi." per this task's own brief). A future,
separately-approved phase would call evaluate_circuit() from wherever
per-signal or per-cycle loss/drawdown data is available and feed its
CircuitDecision into EmergencyManager.activate_pause()/activate_kill().

Thresholds are this module's own defaults, not a shared import from
risk/risk_manager.py's RiskConfig.max_drawdown -- core/ must not import
risk/ (CLAUDE.md layer isolation; risk/ sits above core/ in the
pipeline, never the reverse). DEFAULT_MAX_DAILY_DRAWDOWN mirrors
risk/risk_manager.py's own default (0.10) in value only, as an
independent constant -- reconciling the two, if they should ever
diverge, is a future explicit decision, not this phase's.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

DEFAULT_MAX_CONSECUTIVE_LOSSES = 3
DEFAULT_MAX_DAILY_DRAWDOWN = 0.10
_WARNING_DRAWDOWN_RATIO = 0.5


class CircuitDecision(Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    WARNING = "WARNING"


@dataclass(frozen=True)
class CircuitBreakerInput:
    """
    loss_count: consecutive losses observed so far (caller-computed --
        this module does not track a running count itself).
    daily_drawdown: today's drawdown as a fraction (0.05 = 5%).
    api_status: a free-text provider health label (e.g. "OK",
        "DEGRADED", "DOWN") -- same convention as
        monitoring.provider_health.ProviderStatus's own string values,
        not imported here to keep this module dependency-free.
    execution_error: whether the caller observed an execution-layer
        error this cycle (this module does not know what kind).
    """
    loss_count: int = 0
    daily_drawdown: float = 0.0
    api_status: str = "OK"
    execution_error: bool = False


@dataclass(frozen=True)
class CircuitBreakerResult:
    decision: CircuitDecision
    reason: Optional[str] = None


def evaluate_circuit(
    signal: CircuitBreakerInput,
    max_consecutive_losses: int = DEFAULT_MAX_CONSECUTIVE_LOSSES,
    max_daily_drawdown: float = DEFAULT_MAX_DAILY_DRAWDOWN,
) -> CircuitBreakerResult:
    """
    Pure rule evaluation, most severe condition wins:
        execution_error                                -> BLOCK
        loss_count >= max_consecutive_losses            -> BLOCK
        daily_drawdown >= max_daily_drawdown            -> BLOCK
        daily_drawdown >= max_daily_drawdown * 0.5       -> WARNING
        api_status != "OK"                              -> WARNING
        otherwise                                       -> ALLOW
    """
    if signal.execution_error:
        return CircuitBreakerResult(CircuitDecision.BLOCK, "execution error detected")

    if signal.loss_count >= max_consecutive_losses:
        return CircuitBreakerResult(
            CircuitDecision.BLOCK,
            f"{signal.loss_count} consecutive losses (limit: {max_consecutive_losses})",
        )

    if signal.daily_drawdown >= max_daily_drawdown:
        return CircuitBreakerResult(
            CircuitDecision.BLOCK,
            f"daily drawdown {signal.daily_drawdown:.2%} reached limit {max_daily_drawdown:.2%}",
        )

    if signal.daily_drawdown >= max_daily_drawdown * _WARNING_DRAWDOWN_RATIO:
        return CircuitBreakerResult(
            CircuitDecision.WARNING,
            f"daily drawdown {signal.daily_drawdown:.2%} approaching limit {max_daily_drawdown:.2%}",
        )

    if signal.api_status != "OK":
        return CircuitBreakerResult(CircuitDecision.WARNING, f"provider api status: {signal.api_status}")

    return CircuitBreakerResult(CircuitDecision.ALLOW)
