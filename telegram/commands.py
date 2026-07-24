"""
Telegram Layer — command registry foundation.

Pure data: maps a command name to its short description. No command's
internal behavior is implemented here. Handler wiring belongs to
handlers.py; the actual business logic belongs to user_service.py /
admin_service.py / result_handler.py in a later phase.

Phase 61.5 Addendum (per Director review): `ai_status`/`ai_provider`/
`ai_cost`/`ai_usage`/`ai_health`/`owner` are read-only informational
commands, so they are listed in BOTH `OWNER_COMMANDS` and
`ADMIN_COMMANDS` -- exactly the existing `"system"`/`"broadcast"`
precedent (`telegram.command_router._required_level()` checks
`ADMIN_COMMANDS` first, so dual membership means "ADMIN or OWNER", not
"OWNER only"). `doctor` (a system self-diagnostic exposing internal
subsystem reachability) and every other name unique to `OWNER_COMMANDS`
stay OWNER-only.

Phase 61.6 TASK 6: `runtime`/`runtime_events`/`runtime_metrics` (the
Owner Runtime Dashboard) are OWNER-only, not dual-listed -- unlike the
AI product-facing commands above, these expose internal runtime
lifecycle/event/metrics detail, matching `doctor`'s own OWNER-only
posture rather than the dual-listed `ai_*` commands.
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
    "notifications": "Manage notification preference",
    "feedback": "Send feedback",
}

OWNER_COMMANDS = {
    "admin": "Open admin panel",
    "addadmin": "Add a new admin",
    "removeadmin": "Remove an admin",
    "system": "Show system status",
    "broadcast": "Broadcast a message to all users",
    "ai_status": "Show AI Core status",
    "ai_provider": "Show current/fallback provider for a capability",
    "ai_cost": "Show today's AI cost by provider",
    "ai_usage": "Show a user's AI usage",
    "ai_health": "Show AI provider health ranking",
    "owner": "Show the owner dashboard summary",
    "doctor": "Run a system self-diagnostic",
    "runtime": "Show AI runtime lifecycle status",
    "runtime_events": "Show recent AI runtime events",
    "runtime_metrics": "Show AI runtime metrics",
    "runtime_status": "Show the combined AI runtime status panel",
    "runtime_check": "Run the AI runtime self-check",
    "runtime_restart": "Restart the AI runtime back to READY",
    "runtime_provider": "Show one provider's Health/Circuit/Latency/Requests panel",
    "ai_explanation_status": "Show the AI Explanation Intelligence Layer's status",
    "owner_status": "Show GoldBot Core Owner Monitoring system status",
    "health": "Run a full Owner monitoring diagnostic",
    "market": "Show market data monitoring status",
    "signals": "Show today's signal activity counts",
    "errors": "Show recent captured errors",
    "pipeline": "Show the most recent decision pipeline trace",
    "report": "Show the GoldBot daily monitoring report",
    "performance": "Show performance counters (GoldBot Core Owner Monitoring Alpha, Phase B.0)",
}

ADMIN_COMMANDS = {
    "admin": "Open admin panel",
    "stats": "Show bot statistics",
    "users": "List users",
    "userinfo": "Show a user's info",
    "vipinfo": "Show VIP info",
    "broadcast": "Broadcast a message to all users",
    "system": "Show system status",
    "feedbacks": "View feedback list",
    "ai_status": "Show AI Core status",
    "ai_provider": "Show current/fallback provider for a capability",
    "ai_cost": "Show today's AI cost by provider",
    "ai_usage": "Show a user's AI usage",
    "ai_health": "Show AI provider health ranking",
    "owner": "Show the owner dashboard summary",
}
