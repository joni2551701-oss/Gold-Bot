from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class UserRecord:
    """
    Minimal user profile record. Mirrors the 'users' table row shape.
    id and updated_at are intentionally excluded -- repository-internal
    detail, not part of the profile a caller of UserService needs.

    strategy/notifications_enabled (Phase 40) and status/last_activity
    (Phase 45 -- user lifecycle state, deliberately separate from
    subscription plan/status: see telegram/subscription_service.py)
    default so existing positional/keyword construction of this
    dataclass keeps working. An old row with no status column yet
    reads back as "NEW" (the schema default applied by the Phase 45
    migration), never a missing/None value.
    """
    telegram_id: str
    username: Optional[str]
    language: str
    trading_style: str
    risk_percent: float
    timeframe: str
    created_at: datetime
    strategy: str = "Liquidity Sweep"
    notifications_enabled: bool = True
    status: str = "NEW"
    last_activity: Optional[str] = None
