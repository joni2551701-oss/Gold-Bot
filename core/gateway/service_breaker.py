"""
Service circuit breaker (v1.1 Phase 1, module 10; ORDER-064 amendment 5).

A *service-reliability* breaker: when a registered service fails a run of
consecutive calls it trips OPEN, so the Gateway stops routing to it; after
a cooldown it goes HALF_OPEN to admit one trial call, then CLOSED on
success or back to OPEN on failure. Clock-injected (callers pass `now`) so
the cooldown is deterministic and testable.

Foundation Reuse Audit (Constitution Art. 11): `core/emergency/
circuit_breaker.py` already exists, but it is a *trading-domain* breaker
(a pure, stateless ALLOW/BLOCK decision over loss/drawdown/api signals).
Reusing or extending it here would (a) pull trading semantics into the
Gateway -- forbidden, the Gateway knows nothing of Strategy/Decision/Risk
-- and (b) require a stateful OPEN/HALF_OPEN/CLOSED machine its stateless
contract does not have. Both reuse steps are therefore "no", so a distinct
service-scoped breaker is created (named ServiceCircuitBreaker to avoid any
confusion with the trading one).

This module is pure; it imports nothing from the repo.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class BreakerState(Enum):
    CLOSED = "closed"       # healthy, calls flow
    OPEN = "open"           # tripped, calls rejected until cooldown elapses
    HALF_OPEN = "half_open"  # cooldown elapsed, admitting one trial call


class ServiceCircuitBreaker:
    def __init__(self, failure_threshold: int = 3,
                 recovery_timeout: timedelta = timedelta(seconds=30)):
        self._threshold = max(1, failure_threshold)
        self._recovery = recovery_timeout
        self._state = BreakerState.CLOSED
        self._failures = 0
        self._opened_at: Optional[datetime] = None

    @property
    def state(self) -> BreakerState:
        return self._state

    @property
    def failure_count(self) -> int:
        return self._failures

    def allow(self, now: datetime) -> bool:
        """Whether a call may proceed. May move OPEN -> HALF_OPEN on cooldown."""
        if self._state is BreakerState.OPEN:
            if self._opened_at is not None and \
                    now - self._opened_at >= self._recovery:
                self._state = BreakerState.HALF_OPEN
                return True
            return False
        return True                     # CLOSED or HALF_OPEN (trial)

    def record_success(self) -> None:
        self._state = BreakerState.CLOSED
        self._failures = 0
        self._opened_at = None

    def record_failure(self, now: datetime) -> None:
        self._failures += 1
        if self._state is BreakerState.HALF_OPEN:
            self._trip(now)             # trial failed -> back to OPEN
        elif self._failures >= self._threshold:
            self._trip(now)

    def _trip(self, now: datetime) -> None:
        self._state = BreakerState.OPEN
        self._opened_at = now
