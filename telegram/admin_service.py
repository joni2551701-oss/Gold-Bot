"""
Telegram Layer — admin service foundation.

Future home for /admin, /users, /stats, /broadcast business logic
(handlers.py will call into this). No database schema changes, no
user table -- interface placeholder only.
"""


class AdminService:
    """Placeholder for future admin panel logic."""

    def list_users(self):
        pass

    def get_stats(self):
        pass

    def broadcast(self, message: str):
        pass
