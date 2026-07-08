import os

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

    @property
    def TWELVE_DATA_API_KEY(self) -> str: 
        return self.get("TWELVE_DATA_API_KEY")

    @property
    def GEMINI_API_KEY(self) -> str: 
        return self.get("GEMINI_API_KEY")

    @property
    def TELEGRAM_BOT_TOKEN(self) -> str: 
        return self.get("TELEGRAM_BOT_TOKEN")

    @property
    def TELEGRAM_CHAT_ID(self) -> str: 
        return self.get("TELEGRAM_CHAT_ID")
