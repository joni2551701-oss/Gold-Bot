"""
Telegram Layer — Owner Feature Commands (Phase 59.3, TASK 5). Same
"real function, not live-wired" posture as provider_commands.py (same
package).

Two, previously separate, flag systems exist in this codebase with no
single place listing both: configuration/feature_flags.py's
FeatureFlags (Phase A13 -- enable_ai/enable_crypto/enable_swing/
enable_ai_memory/enable_replay, every default False, none wired to a
real feature) and config.py's ENABLE_MT5/ENABLE_TWELVEDATA (Phase
59.1, env-driven, real provider gating). list_features() below is the
first place both are read together -- it does not change either flag
system, only reports on them.
"""

from config import Config
from core_layer.configuration.feature_flags import DEFAULT_FLAGS
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("FeatureCommands")


def list_features() -> ProviderCommandResult:
    """
    The future /features command's payload. Never raises: reads two
    already-constructed, always-safe sources (DEFAULT_FLAGS -- a plain
    dataclass instance, no I/O; Config -- module-level constants, no
    I/O) rather than doing anything that could fail.
    """
    try:
        flags = DEFAULT_FLAGS
        lines = [
            "Reserved feature flags (configuration/feature_flags.py, Phase A13):",
            f"  enable_ai: {flags.enable_ai}",
            f"  enable_crypto: {flags.enable_crypto}",
            f"  enable_swing: {flags.enable_swing}",
            f"  enable_ai_memory: {flags.enable_ai_memory}",
            f"  enable_replay: {flags.enable_replay}",
            "",
            "Provider flags (config.py, Phase 59.1):",
            f"  MARKET_DATA_PROVIDER: {Config.MARKET_DATA_PROVIDER}",
            f"  ENABLE_TWELVEDATA: {Config.ENABLE_TWELVEDATA}",
            f"  ENABLE_MT5: {Config.ENABLE_MT5}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"list_features failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
