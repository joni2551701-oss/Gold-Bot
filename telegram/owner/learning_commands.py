"""
Telegram Layer — Owner Learning Commands (Phase 60.6: Learning Loop
Foundation, TASK 8). Same "real function, not live-wired" posture as
every other module in this package -- see provider_commands.py's own
docstring. NOT registered into telegram/commands.py, NOT called from
telegram/command_router.py or telegram/handlers.py.

Thin wrappers over analytics.learning_report/learning.pattern_detector
-- this module writes no pattern-detection/report computation of its
own. Same "compute from supplied data, don't fetch" posture
validation_commands.py/performance_commands.py/fundamental_commands.py
already established: the caller supplies an already-built
Sequence[LearningRecord] (e.g. from database.learning_repository.LearningRepository.get_recent()
converted to LearningRecord, a wiring step this phase does not do).

Per this whole phase's hard boundary: none of these commands mutate a
strategy parameter, a confidence threshold, or risk sizing -- they
only report what has already been observed.
"""

from typing import Sequence

from analytics.learning_report import build_learning_report, format_learning_report
from learning.models import LearningRecord
from learning.pattern_detector import detect_patterns, filter_high_failure_patterns, filter_high_success_patterns, format_pattern_insight
from telegram.owner.provider_commands import ProviderCommandResult
from core.logger import setup_logger

logger = setup_logger("LearningCommands")


def get_learning_status(records: Sequence[LearningRecord], min_occurrences: int = 3) -> ProviderCommandResult:
    """
    The future `/learning_status` command's payload -- wraps
    analytics.learning_report.build_learning_report()/
    format_learning_report() unmodified. Never raises.
    """
    try:
        report = build_learning_report(records, min_occurrences=min_occurrences)
        return ProviderCommandResult(success=True, message=format_learning_report(report))
    except Exception as e:
        logger.warning(f"get_learning_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_patterns_report(records: Sequence[LearningRecord], min_occurrences: int = 3) -> ProviderCommandResult:
    """
    The future `/patterns` command's payload -- every condition
    combination `learning.pattern_detector.detect_patterns()` found,
    regardless of classification (HIGH_SUCCESS/HIGH_FAILURE/MIXED).
    Never raises: no patterns produces a plain "no patterns" message,
    not an exception.
    """
    try:
        insights = detect_patterns(records, min_occurrences=min_occurrences)
        if not insights:
            return ProviderCommandResult(success=True, message="No patterns found yet.")
        message = "\n\n".join(format_pattern_insight(insight) for insight in insights)
        return ProviderCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"get_patterns_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_failures_report(records: Sequence[LearningRecord], min_occurrences: int = 3) -> ProviderCommandResult:
    """
    The future `/failures` command's payload -- only `HIGH_FAILURE`-
    classified patterns. Never raises.
    """
    try:
        insights = detect_patterns(records, min_occurrences=min_occurrences)
        failures = filter_high_failure_patterns(insights)
        if not failures:
            return ProviderCommandResult(success=True, message="No high-failure conditions found yet.")
        message = "\n\n".join(format_pattern_insight(insight) for insight in failures)
        return ProviderCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"get_failures_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_best_conditions_report(records: Sequence[LearningRecord], min_occurrences: int = 3) -> ProviderCommandResult:
    """
    The future `/best_conditions` command's payload -- only
    `HIGH_SUCCESS`-classified patterns. Never raises.
    """
    try:
        insights = detect_patterns(records, min_occurrences=min_occurrences)
        successes = filter_high_success_patterns(insights)
        if not successes:
            return ProviderCommandResult(success=True, message="No high-success conditions found yet.")
        message = "\n\n".join(format_pattern_insight(insight) for insight in successes)
        return ProviderCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"get_best_conditions_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
