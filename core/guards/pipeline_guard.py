"""
Core Layer — Pipeline Guard (Phase 60.8: Safe Integration Layer,
TASK 2/3, per the Director's own "Official" Worker Brief).

PipelineGuard is the one seam `core/pipeline.py` calls at its own
stage boundaries to ask "should this stage run right now" -- it never
computes a trading decision itself, never touches `decision/`,
`risk/`, `strategies/`, `signals/`, `context/`, `ai/`, or
`execution/`. It composes exactly two already-built managers, per the
brief's own "Boshqa modul chaqirilmaydi" rule:

    configuration.runtime_feature_manager.RuntimeFeatureManager  -- read-only .status() lookups
    core.emergency.emergency_manager.EmergencyManager             -- read-only .get_status() lookups

`core.logger` (used by literally every module in this codebase,
including both managers above) and `core.emergency.emergency_state.EmergencyState`
(the enum PipelineGuard compares against, not a business module) are
treated as cross-cutting infrastructure, not "another module" in the
brief's forbidden sense -- the same posture `EmergencyManager` itself
already takes toward `core.logger`.

Four public methods, one per named pipeline stage boundary:

    before_signal()     -- gates core/pipeline.py's `signal` stage (SignalEngine.generate_signals())
    before_ai()          -- gates the `ai` stage (AIAnalyzer.analyze())
    before_execution()   -- gates the `telegram_delivery` stage (Notifier.send_messages()) -- see
                             "Disclosed Findings" below for why "execution" maps here, not to
                             execution/execution_engine.py
    before_database()    -- gates the `database` stage (SignalRepository.save_signal_record())

Each returns a `GuardDecision(proceed, abort, reason)` -- `proceed`
tells the caller whether to run the stage normally; `abort` (only ever
True on `EmergencyState.KILLED`) tells the caller to stop the entire
pipeline run immediately. What "skip" or "abort" concretely means for
each stage's own output (an empty list, a neutral substitute value, an
early return) is entirely `core/pipeline.py`'s own decision -- this
module only classifies the situation, never the response.

Runtime mapping (registry names, `configuration/feature_registry.py`,
Phase 60.8 TASK 2): `ENABLE_SIGNALS`, `ENABLE_AI`, `ENABLE_DATABASE` are
real, implemented=True, `config.Config`-backed entries -- named
directly per the Director's own brief. All three default to `True`
(`config.Config`'s own env-var default), so a process with no explicit
override reproduces exactly today's pipeline behavior.
`before_execution()` does NOT read a runtime feature flag -- see
"Disclosed Findings" (finding 3) for the blocking reason.

Emergency mapping (`core.emergency.emergency_state.EmergencyState`,
five real values):

    NORMAL       -- proceed (subject to the stage's own feature flag, where one exists)
    WARNING      -- proceed (subject to the stage's own feature flag) + one logger.warning() per check
    PAUSED       -- `before_execution()` -> skip; the other three stages proceed (subject to their own flags)
    MAINTENANCE  -- all four stages -> skip (see "Disclosed Findings" below for the one honest gap this leaves)
    KILLED       -- abort, on whichever hook is checked first

Disclosed Findings
-------------------
1. There is no `before_market_data()` hook in this module's API (the
   Director's brief names exactly four methods) -- `market_data`,
   `data_quality`, `htf_bias`, `context`, and `market_phase` all run
   regardless of Emergency state, including under `MAINTENANCE`/
   `KILLED`. All five are pure, read-only computations with no trade,
   Telegram, or database side effect, so this does not violate the
   safety intent behind either state, but it does mean `MAINTENANCE`'s
   own "Faqat Market Data ... ishga ruxsat" is not literally true --
   several read-only context stages also still run. Not silently
   assumed away: flagged here and in `docs/PIPELINE_GUARD.md`.
2. `before_execution()` maps to `core/pipeline.py`'s `telegram_delivery`
   stage, not to `execution/execution_engine.py` (which stays
   untouched and inert, per the brief's own prohibited-modules list).
   The pipeline has no real "execution" stage today -- Telegram
   delivery is the only point where an actual outward effect happens,
   so it is the practical stand-in for "execution" in a bot with no
   live broker connection.
3. **Blocking, discovered during implementation, not fully anticipated
   by TASK 1's own audit**: `ENABLE_EXECUTION` (the registry name the
   brief explicitly names) was promoted to a real, `enabled=True`
   registry entry and then reverted. Reason:
   `configuration/feature_dependency_validator.py`'s DEPENDENCY_RULES
   already declares "ENABLE_EXECUTION requires ENABLE_RISK,
   ENABLE_DECISION" (both still declared-only/always-False), and
   `validate_feature_dependencies()` checks that rule against the
   *entire* registry snapshot on *every* toggle attempt to *any*
   feature -- not just to `ENABLE_EXECUTION` itself. With
   `ENABLE_EXECUTION` real and `enabled=True`, all 18 tests in
   `tests/configuration/test_runtime_feature_manager.py` plus
   `test_default_registry_has_no_violations` and three
   `telegram/owner/` tests failed (26 total) -- toggling even an
   unrelated feature like `ENABLE_NEWS` was rejected, because the
   dry-run's hypothetical snapshot still carried `ENABLE_EXECUTION`
   forward as `True` against its permanently-unmet dependencies. The
   alternative (defaulting `ENABLE_EXECUTION` to `False` instead) was
   rejected too: that would silently disable live Telegram delivery by
   default, a severe undisclosed behavior change this phase's own
   Acceptance Criteria forbid. `before_execution()` therefore reads
   Emergency state only (`PAUSED`/`MAINTENANCE`/`KILLED` all still work
   correctly) until the Director decides between (a) renaming this
   gate to something that doesn't collide with DEPENDENCY_RULES,
   (b) also promoting `ENABLE_RISK`/`ENABLE_DECISION` (out of this
   phase's scope), or (c) amending DEPENDENCY_RULES itself (also out of
   scope). See `configuration/feature_registry.py`'s own comment for
   the same disclosure.
"""

