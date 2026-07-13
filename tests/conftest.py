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
