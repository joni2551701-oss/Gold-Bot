"""
Gateway health service (v1.1 Phase 1, module 10).

Aggregates named health checks into one OK/DEGRADED/DOWN grade the Gateway
can serve. Checks are injected callables returning bool -- so the real
system-health source (`core_layer/health_monitor/health_monitor.py::classify_health`) is
wired in at composition time rather than imported here.

Foundation Reuse Audit (Constitution Art. 11): `monitoring/health_monitor`
already grades OK/WARNING/CRITICAL, and it is REUSED -- but by *injection*,
not import. The Gateway lives in `core/`, which foundational layers import;
importing `monitoring/` (a higher layer) back into it would invert the
dependency (CLAUDE.md layer isolation). Injecting the check keeps the arrow
pointing the right way and keeps the Gateway testable in isolation. The
local GatewayHealth vocabulary intentionally mirrors HealthStatus in
meaning without importing it, the same independent-constant pattern
`core_layer/emergency/circuit_breaker.py` already uses.

Imports only the stdlib.
"""

from __future__ import annotations

from enum import Enum
from typing import Callable, Dict


class GatewayHealth(Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"


HealthCheck = Callable[[], bool]


class HealthService:
    def __init__(self):
        self._checks: Dict[str, HealthCheck] = {}

    def register_check(self, name: str, check: HealthCheck) -> None:
        self._checks[name] = check

    def _results(self) -> Dict[str, bool]:
        out: Dict[str, bool] = {}
        for name, check in self._checks.items():
            try:
                out[name] = bool(check())
            except Exception:
                out[name] = False
        return out

    def status(self) -> GatewayHealth:
        results = self._results()
        if not results:
            return GatewayHealth.OK
        passed = sum(1 for ok in results.values() if ok)
        if passed == len(results):
            return GatewayHealth.OK
        if passed == 0:
            return GatewayHealth.DOWN
        return GatewayHealth.DEGRADED

    def report(self) -> Dict:
        results = self._results()
        status = self.status()
        return {"status": status.value, "checks": results}
