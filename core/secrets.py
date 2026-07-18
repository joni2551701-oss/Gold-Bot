import os
from typing import Optional

class Secrets:
    """
    Secrets are read from Environment Variables (GitHub Secrets).
    No .env file usage for production security.
    """
    @staticmethod
    def get(key: str, default: str = None) -> str:
        value = os.getenv(key)
        if not value and default is None:
            raise ValueError(f"Secret '{key}' not found in environment.")
        return value or default

    @staticmethod
    def get_optional(key: str) -> Optional[str]:
        """
        Phase 61.2 TASK 2 -- returns None instead of raising when unset,
        for a secret whose absence means "this provider is disabled"
        rather than "the application cannot start" (the existing
        `get()`'s contract, used by required secrets like
        `TELEGRAM_BOT_TOKEN`). `GEMINI_API_KEY` below keeps its
        existing `get()`-based, raise-on-missing behavior unchanged --
        this method is additive, not a replacement.
        """
        return os.getenv(key) or None

    @property
    def TWELVE_DATA_API_KEY(self) -> str:
        return self.get("TWELVE_DATA_API_KEY")

    @property
    def GEMINI_API_KEY(self) -> str:
        return self.get("GEMINI_API_KEY")

    @property
    def OPENAI_API_KEY(self) -> Optional[str]:
        """Phase 61.2 TASK 2 -- optional; a real OpenAIProvider (a future phase) treats None as "disabled", never crashes on a missing key."""
        return self.get_optional("OPENAI_API_KEY")

    @property
    def CLAUDE_API_KEY(self) -> Optional[str]:
        return self.get_optional("CLAUDE_API_KEY")

    @property
    def GROK_API_KEY(self) -> Optional[str]:
        return self.get_optional("GROK_API_KEY")

    @property
    def ELEVENLABS_API_KEY(self) -> Optional[str]:
        """Phase 65.1 TASK 2 -- optional; a real ElevenLabsVoiceProvider (voice/provider_adapters/elevenlabs.py) treats None as "disabled", never crashes on a missing key. Same optional-get treatment as OPENAI_API_KEY (Phase 61.2 TASK 2)."""
        return self.get_optional("ELEVENLABS_API_KEY")

    @property
    def LOCAL_LLM_CONFIG(self) -> Optional[str]:
        """Phase 61.2 TASK 2 -- a connection string/config blob for a future local-inference provider, not an API key; same optional-get treatment since no local provider is implemented yet."""
        return self.get_optional("LOCAL_LLM_CONFIG")

    @property
    def TELEGRAM_BOT_TOKEN(self) -> str: 
        return self.get("TELEGRAM_BOT_TOKEN")

    @property
    def TELEGRAM_CHAT_ID(self) -> str:
        return self.get("TELEGRAM_CHAT_ID")

    @property
    def TELEGRAM_OWNER_ID(self) -> str:
        """
        Telegram user_id of the bot owner, used by telegram/permissions.py.
        Defaults to "" (no owner configured) instead of raising -- the
        permission layer must fail closed (nobody is OWNER), not crash.
        """
        return self.get("TELEGRAM_OWNER_ID", default="")

    @property
    def PHONE_HASH_SALT(self) -> Optional[str]:
        """Phase 61.4 TASK 4 -- optional pepper for core.phone_hash.hash_phone_number(); None means the built-in default pepper is used (see that module's own docstring for why a deployment should set this in production)."""
        return self.get_optional("PHONE_HASH_SALT")
