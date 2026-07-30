"""Shared helpers for Replay Engine tests (module 8)."""

from datetime import datetime, timezone, timedelta

from data.twelve_data_client import Candle
from data.memory.market_memory import MarketMemory
from data.replay.replay_source import SnapshotReplaySource


def ts(i):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(minutes=i)


def candle(i, close=100.0):
    t = ts(i)
    return Candle(timestamp=t, open=close, high=close, low=close, close=close)


def memory(asset="XAUUSD", cap=100):
    return MarketMemory(asset, {"M1": cap})


def snapshot_source(n=5):
    """A source with contiguous M1 candles 0..n-1."""
    return SnapshotReplaySource({"M1": [candle(i) for i in range(n)]})
