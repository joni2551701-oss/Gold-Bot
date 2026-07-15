"""
Configuration Layer — Runtime State Cache (Phase 59.7: Runtime Feature
Toggle Center, TASK 2).

FeatureRuntimeState is one feature's current, in-memory, runtime
value -- distinct from configuration.feature_registry.FeatureDescriptor
(a snapshot of a feature's *static* backing source, e.g.
config.Config.ENABLE_MT5's os.getenv-read value at process start).
FeatureRuntimeState is what an owner has actually toggled at runtime,
held in RuntimeStateCache (this module) and persisted by
database/runtime_feature_repository.py (TASK 3) -- neither of which
this module touches directly; RuntimeStateCache is a plain in-memory
dict wrapper, no I/O.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass(frozen=True)
class FeatureRuntimeState:
    """
    One feature's current runtime value. `enabled`/`disabled` in the
    Director's own brief are the two sides of one boolean -- modeled
    here as a single `enabled: bool` (mirroring
    configuration.feature_registry.FeatureDescriptor's own field name)
    rather than two separate, potentially-inconsistent booleans.
    last_changed/changed_by/reason: same "free text, no fixed
    taxonomy" posture every other Phase 59.x audit-adjacent model
    already uses.
    source: "default" when this state came only from
        configuration.feature_registry.build_feature_registry()'s own
        static value (never toggled at runtime), or "runtime" once a
        database/runtime_feature_repository.py row exists for this
        name (an owner has toggled it at least once, whether or not
        the current value still matches the static default).
    created_at: when this feature was first toggled at runtime --
        None for a "default"-source state (nothing has ever been
        persisted for it yet). Mirrors
        database.runtime_feature_models.RuntimeFeatureRecord.created_at.
    """
    name: str
    enabled: bool
    last_changed: datetime
    changed_by: Optional[str] = None
    reason: Optional[str] = None
    source: str = "default"
    created_at: Optional[datetime] = None


def create_feature_runtime_state(
    name: str,
    enabled: bool,
    changed_by: Optional[str] = None,
    reason: Optional[str] = None,
    source: str = "default",
    created_at: Optional[datetime] = None,
) -> FeatureRuntimeState:
    """Pure, deterministic factory -- stamps last_changed, same convention as every other create_X() factory in this codebase."""
    return FeatureRuntimeState(
        name=name,
        enabled=enabled,
        last_changed=datetime.now(timezone.utc),
        changed_by=changed_by,
        reason=reason,
        source=source,
        created_at=created_at,
    )


class RuntimeStateCache:
    """
    A plain in-memory {name: FeatureRuntimeState} holder -- no
    database access, no dependency validation, no audit logging (those
    are configuration/runtime_feature_manager.py's job, same phase,
    TASK 1). One process-local cache instance per
    RuntimeFeatureManager; never a module-level singleton, so tests
    (and, in the future, multiple independent managers) never share
    state by accident.
    """

    def __init__(self):
        self._states: Dict[str, FeatureRuntimeState] = {}

    def get(self, name: str) -> Optional[FeatureRuntimeState]:
        """Returns None for a name never set -- never raises for a lookup miss, matching this codebase's established convention."""
        return self._states.get(name)

    def set(self, state: FeatureRuntimeState) -> None:
        self._states[state.name] = state

    def all(self) -> List[FeatureRuntimeState]:
        return list(self._states.values())

    def is_enabled(self, name: str, default: bool = False) -> bool:
        """`default` is returned for a name with no cached state yet -- never raises."""
        state = self.get(name)
        return state.enabled if state is not None else default

    def clear(self) -> None:
        """Empties the cache -- used by RuntimeFeatureManager.reload() before re-populating from the database, so a stale in-memory entry never survives a reload."""
        self._states.clear()