from dataclasses import dataclass
from typing import Optional

from configuration.runtime_feature_manager import RuntimeFeatureManager
from core.emergency.emergency_manager import EmergencyManager
from core.emergency.emergency_state import EmergencyState
from core.logger import setup_logger

logger = setup_logger("PipelineGuard")


@dataclass(frozen=True)
class GuardDecision:
    """
    proceed: whether the calling stage should run normally.
    abort: True only for EmergencyState.KILLED -- the caller must stop
        the entire pipeline run immediately, not just this one stage.
        Always implies proceed=False.
    reason: human-readable, logged by the caller on any non-proceed
        outcome -- never raises, never itself logs at ERROR level.
    """
    proceed: bool
    abort: bool = False
    reason: str = ""


class PipelineGuard:
    """
    One guard per `TradingPipeline` instance (constructed once in
    `__init__`, same eager-construction convention every other
    pipeline dependency already uses). Both managers are injectable
    (same optional-dependency convention as every Phase 59.x/60.x
    manager in this codebase) -- a test can supply stub managers
    instead of touching the real database/emergency state.
    """

    def __init__(
        self,
        runtime_feature_manager: Optional[RuntimeFeatureManager] = None,
        emergency_manager: Optional[EmergencyManager] = None,
    ):
        self.runtime_feature_manager = runtime_feature_manager or RuntimeFeatureManager()
        self.emergency_manager = emergency_manager or EmergencyManager()

    def before_signal(self) -> GuardDecision:
        return self._check("signal", "ENABLE_SIGNALS")

    def before_ai(self) -> GuardDecision:
        return self._check("ai", "ENABLE_AI")

    def before_execution(self) -> GuardDecision:
        """
        Emergency-only for now: `feature_name=None`, since
        `ENABLE_EXECUTION` is not a real registry entry -- see this
        module's own "Disclosed Findings" (finding 3) and
        `configuration/feature_registry.py`'s own comment. Promoting it
        was tried and reverted: `configuration/feature_dependency_validator.py`'s
        DEPENDENCY_RULES rejects *every* toggle attempt on *any*
        feature once `ENABLE_EXECUTION` reads `enabled=True` there
        (its declared `ENABLE_RISK`/`ENABLE_DECISION` dependencies stay
        permanently unmet). `EmergencyState.PAUSED`/`.MAINTENANCE`/
        `.KILLED` still gate this stage correctly; only the
        owner-toggleable-at-runtime half of TASK 2's brief is blocked
        on the Director's resolution.
        """
        return self._check("execution", None)

    def before_database(self) -> GuardDecision:
        return self._check("database", "ENABLE_DATABASE")

    def _check(self, stage_name: str, feature_name: Optional[str]) -> GuardDecision:
        """
        Emergency state is checked first (it can force a skip/abort
        regardless of any feature flag); the stage's own runtime
        feature flag (when `feature_name` is not None -- see
        `before_execution()`) is checked only once Emergency state
        allows the stage to be considered at all. Never raises: any
        exception from either manager would be a genuine bug in that
        manager, not something this thin composition layer should mask.
        """
        status = self.emergency_manager.get_status()
        state = status.state

        if state == EmergencyState.KILLED:
            return GuardDecision(proceed=False, abort=True, reason=f"EmergencyState.KILLED (stage={stage_name})")

        if state == EmergencyState.MAINTENANCE:
            return GuardDecision(proceed=False, reason=f"EmergencyState.MAINTENANCE (stage={stage_name})")

        if state == EmergencyState.PAUSED and stage_name == "execution":
            return GuardDecision(proceed=False, reason="EmergencyState.PAUSED (execution skipped)")

        if state == EmergencyState.WARNING:
            logger.warning(
                f"pipeline_guard_warning stage={stage_name} emergency_state=WARNING reason={status.reason}"
            )

        if feature_name is not None:
            feature_state = self.runtime_feature_manager.status(feature_name)
            if feature_state is not None and not feature_state.enabled:
                return GuardDecision(proceed=False, reason=f"{feature_name} disabled")

        return GuardDecision(proceed=True, reason="OK")
