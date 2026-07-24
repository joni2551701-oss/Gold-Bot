"""
HistoricalBootstrap -- the per-asset bootstrap orchestrator (v1.1 Phase 1,
module 5). Loads historical candles into MarketMemory once per timeframe,
with strategy selection (DD-058), resume-from-last-success (DD-056),
cancellation (DD-055), observable progress (DD-054), and metrics (DD-057).

Writes memory only via Module 1 APIs; reuses candle_clock (module 3),
HistoricalProvider + GapRecovery (module 5). Clock-injected (all time from
`now`) so tests are deterministic. No business/signal logic (Trading
Safety); not wired into core/pipeline.py.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Mapping

from core.logger import setup_logger
from data.candle_clock import CandleClock, TIMEFRAME_ORDER
from data.twelve_data_client import Candle
from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleSource
from data.bootstrap.bootstrap_state import BootstrapState, BootstrapStrategy
from data.bootstrap.bootstrap_progress import BootstrapProgress
from data.bootstrap.bootstrap_metrics import BootstrapMetrics
from data.bootstrap.historical_provider import HistoricalProvider, BootstrapCache
from data.bootstrap.gap_recovery import GapRecovery

logger = setup_logger("HistoricalBootstrap")


class HistoricalBootstrap:
    """Orchestrates one asset's historical bootstrap."""

    def __init__(self, memory: MarketMemory, provider: HistoricalProvider,
                 clock: Optional[CandleClock] = None,
                 cache: Optional[BootstrapCache] = None,
                 strategy: BootstrapStrategy = BootstrapStrategy.AUTO,
                 depths: Optional[Mapping[str, int]] = None):
        self._memory = memory
        self._provider = provider
        self._clock = clock or CandleClock()
        self._cache = cache
        self._strategy = strategy
        held = set(memory.timeframes())
        self._timeframes: List[str] = (
            [tf for tf in TIMEFRAME_ORDER if tf in held]
            + sorted(held - set(TIMEFRAME_ORDER)))
        self._depths: Dict[str, int] = dict(depths or {
            tf: memory.timeframe(tf).capacity for tf in self._timeframes})
        self._gap = GapRecovery(memory, provider, self._clock)
        self._states: Dict[str, BootstrapState] = {
            tf: BootstrapState.PENDING for tf in self._timeframes}
        self._metrics = BootstrapMetrics(asset=memory.asset)
        self._cancelled = False
        self._current_tf: Optional[str] = None
        self._started_at: Optional[datetime] = None
        self._finished_at: Optional[datetime] = None

    # -- control --------------------------------------------------------
    def cancel(self) -> None:
        """Request cancellation (DD-055); takes effect between timeframes."""
        self._cancelled = True

    @property
    def strategy(self) -> BootstrapStrategy:
        return self._strategy

    def state(self, timeframe: str) -> BootstrapState:
        return self._states[timeframe]

    # -- run ------------------------------------------------------------
    def run(self, now: datetime) -> BootstrapProgress:
        """
        Execute the bootstrap. Resumes from the last successful timeframe
        (READY timeframes are skipped, DD-056) and honors cancellation.
        """
        now = self._utc(now)
        if self._started_at is None:
            self._started_at = now
        for tf in self._timeframes:
            if self._cancelled:
                break
            if self._states[tf] is BootstrapState.READY:
                continue                       # resume: already done (DD-056)
            self._current_tf = tf
            try:
                self._bootstrap_tf(tf, now)
                self._states[tf] = BootstrapState.READY
            except Exception as exc:
                self._states[tf] = BootstrapState.FAILED
                self._metrics.validation_errors += 1
                logger.warning("Bootstrap[%s|%s] failed: %s",
                               self._memory.asset, tf, exc)
        self._current_tf = None
        if self._cancelled and not self._all_ready():
            for tf in self._timeframes:
                if self._states[tf] in (BootstrapState.PENDING,
                                        BootstrapState.LOADING):
                    self._states[tf] = BootstrapState.CANCELLED
        if self._all_ready():
            self._finished_at = now
        self._metrics.last_bootstrap = now
        return self.progress(now)

    # -- per-timeframe --------------------------------------------------
    def _bootstrap_tf(self, tf: str, now: datetime) -> None:
        strat = self._strategy
        self._states[tf] = BootstrapState.LOADING

        if strat is BootstrapStrategy.RECOVERY_ONLY:
            self._metrics.recovery_count += self._gap.recover(tf, now)
            return

        candles, incremental = self._load(tf, now, strat)

        if candles:
            self._states[tf] = BootstrapState.VALIDATING
            self._validate(candles)
            self._states[tf] = BootstrapState.HYDRATING
            if incremental:
                self._memory.timeframe(tf).merge_closed(
                    candles, source=CandleSource.BOOTSTRAP)
            else:
                self._memory.timeframe(tf).hydrate(
                    candles, source=CandleSource.BOOTSTRAP)
            self._metrics.candles_loaded += len(candles)
            if self._cache is not None:
                self._cache.put(self._memory.asset, tf, candles, now)

        # backfill any residual gap up to now (best-effort)
        self._metrics.recovery_count += self._gap.recover(tf, now)

    def _load(self, tf: str, now: datetime, strat: BootstrapStrategy):
        """Return (candles, is_incremental) per strategy."""
        if strat is BootstrapStrategy.CACHE_ONLY:
            return self._from_cache(tf), False
        if strat is BootstrapStrategy.FULL:
            return self._fetch_recent(tf), False
        if strat is BootstrapStrategy.INCREMENTAL:
            return self._incremental(tf, now), True
        # AUTO
        if self._cache is not None and self._cache.is_fresh(
                self._memory.asset, tf, now):
            return self._from_cache(tf), False                 # warm restart
        if self._cache is not None and self._cache.last_time(
                self._memory.asset, tf) is not None:
            return self._incremental(tf, now), True            # incremental
        return self._fetch_recent(tf), False                   # cold start

    def _fetch_recent(self, tf: str) -> List[Candle]:
        self._metrics.api_requests += 1
        return list(self._provider.fetch_recent(
            self._memory.asset, tf, self._depths[tf]))

    def _incremental(self, tf: str, now: datetime) -> List[Candle]:
        last = self._last_known(tf)
        if last is None:
            return self._fetch_recent(tf)
        start = last + timedelta(minutes=self._clock.minutes(tf))
        end = self._clock.window_start(tf, now)
        if start >= end:
            return []
        self._metrics.api_requests += 1
        return list(self._provider.fetch_range(
            self._memory.asset, tf, start, end))

    def _from_cache(self, tf: str) -> List[Candle]:
        if self._cache is None:
            self._metrics.cache_misses += 1
            return []
        cached = self._cache.get(self._memory.asset, tf)
        if cached:
            self._metrics.cache_hits += 1
            return list(cached)
        self._metrics.cache_misses += 1
        return []

    def _last_known(self, tf: str) -> Optional[datetime]:
        last = self._memory.timeframe(tf).get_last_closed()
        if last is not None:
            return last.timestamp
        if self._cache is not None:
            return self._cache.last_time(self._memory.asset, tf)
        return None

    @staticmethod
    def _validate(candles: List[Candle]) -> None:
        prev = None
        for c in candles:
            if c.timestamp.tzinfo is None:
                raise ValueError("candle timestamp must be tz-aware UTC")
            if prev is not None and c.timestamp < prev:
                raise ValueError("candles must be non-decreasing in time")
            prev = c.timestamp

    # -- progress / metrics --------------------------------------------
    def progress(self, now: Optional[datetime] = None) -> BootstrapProgress:
        total = len(self._timeframes)
        ready = sum(1 for s in self._states.values()
                    if s is BootstrapState.READY)
        remaining = [tf for tf in self._timeframes
                     if self._states[tf] is not BootstrapState.READY]
        return BootstrapProgress(
            asset=self._memory.asset,
            status=self._aggregate_status(),
            progress_pct=(100.0 * ready / total) if total else 100.0,
            current_timeframe=self._current_tf,
            remaining=remaining,
            started_at=self._started_at,
            finished_at=self._finished_at,
        )

    def metrics(self) -> BootstrapMetrics:
        return self._metrics

    def _all_ready(self) -> bool:
        return all(s is BootstrapState.READY for s in self._states.values())

    def _aggregate_status(self) -> BootstrapState:
        states = set(self._states.values())
        if self._all_ready():
            return BootstrapState.READY
        if self._cancelled or BootstrapState.CANCELLED in states:
            return BootstrapState.CANCELLED
        if BootstrapState.FAILED in states:
            return BootstrapState.FAILED
        if states & {BootstrapState.LOADING, BootstrapState.VALIDATING,
                     BootstrapState.HYDRATING} or self._started_at is not None:
            return BootstrapState.LOADING
        return BootstrapState.PENDING

    @staticmethod
    def _utc(now: datetime) -> datetime:
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise ValueError("now must be a timezone-aware datetime (UTC)")
        return now.astimezone(timezone.utc)
