"""
BootstrapProgress -- observable bootstrap progress (DD-054).

A serializable snapshot future consumers (Telegram, Dashboard, Admin
Panel) can display. This module never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from data.bootstrap.bootstrap_state import BootstrapState


@dataclass(frozen=True)
class BootstrapProgress:
    """Point-in-time bootstrap progress for one asset (DD-054)."""
    asset: str
    status: BootstrapState
    progress_pct: float                      # 0.0 .. 100.0
    current_timeframe: Optional[str]         # TF being worked, or None
    remaining: List[str] = field(default_factory=list)   # TFs not yet READY
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
