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

    phone_hash (Phase 61.4 TASK 4): a deterministic, salted hash of
    the user's Telegram-contact-shared phone number
    (core.phone_hash.hash_phone_number()) -- the raw phone number is
    never stored anywhere in this codebase. None for a user who has
    not shared their contact yet (every user before this phase, and
    any user who declines to). Used by ai/access/identity_checker.py
    (Phase 61.4 TASK 5) to detect the same phone re-registering under
    a new telegram_id for repeated free trials.

    trial_started_at (Phase 61.5 TASK 4): an ISO-8601 timestamp string,
    same storage convention as `last_activity` -- set once, the first
    time this user's shared phone passes
    `ai.access.identity_checker.is_phone_reused_by_another_account()`.
    None for a user who has not started a trial yet. Paired with
    `ai.access.trial_manager.trial_status_from_started_at()` to
    compute active/expires_at without a second, database-specific
    reimplementation of that math.
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
    phone_hash: Optional[str] = None
    trial_started_at: Optional[str] = None
