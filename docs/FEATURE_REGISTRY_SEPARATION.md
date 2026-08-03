# Feature Registry Separation

Phase 60.9: Runtime Registry Separation (Architecture Cleanup). Resolves
the exact conflict Phase 60.8 disclosed
(`docs/PIPELINE_GUARD.md`'s "Disclosed Findings", finding 3): promoting
a Trading-pipeline stage gate (`ENABLE_EXECUTION`) into
`configuration/feature_registry.py`'s Runtime Registry collided with
`configuration/feature_dependency_validator.py`'s `DEPENDENCY_RULES`
and broke 26 unrelated tests. This phase removes the root cause instead
of working around it: **Trading-pipeline concepts do not belong in the
Runtime Feature Registry at all.**

No trading logic changed. This is a registry/wiring cleanup only.

## Design principle

Two owner-facing control surfaces now have a strictly separated
vocabulary:

- **`RuntimeFeatureManager`** (`configuration/`) governs
  **Infrastructure Services** — providers, data sources, observation
  modes, reserved feature flags. None of these gate a live trading
  decision.
- **`EmergencyManager`** (`core_layer/emergency/`) governs **Trading
  Control** — Pause, Kill, Maintenance, Resume/Normal. This was already
  true before this phase (Phase 59.9); what changes here is that
  `PipelineGuard` (`core_layer/pipeline/pipeline_guard.py`) now reads
  *exclusively* from `EmergencyManager` for every one of its four
  stage-gate hooks, never from `RuntimeFeatureManager`.

## TASK 1: Full registry audit

Every name known to `configuration/feature_registry.py` before this
phase, audited against this question: does toggling this name gate a
step of the live trading pipeline (`core/pipeline.py`'s
signal/ai/execution/database stages, or the Decision/Risk layers), or
is it an infrastructure/observation concern?

| Feature | Category | Runtime (before) | Runtime (after) | Emergency | Action |
|---|---|---|---|---|---|
| `ENABLE_MT5` | Infrastructure | YES | YES | NO | keep |
| `ENABLE_TWELVEDATA` | Infrastructure | YES | YES | NO | keep |
| `VALIDATION_MODE` | Infrastructure | YES | YES | NO | keep |
| `enable_ai` (lowercase, `FeatureFlags`) | Infrastructure | YES | YES | NO | keep — distinct from the removed uppercase `ENABLE_AI` below |
| `enable_crypto` | Infrastructure | YES | YES | NO | keep |
| `enable_swing` | Infrastructure | YES | YES | NO | keep |
| `enable_ai_memory` | Infrastructure | YES | YES | NO | keep |
| `enable_replay` | Infrastructure | YES | YES | NO | keep |
| `ENABLE_NEWS` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_PAPER` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_BACKTEST` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_ANALYTICS` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_OWNER` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_DATASET_SYNC` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_MARKET_PHASE` (declared-only) | Infrastructure | YES | YES | NO | keep — a context/analysis label, not itself a trade action |
| `ENABLE_BITGET` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_BINANCE` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_FRED` (declared-only) | Infrastructure | YES | YES | NO | keep |
| `ENABLE_SIGNALS` (Phase 60.8) | **Trading** | YES | **NO** | YES | **removed from Runtime Registry** — `PipelineGuard.before_signal()` becomes Emergency-only |
| `ENABLE_AI` uppercase (Phase 60.8) | **Trading** | YES | **NO** | YES | **removed** — `before_ai()` becomes Emergency-only |
| `ENABLE_DATABASE` (Phase 60.8) | **Trading** | YES | **NO** | YES | **removed** — `before_database()` becomes Emergency-only |
| `ENABLE_EXECUTION` (declared-only since Phase 60.8's own revert) | **Trading** | NO (already declared-only) | **NO (removed entirely, not even declared-only)** | YES (already, via `before_execution()`) | **removed from the registry namespace entirely** |
| `ENABLE_RISK` (declared-only) | **Trading** | NO (already declared-only) | **NO (removed entirely)** | indirect (see below) | **removed** |
| `ENABLE_DECISION` (declared-only) | **Trading** | NO (already declared-only) | **NO (removed entirely)** | indirect (see below) | **removed** |

**"Indirect" Emergency coverage for `ENABLE_RISK`/`ENABLE_DECISION`**:
neither ever had (or needs) its own `PipelineGuard` hook — the
Director's own four-hook API (`before_signal`/`before_ai`/
`before_execution`/`before_database`) has no `before_decision()`/
`before_risk()`. Decision and Risk are already covered structurally:
`PipelineGuard.before_signal()`'s skip empties `signal_candidates`,
which cascades through the existing list comprehensions so Decision
and Risk simply have nothing to evaluate — the same mechanism
documented in `docs/PIPELINE_GUARD.md`'s "Design rationale" section,
unchanged by this phase.

## Result

Runtime Registry (`configuration/feature_registry.py`) now contains
**only** Infrastructure names. Every name that gated (or was ever
intended to gate) a live pipeline stage has moved to being governed
exclusively by `EmergencyManager` via `PipelineGuard`. See TASK 2-4
below for the mechanics.

## TASK 2: Runtime Registry cleanup

`ENABLE_SIGNALS`/`ENABLE_AI` (uppercase)/`ENABLE_DATABASE` removed from
`build_feature_registry()`'s implemented entries. `ENABLE_EXECUTION`/
`ENABLE_RISK`/`ENABLE_DECISION` removed from `_DECLARED_ONLY_FEATURES`
entirely (not demoted to declared-only — removed from the namespace).
`config.Config.ENABLE_SIGNALS`/`ENABLE_AI`/`ENABLE_EXECUTION`/
`ENABLE_DATABASE` (all four, added in Phase 60.8) removed from
`config.py` — no longer read anywhere.

## TASK 3: Dependency cleanup

`configuration/feature_dependency_validator.py`'s `DEPENDENCY_RULES`
re-anchored from `{"ENABLE_EXECUTION": ("ENABLE_RISK",
"ENABLE_DECISION")}` to `{"ENABLE_BACKTEST": ("ENABLE_DATASET_SYNC",
"ENABLE_ANALYTICS")}` — both sides of the new rule are Infrastructure
names that will never gate a live pipeline stage, so this validator's
own mechanism can never again be tripped by a Trading-pipeline concern.
~17 pre-existing tests (`tests/configuration/test_feature_dependency_validator.py`,
`tests/configuration/test_runtime_feature_manager.py`,
`tests/configuration/test_runtime_api.py`,
`tests/platform_layer/telegram/owner/test_control_commands.py`) that used
`ENABLE_EXECUTION`/`ENABLE_RISK`/`ENABLE_DECISION` purely as their
worked example for exercising the dependency-rejection *mechanism*
(dry-run rejection, audit-on-reject, snapshot-on-reject, the friendly
disable-rejection message) were rewritten to use
`ENABLE_BACKTEST`/`ENABLE_DATASET_SYNC`/`ENABLE_ANALYTICS` instead —
same assertions, same mechanism coverage, no test deleted or weakened.

## TASK 4: Pipeline Guard audit + simplification

`core_layer/pipeline/pipeline_guard.py`'s `PipelineGuard` no longer imports or
constructs `RuntimeFeatureManager` at all. `_check()` (the private
method all four public hooks call) dropped its `feature_name`
parameter entirely — every hook is now purely a function of
`EmergencyManager.get_status()`. `core/pipeline.py` itself required
**zero changes** — it already only calls
`self.pipeline_guard.before_signal()`/etc. and interprets the returned
`GuardDecision`, never touching `PipelineGuard`'s internals, so the
Emergency-state → proceed/skip/abort mapping and every downstream
cascade (empty candidate list, neutral AI substitution, gated
delivery/persistence) are byte-for-byte unchanged from Phase 60.8. This
satisfies STRICT RULE 3 ("Pipeline ishlashi o'zgarmasligi kerak").

## TASK 5: Runtime API audit

`configuration/runtime_api.py`'s `enable_feature()`/`disable_feature()`/
`feature_status()`/`list_runtime_features()` are all fully generic and
name-driven (`enable_feature(name: str, ...)`, not
`enable_execution()`) — confirmed by reading the full file. **No
Trading-specific function exists or ever existed here.** Nothing to
remove; audit only.

## TASK 6: Owner Command audit

Grepped `platform_layer/telegram/owner/*.py` and this codebase's full `*.py` tree for
`enable_execution`/`disable_execution`/`enable_risk`/`disable_risk`/
`enable_decision`/`disable_decision` — zero matches anywhere.
`platform_layer/telegram/owner/control_commands.py`'s `enable_feature(name)`/
`disable_feature(name)` are (like `runtime_api.py`) fully generic and
name-driven; no `/enable_execution`-style command was ever registered
in `platform_layer/telegram/command_router.py`/`platform_layer/telegram/handlers.py`/
`platform_layer/telegram/commands.py` (confirmed in Phase 60.8's own TASK 1 audit,
unchanged since). **No deprecated command exists to mark** — this
STRICT RULE was already satisfied before this phase; only
`control_commands.py`'s own illustrative docstring example (which
showed `ENABLE_EXECUTION ON` as sample output text, never a real
command) was updated to a current Infrastructure name.
