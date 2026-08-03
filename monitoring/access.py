"""
Monitoring Layer — Access Gate (Phase B.0 Rule 5: "Feature Flag
enable_owner_monitoring. Owner only."). Owner identity is already
enforced structurally by the live `telegram.permissions`/
`telegram.command_router` gate on every `OWNER_COMMANDS` entry (per
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s own "Security" section) --
this function only toggles whether Phase B.0's own new surface
(`/performance`, and the resource/health lines appended to
`/owner_status`) is exposed at all, the same "reserved, always False
by default" convention every other `enable_*` flag in
`configuration/feature_flags.py` already follows.
"""

from goldbot.core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_owner_monitoring_enabled(flags: FeatureFlags = DEFAULT_FLAGS) -> bool:
    return flags.enable_owner_monitoring
