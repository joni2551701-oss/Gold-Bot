"""
Database Layer — Runtime Feature persistence model (Phase 59.7:
Runtime Feature Toggle Center, TASK 3).

Mirrors database_layer/market_repository/sync_state_models.py's own shape (a single, upserted
row per key). One row per feature name -- the persisted counterpart to
configuration.runtime_state.FeatureRuntimeState (same field meaning:
enabled, updated_at, updated_by, reason), so an owner's toggle
survives a process restart.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class RuntimeFeatureRecord:
    """
    Mirrors the 'runtime_features' table row shape. `id` is
    intentionally excluded -- repository-internal detail, same
    convention as every other Phase 59.x model.
    created_at: when this feature was first toggled (first INSERT).
        RuntimeFeatureRepository.set_feature() preserves this across
        every later UPDATE -- only `enabled`/`updated_at`/`updated_by`/
        `reason` change on a re-toggle, never `created_at`.
    """
    feature: str
    enabled: bool
    updated_at: datetime
    created_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    reason: Optional[str] = None


def create_runtime_feature_record(
    feature: str,
    enabled: bool,
    updated_by: Optional[str] = None,
    reason: Optional[str] = None,
) -> RuntimeFeatureRecord:
    """Pure, deterministic factory -- stamps both created_at and updated_at to the same 'now' (a brand-new record's first and only timestamp so far), same convention as every other create_X() factory in this codebase."""
    now = datetime.now(timezone.utc)
    return RuntimeFeatureRecord(
        feature=feature,
        enabled=enabled,
        updated_at=now,
        created_at=now,
        updated_by=updated_by,
        reason=reason,
    )
