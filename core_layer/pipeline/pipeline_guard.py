"""
Core Layer — Pipeline Guard (Phase 60.8: Safe Integration Layer,
TASK 2/3; simplified in Phase 60.9: Runtime Registry Separation,
TASK 4).

PipelineGuard is the one seam `core/pipeline.py` calls at its own
stage boundaries to ask "should this stage run right now" -- it never
computes a trading decision itself, never touches `decision/`,
`risk/`, `strategies/`, `signals/`, `context/`, `ai/`, or
`execution/`.

**As of Phase 60.9, this module composes exactly one manager**:

    core_layer.emergency.emergency_manager.EmergencyManager  -- read-only .get_status() lookups

Phase 60.8 originally also composed
`configuration.runtime_feature_manager.RuntimeFeatureManager`, gating
`before_signal()`/`before_ai()`/`before_database()` by three registry
names (`ENABLE_SIGNALS`/`ENABLE_AI`/`ENABLE_DATABASE`). Phase 60.9
removed that dependency entirely: those three names were Trading-
pipeline concerns that never belonged in the Infrastructure-only
Runtime Registry (see `docs/FEATURE_REGISTRY_SEPARATION.md`'s audit),
and a fourth Trading name (`ENABLE_EXECUTION`) had already collided
with `configuration/feature_dependency_validator.py`'s
`DEPENDENCY_RULES` and broken 26 tests when Phase 60.8 tried to
promote it (see this module's own git history / `docs/PIPELINE_GUARD.md`'s
former "Disclosed Findings" for the full account, now resolved).
**Trading control is now exclusively `EmergencyManager`'s
responsibility; `RuntimeFeatureManager` never influences a pipeline
stage decision.**

`core_layer.logger.logger` and `core_layer.emergency.emergency_state.EmergencyState` (the
enum PipelineGuard compares against) are cross-cutting infrastructure,
not a second "business module."

Four public methods, one per named pipeline stage boundary:

    before_signal()     -- gates core/pipeline.py's `signal` stage (SignalEngine.generate_signals())
    before_ai()          -- gates the `ai` stage (AIAnalyzer.analyze())
    before_execution()   -- gates the `telegram_delivery` stage (Notifier.send_messages()) -- see
                             "Design notes" below for why "execution" maps here, not to
                             execution/execution_engine.py
    before_database()    -- gates the `database` stage (SignalRepository.save_signal_record())

Each returns a `GuardDecision(proceed, abort, reason)` -- `proceed`
tells the caller whether to run the stage normally; `abort` (only ever
True on `EmergencyState.KILLED`) tells the caller to stop the entire
pipeline run immediately. What "skip" or "abort" concretely means for
each stage's own output (an empty list, a neutral substitute value, an
early return) is entirely `core/pipeline.py`'s own decision -- this
module only classifies the situation, never the response.

Emergency mapping (`core_layer.emergency.emergency_state.EmergencyState`,
five real values) -- identical to Phase 60.8, unchanged by this
simplification:

    NORMAL       -- proceed
    WARNING      -- proceed + one logger.warning() per check
    PAUSED       -- `before_execution()` -> skip; the other three stages proceed
    MAINTENANCE  -- all four stages -> skip (see "Design notes" for the one honest gap this leaves)
    KILLED       -- abort, on whichever hook is checked first

Design notes
------------
1. There is no `before_market_data()` hook in this module's API (the
   Director's own Phase 60.8 brief named exactly four methods) --
   `market_data`, `data_quality`, `htf_bias`, `context`, and
   `market_phase` all run regardless of Emergency state, including
   under `MAINTENANCE`/`KILLED`. All five are pure, read-only
   computations with no trade, Telegram, or database side effect, so
   this does not violate the safety intent behind either state, but it
   does mean `MAINTENANCE`'s own "only Market Data" is not literally
   true -- several read-only context stages also still run.
2. `before_execution()` maps to `core/pipeline.py`'s `telegram_delivery`
   stage, not to `execution/execution_engine.py` (which stays
   untouched and inert). The pipeline has no real "execution" stage
   today -- Telegram delivery is the only point where an actual
   outward effect happens, so it is the practical stand-in for
   "execution" in a bot with no live broker connection.
3. `_neutral_ai_result()` (`core/pipeline.py`)'s substitution branch --
   used when `before_ai()` skips but `before_signal()` did not -- is
   not reachable through any real `EmergencyState` combination today:
   the only state that skips `ai` (`MAINTENANCE`) also skips `signal`
   (leaving `signal_candidates` already empty, so there is nothing to
   substitute). The code path stays, correctly implemented and unit-
   tested via a directly-constructed `GuardDecision`/stub guard --
   forward-compatible with a future Emergency state or MAINTENANCE
   refinement that skips AI specifically while still generating
   signals, not dead code to be deleted speculatively.
"""

from dataclasses import dataclass
from typing import Optional

from core_layer.emergency.emergency_manager import EmergencyManager
from core_layer.emergency.emergency_state import EmergencyState
from core_layer.logger.logger import setup_logger

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
    pipeline dependency already uses). `EmergencyManager` is injectable
    (same optional-dependency convention as every Phase 59.x/60.x
    manager in this codebase) -- a test can supply a stub manager
    instead of touching the real database.
    """

    def __init__(self, emergency_manager: Optional[EmergencyManager] = None):
        self.emergency_manager = emergency_manager or EmergencyManager()

    def before_signal(self) -> GuardDecision:
        return self._check("signal")

    def before_ai(self) -> GuardDecision:
        return self._check("ai")

    def before_execution(self) -> GuardDecision:
        return self._check("execution")

    def before_database(self) -> GuardDecision:
        return self._check("database")

    def _check(self, stage_name: str) -> GuardDecision:
        """
        Never raises: any exception from EmergencyManager would be a
        genuine bug in that manager, not something this thin
        composition layer should mask.
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

        return GuardDecision(proceed=True, reason="OK")
