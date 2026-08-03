"""
GitHub Secrets / Environment Configuration Audit -- TASK 0/7.

Confirms the exact env var names the brief asked about
(BITGET_API_KEY, GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
TELEGRAM_OWNER_ID, TWELVE_DATA_API_KEY) against what core/secrets.py
(the sole, already-enforced os.environ read point -- see
core/secrets.py's own docstring and docs/SECURITY.md) actually reads.

BITGET_API_KEY is a genuine audit finding, not an oversight: no
provider in data_layer/providers/ reads it, core/secrets.py has no property
for it, and .env.example/.env.production never mention it -- only an
ENABLE_BITGET feature-registry flag exists for a not-yet-built
provider (configuration/feature_registry.py). This suite pins that
finding down as a regression test, not just a doc note.
"""

import os

from core_layer.secrets import Secrets


def test_telegram_bot_token_reads_exact_env_var_name(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "sentinel-token")
    assert Secrets().TELEGRAM_BOT_TOKEN == "sentinel-token"


def test_telegram_chat_id_reads_exact_env_var_name(monkeypatch):
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "sentinel-chat")
    assert Secrets().TELEGRAM_CHAT_ID == "sentinel-chat"


def test_telegram_owner_id_reads_exact_env_var_name(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "sentinel-owner")
    assert Secrets().TELEGRAM_OWNER_ID == "sentinel-owner"


def test_twelve_data_api_key_reads_exact_env_var_name(monkeypatch):
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "sentinel-twelvedata")
    assert Secrets().TWELVE_DATA_API_KEY == "sentinel-twelvedata"


def test_gemini_api_key_reads_exact_env_var_name(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "sentinel-gemini")
    assert Secrets().GEMINI_API_KEY == "sentinel-gemini"


def test_bitget_api_key_is_not_a_real_secret():
    """
    Audit finding: BITGET_API_KEY does not exist as a used secret
    anywhere in this codebase. core_layer.secrets.Secrets has no
    BITGET_API_KEY property -- confirm that stays true rather than
    silently gaining one without a corresponding provider/audit doc
    update.
    """
    assert not hasattr(Secrets, "BITGET_API_KEY")


def test_env_example_documents_exactly_the_secrets_core_secrets_reads():
    """
    .env.example must list every required/optional var core/secrets.py
    actually reads for the six names this audit covers, and must not
    invent BITGET_API_KEY.
    """
    env_example_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env.example")
    content = open(env_example_path).read()

    for var in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TELEGRAM_OWNER_ID", "TWELVE_DATA_API_KEY", "GEMINI_API_KEY"):
        assert f"{var}=" in content, f"{var} missing from .env.example"

    assert "BITGET_API_KEY" not in content


def test_missing_telegram_bot_token_raises_with_name_in_message(monkeypatch):
    """The exact failure platform_layer/telegram/polling.py's run_polling() catches -- message names the variable."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    try:
        Secrets().TELEGRAM_BOT_TOKEN
        assert False, "expected ValueError"
    except ValueError as e:
        assert "TELEGRAM_BOT_TOKEN" in str(e)
