"""
Database Layer — Configuration Snapshot persistence model (Phase 59.6:
Audit & Observability Foundation, TASK 6).

Captures a point-in-time copy of a feature registry
(configuration/feature_registry.py's build_feature_registry(), same
phase) for a future rollback -- "Har owner o'zgartirishidan oldin
config_snapshot saqlanadi. Rollback uchun." per this task's own brief.
This module and its repository only capture and read snapshots; no
apply/restore function exists in this phase -- actually rolling a
configuration back to a saved snapshot is a future, separately-
approved step (it would need to decide how a "declared-only" feature
becomes toggleable at all, which this phase does not attempt). No
owner command calls create_config_snapshot() automatically yet.
"""

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from configuration.feature_registry import FeatureDescriptor


@dataclass(frozen=True)
class ConfigSnapshotRecord:
    """
    Mirrors the 'config_snapshots' table row shape. `id` is
    intentionally excluded -- repository-internal detail, same
    convention as every other Phase 59.x model in this codebase.
    feature_state: a JSON object string of {feature_name: enabled} --
        the same shape json.loads() reverses directly into a plain
        dict; kept as a string here (not parsed back into
        List[FeatureDescriptor]) since a snapshot only needs to
        remember each name's enabled/disabled value, not the full
        descriptor (implemented/source/description are static facts
        about the registry itself, not something that changes between
        snapshots).
    taken_by/reason: optional free text, same "no fixed taxonomy yet"
        posture every other Phase 59.6 model already uses.
    """
    snapshot_id: str
    feature_state: str
    taken_at: datetime
    taken_by: Optional[str] = None
    reason: Optional[str] = None

    def feature_state_dict(self) -> Dict[str, bool]:
        """Parses `feature_state` back into a plain {name: enabled} dict -- the inverse of create_config_snapshot()'s own json.dumps() call."""
        return json.loads(self.feature_state)


def create_config_snapshot(
    registry: Sequence['FeatureDescriptor'],
    taken_by: Optional[str] = None,
    reason: Optional[str] = None,
) -> ConfigSnapshotRecord:
    """Generates snapshot_id (str(uuid.uuid4()), same convention as analytics.signal_performance.generate_performance_id()), stamps taken_at, and serializes `registry` into {name: enabled} JSON."""
    feature_state = json.dumps({entry.name: entry.enabled for entry in registry})
    return ConfigSnapshotRecord(
        snapshot_id=str(uuid.uuid4()),
        feature_state=feature_state,
        taken_at=datetime.now(timezone.utc),
        taken_by=taken_by,
        reason=reason,
    )
