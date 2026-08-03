from ai.access.permissions import AIRole
from ai.trade_journal.journal_runtime import TradeJournalRuntime
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_trade_journal=True)
DISABLED = FeatureFlags(enable_trade_journal=False)


def _runtime(flags=ENABLED):
    return TradeJournalRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(
        chart_id="chart_1", trade_id="trade_1", symbol="XAUUSD", timeframe="H4",
        direction="BUY", role=AIRole.OWNER,
    )
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.symbol == "XAUUSD"
    assert result.chart_id == "chart_1"
    assert result.trade_id == "trade_1"


def test_create_admin_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.ADMIN) is None


def test_create_vip_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.VIP) is None


def test_create_premium_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.PREMIUM) is None


def test_create_free_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.FREE) is None


def test_create_blocked_when_flag_disabled_even_for_owner():
    runtime = _runtime(flags=DISABLED)
    assert _create(runtime) is None


def test_create_generates_unique_journal_id():
    runtime = _runtime()
    a = _create(runtime)
    b = _create(runtime)
    assert a.journal_id != b.journal_id


def test_create_stamps_created_at():
    runtime = _runtime()
    result = _create(runtime)
    assert result.created_at != ""


def test_create_relays_entry_sl_tp():
    runtime = _runtime()
    result = _create(runtime, entry=3400.0, sl=3390.0, tp=3420.0)
    assert result.entry == 3400.0
    assert result.sl == 3390.0
    assert result.tp == 3420.0


def test_create_relays_result_confidence_reason_lesson_mistakes():
    runtime = _runtime()
    result = _create(
        runtime, result="WIN", confidence=0.8, reason="H4 BOS",
        lesson="wait for retest", mistakes=["entered early"],
    )
    assert result.result == "WIN"
    assert result.confidence == 0.8
    assert result.reason == "H4 BOS"
    assert result.lesson == "wait for retest"
    assert result.mistakes == ("entered early",)


def test_create_never_produces_buy_sell_verdict_of_its_own():
    """Rule 2: create() only relays the caller-supplied direction, never computes one."""
    runtime = _runtime()
    for direction in ("BUY", "SELL", "WAIT", "SKIP"):
        result = _create(runtime, direction=direction)
        assert result.direction == direction


def test_get_owner_succeeds():
    runtime = _runtime()
    created = _create(runtime)
    fetched = runtime.get(created.journal_id, AIRole.OWNER)
    assert fetched == created


def test_get_unknown_journal_id_returns_none():
    runtime = _runtime()
    assert runtime.get("does-not-exist", AIRole.OWNER) is None


def test_get_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.get(created.journal_id, AIRole.ADMIN) is None


def test_get_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.get(created.journal_id, AIRole.OWNER) is None


def test_list_returns_all_created_entries():
    runtime = _runtime()
    a = _create(runtime, trade_id="t1")
    b = _create(runtime, trade_id="t2")
    listed = runtime.list(AIRole.OWNER)
    assert set(listed) == {a, b}


def test_list_empty_when_nothing_created():
    runtime = _runtime()
    assert runtime.list(AIRole.OWNER) == ()


def test_list_admin_blocked_returns_empty_tuple():
    runtime = _runtime()
    _create(runtime)
    assert runtime.list(AIRole.ADMIN) == ()


def test_list_blocked_when_flag_disabled():
    runtime = _runtime()
    _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.list(AIRole.OWNER) == ()


def test_update_notes_updates_reason():
    runtime = _runtime()
    created = _create(runtime, reason="initial reason")
    updated = runtime.update_notes(created.journal_id, AIRole.OWNER, reason="revised reason")
    assert updated.reason == "revised reason"


def test_update_notes_updates_lesson():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_notes(created.journal_id, AIRole.OWNER, lesson="new lesson")
    assert updated.lesson == "new lesson"


def test_update_notes_updates_mistakes():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_notes(created.journal_id, AIRole.OWNER, mistakes=["late entry"])
    assert updated.mistakes == ("late entry",)


def test_update_notes_leaves_unspecified_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, reason="original", lesson="original lesson")
    updated = runtime.update_notes(created.journal_id, AIRole.OWNER, mistakes=["x"])
    assert updated.reason == "original"
    assert updated.lesson == "original lesson"


def test_update_notes_never_changes_chart_id_trade_id_direction():
    """TASK 4's own narrow scope: only reason/lesson/mistakes are updatable."""
    runtime = _runtime()
    created = _create(runtime, chart_id="chart_x", trade_id="trade_x", direction="SELL")
    updated = runtime.update_notes(created.journal_id, AIRole.OWNER, reason="updated")
    assert updated.chart_id == "chart_x"
    assert updated.trade_id == "trade_x"
    assert updated.direction == "SELL"


def test_update_notes_unknown_journal_id_returns_none():
    runtime = _runtime()
    assert runtime.update_notes("does-not-exist", AIRole.OWNER, reason="x") is None


def test_update_notes_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update_notes(created.journal_id, AIRole.ADMIN, reason="x") is None


def test_update_notes_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update_notes(created.journal_id, AIRole.OWNER, reason="x") is None


def test_update_notes_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update_notes(created.journal_id, AIRole.OWNER, lesson="persisted lesson")
    fetched = runtime.get(created.journal_id, AIRole.OWNER)
    assert fetched.lesson == "persisted lesson"


def test_runtime_default_construction_never_raises():
    assert TradeJournalRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, trade_id=f"trade_{role.value}")
        assert result is None or result.symbol == "XAUUSD"


def test_multiple_entries_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, trade_id="t1", symbol="XAUUSD")
    b = _create(runtime, trade_id="t2", symbol="EURUSD")
    assert runtime.get(a.journal_id, AIRole.OWNER).symbol == "XAUUSD"
    assert runtime.get(b.journal_id, AIRole.OWNER).symbol == "EURUSD"


def test_runtime_never_computes_analytics():
    """Rule 4: TradeJournalRuntime has no method beyond create/get/list/update_notes."""
    runtime = TradeJournalRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "update_notes"}
