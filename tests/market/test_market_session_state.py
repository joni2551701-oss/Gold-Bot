"""
market/ facade — SessionState projection (TASK-CORE-005).

Proves the session view reads context.session.current_session and
combines it with stream/'s shared weekend clock
(stream.stream_mode.is_weekend), so the market façade's session label
agrees with the stream layer. `now` is injected for deterministic
weekend behaviour.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from market.session_state import SessionState

# Sat 2026-01-03 12:00 UTC (forex weekend) and Wed 2026-01-07 12:00 UTC (open).
_WEEKEND = datetime(2026, 1, 3, 12, 0, tzinfo=timezone.utc)
_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def _schema(session):
    return SimpleNamespace(session=SimpleNamespace(current_session=session))


def test_reads_context_session_on_a_weekday():
    st = SessionState.from_context(_schema("LONDON"), now=_WEEKDAY)
    assert st.current_session == "LONDON"
    assert st.is_weekend is False
    assert st.label == "LONDON"


def test_weekend_clock_overrides_stale_session_label():
    st = SessionState.from_context(_schema("LONDON"), now=_WEEKEND)
    assert st.is_weekend is True
    assert st.label == "WEEKEND_WAIT"


def test_no_session_on_weekday_is_off_session():
    st = SessionState.from_context(_schema(None), now=_WEEKDAY)
    assert st.current_session is None
    assert st.label == "OFF_SESSION"


def test_empty_context_does_not_raise():
    st = SessionState.from_context(SimpleNamespace(), now=_WEEKDAY)
    assert st.current_session is None
    assert st.label == "OFF_SESSION"
