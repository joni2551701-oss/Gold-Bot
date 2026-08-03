# ai_layer / ai_service / access

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `access_control.py` -- AI Layer — AI Access Control (Phase 61.0: AI Infrastructure
- `identity_checker.py` -- AI Layer — AI Identity Checker (Phase 61.4: AI Product & Control
- `permission_service.py` -- AI Layer — AI Permission Service (Phase 61.4: AI Product & Control
- `permissions.py` -- AI Layer — AI Access Roles (Phase 61.0: AI Infrastructure Foundation,
- `subscription_policy.py` -- AI Layer — Subscription Policy (Phase 61.4: AI Product & Control
- `tool_permissions.py` -- AI Layer — AI Tool Permission Matrix (Phase 61.1: AI Provider
- `trial_manager.py` -- AI Layer — AI Trial Manager (Phase 61.4: AI Product & Control Layer,
- `usage_limits.py` -- AI Layer — AI Usage Limits (Phase 61.0: AI Infrastructure Foundation,
- `user_capability.py` -- AI Layer — User Capability (Phase 61.4: AI Product & Control Layer,

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `access_control.py`: class `AccessControl`
- `identity_checker.py`: function `is_phone_reused_by_another_account()`
- `permission_service.py`: function `resolve_ai_role()`
- `permissions.py`: class `AIRole`
- `subscription_policy.py`: function `plan_to_ai_role()`
- `tool_permissions.py`: class `ToolPermissions`
- `trial_manager.py`: class `TrialEligibilityResult`
- `trial_manager.py`: class `TrialStatus`
- `trial_manager.py`: class `TrialManager`
- `trial_manager.py`: function `trial_status_from_started_at()`
- `usage_limits.py`: class `UsageCheckResult`
- `usage_limits.py`: class `UsageLimiter`
- `user_capability.py`: class `UserCapability`
- `user_capability.py`: class `UserCapabilityService`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
