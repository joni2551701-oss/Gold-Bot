"""
Configuration Layer — Feature Registry (Phase 59.6: Audit &
Observability Foundation, TASK 4; separated from Trading concerns in
Phase 60.9: Runtime Registry Separation).

One structured catalog of every feature name this codebase knows
about -- real, backed flags and reserved, declared-only names alike --
matching this task's own brief ("Barcha feature bitta registry'da").
Not runtime: build_feature_registry() only *reads* already-computed
values (config.Config's module-level constants,
configuration.feature_flags.DEFAULT_FLAGS) and reports declared-only
names as a fixed, safe False -- it does not gate, enable, or disable
anything, and nothing in core/pipeline.py, decision/, risk/, or
execution/ reads this module.

**Infrastructure only, as of Phase 60.9** (see
docs/FEATURE_REGISTRY_SEPARATION.md for the full audit): every name in
this registry is a provider/data-source/observation-mode/reserved
concern, never a live-trading-pipeline stage gate. Phase 60.8 briefly
added three Trading-pipeline gates here (ENABLE_SIGNALS/ENABLE_AI/
ENABLE_DATABASE) and found a fourth (ENABLE_EXECUTION) collided with
configuration/feature_dependency_validator.py's own dependency rules;
this phase removes all four (plus the already-declared-only
ENABLE_RISK/ENABLE_DECISION) from this registry entirely --
core_layer/pipeline/pipeline_guard.py's PipelineGuard now reads exclusively
from core_layer.emergency.emergency_manager.EmergencyManager for every
pipeline-stage decision, never from this module.

Relationship to platform_layer/telegram/owner/feature_commands.py's list_features()
(Phase 59.3, TASK 5, unmodified by this phase): that function already
reads the same two real sources (Config, DEFAULT_FLAGS) and renders
them as ad-hoc text for a future /features command. This module is the
structured data layer underneath that same idea, extended with the
declared-only names this task's own brief lists -- a data model a
future report/command can build on, not a replacement for or a change
to list_features()'s own tested output.

Two kinds of entry:
- implemented=True: a real flag with a real backing source
  (config.Config's os.getenv()-read constants, or
  configuration.feature_flags.FeatureFlags' dataclass fields) --
  `enabled` reflects that source's actual current value.
- implemented=False: a name this task's own brief lists that has no
  real backing anywhere in this codebase yet (no os.getenv call, no
  dataclass field) -- `enabled` is always a fixed, safe False, the
  same "a flag existing here does not mean the feature exists"
  posture configuration/feature_flags.py's own docstring already
  established for enable_ai/enable_crypto/enable_swing. Declaring
  these names now gives
  configuration/feature_dependency_validator.py (same phase, TASK 5)
  stable names to reference -- it does not create a new environment
  variable or any other real switch.
"""

from dataclasses import dataclass
from typing import List

from config import Config
from core_layer.configuration.feature_flags import DEFAULT_FLAGS

# Names this task's own brief lists that have no real backing anywhere
# in this codebase today. Always False, always "declared" -- see
# module docstring. Deliberately does NOT include "ENABLE_BACKTEST" as
# a synonym for FeatureFlags.enable_replay (a real, already-named
# field, Phase A13) -- the two are kept as distinct registry entries
# rather than silently aliased.
#
# Phase 60.9 (Runtime Registry Separation): "ENABLE_EXECUTION",
# "ENABLE_RISK", "ENABLE_DECISION" were removed from this tuple
# entirely -- all three are Trading-pipeline concerns (see
# docs/FEATURE_REGISTRY_SEPARATION.md's audit table), not
# Infrastructure, and do not belong in this registry's namespace even
# as safe, always-False placeholders. This is the root-cause fix for
# the Phase 60.8 finding: ENABLE_EXECUTION's mere presence here (even
# declared-only) kept configuration/feature_dependency_validator.py's
# DEPENDENCY_RULES anchored to a Trading name, which is exactly the
# coupling this phase removes.
_DECLARED_ONLY_FEATURES = (
    "ENABLE_NEWS",
    "ENABLE_PAPER",
    "ENABLE_BACKTEST",
    "ENABLE_ANALYTICS",
    "ENABLE_OWNER",
    "ENABLE_DATASET_SYNC",
    "ENABLE_MARKET_PHASE",
    "ENABLE_BITGET",
    "ENABLE_BINANCE",
    "ENABLE_FRED",
)


