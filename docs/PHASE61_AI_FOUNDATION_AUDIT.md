# Phase 61.0 — AI Infrastructure Foundation: Reuse Audit

TASK 1 of the Phase 61.0 Worker Brief. Code-writing is deliberately
out of scope for this section — every finding below is Already
exists / Can extend / Cannot reuse, with a reason, following the
Module Reuse Principle (`CLAUDE.md`): does this exist? can it be
extended? only if both are no, a new module is justified. TASK 2-9's
new packages (`ai/capabilities/`, `ai/providers/`, `ai/router/`,
`ai/context/`, `ai/access/`, `ai/session/`, `ai/tools/`, `ai/audit/`)
are each justified below by the "Cannot reuse" rows that name them.

## `ai/`

| Module | Status | Reason |
|---|---|---|
| `ai/interfaces.py` (`AIAnalyzerInterface`, `MarketContext`, `UserContext`, `AIResponse`) | Already exists | Phase 55's provider-agnostic contract. `MarketContext`/`UserContext` are the exact shapes TASK 5's `ai/context/` composes into `AIContext`; `AIAnalyzerInterface`'s advisory-only boundary is restated, not re-invented, by TASK 3's `BaseAIProvider`. |
| `ai/ai_analyzer.py` (`AIAnalyzer`, live, wired into `core/pipeline.py`) | Cannot reuse for TASK 2-9 | This is the live production pipeline stage (signal-candidate scoring), not a capability/provider abstraction. Phase 61.0's new packages sit beside it, never replace or call it — untouched this phase, per the brief's own restriction on `core/pipeline.py`. |
| `ai/analyzer/ai_analyzer.py` | Already exists | Phase 55 re-export shim for the above. No change needed. |
| `ai/ai_prompt.py` (Gemini-specific signal-validation prompt+schema builder) | Cannot reuse | Tightly coupled to `SignalCandidate`/`ContextSnapshot`/`ConfidenceResult` for one job (signal validation JSON schema). Not a general capability/provider prompt shape — left untouched. |
| `ai/prompts/prompt_manager.py` (`PromptManager`) | Can extend (future phase) | Already the general-purpose, `MarketContext`/`UserContext`-shaped template registry (Phase 55, extended Phase 60.5). TASK 3-4 (Provider Interface, Router) do not need prompt text this phase — placeholder providers return static stub responses, no prompt is built or sent. Left unmodified this phase; a future Phase 61.1 (Prompt System) is the natural extension point, not a new prompt module now. |
| `ai/confidence_model.py` (`evaluate_confidence`) | Cannot reuse | Deterministic technical scoring over `SignalCandidate`/`ContextSnapshot`, unrelated to AI capability/provider selection. Untouched. |
| `ai/learning_context.py` (`LearningContext`, `build_learning_context`) | Can extend (future phase) | Already the AI-facing bundling of learning data (recent_failures/successful_patterns/strategy_stats/patterns/failures/regimes/confidence). TASK 5's `ai/context/context_builder.py` composes an already-built `LearningContext` as one of its five named inputs rather than rebuilding any of this logic. |
| `ai/memory/context_memory.py` (`ContextMemory`) | Cannot reuse for TASK 7 | In-memory per-key store keyed by a plain string, built for "what did I tell this user last" persistence across calls. TASK 7's Session is explicitly the opposite lifetime ("Session vaqtinchalik" — temporary, one conversation) — reusing `ContextMemory` for a session would conflate two different lifetimes the Director's own brief keeps distinct. `ai/session/` is justified as new; `ContextMemory` stays exactly as-is and is not modified or imported by it. |
| `ai/profiles/user_profile.py` (`AIUserProfile`) | Can extend (used as-is) | Already the typed, database-independent AI-facing user projection (experience_level/preferred_strategy/risk_style/language). TASK 5's `ai/context/` reads this directly as one of its five named inputs ("User Profile") — no new user-profile type is created. |
| `ai/journal/trade_journal.py` (`TradeJournalEntry`) | Can extend (used as-is) | Already the richer completed-trade record. TASK 5's `ai/context/` reads this directly for its "Trade History" input — no new trade-history type is created. |
| `ai/journal/failure_analysis.py` (`FailureAnalysisEntry`) | Already exists | Narrower, failure-specific record; not needed by any Phase 61.0 TASK directly (learning_context.py already folds failure data in via `recent_failures`). Untouched. |
| `ai/trade_journal.py` | Already exists | Phase 55 compatibility shim. Untouched. |
| `ai/capabilities/` | Cannot reuse — new (TASK 2) | No existing module names an independently-toggleable AI capability (CHAT/ANALYSIS/EXPLANATION/...). `configuration/feature_registry.py` is Infrastructure-only as of Phase 60.9 and structurally cannot hold Trading/AI-behavior concerns (see `docs/FEATURE_REGISTRY_SEPARATION.md`) — extending it would repeat the exact Phase 60.8 collision Phase 60.9 fixed. A new, AI-scoped registry is the correct boundary. |
| `ai/providers/` | Cannot reuse — new (TASK 3) | `ai/ai_analyzer.py`/`ai/ai_prompt.py` are both single-provider-shaped (heuristic stub / Gemini-specific) with no vendor-selection abstraction. `ai/interfaces.py`'s `AIAnalyzerInterface` defines the *analysis* contract shape but has no notion of multiple named providers, a registry, or selection logic. Genuinely new. |
| `ai/router/` | Cannot reuse — new (TASK 4) | Nothing in the codebase today maps a capability to a provider; this selection logic does not exist anywhere else. |
| `ai/context/` | Cannot reuse as a single module — new, but composes existing types | No existing module combines `MarketContext` + `SignalSchema` + `AIUserProfile` + `TradeJournalEntry` + `LearningContext` into one caller-facing `AIContext`. The new module's job is composition of the above already-existing types, not reimplementation of any of them. |
| `ai/access/` | Cannot reuse — new (TASK 6) | See `telegram/owner/owner_roles.py` and `database/models.py` below — a role hierarchy exists, but no capability-permission matrix exists anywhere. |
| `ai/session/` | Cannot reuse — new (TASK 7) | See `ai/memory/context_memory.py` above. |
| `ai/tools/` | Cannot reuse — new (TASK 8) | No tool-interface abstraction exists in the codebase; `context/`, `analytics/`, and `data/` modules are called directly by their own owners today, never through an AI-facing tool contract. |
| `ai/audit/` | Cannot reuse — new (TASK 9) | `database/audit_log_repository.py` (see below) audits owner/runtime actions, not AI provider calls (latency/token/cost/capability has no existing home). |

