# AI Product & Control Layer (Phase 61.4)

The fifth v0.4 AI Core phase. Where 61.0-61.3 built the AI Core itself
(providers, runtime, context, knowledge, tools, conversation), 61.4
builds the missing product-control layer around it — real access
control tied to real users, owner-facing commands, phone-based
registration, trial-abuse protection, and per-user cost accounting.
Full reuse audit: `docs/PHASE61_4_PRODUCT_CONTROL_AUDIT.md` (TASK 1).

**Still foundation, not live-wired.** Every module below is real,
tested, and documented, but nothing is registered into
`platform_layer/telegram/command_router.py`, `core/pipeline.py`, or any live handler
— same posture every Phase 61.x module has used.

## TASK 2 — AI Access Control Integration

Three role concepts already existed by deliberate design before this
phase: `platform_layer/telegram/permissions.py`'s `PermissionLevel` (OWNER/ADMIN/USER,
live), `platform_layer/telegram/owner/owner_roles.py`'s `OwnerRole` (admin-console
hierarchy, foundation only), and `ai/access/permissions.py`'s `AIRole`
(OWNER/ADMIN/VIP/PREMIUM/FREE, never wired to real data). TASK 2 does
**not** add a fourth enum — it adds the missing resolver:

- `ai/access/subscription_policy.py` — pure `plan_to_ai_role(plan)`
  mapping (`SubscriptionRecord.plan` string -> `AIRole`), fails closed
  to `FREE` for `None`/unrecognized input.
- `ai/access/permission_service.py` — `resolve_ai_role(is_owner,
  is_admin, plan)`, priority OWNER > ADMIN > subscription-derived
  role. Takes already-resolved booleans/plan string, **never imports
  `telegram/` or `database/` itself** — the caller (a future
  `telegram/`-side integration) already legitimately has
  `platform_layer.telegram.permissions.is_owner()`/`is_admin()` and
  `platform_layer.telegram.subscription_service.SubscriptionService.get_plan()`
  available and passes their results in. Same `TYPE_CHECKING`-free,
  accept-already-resolved-facts pattern established for `ai/` ->
  `context/`/`database/` boundaries in prior phases.
- `ai/access/user_capability.py` — `UserCapabilityService`, one
  "can this real user do X right now" lookup composing
  `AccessControl`/`ToolPermissions`/`UsageLimiter` (all three
  unmodified), so a caller needs one call instead of three.
- **Correction**: `ai/access/tool_permissions.py`'s
  `_DEFAULT_TOOL_MATRIX` had drifted — `"learning_tool"` (added Phase
  61.3 TASK 4) was missing from every role's set. Fixed in place.
- **Correction**: `ai/access/usage_limits.py`'s `UsageLimiter.__init__`
  previously aliased `_DEFAULT_DAILY_LIMITS` directly rather than
  copying it — a `set_limit()` call on one instance would have
  silently mutated the shared module-level default for every other
  instance in the process. Fixed (`dict(...)` copy) as part of adding
  `set_limit()`, the method `/ai_limit` needs.

## TASK 3 — Telegram AI Owner Commands

