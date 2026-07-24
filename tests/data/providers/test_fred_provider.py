"""
Phase 59.2, TASK 4/9 -- data/providers/fred_provider.py and
fundamental_base.py tests.
"""

from datetime import datetime, timezone

import pytest

from data.providers.base_provider import DataProvider, ProviderStatus
from data.providers.fred_provider import SERIES_INFLATION, SERIES_INTEREST_RATE, SUPPORTED_SERIES, FredProvider
from data.providers.fundamental_base import FundamentalDataPoint, FundamentalDataProvider, FundamentalSnapshot


def test_fred_provider_is_a_fundamental_data_provider():
    assert issubclass(FredProvider, FundamentalDataProvider)


def test_fundamental_data_provider_is_a_data_provider():
    assert issubclass(FundamentalDataProvider, DataProvider)


def test_get_provider_name_returns_fred():
    provider = FredProvider()
    assert provider.get_provider_name() == "fred"


def test_get_market_status_always_unavailable_and_never_raises():
    provider = FredProvider()
    status = provider.get_market_status()
    assert isinstance(status, ProviderStatus)
    assert status.available is False


@pytest.mark.parametrize("series_id", SUPPORTED_SERIES)
def test_get_macro_indicator_raises_not_implemented_for_supported_series(series_id):
    provider = FredProvider()
    with pytest.raises(NotImplementedError):
        provider.get_macro_indicator(series_id)


def test_get_macro_indicator_raises_value_error_for_unsupported_series():
    provider = FredProvider()
    with pytest.raises(ValueError):
        provider.get_macro_indicator("NOT_A_REAL_SERIES")


def test_get_interest_rate_raises_not_implemented():
    provider = FredProvider()
    with pytest.raises(NotImplementedError):
        provider.get_interest_rate()


def test_get_inflation_data_raises_not_implemented():
    provider = FredProvider()
    with pytest.raises(NotImplementedError):
        provider.get_inflation_data()


def test_series_ids_are_the_real_verified_fred_codes():
    assert SERIES_INTEREST_RATE == "FEDFUNDS"
    assert SERIES_INFLATION == "CPIAUCSL"


# --- FundamentalDataPoint / FundamentalSnapshot ---

def test_fundamental_data_point_to_dict_is_json_safe():
    import json

    point = FundamentalDataPoint(
        series_id="FEDFUNDS", value=5.25, unit="percent",
        as_of=datetime(2026, 1, 1, tzinfo=timezone.utc), source="fred",
    )
    data = point.to_dict()
    json.dumps(data)  # must not raise
    assert isinstance(data["as_of"], str)


def test_fundamental_snapshot_defaults_to_empty_indicators():
    snapshot = FundamentalSnapshot(snapshot_id="snap-1", created_at=datetime.now(timezone.utc))
    assert snapshot.indicators == {}


def test_fundamental_snapshot_to_dict_serializes_nested_points():
    import json

    point = FundamentalDataPoint(
        series_id="CPIAUCSL", value=310.3, unit="index",
        as_of=datetime(2026, 1, 1, tzinfo=timezone.utc), source="fred",
    )
    snapshot = FundamentalSnapshot(
        snapshot_id="snap-1",
        created_at=datetime.now(timezone.utc),
        indicators={"cpi": point},
    )
    data = snapshot.to_dict()
    json.dumps(data)  # must not raise
    assert data["indicators"]["cpi"]["series_id"] == "CPIAUCSL"


# --- Phase 60.5 TASK 3: collect_snapshot() ---

def test_collect_snapshot_returns_a_real_snapshot_never_raises():
    provider = FredProvider()

    snapshot = provider.collect_snapshot()  # must not raise, even though every fetch is NotImplementedError today

    assert isinstance(snapshot, FundamentalSnapshot)
    assert snapshot.indicators == {}
    assert snapshot.snapshot_id
    assert snapshot.created_at is not None


def test_collect_snapshot_only_includes_successfully_fetched_indicators(monkeypatch):
    provider = FredProvider()
    point = FundamentalDataPoint(
        series_id="FEDFUNDS", value=5.25, unit="percent",
        as_of=datetime(2026, 1, 1, tzinfo=timezone.utc), source="fred",
    )
    monkeypatch.setattr(provider, "get_interest_rate", lambda: point)

    snapshot = provider.collect_snapshot()

    assert snapshot.indicators == {"interest_rate": point}


def test_collect_snapshot_keys_are_logical_names_not_series_ids():
    provider = FredProvider()

    snapshot = provider.collect_snapshot()

    for key in snapshot.indicators:
        assert key in ("interest_rate", "inflation", "dollar_index")


def test_fred_provider_never_generates_a_signal_or_knows_strategy():
    provider = FredProvider()
    forbidden_terms = ("signal", "strategy", "decision")
    for attr in dir(provider):
        if attr.startswith("_"):
            continue
        assert not any(term in attr.lower() for term in forbidden_terms), attr
