from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AdminRecord:
    """
    Minimal admin record. Mirrors the 'admins' table row shape.
    id is intentionally excluded -- repository-internal detail, not
    part of the record a caller of AdminService needs.
    """
    telegram_id: str
    role: str
    created_at: datetime
