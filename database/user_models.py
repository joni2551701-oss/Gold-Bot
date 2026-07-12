from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class UserRecord:
    """
    Minimal user profile record. Mirrors the 'users' table row shape.
    id and updated_at are intentionally excluded -- repository-internal
    detail, not part of the profile a caller of UserService needs.
    """
    telegram_id: str
    username: Optional[str]
    language: str
    trading_style: str
    risk_percent: float
    timeframe: str
    created_at: datetime
