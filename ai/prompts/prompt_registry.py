"""
AI Layer — Prompt Registry (Phase 61.1: AI Provider Reliability
Foundation, TASK 5; extended Phase 61.1.1: AI Foundation Corrections,
TASK 3).

Extends `ai/prompts/` with version/active/rollback bookkeeping over
named prompts (e.g. "market_analysis" v1/v2/v3) -- `PromptManager`
itself is not replaced or renamed; its existing methods
(`get_market_analysis_prompt()`, etc.) stay exactly as they are. This
registry only tracks *which version is active* for a given prompt
name; a future phase is where `PromptManager` would consult it to
decide which template text to build (not wired this phase, matching
every other "foundation, not yet live-wired" module in this
codebase).

Phase 61.1.1 TASK 3 adds `PromptLifecycleState` (ACTIVE/DEPRECATED/
ARCHIVED) as a field on `PromptVersionRecord`. A version defaults to
ACTIVE when registered -- fully backward compatible with every Phase
61.1 caller, none of which ever exercised a non-default state.
`set_active()` and `rollback()` both now refuse to make a
DEPRECATED or ARCHIVED version the active one: a deprecated/archived
version stays visible via `list_versions()` (history is never
deleted) but can never again become the selected version through
either path.
"""

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from core_layer.logger.logger import setup_logger

logger = setup_logger("PromptRegistry")


class PromptLifecycleState(Enum):
    """
    ACTIVE: normal, selectable state -- the default for every newly
        registered version.
    DEPRECATED: still exists, still listed, but `set_active()`/
        `rollback()` refuse to select it -- "Tanlanmaydi. Lekin
        mavjud."
    ARCHIVED: history only -- "Runtime ishlatmaydi." Same selection
        refusal as DEPRECATED; kept as a distinct value rather than
        reusing DEPRECATED so a caller inspecting `list_versions()`
        can tell "retired on purpose" apart from "actively being
        phased out."
    """
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


# States set_active()/rollback() may select. Never DEPRECATED/ARCHIVED.
_SELECTABLE_STATES = frozenset({PromptLifecycleState.ACTIVE})


@dataclass(frozen=True)
class PromptVersionRecord:
    prompt_name: str
    version: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: Optional[datetime] = None
    state: PromptLifecycleState = PromptLifecycleState.ACTIVE


class PromptRegistry:
    """In-memory only, like every other Phase 61.0/61.1 foundation module -- no persistence."""

    def __init__(self) -> None:
        self._versions: Dict[str, List[PromptVersionRecord]] = {}
        self._active: Dict[str, str] = {}

    def register(self, prompt_name: str, version: str, metadata: Optional[Dict[str, Any]] = None) -> PromptVersionRecord:
        """The first version ever registered for a `prompt_name` becomes active automatically -- a caller registering only one version needs no separate `set_active()` call. Always registered ACTIVE -- use `deprecate()`/`archive()` to change state afterward."""
        record = PromptVersionRecord(
            prompt_name=prompt_name, version=version, metadata=metadata or {},
            registered_at=datetime.now(timezone.utc),
        )
        self._versions.setdefault(prompt_name, []).append(record)
        if prompt_name not in self._active:
            self._active[prompt_name] = version
        logger.info(f"Prompt version registered: prompt={prompt_name} version={version}")
        return record

    def _record_of(self, prompt_name: str, version: str) -> Optional[PromptVersionRecord]:
        return next((r for r in self._versions.get(prompt_name, []) if r.version == version), None)

    def _set_state(self, prompt_name: str, version: str, state: PromptLifecycleState) -> bool:
        versions = self._versions.get(prompt_name, [])
        index = next((i for i, r in enumerate(versions) if r.version == version), None)
        if index is None:
            logger.warning(f"{state.value} rejected: {prompt_name} has no registered version {version}")
            return False
        versions[index] = replace(versions[index], state=state)
        logger.info(f"Prompt version {state.value.lower()}: prompt={prompt_name} version={version}")
        return True

    def deprecate(self, prompt_name: str, version: str) -> bool:
        """Never raises: returns False if `version` was never registered. Does not change which version is currently active -- only affects future set_active()/rollback() selection."""
        return self._set_state(prompt_name, version, PromptLifecycleState.DEPRECATED)

    def archive(self, prompt_name: str, version: str) -> bool:
        return self._set_state(prompt_name, version, PromptLifecycleState.ARCHIVED)

    def state_of(self, prompt_name: str, version: str) -> Optional[PromptLifecycleState]:
        record = self._record_of(prompt_name, version)
        return record.state if record else None

    def set_active(self, prompt_name: str, version: str) -> bool:
        """Returns False and leaves state unchanged if `version` was never registered for `prompt_name`, or if it is DEPRECATED/ARCHIVED -- never raises, never silently activates an unknown or retired version."""
        record = self._record_of(prompt_name, version)
        if record is None:
            logger.warning(f"set_active rejected: {prompt_name} has no registered version {version}")
            return False
        if record.state not in _SELECTABLE_STATES:
            logger.warning(f"set_active rejected: {prompt_name} version {version} is {record.state.value}")
            return False
        self._active[prompt_name] = version
        logger.info(f"Prompt active version set: prompt={prompt_name} version={version}")
        return True

    def active_version(self, prompt_name: str) -> Optional[str]:
        return self._active.get(prompt_name)

    def rollback(self, prompt_name: str) -> Optional[str]:
        """Moves the active pointer to the version immediately before the current active one, in registration order. Returns the new active version, or None if there is nothing earlier to roll back to (no versions registered, the active version is already the first one), or if that earlier version is DEPRECATED/ARCHIVED -- a deprecated/archived version is never selected by rollback() either, even though it still exists in `list_versions()`."""
        versions = self._versions.get(prompt_name, [])
        current = self._active.get(prompt_name)
        if not versions or current is None:
            return None

        index = next((i for i, r in enumerate(versions) if r.version == current), None)
        if index is None or index == 0:
            return None

        previous_record = versions[index - 1]
        if previous_record.state not in _SELECTABLE_STATES:
            logger.warning(
                f"rollback rejected: {prompt_name} previous version {previous_record.version} is {previous_record.state.value}"
            )
            return None

        self._active[prompt_name] = previous_record.version
        logger.info(f"Prompt rolled back: prompt={prompt_name} version={previous_record.version}")
        return previous_record.version

    def list_versions(self, prompt_name: str) -> List[PromptVersionRecord]:
        return list(self._versions.get(prompt_name, []))
