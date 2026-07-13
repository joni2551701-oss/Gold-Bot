import os

import pytest

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123456789:AAFakeTestTokenForPytestOnly000")
os.environ.setdefault("TELEGRAM_CHAT_ID", "999999")
os.environ.setdefault("TELEGRAM_OWNER_ID", "111")
os.environ.setdefault("TWELVE_DATA_API_KEY", "unused")
os.environ.setdefault("GEMINI_API_KEY", "unused")

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
