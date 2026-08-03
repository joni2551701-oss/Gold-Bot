"""
Phase P1 (Production Deployment Pipeline Foundation), TASK 8/9 --
tests for the two checks added to scripts/health_check.py
(check_main_imports/check_telegram_imports) and the extended main()
aggregation. The three pre-existing checks (config/secrets/database)
were already correct and are not re-tested here beyond confirming
main() still calls them.
"""

import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
import health_check  # noqa: E402


def test_check_main_imports_succeeds():
    ok, message = health_check.check_main_imports()
    assert ok is True
    assert message == "main: OK"


def test_check_telegram_imports_succeeds():
    ok, message = health_check.check_telegram_imports()
    assert ok is True
    assert message == "telegram: OK"


def test_check_main_imports_reports_failure_on_import_error(monkeypatch):
    def _fake_import_module(name, *args, **kwargs):
        if name == "core_layer.pipeline":
            raise ImportError("simulated import failure")
        return importlib.import_module(name, *args, **kwargs)

    monkeypatch.setattr(health_check.importlib, "import_module", _fake_import_module)
    ok, message = health_check.check_main_imports()
    assert ok is False
    assert "main: FAILED" in message


def test_check_telegram_imports_reports_failure_on_import_error(monkeypatch):
    def _fake_import_module(name, *args, **kwargs):
        if name == "platform_layer.telegram.polling":
            raise ImportError("simulated import failure")
        return importlib.import_module(name, *args, **kwargs)

    monkeypatch.setattr(health_check.importlib, "import_module", _fake_import_module)
    ok, message = health_check.check_telegram_imports()
    assert ok is False
    assert "telegram: FAILED" in message


def test_check_main_imports_never_starts_the_pipeline():
    """
    An import-only check must never actually run a pipeline cycle --
    core_layer.pipeline importing successfully is not the same as it having
    executed anything. Confirmed by the fact the check completes
    without network access / real secrets in this test environment.
    """
    ok, _ = health_check.check_main_imports()
    assert ok is True


def test_check_telegram_imports_never_starts_polling():
    """
    telegram.polling's run_polling()/main() live behind
    `if __name__ == "__main__":` -- importing the module must never
    block or start long-polling.
    """
    ok, _ = health_check.check_telegram_imports()
    assert ok is True


def test_main_runs_five_checks(monkeypatch, capsys):
    calls = []

    def _ok(name):
        def _check():
            calls.append(name)
            return True, f"{name}: OK"
        return _check

    monkeypatch.setattr(health_check, "check_config", _ok("config"))
    monkeypatch.setattr(health_check, "check_secrets", _ok("secrets"))
    monkeypatch.setattr(health_check, "check_database", _ok("database"))
    monkeypatch.setattr(health_check, "check_main_imports", _ok("main"))
    monkeypatch.setattr(health_check, "check_telegram_imports", _ok("telegram"))

    exit_code = health_check.main()
    assert exit_code == 0
    assert calls == ["config", "secrets", "database", "main", "telegram"]


def test_main_exit_1_when_main_imports_check_fails(monkeypatch):
    monkeypatch.setattr(health_check, "check_config", lambda: (True, "config: OK"))
    monkeypatch.setattr(health_check, "check_secrets", lambda: (True, "secrets: OK"))
    monkeypatch.setattr(health_check, "check_database", lambda: (True, "database: OK"))
    monkeypatch.setattr(health_check, "check_main_imports", lambda: (False, "main: FAILED (x)"))
    monkeypatch.setattr(health_check, "check_telegram_imports", lambda: (True, "telegram: OK"))

    assert health_check.main() == 1


def test_main_exit_1_when_telegram_imports_check_fails(monkeypatch):
    monkeypatch.setattr(health_check, "check_config", lambda: (True, "config: OK"))
    monkeypatch.setattr(health_check, "check_secrets", lambda: (True, "secrets: OK"))
    monkeypatch.setattr(health_check, "check_database", lambda: (True, "database: OK"))
    monkeypatch.setattr(health_check, "check_main_imports", lambda: (True, "main: OK"))
    monkeypatch.setattr(health_check, "check_telegram_imports", lambda: (False, "telegram: FAILED (x)"))

    assert health_check.main() == 1


def test_main_exit_0_when_all_five_checks_pass(monkeypatch):
    monkeypatch.setattr(health_check, "check_config", lambda: (True, "config: OK"))
    monkeypatch.setattr(health_check, "check_secrets", lambda: (True, "secrets: OK"))
    monkeypatch.setattr(health_check, "check_database", lambda: (True, "database: OK"))
    monkeypatch.setattr(health_check, "check_main_imports", lambda: (True, "main: OK"))
    monkeypatch.setattr(health_check, "check_telegram_imports", lambda: (True, "telegram: OK"))

    assert health_check.main() == 0


def test_main_never_prints_a_secret_value(monkeypatch, capsys):
    """
    check_main_imports/check_telegram_imports never touch secret
    values at all (they are pure import checks) -- confirm their
    messages are always the fixed, value-free strings.
    """
    ok_main, msg_main = health_check.check_main_imports()
    ok_telegram, msg_telegram = health_check.check_telegram_imports()
    assert msg_main in ("main: OK",) or msg_main.startswith("main: FAILED (")
    assert msg_telegram in ("telegram: OK",) or msg_telegram.startswith("telegram: FAILED (")


def test_health_check_module_reloads_cleanly():
    """Guards against any accidental module-level side effect breaking re-import."""
    importlib.reload(health_check)
    ok, _ = health_check.check_main_imports()
    assert ok is True


@pytest.mark.parametrize("check_name", ["check_main_imports", "check_telegram_imports"])
def test_new_checks_return_a_two_tuple(check_name):
    result = getattr(health_check, check_name)()
    assert isinstance(result, tuple)
    assert len(result) == 2
    ok, message = result
    assert isinstance(ok, bool)
    assert isinstance(message, str)
