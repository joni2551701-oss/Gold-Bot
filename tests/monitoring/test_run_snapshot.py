"""GoldBot Core Owner Snapshot Reporter Alpha, TASK 6/7 -- monitoring/run_snapshot.py tests."""

import asyncio
import logging
from unittest.mock import patch

from monitoring.run_snapshot import _verify_secrets, run_snapshot_report


def _all_secrets_present(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456789:AAFakeToken0000000000000000000")
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "unused")
    monkeypatch.setenv("GEMINI_API_KEY", "unused")


def test_verify_secrets_true_when_all_present(monkeypatch):
    _all_secrets_present(monkeypatch)
    assert _verify_secrets() is True


def test_verify_secrets_false_when_bot_token_missing(monkeypatch):
    _all_secrets_present(monkeypatch)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    assert _verify_secrets() is False


def test_verify_secrets_false_when_owner_id_missing(monkeypatch):
    _all_secrets_present(monkeypatch)
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    assert _verify_secrets() is False


def test_verify_secrets_true_even_when_twelve_data_key_missing(monkeypatch):
    """TWELVE_DATA_API_KEY is visibility-only, never blocks sending."""
    _all_secrets_present(monkeypatch)
    monkeypatch.delenv("TWELVE_DATA_API_KEY", raising=False)
    assert _verify_secrets() is True


def test_verify_secrets_true_even_when_gemini_key_missing(monkeypatch):
    """GEMINI_API_KEY is visibility-only, never blocks sending."""
    _all_secrets_present(monkeypatch)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert _verify_secrets() is True


def test_verify_secrets_logs_exact_abort_reason_for_missing_token(monkeypatch, caplog):
    _all_secrets_present(monkeypatch)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    with caplog.at_level(logging.ERROR, logger="SnapshotReporter"):
        _verify_secrets()

    messages = [r.message for r in caplog.records]
    assert any("Snapshot send aborted: Missing TELEGRAM_BOT_TOKEN" in m for m in messages)


def test_verify_secrets_logs_exact_abort_reason_for_missing_owner_id(monkeypatch, caplog):
    _all_secrets_present(monkeypatch)
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)

    with caplog.at_level(logging.ERROR, logger="SnapshotReporter"):
        _verify_secrets()

    messages = [r.message for r in caplog.records]
    assert any("Snapshot send aborted: Missing TELEGRAM_OWNER_ID" in m for m in messages)


def test_verify_secrets_never_logs_a_value(monkeypatch, caplog):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "super-secret-token-value")
    _all_secrets_present(monkeypatch)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "super-secret-token-value")

    with caplog.at_level(logging.INFO, logger="SnapshotReporter"):
        _verify_secrets()

    messages = [r.message for r in caplog.records]
    assert not any("super-secret-token-value" in m for m in messages)


def test_run_snapshot_report_returns_false_when_secrets_missing(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    result = asyncio.run(run_snapshot_report())
    assert result is False


def test_run_snapshot_report_returns_true_on_successful_send(monkeypatch):
    _all_secrets_present(monkeypatch)

    async def fake_send_snapshot(message):
        class Result:
            sent = True
        return Result()

    with patch("monitoring.run_snapshot.send_snapshot", fake_send_snapshot):
        result = asyncio.run(run_snapshot_report())

    assert result is True


def test_run_snapshot_report_returns_false_on_failed_send(monkeypatch):
    _all_secrets_present(monkeypatch)

    async def fake_send_snapshot(message):
        class Result:
            sent = False
        return Result()

    with patch("monitoring.run_snapshot.send_snapshot", fake_send_snapshot):
        result = asyncio.run(run_snapshot_report())

    assert result is False


def test_run_snapshot_report_returns_false_on_collection_failure(monkeypatch):
    _all_secrets_present(monkeypatch)

    with patch("monitoring.run_snapshot.collect_snapshot", side_effect=Exception("boom")):
        result = asyncio.run(run_snapshot_report())

    assert result is False


def test_run_snapshot_report_never_raises_on_collection_failure(monkeypatch):
    _all_secrets_present(monkeypatch)
    with patch("monitoring.run_snapshot.collect_snapshot", side_effect=Exception("boom")):
        asyncio.run(run_snapshot_report())  # must not raise


def test_main_exits_nonzero_on_failure(monkeypatch):
    import monitoring.run_snapshot as run_snapshot_module

    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    try:
        run_snapshot_module.main()
        assert False, "expected SystemExit"
    except SystemExit as e:
        assert e.code != 0


def test_main_exits_cleanly_on_success(monkeypatch):
    import monitoring.run_snapshot as run_snapshot_module

    _all_secrets_present(monkeypatch)

    async def fake_report():
        return True

    with patch.object(run_snapshot_module, "run_snapshot_report", fake_report):
        try:
            run_snapshot_module.main()
        except SystemExit:
            assert False, "main() should not call sys.exit() on success"
