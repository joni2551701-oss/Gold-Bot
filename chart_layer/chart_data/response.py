"""Chart Service Foundation — Chart Response contract (FLOW-016).

ChartResponse carries metadata, status, chart_reference and timestamp.
When the renderer produces a placeholder (Foundation scope), the
response status is PLACEHOLDER — the contract is complete regardless.
Lives in Chart_Data as the chart-data output contract.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from .models import ChartStatus


@dataclass
class ChartResponse:
    status: ChartStatus
    chart_reference: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    @classmethod
    def success(cls, chart_reference, metadata=None, cached=False):
        return cls(
            status=ChartStatus.CACHED if cached else ChartStatus.CREATED,
            chart_reference=chart_reference,
            metadata=dict(metadata or {}),
        )

    @classmethod
    def placeholder(cls, chart_reference=None, metadata=None):
        return cls(
            status=ChartStatus.PLACEHOLDER,
            chart_reference=chart_reference,
            metadata=dict(metadata or {}),
        )

    @classmethod
    def failed(cls, reason, metadata=None):
        md = dict(metadata or {})
        md["error"] = reason
        return cls(status=ChartStatus.FAILED, chart_reference=None, metadata=md)

    @property
    def ok(self) -> bool:
        return self.status in (
            ChartStatus.CREATED,
            ChartStatus.CACHED,
            ChartStatus.PLACEHOLDER,
        )
