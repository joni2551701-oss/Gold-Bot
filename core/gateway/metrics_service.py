"""
Gateway metrics (v1.1 Phase 1, module 10).

Counts requests by outcome and by service so Monitoring can read Gateway
throughput and error rates. Pure accumulation over already-known outcomes;
never fabricates a value.

Imports only the sibling status enum.
"""

from __future__ import annotations

from typing import Dict

from core.gateway.gateway_request import GatewayResponse, GatewayStatus


class GatewayMetrics:
    def __init__(self):
        self.total = 0
        self.by_status: Dict[str, int] = {}
        self.by_service: Dict[str, int] = {}

    def record(self, response: GatewayResponse) -> None:
        self.total += 1
        key = response.status.value
        self.by_status[key] = self.by_status.get(key, 0) + 1
        if response.service:
            self.by_service[response.service] = \
                self.by_service.get(response.service, 0) + 1

    @property
    def failures(self) -> int:
        bad = (GatewayStatus.ERROR, GatewayStatus.UNAVAILABLE)
        return sum(self.by_status.get(s.value, 0) for s in bad)

    def snapshot(self) -> Dict:
        return {
            "total": self.total,
            "by_status": dict(self.by_status),
            "by_service": dict(self.by_service),
            "failures": self.failures,
        }
