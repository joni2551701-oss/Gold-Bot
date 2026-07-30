"""Shared helpers for Snapshot Infrastructure tests (module 9)."""

from datetime import datetime, timezone, timedelta

from data.twelve_data_client import Candle
from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleSource
from data.persistence.persistent_store import InMemoryStorageBackend
from data.snapshots.manager import SnapshotManager
from data.snapshots.catalog import SnapshotCatalog
from data.snapshots.lifecycle import SnapshotLifecycle


def ts(i, tf_minutes=1):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(
        minutes=i * tf_minutes)


def candle(i, close=100.0, tf_minutes=1):
    t = ts(i, tf_minutes)
    return Candle(timestamp=t, open=close, high=close, low=close, close=close)


def memory_with(asset="XAUUSD", caps=None, m1=5):
    """A MarketMemory hydrated with `m1` contiguous M1 candles."""
    mem = MarketMemory(asset, caps or {"M1": 100})
    mem.timeframe("M1").hydrate([candle(i) for i in range(m1)],
                                source=CandleSource.BOOTSTRAP)
    return mem


def new_backend():
    return InMemoryStorageBackend()


def new_manager(backend=None, bus=None, policy=None):
    return SnapshotManager(backend or new_backend(), bus=bus, policy=policy)


def new_lifecycle(backend=None):
    backend = backend or new_backend()
    return SnapshotLifecycle(backend, SnapshotCatalog(backend))
