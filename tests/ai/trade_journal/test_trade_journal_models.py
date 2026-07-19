import dataclasses

from ai.trade_journal.models import ReplayContext, TradeJournalEntry, generate_journal_id


def _entry(**overrides):
    defaults = dict(
        journal_id="j1", chart_id="chart_1", trade_id="trade_1", symbol="XAUUSD",
        timeframe="H4", direction="BUY",
    )
    defaults.update(overrides)
    return TradeJournalEntry(**defaults)


def test_trade_journal_entry_defaults():
    entry = _entry()
    assert entry.entry is None
    assert entry.sl is None
    assert entry.tp is None
    assert entry.result is None
    assert entry.confidence is None
    assert entry.reason is None
    assert entry.lesson is None
    assert entry.mistakes == ()
    assert entry.created_at == ""


def test_trade_journal_entry_is_frozen():
    entry = _entry()
    try:
        entry.symbol = "EURUSD"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_trade_journal_entry_accepts_all_fields():
    entry = _entry(
        entry=3400.0, sl=3390.0, tp=3420.0, result="WIN", confidence=0.8,
        reason="H4 BOS", lesson="wait for retest", mistakes=["entered early"],
        created_at="2026-01-01T00:00:00Z",
    )
    assert entry.entry == 3400.0
    assert entry.sl == 3390.0
    assert entry.tp == 3420.0
    assert entry.result == "WIN"
    assert entry.confidence == 0.8
    assert entry.reason == "H4 BOS"
    assert entry.lesson == "wait for retest"
    assert entry.mistakes == ["entered early"]
    assert entry.created_at == "2026-01-01T00:00:00Z"


def test_trade_journal_entry_field_names_match_task_2_contract():
    field_names = {f.name for f in dataclasses.fields(TradeJournalEntry)}
    assert field_names == {
        "journal_id", "chart_id", "trade_id", "symbol", "timeframe", "direction",
        "entry", "sl", "tp", "result", "confidence", "reason", "lesson", "mistakes", "created_at",
    }


def test_trade_journal_entry_chart_id_and_trade_id_are_mandatory():
    """Director Note 4: chart_id and trade_id are required positional fields, no default."""
    field_by_name = {f.name: f for f in dataclasses.fields(TradeJournalEntry)}
    assert field_by_name["chart_id"].default is dataclasses.MISSING
    assert field_by_name["trade_id"].default is dataclasses.MISSING


def test_trade_journal_entry_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(TradeJournalEntry)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_trade_journal_entry_mistakes_is_sequence():
    entry = _entry(mistakes=("late entry", "no stop discipline"))
    assert entry.mistakes == ("late entry", "no stop discipline")


def test_trade_journal_entry_equality():
    a = _entry()
    b = _entry()
    assert a == b


def test_trade_journal_entry_inequality_on_journal_id():
    a = _entry(journal_id="j1")
    b = _entry(journal_id="j2")
    assert a != b


def test_trade_journal_entry_relays_direction_never_computes():
    for direction in ("BUY", "SELL", "WAIT", "SKIP"):
        entry = _entry(direction=direction)
        assert entry.direction == direction


def test_trade_journal_entry_confidence_relayed_as_is_no_scale_conversion():
    """Rule 4: Journal never transforms confidence -- 0-100, 0-1, or any value is stored verbatim."""
    entry = _entry(confidence=82.0)
    assert entry.confidence == 82.0
    entry2 = _entry(confidence=0.82)
    assert entry2.confidence == 0.82


def test_replay_context_defaults():
    ctx = ReplayContext(trade_id="t1", chart_id="c1")
    assert ctx.snapshot_id is None
    assert ctx.comment is None
    assert ctx.sequence == 0


def test_replay_context_is_frozen():
    ctx = ReplayContext(trade_id="t1", chart_id="c1")
    try:
        ctx.trade_id = "t2"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_replay_context_field_names_match_task_3_contract():
    field_names = {f.name for f in dataclasses.fields(ReplayContext)}
    assert field_names == {"trade_id", "chart_id", "snapshot_id", "comment", "sequence"}


def test_replay_context_never_stores_media_bytes():
    """Director Note 3: no field on ReplayContext carries video/image/binary data."""
    for f in dataclasses.fields(ReplayContext):
        assert "bytes" not in str(f.type).lower()
        assert "binary" not in str(f.type).lower()
        assert "video" not in f.name.lower()
        assert "image" not in f.name.lower()


def test_replay_context_accepts_full_metadata():
    ctx = ReplayContext(trade_id="t1", chart_id="c1", snapshot_id="snap_1", comment="entry point", sequence=3)
    assert ctx.snapshot_id == "snap_1"
    assert ctx.comment == "entry point"
    assert ctx.sequence == 3


def test_generate_journal_id_returns_string():
    journal_id = generate_journal_id()
    assert isinstance(journal_id, str)
    assert journal_id != ""


def test_generate_journal_id_unique():
    ids = {generate_journal_id() for _ in range(20)}
    assert len(ids) == 20


def test_trade_journal_entry_symbol_timeframe_direction_required():
    field_by_name = {f.name: f for f in dataclasses.fields(TradeJournalEntry)}
    for required in ("journal_id", "symbol", "timeframe", "direction"):
        assert field_by_name[required].default is dataclasses.MISSING
