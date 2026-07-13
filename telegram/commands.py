"""
Telegram Layer — command registry foundation.

Pure data: maps a command name to its short description. No command's
internal behavior is implemented here. Handler wiring belongs to
handlers.py; the actual business logic belongs to user_service.py /
admin_service.py / result_handler.py in a later phase.
"""

COMMANDS = {
    "start": "Start user registration",
    "help": "Show commands",
    "profile": "Show profile",
    "signal": "Latest signal",
    "history": "Signal history",
    "status": "Bot status",
    "about": "About GoldBot",
}

ADMIN_COMMANDS = {
    "admin": "Open admin panel",
    "users": "List users",
    "stats": "Show bot statistics",
    "broadcast": "Broadcast a message to all users",
}
