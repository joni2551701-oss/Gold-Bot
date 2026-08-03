"""TASK-CORE-004 -- StreamRouter + StreamSubscriber contract + fault isolation."""

from datetime import datetime, timezone

from data_layer.live_data.stream.stream_event import StreamEvent
from data_layer.live_data.stream.stream_router import StreamRouter
from data_layer.live_data.stream.stream_subscriber import CallbackSubscriber, StreamSubscriber


def _event():
    return StreamEvent(symbol="XAUUSD", timeframe="M15",
                       timestamp=datetime(2026, 1, 2, tzinfo=timezone.utc),
                       open=2000.0, high=2010.0, low=1995.0, close=2005.0)


class _Recorder(StreamSubscriber):
    def __init__(self, name):
        self._name = name
        self.received = []

    @property
    def name(self):
        return self._name

    def on_event(self, event):
        self.received.append(event)


class _Boom(StreamSubscriber):
    @property
    def name(self):
        return "boom"

    def on_event(self, event):
        raise RuntimeError("subscriber failure")


def test_subscribe_and_route_delivers():
    router = StreamRouter()
    rec = _Recorder("market")
    router.subscribe(rec)
    result = router.route(_event())
    assert rec.received and result.delivered == ["market"]


def test_multiple_subscribers_all_receive():
    router = StreamRouter()
    a, b = _Recorder("market"), _Recorder("chart")
    router.subscribe(a)
    router.subscribe(b)
    router.route(_event())
    assert a.received and b.received


def test_failing_subscriber_isolated():
    router = StreamRouter()
    good = _Recorder("market")
    router.subscribe(_Boom())
    router.subscribe(good)
    result = router.route(_event())
    assert "boom" in result.failed
    assert "market" in result.delivered
    assert good.received  # good subscriber still got the event


def test_unsubscribe():
    router = StreamRouter()
    rec = _Recorder("market")
    router.subscribe(rec)
    router.unsubscribe("market")
    router.route(_event())
    assert not rec.received
    assert router.subscribers() == []


def test_resubscribe_same_name_replaces():
    router = StreamRouter()
    a, b = _Recorder("market"), _Recorder("market")
    router.subscribe(a)
    router.subscribe(b)
    router.route(_event())
    assert b.received and not a.received


def test_callback_subscriber_adapter():
    router = StreamRouter()
    got = []
    router.subscribe(CallbackSubscriber("fn", lambda e: got.append(e)))
    router.route(_event())
    assert len(got) == 1
