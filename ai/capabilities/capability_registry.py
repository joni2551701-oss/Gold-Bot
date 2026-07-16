"""
AI Layer — Capability Registry (Phase 61.0: AI Infrastructure
Foundation, TASK 2).

Same *shape* as `configuration/feature_registry.py`'s
`FeatureDescriptor` + `build_feature_registry()` (a descriptor
dataclass plus a registry-building function), deliberately not the
same *instance* or *namespace* -- `docs/PHASE61_AI_FOUNDATION_AUDIT.md`
TASK 1 found that registry is Infrastructure-only as of Phase 60.9 and
reusing it for an AI-behavior concern would repeat the exact coupling
Phase 60.9 was created to remove. This registry lives entirely inside
`ai/` and is never read by `configuration/` or
`core/guards/pipeline_guard.py`.

In-memory only, like every other Phase 61.0 module -- no persistence,
no database integration.
"""

from dataclasses import dataclass

from ai.capabilities.capability import Capability

# Default enablement: the six capabilities the Phase 61.0 brief lists
# as this phase's near-term focus (CHAT/ANALYSIS/EXPLANATION/SUMMARY/
# MEMORY/EDUCATION) default to enabled=True; the remaining six
# (TOOL_CALLING/VISION/IMAGE/VIDEO/VOICE/DOCUMENT) default to
# enabled=False -- declared now for a stable name every future phase
# can reference, matching `configuration/feature_registry.py`'s own
# "declared, not yet real" convention for not-yet-built features.
_DEFAULT_ENABLED = frozenset({
    Capability.CHAT,
    Capability.ANALYSIS,
    Capability.EXPLANATION,
    Capability.SUMMARY,
    Capability.MEMORY,
    Capability.EDUCATION,
})


@dataclass(frozen=True)
class CapabilityDescriptor:
    """
    capability: the stable enum identity.
    enabled: this registry's own default state -- a static description,
        not the live, toggle-aware state `CapabilityManager` (TASK 2's
        other module) tracks. A caller wanting current runtime state
        uses `CapabilityManager`, not this registry, directly.
    description: human-readable note.
    """
    capability: Capability
    enabled: bool
    description: str = ""


def build_capability_registry() -> list:
    """Never raises: pure, static construction from `Capability`'s own fixed enum values."""
    return [
        CapabilityDescriptor(
            capability=capability,
            enabled=capability in _DEFAULT_ENABLED,
            description=f"{capability.value} -- advisory AI capability (Phase 61.0 foundation).",
        )
        for capability in Capability
    ]
