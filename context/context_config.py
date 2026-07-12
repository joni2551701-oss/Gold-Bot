from dataclasses import dataclass


@dataclass(frozen=True)
class ContextConfig:
    """
    Immutable, shared configuration for the Context Layer detection
    pipeline.

    This is the single source of truth for pipeline-wide detection
    parameters. All Context Layer modules (market structure, liquidity,
    and future additions such as volume, HTF bias, session detection,
    or premium/discount zoning) must import this module rather than
    defining their own configuration class.

    Kept intentionally separate from the global application Config to
    isolate strategy/detection parameters (which may be optimized via
    backtesting) from environment and infrastructure settings.
    """
    swing_left_strength: int = 2
    swing_right_strength: int = 2
    liquidity_equal_level_tolerance: float = 0.30
