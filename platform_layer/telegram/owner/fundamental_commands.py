"""
Telegram Layer — Owner Fundamental Commands (Phase 60.5: Fundamental
Intelligence Foundation, TASK 8). Same "real function, not live-wired"
posture as every other module in this package -- see
provider_commands.py's own docstring. NOT registered into
platform_layer/telegram/commands.py, NOT called from platform_layer/telegram/command_router.py or
platform_layer/telegram/handlers.py.

Thin wrappers over context.fundamental_context/context.fundamental_scoring
-- this module writes no macro classification/scoring logic of its
own. Same "compute from supplied data, don't fetch" posture
validation_commands.py/performance_commands.py already established:
the caller supplies an already-built FundamentalContextSnapshot/
FundamentalScoreResult (nothing in this codebase fetches real FRED
data yet -- data_layer.providers.fred_provider.FredProvider is still a
foundation-only stub, see its own module docstring).

Per this whole phase's hard boundary: none of these commands return
"BUY"/"SELL", approve/reject anything, or touch decision/risk/execution
-- they only report a macro bias, a score, and a Fed reading.
"""

from context_layer.fundamental.fundamental_context import FundamentalContextSnapshot
from context_layer.fundamental.fundamental_scoring import FundamentalScoreResult, format_fundamental_score
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("FundamentalCommands")


def get_macro_status(fundamental: FundamentalContextSnapshot) -> ProviderCommandResult:
    """
    The future `/macro_status` command's payload -- reports every
    per-indicator bias already carried on an already-built
    FundamentalContextSnapshot. Never raises: a snapshot with every
    field None (the common case today, since FredProvider has no real
    connection yet) reports "unknown" for each, not an exception.
    """
    try:
        lines = [
            "Macro Status",
            f"DXY Bias: {fundamental.dxy_bias or 'unknown'}",
            f"Rates Bias: {fundamental.rates_bias or 'unknown'}",
            f"Inflation Bias: {fundamental.inflation_bias or 'unknown'}",
            f"Fed Expectation: {fundamental.fed_expectation or 'unknown'}",
            f"Risk Sentiment: {fundamental.risk_sentiment or 'unknown'}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_macro_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_fundamental_score_report(score: FundamentalScoreResult) -> ProviderCommandResult:
    """
    The future `/fundamental_score` command's payload -- wraps
    context.fundamental_scoring.format_fundamental_score() unmodified,
    matching the Director's own worked example shape ("Macro Bias:
    BULLISH GOLD / Confidence: 78% / Reasons: ..."). Never raises.
    """
    try:
        return ProviderCommandResult(success=True, message=format_fundamental_score(score))
    except Exception as e:
        logger.warning(f"get_fundamental_score_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_fed_status(fundamental: FundamentalContextSnapshot) -> ProviderCommandResult:
    """
    The future `/fed_status` command's payload -- a focused subset of
    get_macro_status() naming only the Fed-specific readings
    (fed_rate, fed_expectation). Never raises.
    """
    try:
        fed_rate = f"{fundamental.fed_rate:.2f}%" if fundamental.fed_rate is not None else "unknown"
        lines = [
            "Fed Status",
            f"Fed Funds Rate: {fed_rate}",
            f"Fed Expectation: {fundamental.fed_expectation or 'unknown'}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_fed_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
