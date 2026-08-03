"""
Configuration Layer — Runtime Feature Manager (Phase 59.7: Runtime
Feature Toggle Center, TASK 1/4/5/6/7/8).

Turns the Phase 59.6 configuration foundation into an actual runtime
controller -- an owner (once a future Phase 59.8 Owner Dashboard wires
a command to it) can enable/disable a named feature without a bot
restart, with the change validated, persisted, audited, and
snapshotted. This phase does not touch core/pipeline.py, any Telegram
handler, or telegram/command_router.py -- RuntimeFeatureManager is
only ever constructed and called directly (e.g. from a test, or a
future Owner Dashboard service function), never from the live
pipeline or bot routing.

Composes, rather than reimplements, every relevant Phase 59.5/59.6
foundation piece:
    configuration.feature_registry.build_feature_registry()   -- static defaults (TASK 4)
    configuration.runtime_state.RuntimeStateCache              -- in-memory holder (TASK 2)
    database.runtime_feature_repository.RuntimeFeatureRepository -- persistence (TASK 3)
    configuration.feature_dependency_validator.validate_feature_dependencies() -- dry run (TASK 5/6)
    database.audit_log_repository.AuditLogRepository            -- audit trail (TASK 7)
    database.config_snapshot_repository.ConfigSnapshotRepository -- rollback capture (TASK 8)

Method naming: enable()/disable()/status() are this module's own
primary names (no "_feature" stutter on a method that already lives on
a *FeatureManager*). enable_feature()/disable_feature()/
get_feature_state()/validate_dependencies() are thin, additive aliases
matching the Director's own resume-brief literal API surface --
delegating to the primary methods, not a second implementation.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional

from core_layer.configuration.feature_dependency_validator import (
    DEPENDENCY_RULES,
    DependencyValidationResult,
    format_dependency_violations,
    validate_feature_dependencies,
)
from core_layer.configuration.feature_registry import FeatureDescriptor, build_feature_registry
from core_layer.configuration.runtime_state import FeatureRuntimeState, RuntimeStateCache
from database_layer.audit_log.audit_log_repository import AuditLogRepository
from database_layer.journal_repository.config_snapshot_repository import ConfigSnapshotRepository
from database_layer.journal_repository.config_snapshot_models import create_config_snapshot
from database_layer.journal_repository.runtime_feature_repository import RuntimeFeatureRepository
from core_layer.logger.logger import setup_logger

logger = setup_logger("RuntimeFeatureManager")


@dataclass(frozen=True)
class ToggleResult:
    """
    success: False for a dry-run rejection (TASK 6) -- the underlying
        state is left completely unchanged (no persistence write, no
        cache mutation, no audit "SUCCESS" entry) when this is False.
        A rejected attempt still writes one audit entry with
        result="REJECTED" (TASK 7) so the attempt itself is not
        silently lost.
    reason: a human-readable rejection explanation, or the
        caller-supplied `reason` for a successful toggle.
    """
    success: bool
    feature: str
    enabled: bool
    reason: Optional[str] = None


def _dependents_requiring(name: str, enabled_names: set) -> List[str]:
    """Every feature in DEPENDENCY_RULES that (a) currently-enabled and (b) lists `name` among its own required dependencies -- i.e. who would break if `name` were disabled right now."""
    return sorted(
        feature for feature, required in DEPENDENCY_RULES.items()
        if feature in enabled_names and name in required
    )


class RuntimeFeatureManager:
    """
    One process-local manager -- own RuntimeStateCache, own repository
    instances (each injectable, same optional-dependency convention as
    TwelveDataProvider's own `client` parameter). Auto-loads on
    construction (`load()` called from `__init__`) -- "Bot ishga
    tushganda ... Auto load" per this task's own brief, scoped to this
    manager's own construction rather than to core/pipeline.py or
    main.py (neither of which constructs a RuntimeFeatureManager in
    this phase).
    """

    def __init__(
        self,
        runtime_feature_repository: Optional[RuntimeFeatureRepository] = None,
        audit_log_repository: Optional[AuditLogRepository] = None,
        config_snapshot_repository: Optional[ConfigSnapshotRepository] = None,
    ):
        self.repository = runtime_feature_repository or RuntimeFeatureRepository()
        self.audit_log_repository = audit_log_repository or AuditLogRepository()
        self.config_snapshot_repository = config_snapshot_repository or ConfigSnapshotRepository()
        self.cache = RuntimeStateCache()
        self.load()

    def load(self) -> None:
        """
        TASK 4 (Feature Loader): clears the cache, seeds it from
        configuration.feature_registry.build_feature_registry()'s own
        static `enabled` value per name (source="default"), then
        overlays any persisted
        database.runtime_feature_repository.RuntimeFeatureRepository
        row on top (source="runtime") -- a feature an owner has never
        toggled keeps its static default; one that was toggled and
        persisted (including across a restart -- a fresh
        RuntimeFeatureManager backed by the same repository reads the
        same state back) wins.
        """
        self.cache.clear()

        for descriptor in build_feature_registry():
            self.cache.set(FeatureRuntimeState(
                name=descriptor.name, enabled=descriptor.enabled,
                last_changed=datetime.now(timezone.utc), source="default",
            ))

        for record in self.repository.get_all_features():
            self.cache.set(FeatureRuntimeState(
                name=record.feature, enabled=record.enabled, last_changed=record.updated_at,
                changed_by=record.updated_by, reason=record.reason,
                source="runtime", created_at=record.created_at,
            ))

    def reload(self) -> None:
        """Re-reads from the database, discarding any purely in-memory value -- the same operation as load(), named separately per this task's own brief."""
        self.load()

    def status(self, name: str) -> Optional[FeatureRuntimeState]:
        """The current cached runtime state for `name`, or None if it has never been seen (not in the registry and never toggled)."""
        return self.cache.get(name)

    def get_feature_state(self, name: str) -> Optional[Dict]:
        """
        Alias/view over status() returning the plain-dict shape this
        task's own brief names:

            {"feature": "ENABLE_TWELVEDATA", "state": "ACTIVE",
             "source": "runtime", "updated_at": "..."}

        None for a name never seen (same as status()).
        """
        state = self.status(name)
        if state is None:
            return None
        return {
            "feature": state.name,
            "state": "ACTIVE" if state.enabled else "INACTIVE",
            "source": state.source,
            "updated_at": state.last_changed.isoformat(),
        }

    def list_features(self) -> List[FeatureRuntimeState]:
        """Every feature currently known to this manager (registry-declared or persisted-only), in no particular order."""
        return self.cache.all()

    def _dry_run(self, name: str, new_enabled: bool) -> DependencyValidationResult:
        """
        TASK 5/6: builds a hypothetical {name: enabled} snapshot -- the
        current cache with `name` set to `new_enabled` -- and runs
        configuration.feature_dependency_validator.validate_feature_dependencies()
        against it. `implemented`/`source` on the constructed
        FeatureDescriptor entries are placeholders (the validator only
        reads `.name`/`.enabled`, see feature_dependency_validator.py's
        own DEPENDENCY_RULES contract) -- this is purely a dependency
        check, not a re-derivation of each feature's real backing
        source.
        """
        hypothetical_state = {state.name: state.enabled for state in self.cache.all()}
        hypothetical_state[name] = new_enabled
        hypothetical_registry = [
            FeatureDescriptor(name=n, enabled=enabled, implemented=True, source="runtime")
            for n, enabled in hypothetical_state.items()
        ]
        return validate_feature_dependencies(hypothetical_registry, rules=DEPENDENCY_RULES)

    def validate_dependencies(
        self, name: Optional[str] = None, new_enabled: Optional[bool] = None
    ) -> DependencyValidationResult:
        """
        Public entry point for TASK 6's dry run. With `name` (and
        optionally `new_enabled`, defaulting to that feature's current
        cached value -- i.e. "would this feature's current state still
        be valid"), validates the hypothetical post-toggle state via
        _dry_run(). With no arguments, validates the manager's current
        *actual* cached state as-is (no hypothetical change) -- useful
        for a future "is everything currently consistent" health
        check.
        """
        if name is None:
            current_registry = [
                FeatureDescriptor(name=state.name, enabled=state.enabled, implemented=True, source="runtime")
                for state in self.cache.all()
            ]
            return validate_feature_dependencies(current_registry, rules=DEPENDENCY_RULES)

        if new_enabled is None:
            new_enabled = self.cache.is_enabled(name, default=False)
        return self._dry_run(name, new_enabled)

    def _rejection_reason(self, name: str, new_enabled: bool, validation: DependencyValidationResult) -> str:
        """
        TASK 6's own worked example ("Cannot disable ENABLE_AI.
        Dependent features active: AI_EXPLANATION") gets this
        specific, friendlier phrasing when the rejection is a disable
        blocked by an active dependent. An enable rejected for its own
        unmet dependency keeps the existing
        format_dependency_violations() phrasing ("X requires Y") --
        the two rejection directions read differently on purpose:
        disabling names WHO is still relying on you, enabling names
        WHAT you still need.
        """
        if not new_enabled:
            enabled_names = {state.name for state in self.cache.all() if state.enabled}
            dependents = _dependents_requiring(name, enabled_names)
            if dependents:
                return f"Cannot disable {name}. Dependent features active: {', '.join(dependents)}"
        return format_dependency_violations(validation)

    def _apply_toggle(self, name: str, new_enabled: bool, changed_by: Optional[str], reason: Optional[str]) -> ToggleResult:
        validation = self._dry_run(name, new_enabled)

        if not validation.valid:
            violation_text = self._rejection_reason(name, new_enabled, validation)
            self.audit_log_repository.log_action(
                actor=changed_by or "unknown", action="TOGGLE_FEATURE", target=name,
                result="REJECTED", details=violation_text,
            )
            logger.warning(f"Runtime toggle rejected: {name} -> {new_enabled} ({violation_text})")
            return ToggleResult(success=False, feature=name, enabled=new_enabled, reason=violation_text)

        record = self.repository.set_feature(name, new_enabled, updated_by=changed_by, reason=reason)
        self.cache.set(FeatureRuntimeState(
            name=name, enabled=new_enabled, last_changed=record.updated_at,
            changed_by=changed_by, reason=reason, source="runtime", created_at=record.created_at,
        ))

        self.audit_log_repository.log_action(
            actor=changed_by or "unknown",
            action="FEATURE_ENABLED" if new_enabled else "FEATURE_DISABLED",
            target=name, result="SUCCESS", details=reason,
        )

        snapshot_registry = [
            FeatureDescriptor(name=state.name, enabled=state.enabled, implemented=True, source="runtime")
            for state in self.cache.all()
        ]
        snapshot = create_config_snapshot(
            snapshot_registry, taken_by=changed_by, reason=f"feature toggle: {name} -> {new_enabled}",
        )
        self.config_snapshot_repository.save_snapshot(snapshot)

        return ToggleResult(success=True, feature=name, enabled=new_enabled, reason=reason)

    def enable(self, name: str, changed_by: Optional[str] = None, reason: Optional[str] = None) -> ToggleResult:
        return self._apply_toggle(name, True, changed_by, reason)

    def disable(self, name: str, changed_by: Optional[str] = None, reason: Optional[str] = None) -> ToggleResult:
        return self._apply_toggle(name, False, changed_by, reason)

    def toggle(self, name: str, changed_by: Optional[str] = None, reason: Optional[str] = None) -> ToggleResult:
        """Flips whatever the feature's current cached value is (False if never seen before) -- see RuntimeStateCache.is_enabled()'s own default-on-miss behavior."""
        current = self.cache.is_enabled(name, default=False)
        return self._apply_toggle(name, not current, changed_by, reason)

    # --- Aliases matching the Director's literal Phase 59.7 resume-brief API surface ---

    def enable_feature(self, name: str, changed_by: Optional[str] = None, reason: Optional[str] = None) -> ToggleResult:
        """Alias for enable() -- see class/module docstring on why both names exist."""
        return self.enable(name, changed_by=changed_by, reason=reason)

    def disable_feature(self, name: str, changed_by: Optional[str] = None, reason: Optional[str] = None) -> ToggleResult:
        """Alias for disable() -- see class/module docstring on why both names exist."""
        return self.disable(name, changed_by=changed_by, reason=reason)
