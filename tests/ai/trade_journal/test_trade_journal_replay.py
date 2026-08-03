"""
Phase 66.2 TASK 3/9 — ReplayContext-specific tests, separated from
test_trade_journal_models.py per TASK 9's own explicit test category
list ("Models, Runtime, Replay, Integration, Isolation, Trading Core
ZERO DIFF").
"""

from ai_layer.knowledge_ai.knowledge_base.trade_journal.models import ReplayContext


def test_replay_context_trade_id_and_chart_id_required():
    ctx = ReplayContext(trade_id="t1", chart_id="c1")
    assert ctx.trade_id == "t1"
    assert ctx.chart_id == "c1"


def test_replay_context_default_sequence_is_zero():
    ctx = ReplayContext(trade_id="t1", chart_id="c1")
    assert ctx.sequence == 0


def test_replay_context_sequence_orders_a_timeline():
    points = [ReplayContext(trade_id="t1", chart_id="c1", sequence=i) for i in range(5)]
    assert [p.sequence for p in points] == [0, 1, 2, 3, 4]


def test_replay_context_snapshot_id_is_optional_string_reference():
    ctx = ReplayContext(trade_id="t1", chart_id="c1", snapshot_id="snap_42")
    assert ctx.snapshot_id == "snap_42"


def test_replay_context_comment_is_free_text():
    ctx = ReplayContext(trade_id="t1", chart_id="c1", comment="price rejected at OB")
    assert ctx.comment == "price rejected at OB"


def test_replay_context_multiple_points_share_trade_and_chart_link():
    a = ReplayContext(trade_id="t1", chart_id="c1", sequence=0)
    b = ReplayContext(trade_id="t1", chart_id="c1", sequence=1)
    assert a.trade_id == b.trade_id
    assert a.chart_id == b.chart_id
    assert a.sequence != b.sequence


def test_replay_context_no_video_field():
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(ReplayContext)}
    assert "video" not in field_names
    assert "screenshot" not in field_names
    assert "animation" not in field_names


def test_replay_context_equality():
    a = ReplayContext(trade_id="t1", chart_id="c1", sequence=0)
    b = ReplayContext(trade_id="t1", chart_id="c1", sequence=0)
    assert a == b
