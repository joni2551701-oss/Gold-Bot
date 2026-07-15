"""
Configuration Layer — Feature Registry (Phase 59.6: Audit &
Observability Foundation, TASK 4).

One structured catalog of every feature name this codebase knows
about -- real, backed flags and reserved, declared-only names alike --
matching this task's own brief ("Barcha feature bitta registry'da").
Not runtime: build_feature_registry() only *reads* already-computed
values (config.Config's module-level constants,
configuration.feature_flags.DEFAULT_FLAGS) and reports declared-only
names as a fixed, safe False -- it does not gate, enable, or disable
anything, and nothing in core/pipeline.py, decision/, risk/, or
execution/ reads this module.

Relationship to telegram/owner/feature_commands.py's list_features()
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
from configuration.feature_flags import DEFAULT_FLAGS

# Names this task's own brief lists that have no real backing anywhere
# in this codebase today. Always False, always "declared" -- see
# module docstring. Deliberately does NOT include "ENABLE_BACKTEST" as
# a synonym for FeatureFlags.enable_replay (a real, already-named
# field, Phase A13) -- the two are kept as distinct registry entries
# rather than silently aliased.
#
# "ENABLE_EXECUTION" stays declared-only here, unlike the other three
# Phase 60.8 (Safe Integration Layer, TASK 2) gate names below -- see
# that section's own comment and docs/PIPELINE_GUARD.md's "Disclosed
# Findings" for why: promoting it to implemented=True/enabled=True was
# tried and reverted, since
# configuration/feature_dependency_validator.py's DEPENDENCY_RULES
# already declares "ENABLE_EXECUTION requires ENABLE_RISK,
# ENABLE_DECISION" (both still declared-only, always False) -- and
# `validate_feature_dependencies()` checks that rule against the
# *entire* registry snapshot on every single toggle attempt to *any*
# feature, not just to ENABLE_EXECUTION itself. With ENABLE_EXECUTION
# enabled=True, every one of RuntimeFeatureManager's own toggle tests
# (`tests/configuration/test_runtime_feature_manager.py`, 18 tests) and
# `test_default_registry_has_no_violations` failed. Blocking, not
# silently worked around: PipelineGuard.before_execution() reads only
# EmergencyManager (PAUSED/MAINTENANCE/KILLED all still work) until the
# Director resolves the naming conflict.
_DECLARED_ONLY_FEATURES = (
    "ENABLE_NEWS",
    "ENABLE_PAPER",
    "ENABLE_EXECUTION",
    "ENABLE_BACKTEST",
    "ENABLE_ANALYTICS",
    "ENABLE_OWNER",
    "ENABLE_DATASET_SYNC",
    "ENABLE_MARKET_PHASE",
    "ENABLE_BITGET",
    "ENABLE_BINANCE",
    "ENABLE_FRED",
    "ENABLE_RISK",
    "ENABLE_DECISION",
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
        # Phase 60.8 (Safe Integration Layer, TASK 2): the four stage
        # gates core/guards/pipeline_guard.py's PipelineGuard reads via
        # RuntimeFeatureManager.status(). All default True (Config's
        # own env-var default) -- a process with no override reproduces
        # exactly today's pipeline behavior.
        FeatureDescriptor(
            name="ENABLE_SIGNALS", enabled=Config.ENABLE_SIGNALS, implemented=True,
            source="config.Config", description="PipelineGuard.before_signal() gate -- disables core/pipeline.py's signal-generation stage only.",
        ),
        FeatureDescriptor(
            name="ENABLE_AI", enabled=Config.ENABLE_AI, implemented=True,
            source="config.Config", description="PipelineGuard.before_ai() gate -- disables core/pipeline.py's AI-analysis stage only; Decision Engine still runs against a neutral default. Distinct from the pre-existing lowercase 'enable_ai' above.",
        ),
        # ENABLE_EXECUTION is NOT promoted here -- see this file's own
        # _DECLARED_ONLY_FEATURES comment. It stays declared-only
        # (implemented=False, always False) below, same as before Phase
        # 60.8. config.Config.ENABLE_EXECUTION still exists (Phase 60.8
        # added it) but is not read by this registry yet -- it is
        # PipelineGuard's own construction-time fallback only (see
        # core/guards/pipeline_guard.py's before_execution() docstring),
        # pending the Director's resolution of the DEPENDENCY_RULES
        # conflict.
        FeatureDescriptor(
            name="ENABLE_DATABASE", enabled=Config.ENABLE_DATABASE, implemented=True,
            source="config.Config", description="PipelineGuard.before_database() gate -- disables core/pipeline.py's signal-persistence stage only.",
        ),
    ]

    for name in _DECLARED_ONLY_FEATURES:
        entries.append(FeatureDescriptor(
            name=name, enabled=False, implemented=False,
            source="declared", description="Named by Phase 59.6's own brief -- no real backing exists yet.",
        ))

    return entries
