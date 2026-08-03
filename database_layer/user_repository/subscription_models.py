from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class SubscriptionRecord:
    """
    Minimal subscription record. Mirrors the 'subscriptions' table row
    shape. id/created_at/updated_at are intentionally excluded --
    repository-internal detail, not part of what a caller of
    SubscriptionService needs (started_at already covers "when did
    this subscription begin").
    """
    telegram_id: str
    plan: str
    status: str
    started_at: datetime
    expires_at: Optional[datetime]
