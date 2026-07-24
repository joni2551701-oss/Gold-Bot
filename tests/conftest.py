import os

import pytest

# Forced (not setdefault): several tests hardcode "111" as the OWNER
# telegram_id (matching this value). setdefault() would silently lose
# to a pre-existing TELEGRAM_OWNER_ID in the calling shell/CI
# environment, breaking every OWNER-permission test in a way that's
# hard to diagnose (found during Phase 47.1 CI validation -- the first
# draft of .github/workflows/ci.yml set TELEGRAM_OWNER_ID=1 and broke
# 5 tests silently). The test suite must be deterministic regardless
# of ambient environment state.
os.environ["TELEGRAM_BOT_TOKEN"] = "123456789:AAFakeTestTokenForPytestOnly000"
os.environ["TELEGRAM_CHAT_ID"] = "999999"
os.environ["TELEGRAM_OWNER_ID"] = "111"
os.environ["TWELVE_DATA_API_KEY"] = "unused"
os.environ["GEMINI_API_KEY"] = "unused"

import config  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database(tmp_path):
    """
    Points config.Config.DB_PATH at a fresh SQLite file per test, so
    every test starts from a clean, isolated database -- none of them
    can pollute another test or the repo's real database/goldbot.db.
    """
    config.Config.DB_PATH = str(tmp_path / "test.db")
    yield


# ---------------------------------------------------------------------------
# Phase 52 shared fixtures. Every fixture below builds real rows through the
# real service/repository layer (never hand-crafted SQL) so a fixture can
# never drift out of sync with the schema/service contracts it represents.
# Each test gets its own fresh_database (above), so these telegram_ids never
# collide across tests even though several fixtures reuse simple values.
# ---------------------------------------------------------------------------

@pytest.fixture
def test_user():
    """A freshly registered FREE-plan user. Returns the UserRecord."""
    from telegram.user_service import UserService

    result = UserService().register_user("8001", username="fixture_user")
    assert result.success is True
    return result.profile


@pytest.fixture
def premium_user():
    """A registered user with an active PREMIUM subscription."""
    from telegram.user_service import UserService
    from telegram.subscription_service import SubscriptionService
    from database.subscription_repository import SubscriptionRepository

    telegram_id = "8002"
    UserService().register_user(telegram_id, username="fixture_premium")
    SubscriptionService().get_plan(telegram_id)  # lazily creates the FREE row
    SubscriptionRepository().update_plan(telegram_id, "PREMIUM")
    return telegram_id


@pytest.fixture
def vip_user():
    """A registered user with an active VIP subscription."""
    from telegram.user_service import UserService
    from telegram.subscription_service import SubscriptionService
    from database.subscription_repository import SubscriptionRepository

    telegram_id = "8003"
    UserService().register_user(telegram_id, username="fixture_vip")
    SubscriptionService().get_plan(telegram_id)
    SubscriptionRepository().update_plan(telegram_id, "VIP")
    return telegram_id


@pytest.fixture
def admin_user():
    """A registered user who is also an ADMIN (not OWNER)."""
    from telegram.user_service import UserService
    from database.admin_repository import AdminRepository

    telegram_id = "8004"
    UserService().register_user(telegram_id, username="fixture_admin")
    AdminRepository().add_admin(telegram_id)
    return telegram_id


@pytest.fixture
def owner_user():
    """
    The configured OWNER. Uses TELEGRAM_OWNER_ID ("111", set above) --
    OWNER status comes from that env var alone (core/secrets.py /
    telegram/permissions.py), never from an 'admins' table row.
    """
    from telegram.user_service import UserService

    telegram_id = "111"
    UserService().register_user(telegram_id, username="fixture_owner")
    return telegram_id


@pytest.fixture
def mock_signal_candidate():
    """
    Factory fixture: mock_signal_candidate(signal_type=..., entry=...,
    stop_loss=..., take_profit=..., confidence=..., strategy_name=...)
    -> SignalCandidate. Defaults produce a geometrically valid BUY.
    """
    from signals.models import SignalCandidate, SignalType

    def _make(
        signal_type=SignalType.BUY,
        entry=4065.0,
        stop_loss=4060.0,
        take_profit=4080.0,
        confidence=0.9,
        strategy_name="FIXTURE_STRATEGY",
    ):
        return SignalCandidate(
            signal_type=signal_type,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            strategy_name=strategy_name,
            confidence=confidence,
            reasons=["fixture candidate"],
        )

    return _make


@pytest.fixture
def mock_pipeline():
    """
    Factory fixture: mock_pipeline(candidates, ai_results) -> a real
    TradingPipeline with only the data-fetch layer stubbed (no live
    Twelve Data / Telegram network calls possible in a test run) --
    every other layer (Decision, Risk, the approve+select filter,
    SignalFormatter, Notifier, SignalRepository) is real, unmodified
    production code. `candidates` is a list[SignalCandidate];
    `ai_results` is a same-length list[AIAnalysisResult].
    """
    from core.pipeline import TradingPipeline
    from data.market_data import MarketSnapshot

    def _make(candidates, ai_results):
        pipeline = TradingPipeline(
            symbol="XAUUSD", interval="M15", outputsize=200,
            send_notifications=True, persist_signals=True,
        )
        pipeline.signal_engine.generate_signals = lambda context: candidates
        pipeline.data_normalizer.get_candles = lambda *a, **k: []
        # Phase A2: run() also fetches an HTF (Daily/H4/H1) snapshot
        # independently of get_candles() above -- stub it too so this
        # fixture's "no live network calls" guarantee still holds.
        pipeline.data_normalizer.get_snapshot = lambda *a, **k: MarketSnapshot(symbol="XAUUSD")
        results_iter = iter(ai_results)
        pipeline.ai_analyzer.analyze = lambda candidate, context: next(results_iter)
        return pipeline

    return _make


@pytest.fixture
def mock_ai_result():
    """
    Factory fixture: mock_ai_result(approved=..., confidence=...,
    risk_score=..., explanation=...) -> AIAnalysisResult.
    """
    from ai.ai_analyzer import AIAnalysisResult

    def _make(approved=True, confidence=0.9, risk_score=0.1, explanation="fixture"):
        return AIAnalysisResult(
            approved=approved, confidence=confidence,
            risk_score=risk_score, explanation=explanation,
        )

    return _make
