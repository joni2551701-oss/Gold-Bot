from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.trading_analyst.access import is_trading_analyst_enabled_for
from core_layer.configuration.feature_flags import FeatureFlags


def test_owner_allowed_when_flag_on():
    flags = FeatureFlags(enable_trading_analyst=True)
    assert is_trading_analyst_enabled_for(AIRole.OWNER, flags) is True


def test_owner_blocked_when_flag_off():
    flags = FeatureFlags(enable_trading_analyst=False)
    assert is_trading_analyst_enabled_for(AIRole.OWNER, flags) is False


def test_admin_blocked_even_when_flag_on():
    flags = FeatureFlags(enable_trading_analyst=True)
    assert is_trading_analyst_enabled_for(AIRole.ADMIN, flags) is False


def test_vip_blocked_even_when_flag_on():
    flags = FeatureFlags(enable_trading_analyst=True)
    assert is_trading_analyst_enabled_for(AIRole.VIP, flags) is False


def test_premium_blocked_even_when_flag_on():
    flags = FeatureFlags(enable_trading_analyst=True)
    assert is_trading_analyst_enabled_for(AIRole.PREMIUM, flags) is False


def test_free_blocked_even_when_flag_on():
    flags = FeatureFlags(enable_trading_analyst=True)
    assert is_trading_analyst_enabled_for(AIRole.FREE, flags) is False


def test_default_flags_instance_has_trading_analyst_disabled():
    assert FeatureFlags().enable_trading_analyst is False


def test_is_trading_analyst_enabled_for_uses_default_flags_when_omitted():
    assert is_trading_analyst_enabled_for(AIRole.OWNER) is False