## `context/`

| Module | Status | Reason |
|---|---|---|
| `context_layer/context_engine/context_orchestrator.py` (`ContextSnapshot`) | Cannot reuse directly by AI | Already deliberately excluded from the AI-facing surface — `ai/interfaces.py`'s own docstring states `MarketContext` is "deliberately narrower than `context.context_orchestrator.ContextSnapshot`... so a future provider's input contract doesn't leak internal Context Layer types into `ai/`." TASK 5's `ai/context/` continues this boundary: it composes from `MarketContext`, never imports `ContextSnapshot` itself. |
| `context_layer/fundamental/fundamental_context.py` (`FundamentalContextSnapshot`) | Already exists, used indirectly | Already consumed by `PromptManager.get_fundamental_analysis_prompt()`. Not a direct TASK 5 input (the Director's brief names Market Context/Signal Schema/User Profile/Trade History/Learning Context, not fundamentals) — left as a future extension point, not added speculatively. |

## `learning/`

| Module | Status | Reason |
|---|---|---|
| `learning/models.py` (`LearningRecord`), `learning/pattern_detector.py`, `learning/confidence.py`, `learning/regime_memory.py`, `learning/outcome_analyzer.py`, `learning/trade_event_bridge.py` | Already exists, reused via `ai/learning_context.py` | None of these are imported directly by any new Phase 61.0 package — `ai/context/context_builder.py` (TASK 5) takes an already-built `LearningContext` as input, matching this codebase's own established pattern (`ai/learning_context.py`'s docstring: "reuses... directly", "does NOT itself generate"). Re-importing `learning/` internals into `ai/context/` would duplicate `ai/learning_context.py`'s existing composition role. |

## `database/`

