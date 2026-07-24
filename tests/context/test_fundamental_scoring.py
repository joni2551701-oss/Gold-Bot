"""
Phase 60.5: Fundamental Intelligence Foundation, TASK 5 --
context/fundamental_scoring.py tests.
"""

from context.fundamental_scoring import (
    FundamentalScoreResult,
    FundamentalScoreWeights,
    compute_fundamental_score,
    explain_fundamental_score,
    format_fundamental_score,
)


def test_no_inputs_produces_a_fully_neutral_result():
    result = compute_fundamental_score()

    assert isinstance(result, FundamentalScoreResult)
    assert result.macro_score == 50.0
    assert result.gold_bias == "NEUTRAL"
    assert result.confidence == 0.0


def test_all_bullish_produces_the_maximum_score():
    result = compute_fundamental_score(
        dxy_bias="BULLISH", rates_bias="BULLISH", inflation_bias="BULLISH", risk_sentiment="BULLISH"
    )

    assert result.macro_score == 100.0
    assert result.gold_bias == "BULLISH"
    assert result.confidence == 100.0


def test_all_bearish_produces_the_minimum_score():
    result = compute_fundamental_score(
        dxy_bias="BEARISH", rates_bias="BEARISH", inflation_bias="BEARISH", risk_sentiment="BEARISH"
    )

    assert result.macro_score == 0.0
    assert result.gold_bias == "BEARISH"
    assert result.confidence == 100.0


def test_mixed_biases_partially_cancel():
    result = compute_fundamental_score(dxy_bias="BULLISH", rates_bias="BEARISH")

    weights = FundamentalScoreWeights()
    raw = weights.dxy - weights.rates
    max_raw = weights.dxy + weights.rates + weights.inflation + weights.risk
    expected = 50.0 + (raw / max_raw) * 50.0
    assert round(result.macro_score, 6) == round(expected, 6)


def test_unrecognized_bias_string_contributes_nothing():
    result = compute_fundamental_score(dxy_bias="UNKNOWN")

    assert result.macro_score == 50.0


def test_fed_expectation_is_carried_through_but_not_scored():
    neutral = compute_fundamental_score(fed_expectation="HAWKISH")
    with_bias = compute_fundamental_score(dxy_bias="BULLISH", fed_expectation="HAWKISH")

    assert neutral.macro_score == 50.0
    assert neutral.fed_expectation == "HAWKISH"
    assert with_bias.fed_expectation == "HAWKISH"


def test_inputs_are_carried_through_unchanged():
    result = compute_fundamental_score(
        dxy_bias="BEARISH", rates_bias="BULLISH", inflation_bias="NEUTRAL", risk_sentiment="BULLISH"
    )

    assert result.dxy_bias == "BEARISH"
    assert result.rates_bias == "BULLISH"
    assert result.inflation_bias == "NEUTRAL"
    assert result.risk_sentiment == "BULLISH"


def test_gold_bias_thresholds_around_neutral_band():
    # A single BULLISH inflation_bias (weight 10/60) nudges the score up but not past the 60 threshold.
    result = compute_fundamental_score(inflation_bias="BULLISH")

    assert 50.0 < result.macro_score < 60.0
    assert result.gold_bias == "NEUTRAL"


def test_custom_weights_are_respected():
    weights = FundamentalScoreWeights(dxy=100.0, rates=0.0, inflation=0.0, risk=0.0)

    result = compute_fundamental_score(dxy_bias="BEARISH", weights=weights)

    assert result.macro_score == 0.0
    assert result.gold_bias == "BEARISH"


def test_never_raises_with_zero_weight_config():
    weights = FundamentalScoreWeights(dxy=0.0, rates=0.0, inflation=0.0, risk=0.0)

    result = compute_fundamental_score(dxy_bias="BULLISH", weights=weights)  # must not raise (max_raw == 0)

    assert result.macro_score == 50.0


# --- Phase 60.5 TASK 8 support: explain_fundamental_score() / format_fundamental_score() ---

def test_explain_fundamental_score_empty_for_fully_neutral_result():
    result = compute_fundamental_score()

    assert explain_fundamental_score(result) == []


def test_explain_fundamental_score_skips_none_and_neutral_components():
    result = compute_fundamental_score(dxy_bias="BULLISH", rates_bias="NEUTRAL", inflation_bias=None)

    reasons = explain_fundamental_score(result)

    assert reasons == ["DXY: BULLISH"]


def test_explain_fundamental_score_follows_fixed_component_order():
    result = compute_fundamental_score(
        risk_sentiment="BULLISH", dxy_bias="BEARISH", inflation_bias="BULLISH", rates_bias="BEARISH"
    )

    reasons = explain_fundamental_score(result)

    assert reasons == ["DXY: BEARISH", "Rates: BEARISH", "Inflation: BULLISH", "Risk sentiment: BULLISH"]


def test_format_fundamental_score_matches_the_directors_worked_example_shape():
    result = compute_fundamental_score(
        dxy_bias="BULLISH", rates_bias="BULLISH", inflation_bias="BULLISH", risk_sentiment="BULLISH"
    )

    text = format_fundamental_score(result)

    assert "Macro Bias:" in text
    assert "BULLISH GOLD" in text
    assert "Confidence:" in text
    assert "100%" in text
    assert "Reasons:" in text
    assert "- DXY: BULLISH" in text


def test_format_fundamental_score_neutral_has_no_gold_suffix():
    result = compute_fundamental_score()

    text = format_fundamental_score(result)

    assert "NEUTRAL" in text
    assert "NEUTRAL GOLD" not in text


def test_format_fundamental_score_never_raises_with_no_reasons():
    result = compute_fundamental_score()

    text = format_fundamental_score(result)  # must not raise

    assert "Reasons:" in text