@dataclass(frozen=True)
class FeatureDescriptor:
    """
    name: a stable, unique identifier within one registry (e.g.
        "ENABLE_MT5", "enable_ai", "ENABLE_NEWS") -- deliberately not
        normalized to one casing, since it echoes each source's own
        real name (config.Config's SCREAMING_CASE vs
        FeatureFlags' snake_case dataclass fields) rather than
        inventing a third convention.
    enabled: the flag's current value -- always False for a
        declared-only (implemented=False) entry.
    implemented: whether a real backing source exists (see module
        docstring).
    source: where this entry's value comes from, e.g.
        "config.Config", "configuration.feature_flags.FeatureFlags",
        or "declared" for a not-yet-backed name.
    description: optional human-readable note.
    """
    name: str
    enabled: bool
    implemented: bool
    source: str
    description: str = ""


def build_feature_registry() -> List[FeatureDescriptor]:
    """Never raises: every source read here is either a plain module-level constant or an already-constructed dataclass instance, no I/O."""
    entries = [
        FeatureDescriptor(
            name="ENABLE_MT5", enabled=Config.ENABLE_MT5, implemented=True,
            source="config.Config", description="MT5 provider gate (Phase 59.1) -- MT5Provider itself stays an inert stub regardless.",
        ),
        FeatureDescriptor(
            name="ENABLE_TWELVEDATA", enabled=Config.ENABLE_TWELVEDATA, implemented=True,
            source="config.Config", description="TwelveData provider gate (Phase 59.1) -- the only real, live market data source today.",
        ),
        FeatureDescriptor(
            name="VALIDATION_MODE", enabled=Config.VALIDATION_MODE, implemented=True,
            source="config.Config", description="Phase 59 Real Market Validation Foundation's own observation flag -- not read by core/pipeline.py.",
        ),
        FeatureDescriptor(
            name="enable_ai", enabled=DEFAULT_FLAGS.enable_ai, implemented=True,
            source="configuration.feature_flags.FeatureFlags", description="Reserved (Phase A13) -- ai/ai_analyzer.py stays a heuristic stub regardless.",
        ),
        FeatureDescriptor(
            name="enable_crypto", enabled=DEFAULT_FLAGS.enable_crypto, implemented=True,
            source="configuration.feature_flags.FeatureFlags", description="Reserved (Phase A13) -- no Crypto AssetType profile exists.",
        ),
        FeatureDescriptor(
            name="enable_swing", enabled=DEFAULT_FLAGS.enable_swing, implemented=True,
            source="configuration.feature_flags.FeatureFlags", description="Reserved (Phase A13) -- no swing-timeframe strategy exists.",
        ),
        FeatureDescriptor(
            name="enable_ai_memory", enabled=DEFAULT_FLAGS.enable_ai_memory, implemented=True,
            source="configuration.feature_flags.FeatureFlags", description="Reserved (Phase A13) -- ai/journal/trade_journal.py exists independently of this flag.",
        ),
        FeatureDescriptor(
            name="enable_replay", enabled=DEFAULT_FLAGS.enable_replay, implemented=True,
            source="configuration.feature_flags.FeatureFlags", description="Reserved (Phase A13) -- no backtest/replay harness exists.",
        ),
        # Phase 60.8 briefly added ENABLE_SIGNALS/ENABLE_AI/ENABLE_DATABASE
        # here as PipelineGuard's own runtime-feature gates. Phase 60.9
        # (Runtime Registry Separation) removed all three -- they are
        # Trading-pipeline stage gates, not Infrastructure, and
        # PipelineGuard now reads exclusively from EmergencyManager for
        # every stage decision. See docs/FEATURE_REGISTRY_SEPARATION.md.
    ]

    for name in _DECLARED_ONLY_FEATURES:
        entries.append(FeatureDescriptor(
            name=name, enabled=False, implemented=False,
            source="declared", description="Named by Phase 59.6's own brief -- no real backing exists yet.",
        ))

    return entries
