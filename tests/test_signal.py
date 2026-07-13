"""
Phase 47 — Signal Layer tests: persistence, service read paths, history.

No Signal Engine / AI / Decision / Risk logic is exercised here -- only
the database -> SignalRepository -> SignalService -> SignalFormatter
chain that the Telegram layer depends on.
"""


def _seed_signal(signal_id="sig-1", confidence=0.8):
    from database.signal_repository import SignalRepository

    repo = SignalRepository()
    repo.create_signal({
        "signal_id": signal_id,
        "symbol": "XAUUSD",
        "direction": "BUY",
        "entry_zone_min": 2000.0,
        "entry_zone_max": 2000.0,
        "stop_loss": 1990.0,
        "take_profit_1": 2030.0,
        "take_profit_2": 0.0,
        "risk_percent": 0.0,
        "lot_size": 0.0,
        "strategy_name": "Liquidity Sweep",
        "strategy": "Liquidity Sweep",
        "confidence_score": confidence,
        "ai_explanation": "test",
    })
    return repo


def test_signal_service_get_latest_signal():
    from telegram.signal_service import SignalService

    _seed_signal()
    result = SignalService().get_latest_signal()
    assert result.success is True
    assert result.signal["signal_id"] == "sig-1"


def test_signal_service_get_latest_signal_empty_database():
    from telegram.signal_service import SignalService

    result = SignalService().get_latest_signal()
    assert result.success is False
    assert result.reason == "No active signal available."


def test_signal_service_history_returns_newest_first():
    from telegram.signal_service import SignalService

    repo = _seed_signal("sig-1")
    repo.create_signal({
        "signal_id": "sig-2", "symbol": "XAUUSD", "direction": "SELL",
        "entry_zone_min": 2010.0, "entry_zone_max": 2010.0, "stop_loss": 2020.0,
        "take_profit_1": 1990.0, "take_profit_2": 0.0, "risk_percent": 0.0,
        "lot_size": 0.0, "strategy_name": "FVG", "confidence_score": 0.6,
        "ai_explanation": "test",
    })

    result = SignalService().get_signal_history(limit=5)
    assert result.success is True
    assert len(result.signals) == 2
    assert result.signals[0]["signal_id"] == "sig-2"  # most recently created


def test_signal_formatter_renders_row_with_all_phase39_fields():
    from telegram.signal_formatter import SignalFormatter
    from telegram.signal_service import SignalService

    _seed_signal()
    row = SignalService().get_latest_signal().signal
    text = SignalFormatter().format_signal_row(row)

    assert "GOLD SIGNAL" in text
    assert "Symbol:\nXAUUSD" in text
    assert "Strategy:\nLiquidity Sweep" in text
    assert "Confidence:\n80%" in text


def test_signal_access_free_plan_denied_premium_allowed():
    """Save signal exists, but a FREE user is denied delivery via SignalAccessService."""
    from telegram.signal_access_service import SignalAccessService
    from telegram.subscription_service import SubscriptionService

    _seed_signal()
    access = SignalAccessService()

    assert access.can_access_signal("7001") is False  # default FREE plan

    SubscriptionService().get_plan("7001")  # ensure subscription row exists
    from database.subscription_repository import SubscriptionRepository
    SubscriptionRepository().update_plan("7001", "PREMIUM")

    assert access.can_access_signal("7001") is True
