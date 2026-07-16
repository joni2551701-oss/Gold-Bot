# Phase 61.4 — AI Product & Control Layer: Reuse Audit

TASK 1 of the Phase 61.4 Worker Brief. Audits `telegram/`, `database/`,
`ai/access/`, `ai/audit/`, `configuration/` before any code is
written. Per the Module Reuse Principle: "Agar reuse qilsa bo'ladigan
modul topilsa, yangi kod yozilmaydi" — every later TASK's design
decision traces back to a finding here.

## `telegram/` — three separate role concepts already exist, deliberately

- `telegram/permissions.py`'s `PermissionLevel` (OWNER/ADMIN/USER) —
  the one **live**, wired-into-`command_router.py` gate. `is_owner()`
  reads `Secrets().TELEGRAM_OWNER_ID`; `is_admin()` reads the
  `admins` table via `telegram/admin_service.py`.
- `telegram/owner/owner_roles.py`'s `OwnerRole`
  (OWNER/SUPER_ADMIN/ADMIN/VIEWER) — foundation only (Phase 59.6 TASK
  3), a finer admin-console hierarchy, not wired into any command's
  gate check.
- `ai/access/permissions.py`'s `AIRole` (OWNER/ADMIN/VIP/PREMIUM/FREE)
  — Phase 61.0's AI-capability-entitlement enum, **not wired to any
  real user lookup**. Its own docstring already explains why it is
  distinct by design from the two above (subscription tiers vs.
  admin-console tiers) — reusing either existing enum's name would
  conflate two concerns the codebase already keeps apart.

**Finding for TASK 2 ("AI Access Control Integration")**: this is not
a request for a fourth role enum. It is the missing resolver — a
function/service that reads a real `telegram_id`'s `PermissionLevel`
(via `telegram/permissions.py`, unmodified) and `SubscriptionRecord.plan`
(via `telegram/subscription_service.py`, unmodified) and maps the pair
into an `AIRole`, so `ai/access/access_control.py`'s already-built
matrix finally has real data flowing into it instead of a caller
hand-picking a role.

- `telegram/subscription_service.py` (Phase 42) — `SubscriptionService`
  bridges `/plan`/`/subscription`/`/upgrade` to
  `database.subscription_repository.SubscriptionRepository`.
  `SIGNAL_ACCESS_PLANS = {"PREMIUM", "VIP"}`, `DEFAULT_PLAN = "FREE"`
  — confirms `SubscriptionRecord.plan`'s real values already match
  `AIRole.PREMIUM`/`AIRole.VIP`/`AIRole.FREE` by name. The resolver
  needs no new vocabulary here, only a mapping function.
- `telegram/admin_service.py` (Phase 37/41/46) — `AdminService`
  already has a real, async, event-loop-safe `broadcast()`. Not
  reused this phase (Broadcast is explicitly deferred to v0.5 per the
  Director's own decision) — noted only so a future phase doesn't
  duplicate it.
- `telegram/commands.py` / `telegram/command_router.py` — `COMMANDS`/
  `OWNER_COMMANDS`/`ADMIN_COMMANDS` dicts + `_required_level()` is the
  one existing pattern any new `telegram/owner/ai_commands.py` must
  follow. **Confirmed: none of the 18 existing `telegram/owner/*.py`
  modules are registered into these dicts or `command_router.py`'s
  dispatch today** (`docs/FOUNDATION_FREEZE_v0.4.md`'s own roadmap
  names this live-wiring as future v0.9 work) — `ai_commands.py`
  follows the exact same "foundation, not yet live-wired" posture
  every prior owner-command module has used, not an exception.

## `database/` — no phone number field or hashing utility anywhere

- `database/user_models.py`'s `UserRecord`: `telegram_id`, `username`,
  `language`, `trading_style`, `risk_percent`, `timeframe`,
  `created_at`, `strategy`, `notifications_enabled`, `status`,
  `last_activity`. **No `phone`/`phone_hash` field, no `role` field.**
- `database/subscription_models.py`'s `SubscriptionRecord`:
  `telegram_id`, `plan`, `status`, `started_at`, `expires_at`.
- `database/admin_models.py`'s `AdminRecord`: `telegram_id`, `role`
  (free text, e.g. `"ADMIN"`/`"SUPER_ADMIN"`), `created_at`.
- **Confirmed via repo-wide grep: zero `phone` references and zero
  `hashlib`/hash usage anywhere in `database/`, `telegram/`, or
  `core/`.** TASK 3's (AI User Registration, phone hash) storage need
  is genuinely new — no existing field or hashing helper to reuse for
  it. `ai/context/context_adapter.py`'s `compute_context_hash()` (via
  `ai/cache/cache_policy.py`) is the only `hashlib.sha256` precedent
  in the codebase, and it hashes a JSON context payload, not a phone
  number — not directly reusable, but its "deterministic SHA-256,
  never store the raw value" pattern is the one to follow.

