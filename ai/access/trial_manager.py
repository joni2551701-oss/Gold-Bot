"""
AI Layer — AI Trial Manager (Phase 61.4: AI Product & Control Layer,
TASK 5).

In-memory, per-`telegram_id` FREE trial window -- same "foundation
only, no persistence, no timer/scheduler" posture as
`ai/access/usage_limits.py`'s `UsageLimiter`. Trial eligibility
additionally depends on `ai/access/identity_checker.py`'s phone-reuse
check, composed by the caller -- this module never reads a phone
number or a `phone_hash` itself, only the boolean result of that
check.

"1 telefon = 1 trial" (one phone = one trial): `check_eligibility()`
rejects a new trial outright when `phone_reused=True`, regardless of
whether the requesting `telegram_id` has ever started a trial before
-- the phone-based block always wins over the telegram_id-based one.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

DEFAULT_TRIAL_DURATION = timedelta(days=7)


@dataclass(frozen=True)
class TrialEligibilityResult:
    eligible: bool
    reason: str


@dataclass(frozen=True)
class TrialStatus:
    started_at: Optional[datetime]
    active: bool
    expires_at: Optional[datetime]


class TrialManager:
    """Every dependency is injectable (`trial_duration`), same convention as every other Phase 61.x foundation class."""

    def __init__(self, trial_duration: timedelta = DEFAULT_TRIAL_DURATION) -> None:
        self._duration = trial_duration
        self._trials: Dict[str, datetime] = {}

    def check_eligibility(self, telegram_id: str, phone_reused: bool) -> TrialEligibilityResult:
        """Read-only check -- does not start a trial. Never raises."""
        if phone_reused:
            return TrialEligibilityResult(
                eligible=False, reason="phone number already used for a trial on another account",
            )
        if telegram_id in self._trials:
            return TrialEligibilityResult(eligible=False, reason="trial already started for this account")
        return TrialEligibilityResult(eligible=True, reason="")

    def start_trial(
        self, telegram_id: str, phone_reused: bool, now: Optional[datetime] = None,
    ) -> TrialEligibilityResult:
        """Starts a trial only if check_eligibility() allows it -- never overwrites an already-recorded start, never raises."""
        eligibility = self.check_eligibility(telegram_id, phone_reused)
        if not eligibility.eligible:
            return eligibility
        self._trials[telegram_id] = now if now is not None else datetime.now(timezone.utc)
        return TrialEligibilityResult(eligible=True, reason="trial started")

    def status_of(self, telegram_id: str, now: Optional[datetime] = None) -> TrialStatus:
        """Never raises: a telegram_id with no recorded trial reports active=False, started_at=None, expires_at=None."""
        started_at = self._trials.get(telegram_id)
        if started_at is None:
            return TrialStatus(started_at=None, active=False, expires_at=None)

        check_time = now if now is not None else datetime.now(timezone.utc)
        expires_at = started_at + self._duration
        return TrialStatus(started_at=started_at, active=check_time < expires_at, expires_at=expires_at)
