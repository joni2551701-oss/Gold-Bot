"""
Telegram Layer — Owner Dataset Commands (Phase 59.5: Historical Data
Collection & Validation Foundation, TASK 7). Same "real function, not
live-wired" posture as provider_commands.py/system_commands.py/
feature_commands.py/report_commands.py/validation_commands.py (same
package) -- see provider_commands.py's own docstring.

Unlike report_commands.py/validation_commands.py (which take
already-computed data as input, since nothing persists a day's/week's
worth of SignalSchema/SignalPerformance anywhere yet), the functions
here call the REAL RawCandleRepository/SyncStateRepository directly --
raw_candles and sync_state (Phase 59.3/Phase 59.5 TASK 2) are real,
persisted tables today, so there is real data to query, the same
posture provider_commands.py's list_providers()/get_data_status()
already uses for the real ProviderRegistry/provider_health backing
store.
"""

from typing import Optional

from analytics.dataset_report import build_dataset_report, format_dataset_report
from data_layer.providers.provider_comparison import compare_providers
from database_layer.market_repository.raw_candle_repository import RawCandleRepository
from database_layer.market_repository.sync_state_repository import SyncStateRepository
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("DatasetCommands")


def get_dataset_status(
    symbol: str,
    timeframe: str,
    raw_candle_repository: Optional[RawCandleRepository] = None,
) -> ProviderCommandResult:
    """
    The future `/dataset`/`/dataset_status` command's payload --
    analytics.dataset_report.build_dataset_report()/format_dataset_report()
    (same phase, TASK 5) run against every stored candle for
    (symbol, timeframe), across all providers. Never raises: no stored
    candles produces the same all-zero report those functions already
    return for an empty list, not an exception.
    """
    try:
        repository = raw_candle_repository or RawCandleRepository()
        candles = repository.get_candles(symbol, timeframe)
        report = build_dataset_report(candles)
        return ProviderCommandResult(success=True, message=format_dataset_report(report))
    except Exception as e:
        logger.warning(f"get_dataset_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_history_status(
    symbol: str,
    timeframe: str,
    raw_candle_repository: Optional[RawCandleRepository] = None,
) -> ProviderCommandResult:
    """
    The future `/history_status` command's payload -- a lighter-weight
    view than get_dataset_status(): just the stored candle count and
    oldest/newest timestamp for (symbol, timeframe), via
    RawCandleRepository.count_candles()/get_candles() directly (no
    validation/coverage computation). Never raises: zero stored
    candles reports "Candles: 0" with no oldest/newest, not an error.
    """
    try:
        repository = raw_candle_repository or RawCandleRepository()
        count = repository.count_candles(symbol, timeframe)
        candles = repository.get_candles(symbol, timeframe)
        oldest = candles[0].timestamp.isoformat() if candles else "N/A"
        newest = candles[-1].timestamp.isoformat() if candles else "N/A"

        lines = [
            f"Symbol: {symbol}",
            f"Timeframe: {timeframe}",
            f"Candles: {count}",
            f"Oldest: {oldest}",
            f"Newest: {newest}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_history_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_sync_status(
    provider: str,
    symbol: str,
    timeframe: str,
    sync_state_repository: Optional[SyncStateRepository] = None,
) -> ProviderCommandResult:
    """
    The future `/sync_status` command's payload -- reports the current
    incremental-sync watermark (data_layer/historical_data/historical_data_collector.py's
    sync_historical_candles(), same phase, TASK 2) for
    (provider, symbol, timeframe). Never raises: no prior sync state
    reports that plainly, not an error.
    """
    try:
        repository = sync_state_repository or SyncStateRepository()
        state = repository.get_sync_state(provider, symbol, timeframe)
        if state is None:
            message = f"{provider}|{symbol}|{timeframe}: no sync state yet"
        else:
            message = f"{provider}|{symbol}|{timeframe}: last synced {state.last_timestamp.isoformat()}"
        return ProviderCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"get_sync_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_provider_compare(
    symbol: str,
    timeframe: str,
    provider_a: str,
    provider_b: str,
    raw_candle_repository: Optional[RawCandleRepository] = None,
) -> ProviderCommandResult:
    """
    The future `/provider_compare` command's payload --
    data_layer.providers.provider_comparison.compare_providers() (same phase, TASK 6)
    run against each provider's own stored candles for (symbol,
    timeframe). Foundation only: reports a summary, performs no
    auto-correction (see provider_comparison.py's own docstring).
    Never raises: no overlapping timestamps between the two providers
    reports "No overlapping candles to compare", not an error.
    """
    try:
        repository = raw_candle_repository or RawCandleRepository()
        candles_a = repository.get_candles(symbol, timeframe, provider=provider_a)
        candles_b = repository.get_candles(symbol, timeframe, provider=provider_b)
        comparisons = compare_providers(candles_a, candles_b)

        if not comparisons:
            return ProviderCommandResult(
                success=True,
                message=f"{provider_a} vs {provider_b} ({symbol}|{timeframe}): No overlapping candles to compare",
            )

        avg_close_diff = sum(c.close_diff for c in comparisons) / len(comparisons)
        within_tolerance_count = sum(1 for c in comparisons if c.within_tolerance)

        lines = [
            f"{provider_a} vs {provider_b} ({symbol}|{timeframe})",
            f"Compared: {len(comparisons)}",
            f"Avg close diff: {avg_close_diff:.4f}",
            f"Within tolerance: {within_tolerance_count}/{len(comparisons)}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_provider_compare failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
