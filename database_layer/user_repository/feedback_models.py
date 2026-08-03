from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FeedbackRecord:
    """
    Feedback entry record. Mirrors the 'feedback' table row shape.
    Unlike UserRecord/AdminRecord/SubscriptionRecord, id IS included
    here -- it's the user-facing feedback ticket number (e.g. "#12" in
    /feedback's confirmation and /feedbacks' admin listing), not just
    a repository-internal detail.
    """
    id: int
    telegram_id: str
    message: str
    status: str
    created_at: datetime
