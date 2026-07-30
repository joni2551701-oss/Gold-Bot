"""
data.bootstrap -- GoldBot v1.1 Market Data Foundation: Historical
Bootstrap (Phase 1 module 5).

One-time-per-timeframe historical load into MarketMemory, plus gap
recovery, incremental/cold/warm paths, resume, cancellation, progress and
metrics. Vendor-agnostic (a HistoricalProvider abstraction), restart-safe,
monitoring-friendly. Feeds Memory only via Module 1 APIs; no
business/signal logic (Trading Safety).

- bootstrap_state.py     -- BootstrapState + BootstrapStrategy (DD-058)
- bootstrap_progress.py  -- BootstrapProgress (DD-054)
- bootstrap_metrics.py   -- BootstrapMetrics (DD-057)
- historical_provider.py -- HistoricalProvider abstraction + cache protocol
- twelve_data_historical_provider.py -- Twelve Data adapter (Art.11 reuse)
- gap_recovery.py        -- window-gap detection + fill
- historical_bootstrap.py-- the orchestrator (strategies, resume, cancel)

This package never imports from telegram/, ai/, decision/, risk/,
strategies/, signals/, context/, or database/.
"""

from data.bootstrap.bootstrap_state import BootstrapState, BootstrapStrategy
from data.bootstrap.bootstrap_progress import BootstrapProgress
from data.bootstrap.bootstrap_metrics import BootstrapMetrics
from data.bootstrap.historical_provider import (
    HistoricalProvider, BootstrapCache, InMemoryBootstrapCache,
)
from data.bootstrap.gap_recovery import GapRecovery
from data.bootstrap.bootstrap_events import BootstrapEventHook
from data.bootstrap.historical_bootstrap import HistoricalBootstrap

__all__ = [
    "BootstrapState",
    "BootstrapStrategy",
    "BootstrapProgress",
    "BootstrapMetrics",
    "HistoricalProvider",
    "BootstrapCache",
    "InMemoryBootstrapCache",
    "GapRecovery",
    "BootstrapEventHook",
    "HistoricalBootstrap",
]