`platform_layer/telegram/owner/ai_commands.py` (new) — `ai_status()`, `ai_provider()`,
`ai_disable()`/`ai_enable()`, `ai_limit()`. Mirrors
`platform_layer/telegram/owner/provider_commands.py`'s own shape exactly: standalone
functions returning an `AICommandResult`, every `ai/` object
injectable, this module never constructs a live `AIService` or reads
its internal state. "Runtime: Online/Offline" is derived from whether
any registered provider is currently healthy — never a hardcoded
constant. "Health: N%" in `ai_provider()` reads
`ai_layer.ai_service.audit.provider_stats.ProviderStats.success_rate` when call history
exists, or reports "N/A" rather than fabricating a percentage.
Confirmed (per TASK 1's audit): none of the 18 pre-existing
`platform_layer/telegram/owner/*.py` modules are registered into
`platform_layer/telegram/commands.py`'s dicts or `command_router.py`'s dispatch
either — this file follows that exact same convention.

## TASK 4 — AI User Registration Foundation

`database_layer/user_repository/user_models.py`'s `UserRecord` gained `phone_hash:
Optional[str] = None` (additive, same convention as every prior
lifecycle-field addition). `database_layer/database_manager/models.py`'s
`_migrate_users_schema()` adds the column to a pre-existing `users`
table (idempotent, `PRAGMA table_info` check first — same pattern as
the Phase 45 `status`/`last_activity` migration). **The raw phone
number is never stored anywhere in this codebase.**

`core_layer/secrets/phone_hash.py` (new) — `hash_phone_number(phone, salt=None)`:
deterministic, HMAC-SHA256-salted hash (not a bare `hashlib.sha256`,
which would be practically reversible given a phone number's limited
entropy). Reads `core.secrets.Secrets.PHONE_HASH_SALT` (new optional
secret) when no explicit salt is given, falling back to a documented
built-in pepper if unset — determinism (same phone -> same hash across
restarts) is required for TASK 5's trial-matching to work at all, so a
missing salt degrades security rather than breaking functionality.

`database_layer/user_repository/user_repository.py` gained `set_phone_hash()` and
`get_users_by_phone_hash()` — the second is TASK 5's abuse-detection
read path (every `telegram_id` sharing one phone_hash).

## TASK 5 — Anti-Abuse / Free Trial Protection

`ai/access/identity_checker.py` (new) —
`is_phone_reused_by_another_account(current_telegram_id,
telegram_ids_sharing_phone)`: a pure function over caller-supplied
telegram_id strings, never imports `database/`. The caller already
queried `UserRepository.get_users_by_phone_hash()` and passes the
result in.

`ai/access/trial_manager.py` (new) — `TrialManager`: in-memory,
per-telegram_id 7-day FREE trial window (`DEFAULT_TRIAL_DURATION`),
same "foundation only, no persistence" posture as
`ai/access/usage_limits.py`'s `UsageLimiter`. "1 phone = 1 trial":
`check_eligibility()`/`start_trial()` reject a new trial outright when
`phone_reused=True`, regardless of whether the requesting telegram_id
has started a trial before — the phone-based block always wins.

## TASK 6 — AI Usage Accounting

`ai/audit/usage_accounting.py` (new file, inside the existing
`ai/audit/` package — not a new `ai/billing/` top-level package, per
TASK 1's own audit finding) — `compute_user_usage(requests,
responses)`: generalizes `ai/audit/trace.py`'s own `request_id ->
telegram_id` join (Phase 61.3 TASK 8) from "one request_id" to "every
request_id belonging to one telegram_id," aggregating calls/tokens/
cost per user and per provider. No new log field, no new storage
layer — pure aggregation over `RequestLog`/`ResponseLog`'s existing,
unmodified data, matching `ai/audit/provider_stats.py`'s own
`compute_provider_stats()` pattern.

The Director's own "Today AI Cost: Gemini $12.40 / GPT $8.20 / Total
$20.60" worked example is a per-*provider* summary, not per-user — it
was already fully satisfiable by the existing, unmodified
`compute_provider_stats()`; `platform_layer/telegram/owner/ai_commands.py` gained
`ai_cost(provider_stats)` (formats that existing data into exactly
this shape) and `ai_usage(telegram_id, user_usage)` (the new per-user
dimension, formats `compute_user_usage()`'s output).

## Isolation re-verification (TASK 7, matching every prior phase's closing step)

AST-based import sweep (`ast.walk()` over every `.py` file under
`ai/`), re-run at the end of this phase:

| Target | Import sites found |
|---|---|
| `decision/` | **0** |
| `risk/` | **0** |
| `execution/` | **0** |
| `strategies/` | **0** |
| `database/` | **0** |
| `telegram/` | **0** |
| `signals/` | 7 (unchanged from Phase 61.3 — no new site this phase) |
| `context/` | 6 total, only 3 runtime (all 3 pre-date this entire v0.4 AI Core arc); the other 3 remain `TYPE_CHECKING`-only, unchanged from Phase 61.3 |

`platform_layer/telegram/owner/ai_commands.py` was checked separately (it sits
outside the `ai/` isolation boundary by design — a Telegram-side
consumer of `ai/` status objects, the same relationship every other
`platform_layer/telegram/owner/*.py` module has to its own domain): zero imports of
`decision/`/`risk/`/`execution/`/`strategies/` — this module reads
`ai/` state, it never approves, rejects, or executes a trade.

## Not wired

`ai/access/permission_service.py`, `user_capability.py`,
`identity_checker.py`, `trial_manager.py`,
`platform_layer/telegram/owner/ai_commands.py`, and `ai/audit/usage_accounting.py`
are not called from `core/pipeline.py`, any live Telegram handler, or
`platform_layer/telegram/command_router.py` — foundation only.

## Tests

1879 tests total (up from 1812 at the start of this phase), zero
regressions in the pre-existing suite.

## Deliberately out of scope (Director's own decision)

Broadcast Foundation, Voice, Video, Media Layer — explicitly moved to
a future v0.5 Product Media Layer in this phase's own brief, not
built here.
