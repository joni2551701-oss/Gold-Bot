"""
Phase 60.5, TASK 8 -- platform_layer/telegram/owner/fundamental_commands.py tests.
No mocks: real FundamentalContextSnapshot/FundamentalScoreResult
construction, same convention as every other platform_layer/telegram/owner/ test.
"""

from context_layer.fundamental.fundamental_context import compute_fundamental_context, merge_fundamental_score
from context_layer.fundamental.fundamental_scoring import compute_fundamental_score
from data_layer.providers.fundamental_base import FundamentalDataPoint
from datetime import datetime, timezone

from platform_layer.telegram.owner.fundamental_commands import get_fed_status, get_fundamental_score_report, get_macro_status
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def test_get_macro_status_returns_a_report():
    score = compute_fundamental_score(dxy_bias="BULLISH", fed_expectation="HAWKISH")
    fundamental = merge_fundamental_score(compute_fundamental_context(), score)

    result = get_macro_status(fundamental)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "BULLISH" in result.message
    assert "HAWKISH" in result.message


def test_get_macro_status_never_raises_on_all_none_snapshot():
    fundamental = compute_fundamental_context()

    result = get_macro_status(fundamental)

    assert result.success is True
    assert "unknown" in result.message


def test_get_fundamental_score_report_returns_a_report():
    score = compute_fundamental_score(dxy_bias="BULLISH", rates_bias="BULLISH")

    result = get_fundamental_score_report(score)

    assert result.success is True
    assert "Macro Bias:" in result.message
    assert "Reasons:" in result.message


def test_get_fed_status_reports_fed_rate_and_expectation():
    point = FundamentalDataPoint(
        series_id="FEDFUNDS", value=5.25, unit="percent",
        as_of=datetime(2026, 1, 1, tzinfo=timezone.utc), source="fred",
    )
    snapshot = compute_fundamental_context(interest_rate=point)
    score = compute_fundamental_score(fed_expectation="DOVISH")
    fundamental = merge_fundamental_score(snapshot, score)

    result = get_fed_status(fundamental)

    assert result.success is True
    assert "5.25%" in result.message
    assert "DOVISH" in result.message


def test_get_fed_status_never_raises_on_unknown_fed_rate():
    fundamental = compute_fundamental_context()

    result = get_fed_status(fundamental)

    assert result.success is True
    assert "unknown" in result.message
