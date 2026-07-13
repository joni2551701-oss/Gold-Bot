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
    "settings": "Manage profile settings",
    "language": "Change language",
    "risk": "Change risk percent",
    "strategy": "Change trading style",
    "timeframe": "Change timeframe",
    "signal": "Latest signal",
    "history": "Signal history",
    "status": "Bot status",
    "about": "About GoldBot",
    "plan": "Plan information",
    "subscription": "Subscription status",
    "upgrade": "Upgrade foundation",
}

OWNER_COMMANDS = {
    "admin": "Open admin panel",
    "addadmin": "Add a new admin",
    "removeadmin": "Remove an admin",
    "system": "Show system status",
    "broadcast": "Broadcast a message to all users",
}

ADMIN_COMMANDS = {
    "admin": "Open admin panel",
    "stats": "Show bot statistics",
    "users": "List users",
    "userinfo": "Show a user's info",
    "vipinfo": "Show VIP info",
    "broadcast": "Broadcast a message to all users",
    "system": "Show system status",
}
