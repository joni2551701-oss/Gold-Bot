"""
Monitoring Layer — Owner Snapshot model (GoldBot Core Owner Snapshot
Reporter Alpha, TASK 1).

Pure data model only -- no AI, no trading logic, no I/O. Every field
is sourced from an existing monitoring/* function by
monitoring/snapshot_collector.py; this module only defines the shape.
See docs/PHASE_OWNER_SNAPSHOT_AUDIT.md for the full reuse audit and
docs/OWNER_SNAPSHOT_REPORTER.md for what `telegram_status`/
`uptime_info` honestly do and do not mean in a GitHub-Actions,
one-shot-process context.
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
