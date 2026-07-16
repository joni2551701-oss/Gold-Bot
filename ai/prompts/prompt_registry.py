"""
AI Layer — Prompt Registry (Phase 61.1: AI Provider Reliability
Foundation, TASK 5).

Extends `ai/prompts/` with version/active/rollback bookkeeping over
named prompts (e.g. "market_analysis" v1/v2/v3) -- `PromptManager`
itself is not replaced or renamed; its existing methods
(`get_market_analysis_prompt()`, etc.) stay exactly as they are. This
registry only tracks *which version is active* for a given prompt
name; a future phase is where `PromptManager` would consult it to
decide which template text to build (not wired this phase, matching
every other "foundation, not yet live-wired" module in this
codebase).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core.logger import setup_logger

logger = setup_logger("PromptRegistry")


@dataclass(frozen=True)
class PromptVersionRecord:
    prompt_name: str
    version: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: Optional[datetime] = None


class PromptRegistry:
    """In-memory only, like every other Phase 61.0/61.1 foundation module -- no persistence."""

    def __init__(self) -> None:
        self._versions: Dict[str, List[PromptVersionRecord]] = {}
        self._active: Dict[str, str] = {}

    def register(self, prompt_name: str, version: str, metadata: Optional[Dict[str, Any]] = None) -> PromptVersionRecord:
        """The first version ever registered for a `prompt_name` becomes active automatically -- a caller registering only one version needs no separate `set_active()` call."""
        record = PromptVersionRecord(
            prompt_name=prompt_name, version=version, metadata=metadata or {},
            registered_at=datetime.now(timezone.utc),
        )
        self._versions.setdefault(prompt_name, []).append(record)
        if prompt_name not in self._active:
            self._active[prompt_name] = version
        logger.info(f"Prompt version registered: prompt={prompt_name} version={version}")
        return record

    def set_active(self, prompt_name: str, version: str) -> bool:
        """Returns False and leaves state unchanged if `version` was never registered for `prompt_name` -- never raises, never silently activates an unknown version."""
        if not any(r.version == version for r in self._versions.get(prompt_name, [])):
            logger.warning(f"set_active rejected: {prompt_name} has no registered version {version}")
            return False
        self._active[prompt_name] = version
        logger.info(f"Prompt active version set: prompt={prompt_name} version={version}")
        return True

    def active_version(self, prompt_name: str) -> Optional[str]:
        return self._active.get(prompt_name)

    def rollback(self, prompt_name: str) -> Optional[str]:
        """Moves the active pointer to the version immediately before the current active one, in registration order. Returns the new active version, or None if there is nothing earlier to roll back to (no versions registered, or the active version is already the first one)."""
        versions = self._versions.get(prompt_name, [])
        current = self._active.get(prompt_name)
        if not versions or current is None:
            return None

        index = next((i for i, r in enumerate(versions) if r.version == current), None)
        if index is None or index == 0:
            return None

        previous_version = versions[index - 1].version
        self._active[prompt_name] = previous_version
        logger.info(f"Prompt rolled back: prompt={prompt_name} version={previous_version}")
        return previous_version

    def list_versions(self, prompt_name: str) -> List[PromptVersionRecord]:
        return list(self._versions.get(prompt_name, []))