## `ai/access/` — the entitlement matrices are already correctly separated, one has drifted

- `access_control.py`'s `AccessControl` — Role x Capability matrix.
  Unmodified, no gap found for TASK 2.
- `usage_limits.py`'s `UsageLimiter` — in-memory, per-`(telegram_id,
  capability)` daily call counter with a role-based ceiling. This
  already covers *count*-based limiting; it does not track cost or
  tokens (see `ai/audit/` finding below for TASK 5).
- `tool_permissions.py`'s `_DEFAULT_TOOL_MATRIX` — **drift found**:
  does not include `"learning_tool"`, added in Phase 61.3 TASK 4,
  after this matrix was last touched (Phase 61.1 TASK 6). Not a
  blocking bug (an omitted tool simply has no role granted access,
  fail-closed, not fail-open) but flagged here for TASK 2 to correct
  in-place rather than rediscovering it independently.

## `ai/audit/` — the per-user cost join already has both halves built, just never joined

- `ai/audit/request_log.py`'s `AIRequestLogEntry` carries `telegram_id`.
- `ai/audit/response_log.py`'s `AIResponseLogEntry` carries `tokens`/
  `cost`, but **not** `telegram_id`.
- `ai/audit/provider_stats.py`'s `compute_provider_stats()` aggregates
  `tokens`/`cost` **per provider**, never per user.
- `ai/audit/trace.py`'s `trace_request()` (Phase 61.3 TASK 8) already
  joins one `request_id`'s `RequestLog` entry (which has `telegram_id`)
  with its `ResponseLog` entries (which have `cost`/`tokens`) — this
  is exactly the join TASK 5's "AI Usage Accounting" needs, just
  currently scoped to one `request_id` at a time rather than
  aggregated across all of a user's calls.

**Finding for TASK 5**: a per-user cost/usage aggregator is a
`request_id -> telegram_id` join over `RequestLog.all()` combined with
a `request_id -> cost/tokens` lookup over `ResponseLog.all()` — the
same two lists `trace_request()` already reads, generalized from "one
request_id" to "every request_id belonging to one telegram_id". No new
log field, no new storage layer; this is an aggregation function over
existing, unmodified `ai/audit/` data, matching `provider_stats.py`'s
own "pure aggregation over an already-recorded history" pattern.

## `configuration/` — a separate, unrelated concern; do not conflate

`configuration/feature_registry.py`'s `FeatureDescriptor`/
`build_feature_registry()` governs **Infrastructure** feature toggles
(data providers, runtime feature flags) — Phase 60.9's "Runtime
Registry Separation" already drew a hard line between this and any
trading/AI-facing control (`docs/FEATURE_REGISTRY_SEPARATION.md`).
Nothing in Phase 61.4 should register an AI capability flag here;
`ai/capabilities/capability_manager.py` remains the correct, already-
separate home for that, unchanged this phase.

## Summary of what's built new vs. reused (for TASK 2-5)

| TASK | New | Reused |
|---|---|---|
| 2 (AI Access Control Integration) | A resolver: real `telegram_id` -> `PermissionLevel` + `SubscriptionRecord.plan` -> `AIRole`. `tool_permissions.py`'s stale matrix corrected in place. | `telegram/permissions.py`, `telegram/subscription_service.py`, `ai/access/access_control.py`/`usage_limits.py` (all unmodified) |
| 3 (Telegram AI Owner Commands) | `telegram/owner/ai_commands.py` — foundation only, not registered into `command_router.py`, same posture as every other `telegram/owner/*.py` module. | `telegram/commands.py`'s dict shape (read as a pattern, not imported into); `ai/router/router.py`'s `provider_metrics()`; `ai/access/access_control.py`/`capability_manager.py` for status |
| 4 (AI User Registration Foundation) | `phone_hash` field + a `hash_phone_number()` helper (SHA-256, never store raw). | `database/user_models.py`'s existing `UserRecord` shape/migration convention |
| 5 (Anti-Abuse / Trial Protection) | `ai/access/trial_manager.py` — trial-window check keyed on `(telegram_id, phone_hash)`. | TASK 4's `phone_hash`; `ai/access/usage_limits.py`'s reset/counter shape as the closest existing precedent for per-key state |
| 6 (AI Usage Accounting) | A per-`telegram_id` aggregation function. | `ai/audit/request_log.py`/`response_log.py`/`trace.py` (all unmodified) — generalizes the existing join, no new log field |

## Deliberately out of scope this phase (Director's own decision)

Broadcast Foundation, Voice, Video, Media Layer — moved to v0.5
Product Media Layer per the Director's explicit ruling in this
phase's own brief. `telegram/admin_service.py`'s existing `broadcast()`
is noted above only so a future phase reuses it rather than
duplicating it.