| Module | Status | Reason |
|---|---|---|
| `database/audit_log_repository.py` (`AuditLogRepository`) | Cannot reuse for TASK 9 this phase | Real, persisted, wired into `RuntimeFeatureManager`/`EmergencyManager` for Infrastructure/Trading-control audit trails. TASK 9's brief explicitly says "Real DB yozish shart emas... Foundation" (no real DB write required) — `ai/audit/` this phase is an in-memory/interface foundation, deliberately not wired to `AuditLogRepository` yet, so as to not create a new, silent write path into the audit table outside this phase's explicit review. A future phase may wire `ai/audit/` to a real repository (new `database/ai_audit_repository.py`, following this same table's existing per-concern-repository convention) — not this phase. |
| `database/models.py` (`plan` column: `'FREE'` / presumably `'PREMIUM'`/`'VIP'` string values, no dedicated enum class) | Can extend / read, not modify | TASK 6's role dimension is `OWNER`/`ADMIN`/`VIP`/`PREMIUM`/`FREE`. No `SubscriptionTier` enum exists in `database/models.py` today — subscription `plan` is a free-text column. `ai/access/permissions.py` defines its own `Role` enum for this purpose (naming it distinctly, e.g. `AIRole`, to avoid colliding with any future real enum) rather than retrofitting a typed enum onto the existing string column, which is out of this phase's scope (`database/` schema changes are not named in TASK 1-9). |
| `database/admin_repository.py`, `database/user_repository.py`, `database/subscription_repository.py` | Already exists, not called this phase | `ai/access/` is a foundation permission-matrix module only (Role × Capability → allowed/denied), not wired to read a real user's actual role from the database this phase — same "foundation, not yet live-wired" posture as every prior Phase 59-60 module. A future integration phase connects `ai/access/` to these repositories. |

## `telegram/owner/`

| Module | Status | Reason |
|---|---|---|
| `telegram/owner/owner_roles.py` (`OwnerRole`: OWNER/SUPER_ADMIN/ADMIN/VIEWER) | Cannot reuse directly for TASK 6 | Named and scoped for the Owner Dashboard's admin hierarchy specifically (`resolve_owner_role()` reads `telegram.permissions.is_owner()` + the `admins` table). TASK 6's Role axis is user-subscription-shaped (`OWNER`/`ADMIN`/`VIP`/`PREMIUM`/`FREE` — a different set: VIP/PREMIUM/FREE are subscription tiers, not admin tiers, and do not exist in `OwnerRole` at all). Importing/aliasing `OwnerRole` would conflate two genuinely different hierarchies (admin-console access vs. AI-capability entitlement) — same disambiguation-by-naming precedent used throughout this codebase (e.g. `AIAnalysisResult` vs `AIResponse`). `ai/access/permissions.py` defines its own enum. |
| No existing `telegram/owner/ai_*.py` command module | Confirmed absent | Grep across `telegram/owner/*.py` found no AI-related owner command file — TASK 2-9 have no existing owner-command surface to extend, and per the brief none is added this phase (foundation only, no live wiring). |
| `telegram/permissions.py` (`PermissionLevel`: OWNER/ADMIN/USER, live-wired into `command_router.py`) | Cannot reuse directly | Real, live permission gate for Telegram command routing — a three-level hierarchy, not the five-level subscription-shaped Role TASK 6 needs. Same reasoning as `OwnerRole` above: a new, purpose-built enum in `ai/access/` avoids overloading a live-wired type with a foundation-only concern. |

## `configuration/`

| Module | Status | Reason |
|---|---|---|
| `configuration/feature_registry.py` / `configuration/runtime_feature_manager.py` | Cannot reuse for `ai/capabilities/` | As of Phase 60.9, this registry is structurally Infrastructure-only (providers/data-sources/observation-modes) — `docs/FEATURE_REGISTRY_SEPARATION.md` is the audit that established this and the root-cause fix that makes reusing it for a Trading/AI-behavior concern (like an AI capability toggle) the exact mistake Phase 60.9 was created to prevent. `ai/capabilities/capability_registry.py` is therefore justified as a new, AI-scoped registry — same *shape* (a `Descriptor` dataclass + a registry-building function + a manager with enable/disable/status), deliberately not the same *instance* or *namespace*. |
| `configuration/runtime_state.py` (`RuntimeStateCache`) | Pattern reused, module not imported | `ai/capabilities/capability_manager.py` follows the same in-memory-cache-plus-manager shape TASK 2 asks for, without importing this Infrastructure-scoped class directly (same reasoning as above — the pattern is reusable, the instance is not, because they govern different domains). |

## `core/`

| Module | Status | Reason |
|---|---|---|
| `core_layer/emergency/emergency_manager.py` (`EmergencyManager`) | Not applicable to TASK 2-9 | Sole Trading-control authority (Phase 60.9's "Emergency Only Controls Trading" principle). AI capabilities are not a trading-pipeline stage — `ai/capabilities/` never calls or is called by `EmergencyManager`, and TASK 2's Capability Manager governs advisory AI features only, never a pipeline gate. |
| `core/secrets.py` (`Secrets`, incl. `GEMINI_API_KEY`) | Already exists, not read this phase | TASK 3's placeholder providers make no real API call, so no provider this phase reads `Secrets.GEMINI_API_KEY` or any other credential — a real-provider phase (Phase 61.1+) is where `ai/providers/gemini_provider.py`, etc. would read this. Confirmed present and ready for that future phase; untouched now. |
| `core_layer/logger/logger.py` (`setup_logger`) | Already exists, reused directly | Every new TASK 2-9 module uses this exact existing logger factory, matching the codebase-wide convention — no new logging abstraction is created. |

## Summary

Nine new packages are justified (`ai/capabilities/`, `ai/providers/`,
`ai/router/`, `ai/context/`, `ai/access/`, `ai/session/`, `ai/tools/`,
`ai/audit/`) — in every case, TASK 1 found no existing module that
already provides the capability/provider/routing/session/tool/audit
abstraction, and in every case where an adjacent module exists
(`ai/interfaces.py`, `ai/learning_context.py`, `ai/profiles/user_profile.py`,
`ai/journal/trade_journal.py`, `ai/memory/context_memory.py`,
`telegram/owner/owner_roles.py`, `telegram/permissions.py`,
`configuration/feature_registry.py`), the new module composes or sits
beside it rather than duplicating its logic. No existing module is
modified by this phase's TASK 2-9 (`ai/interfaces.py`,
`ai/learning_context.py`, `ai/profiles/user_profile.py`,
`ai/journal/trade_journal.py` are read, not written).
