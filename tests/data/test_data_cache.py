"""
Phase 59.3, TASK 3 -- data_layer/market_memory/data_cache.py (SmartDataCache) test
coverage.

Audit finding this closes: SmartDataCache already provides exactly
what TASK 3 (Market Data Cache) asks for -- duplicate API call
reduction (per-symbol/interval caching, expiring at the next candle's
open time) and rate-limit protection (a daily request-count warning at
DAILY_WARNING_LIMIT) -- but had zero test coverage anywhere in this
repository, and is not called from core/pipeline.py or any other
module. No data/cache/market_cache.py was built to duplicate it; this
file only closes the test-coverage gap. See docs/PROVIDER_CONTRACTS.md's
Phase 59.3 section for the full "Already implemented — verified" note.

Isolation note: SmartDataCache.__init__ reads Config.BASE_DIR directly
(not Config.DB_PATH, so tests/conftest.py's autouse fresh_database
fixture does NOT isolate it) to build its own state-file path
(<BASE_DIR>/data/.cache_state.json). Every test below monkeypatches
Config.BASE_DIR to pytest's own tmp_path BEFORE constructing
SmartDataCache, so no test ever reads or writes this repository's real
data/.cache_state.json file.
"""

from datetime import datetime, timedelta, timezone

from config import Config
from data_layer.market_memory.data_cache import SmartDataCache
from data_layer.live_data.market_data import MarketSnapshot
from data_layer.providers.twelve_data_client import Candle


def _cache(tmp_path, monkeypatch) -> SmartDataCache:
    monkeypatch.setattr(Config, "BASE_DIR", str(tmp_path))
    return SmartDataCache()


def _snapshot(symbol="XAUUSD", interval="M15"):
    candle = Candle(
        timestamp=datetime.now(timezone.utc), open=2000.0, high=2005.0, low=1995.0, close=2001.0
    )
    return MarketSnapshot(symbol=symbol, candles={interval: [candle]}, quality={interval: "OK"})


def test_fresh_cache_has_no_state_file_yet(tmp_path, monkeypatch):
    cache = _cache(tmp_path, monkeypatch)
    assert cache.cache == {}
    assert cache.request_count == 0


def test_cache_miss_fetches_from_normalizer(tmp_path, monkeypatch):
    cache = _cache(tmp_path, monkeypatch)
    calls = []

    def fake_get_snapshot(symbol, intervals):
        calls.append((symbol, intervals))
        return _snapshot(symbol, intervals[0])

    monkeypatch.setattr(cache.normalizer, "get_snapshot", fake_get_snapshot)

    result = cache.get_cached_snapshot("XAUUSD", ["M15"])

    assert len(calls) == 1
    assert isinstance(result, MarketSnapshot)
    assert result.quality["M15"] == "OK"


def test_cache_hit_does_not_call_normalizer_again(tmp_path, monkeypatch):
    """The whole point of TASK 3: a second request for the same still-fresh window must not re-fetch."""
    cache = _cache(tmp_path, monkeypatch)
    calls = []

    def fake_get_snapshot(symbol, intervals):
        calls.append((symbol, intervals))
        return _snapshot(symbol, intervals[0])

    monkeypatch.setattr(cache.normalizer, "get_snapshot", fake_get_snapshot)

    cache.get_cached_snapshot("XAUUSD", ["M15"])
    cache.get_cached_snapshot("XAUUSD", ["M15"])

    assert len(calls) == 1  # second call was a cache hit


def test_expired_entry_triggers_a_re_fetch(tmp_path, monkeypatch):
    cache = _cache(tmp_path, monkeypatch)
    monkeypatch.setattr(cache.normalizer, "get_snapshot", lambda symbol, intervals: _snapshot(symbol, intervals[0]))

    cache.get_cached_snapshot("XAUUSD", ["M15"])
    # Force the cached entry to already be expired.
    cache.cache["XAUUSD"]["M15"]["expires_at"] = datetime.now(timezone.utc) - timedelta(seconds=1)

    calls = []
    monkeypatch.setattr(cache.normalizer, "get_snapshot", lambda symbol, intervals: (calls.append(1), _snapshot(symbol, intervals[0]))[1])

    cache.get_cached_snapshot("XAUUSD", ["M15"])

    assert len(calls) == 1  # re-fetched because the cached entry had expired


def test_request_count_increments_only_on_a_real_fetch(tmp_path, monkeypatch):
    cache = _cache(tmp_path, monkeypatch)
    monkeypatch.setattr(cache.normalizer, "get_snapshot", lambda symbol, intervals: _snapshot(symbol, intervals[0]))

    cache.get_cached_snapshot("XAUUSD", ["M15"])
    assert cache.request_count == 1

    cache.get_cached_snapshot("XAUUSD", ["M15"])  # cache hit
    assert cache.request_count == 1  # unchanged -- rate-limit protection means no wasted count


def test_save_and_load_state_round_trips(tmp_path, monkeypatch):
    cache = _cache(tmp_path, monkeypatch)
    monkeypatch.setattr(cache.normalizer, "get_snapshot", lambda symbol, intervals: _snapshot(symbol, intervals[0]))
    cache.get_cached_snapshot("XAUUSD", ["M15"])

    reloaded = SmartDataCache()  # Config.BASE_DIR still monkeypatched to the same tmp_path
    assert "XAUUSD" in reloaded.cache
    assert reloaded.request_count == 1


def test_load_state_never_raises_on_corrupt_file(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "BASE_DIR", str(tmp_path))
    state_dir = tmp_path / "data"
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / ".cache_state.json").write_text("{ not valid json")

    cache = SmartDataCache()  # must not raise

    assert cache.cache == {}
    assert cache.request_count == 0


def test_never_touches_the_real_repository_cache_state_file(tmp_path, monkeypatch):
    """Explicit isolation guard -- BASE_DIR is always the tmp_path in these tests, never the real repo root."""
    cache = _cache(tmp_path, monkeypatch)
    assert cache.STATE_FILE.startswith(str(tmp_path))
