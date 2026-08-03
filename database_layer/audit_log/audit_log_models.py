"""
Database Layer — Audit Log persistence model (Phase 59.6: Audit &
Observability Foundation, TASK 2).

Records every owner/admin action for later review -- "kim nima
qilganini har doim bilish mumkin" (who did what, always knowable), per
this task's own brief. This module and its repository only record and
read entries; nothing in this codebase writes to it automatically yet
-- no owner command in telegram/owner/ calls
AuditLogRepository.log_action() in this phase. Wiring real owner
actions to call it is a future, separately-approved step (Phase 59.7+
per the Director's own roadmap).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class AuditLogEntry:
    """
    Mirrors the 'audit_log' table row shape. `id` is intentionally
    excluded -- repository-internal detail, same convention as every
    other Phase 59.x model in this codebase.
    actor: who performed the action (e.g. a Telegram user_id, or
        "owner" -- this module does not resolve or validate identity,
        it records whatever string the caller supplies).
    action: a short, stable verb/noun the caller chooses (e.g.
        "ENABLE_PROVIDER", "PANIC", "FEATURE_TOGGLE") -- no fixed
        taxonomy is enforced here, same "free text, no fixed
        taxonomy yet" posture ai.journal.failure_analysis.FailureAnalysisEntry's
        own `reason` field already established.
    target: what the action applied to (e.g. "BITGET", "ENABLE_AI"),
        optional -- some actions (e.g. a bare "/panic all") have no
        single target.
    result: "SUCCESS" or "FAILURE" by convention, not enforced as an
        enum -- a free string, same reasoning as `action`.
    details: optional free-text context (e.g. "Old: TwelveData / New:
        Bitget / Reason: manual switch", matching this task's own
        worked example) -- this module does not structure or parse it.
    created_at: when this entry was recorded.
    """
    actor: str
    action: str
    target: Optional[str] = None
    result: str = "SUCCESS"
    details: Optional[str] = None
    created_at: Optional[datetime] = None


def create_audit_log_entry(
    actor: str,
    action: str,
    target: Optional[str] = None,
    result: str = "SUCCESS",
    details: Optional[str] = None,
) -> AuditLogEntry:
    """Pure, deterministic factory -- stamps created_at, same convention as every other create_X() factory in this codebase."""
    return AuditLogEntry(
        actor=actor,
        action=action,
        target=target,
        result=result,
        details=details,
        created_at=datetime.now(timezone.utc),
    )
