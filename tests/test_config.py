"""
Phase 59 Real Market Validation Foundation, TASK 1 --
config.Config.VALIDATION_MODE tests. No dedicated test file existed
for config.py before this phase.
"""

import subprocess
import sys
from pathlib import Path

from config import Config

_REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validation_mode_defaults_to_false():
    assert Config.VALIDATION_MODE is False


def test_validation_mode_reads_from_environment():
    """
    Phase 59.4 CI Test Isolation Hotfix: this used to call
    importlib.reload(config) in-process. Every module that does `from
    config import Config` (database/database.py, main.py,
    configuration/settings.py, and others) binds that name once, at
    its own first import -- reload() replaces config.Config with a
    brand-new class object but does NOT update those already-bound
    references, permanently desyncing them from config.Config for the
    rest of the test session. tests/conftest.py's fresh_database
    fixture mutates config.Config.DB_PATH (the live module attribute)
    every test, but database/database.py's Database.__init__() reads
    the stale, pre-reload Config class -- so every repository after
    this test ran shared one frozen, un-isolated SQLite file for the
    rest of the run (the cause of the 21 CI-only failures this hotfix
    addresses; see docs/PHASE59_VALIDATION.md's CI hotfix note).

    A subprocess -- a separate Python process/interpreter, not a
    reload of an already-imported module -- exercises the same
    os.getenv() line with zero risk of mutating this test session's
    shared config.Config (or anything importing it) at all.
    """
    result = subprocess.run(
        [sys.executable, "-c", "import os; os.environ['VALIDATION_MODE'] = 'True'; from config import Config; print(Config.VALIDATION_MODE)"],
        cwd=str(_REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "True"


def test_validation_mode_is_a_real_bool_not_a_string():
    assert isinstance(Config.VALIDATION_MODE, bool)
