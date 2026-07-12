"""
Telegram Layer — user service foundation.

Future home for /start, /profile, /settings business logic
(handlers.py will call into this). No database schema for users
exists yet -- this is an interface placeholder only, not backed by
any storage.
"""


class UserService:
    """Placeholder for future user registration/profile/settings logic."""

    def register(self, user_id):
        pass

    def get_profile(self, user_id):
        pass

    def update_settings(self, user_id, settings: dict):
        pass
