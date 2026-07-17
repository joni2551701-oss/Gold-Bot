# GoldBot Documentation Index

**Start here, always, in this order:**

1. [`constitution/CONSTITUTION.md`](constitution/CONSTITUTION.md) —
   the supreme governance document (Phase 62.0). Read this before any
   other document or task brief.
2. [`/CLAUDE.md`](../CLAUDE.md) — Engineering Governance: architecture
   layering, the mandatory Commit Protocol, Trading Safety hard rules.
3. The four `architecture/` documents below — the practical,
   checkable expression of the Constitution's Articles.

## Foundation (Phase 62.0 — the "Foundation Lock")

| Document | What it covers |
|---|---|
| [`constitution/CONSTITUTION.md`](constitution/CONSTITUTION.md) | The 7 Articles every future task binds to |
| [`architecture/ARCHITECTURE_MASTER.md`](architecture/ARCHITECTURE_MASTER.md) | System-wide layer diagram, per-layer CAN/CANNOT |
| [`architecture/MODULE_DEPENDENCIES.md`](architecture/MODULE_DEPENDENCIES.md) | Real, current per-module dependency map |
| [`architecture/IMPORT_RULES.md`](architecture/IMPORT_RULES.md) | Allowed/forbidden import table, line-by-line |
| [`architecture/EXTENSION_GUIDE.md`](architecture/EXTENSION_GUIDE.md) | How to add a new AI capability or Telegram command correctly |
| [`roadmap/VERSIONS.md`](roadmap/VERSIONS.md) | v0.1 → v1.0 version roadmap |
| [`roadmap/AI_EVOLUTION.md`](roadmap/AI_EVOLUTION.md) | AI Foundation → Runtime → ... → Senior Trading AI timeline |
| [`owner/OWNER_PANEL.md`](owner/OWNER_PANEL.md) | Owner Telegram Control Center, section by section |
| [`telegram/TELEGRAM_ARCHITECTURE.md`](telegram/TELEGRAM_ARCHITECTURE.md) | Real Telegram Router → Permission → Handler → Service → Repository flow |
| [`ai/AI_ARCHITECTURE.md`](ai/AI_ARCHITECTURE.md) | Real `ai/` package tree, all 19 subpackages |

## Trading Pipeline & Architecture (general)

| Document | What it covers |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Original full pipeline + AI Runtime data-flow diagrams |
| [`ARCHITECTURE_AUDIT.md`](ARCHITECTURE_AUDIT.md) | Historical architecture audit |
| [`ARCHITECTURE_READINESS_REVIEW.md`](ARCHITECTURE_READINESS_REVIEW.md) | Pre-Phase-59 readiness review |
| [`ARCHITECTURE_RULES.md`](ARCHITECTURE_RULES.md) | Earlier architecture rules (predates the Constitution) |
| [`DEPENDENCY_MAP.md`](DEPENDENCY_MAP.md) | Historical dependency map (see `architecture/MODULE_DEPENDENCIES.md` for the current one) |
| [`MODULE_CONTRACTS.md`](MODULE_CONTRACTS.md) | Module-level contracts |
| [`FOLDER_STRUCTURE_REVIEW.md`](FOLDER_STRUCTURE_REVIEW.md) | Folder structure review |
| [`code_structure.md`](code_structure.md) | Code structure notes |
| [`SYSTEM_OVERVIEW.md`](SYSTEM_OVERVIEW.md) | System overview |
| [`DECISION_PRINCIPLES.md`](DECISION_PRINCIPLES.md) | Decision Engine principles |
| [`PIPELINE_GUARD.md`](PIPELINE_GUARD.md) | Pipeline guard mechanism |
| [`STRATEGY_LIFECYCLE.md`](STRATEGY_LIFECYCLE.md) | Strategy lifecycle |
| [`SIGNAL_SCHEMA.md`](SIGNAL_SCHEMA.md) / [`SIGNAL_QUALITY.md`](SIGNAL_QUALITY.md) | Signal contract and quality rules |
| [`HTF_BIAS.md`](HTF_BIAS.md) / [`MARKET_REGIME.md`](MARKET_REGIME.md) / [`WYCKOFF.md`](WYCKOFF.md) | Context/strategy detection concepts |
| [`CONTEXT_SNAPSHOT.md`](CONTEXT_SNAPSHOT.md) | Context snapshot contract |

## Data & Market Providers

[`MARKET_PROVIDER.md`](MARKET_PROVIDER.md) ·
[`MARKET_DATA_ARCHITECTURE.md`](MARKET_DATA_ARCHITECTURE.md) ·
[`PROVIDER_CONTRACTS.md`](PROVIDER_CONTRACTS.md) ·
[`TRADINGVIEW_PROVIDER.md`](TRADINGVIEW_PROVIDER.md) ·
[`DATA_QUALITY.md`](DATA_QUALITY.md) ·
[`DATA_VALIDATION.md`](DATA_VALIDATION.md) ·
[`DATA_COLLECTION_RULES.md`](DATA_COLLECTION_RULES.md) ·
[`DATASET_COLLECTION.md`](DATASET_COLLECTION.md) ·
[`HISTORICAL_SYNC.md`](HISTORICAL_SYNC.md) ·
[`VALIDATION_GUIDE.md`](VALIDATION_GUIDE.md) ·
[`FEATURE_ENGINEERING.md`](FEATURE_ENGINEERING.md) ·
[`FEATURE_REGISTRY.md`](FEATURE_REGISTRY.md) ·
[`FEATURE_REGISTRY_SEPARATION.md`](FEATURE_REGISTRY_SEPARATION.md) ·
[`RUNTIME_FEATURE_CONTROL.md`](RUNTIME_FEATURE_CONTROL.md)

## Backtesting, Execution & Performance

[`BACKTESTING_ENGINE.md`](BACKTESTING_ENGINE.md) ·
[`REPLAY_ENGINE.md`](REPLAY_ENGINE.md) ·
[`EXECUTION_SIMULATOR.md`](EXECUTION_SIMULATOR.md) ·
[`PERFORMANCE.md`](PERFORMANCE.md) ·
[`PERFORMANCE_METRICS.md`](PERFORMANCE_METRICS.md) ·
[`PERFORMANCE_VALIDATION.md`](PERFORMANCE_VALIDATION.md)

## Learning & Fundamentals

[`LEARNING_LOOP.md`](LEARNING_LOOP.md) ·
[`LEARNING_LOOP_AUDIT.md`](LEARNING_LOOP_AUDIT.md) ·
[`FUNDAMENTAL_INTELLIGENCE.md`](FUNDAMENTAL_INTELLIGENCE.md) ·
[`ADAPTIVE_INTELLIGENCE_AUDIT.md`](ADAPTIVE_INTELLIGENCE_AUDIT.md) ·
[`ASSET_INTELLIGENCE.md`](ASSET_INTELLIGENCE.md) ·
[`SESSION_INTELLIGENCE.md`](SESSION_INTELLIGENCE.md)

## AI Layer (general — see `ai/AI_ARCHITECTURE.md` above for the current real package map)

[`AI_ARCHITECTURE.md`](AI_ARCHITECTURE.md) — Phase 55 pre-integration
audit (historical; superseded as the canonical map by
[`ai/AI_ARCHITECTURE.md`](ai/AI_ARCHITECTURE.md)) ·
[`AI_INFRASTRUCTURE.md`](AI_INFRASTRUCTURE.md) ·
[`AI_PROVIDER_FOUNDATION.md`](AI_PROVIDER_FOUNDATION.md) ·
[`AI_INTELLIGENCE_LAYER.md`](AI_INTELLIGENCE_LAYER.md) ·
[`AI_PRODUCT_CONTROL_LAYER.md`](AI_PRODUCT_CONTROL_LAYER.md) ·
[`AI_PRODUCTION_INTEGRATION.md`](AI_PRODUCTION_INTEGRATION.md) ·
[`AI_RUNTIME_FOUNDATION.md`](AI_RUNTIME_FOUNDATION.md) ·
[`AI_RUNTIME_OPERATIONS.md`](AI_RUNTIME_OPERATIONS.md) ·
[`AI_RUNTIME_FLOW.md`](AI_RUNTIME_FLOW.md) ·
[`EXPLAINABILITY.md`](EXPLAINABILITY.md) ·
[`FOUNDATION_GAP_ANALYSIS.md`](FOUNDATION_GAP_ANALYSIS.md)

## Telegram & Owner Panel

[`telegram_layer.md`](telegram_layer.md) ·
[`OWNER_COMMANDS.md`](OWNER_COMMANDS.md) ·
[`OWNER_PERMISSIONS.md`](OWNER_PERMISSIONS.md) ·
[`EMERGENCY_SYSTEM.md`](EMERGENCY_SYSTEM.md) ·
[`commands_reference.md`](commands_reference.md)

## Database, Security & Operations

[`DATABASE.md`](DATABASE.md) ·
[`database_schema.md`](database_schema.md) ·
[`CONFIGURATION_MANAGEMENT.md`](CONFIGURATION_MANAGEMENT.md) ·
[`CONFIG_SNAPSHOT.md`](CONFIG_SNAPSHOT.md) ·
[`SECURITY.md`](SECURITY.md) ·
[`AUDIT_REPORT.md`](AUDIT_REPORT.md) ·
[`AUDIT_SYSTEM.md`](AUDIT_SYSTEM.md) ·
[`ERROR_HANDLING.md`](ERROR_HANDLING.md) ·
[`LOGGING.md`](LOGGING.md) ·
[`DEPLOYMENT.md`](DEPLOYMENT.md) ·
[`production_setup.md`](production_setup.md) ·
[`TESTING.md`](TESTING.md)

## Development

[`DEVELOPMENT_GUIDE.md`](DEVELOPMENT_GUIDE.md) ·
[`DEVELOPMENT_RULES.md`](DEVELOPMENT_RULES.md) ·
[`DOCUMENTATION_STANDARD.md`](DOCUMENTATION_STANDARD.md) ·
[`DOCUMENTATION_AUDIT.md`](DOCUMENTATION_AUDIT.md)

## Phase History (audits & freeze declarations, chronological)

[`PHASE59_ARCHITECTURE_FREEZE.md`](PHASE59_ARCHITECTURE_FREEZE.md) ·
[`PHASE59_VALIDATION.md`](PHASE59_VALIDATION.md) ·
[`PHASE60_ARCHITECTURE_AUDIT.md`](PHASE60_ARCHITECTURE_AUDIT.md) ·
[`PHASE60_8_INTEGRATION_AUDIT.md`](PHASE60_8_INTEGRATION_AUDIT.md) ·
[`PHASE60_10_FOUNDATION_AUDIT.md`](PHASE60_10_FOUNDATION_AUDIT.md) ·
[`FOUNDATION_FREEZE_v0.4.md`](FOUNDATION_FREEZE_v0.4.md) ·
[`PHASE61_AI_FOUNDATION_AUDIT.md`](PHASE61_AI_FOUNDATION_AUDIT.md) ·
[`PHASE61_1_PROVIDER_AUDIT.md`](PHASE61_1_PROVIDER_AUDIT.md) ·
[`PHASE61_1_1_FOUNDATION_CORRECTIONS.md`](PHASE61_1_1_FOUNDATION_CORRECTIONS.md) ·
[`PHASE61_1_1_FOUNDATION_CORRECTIONS_AUDIT.md`](PHASE61_1_1_FOUNDATION_CORRECTIONS_AUDIT.md) ·
[`PHASE61_2_RUNTIME_AUDIT.md`](PHASE61_2_RUNTIME_AUDIT.md) ·
[`PHASE61_3_INTELLIGENCE_AUDIT.md`](PHASE61_3_INTELLIGENCE_AUDIT.md) ·
[`PHASE61_3_INTELLIGENCE_FREEZE.md`](PHASE61_3_INTELLIGENCE_FREEZE.md) ·
[`PHASE61_4_PRODUCT_CONTROL_AUDIT.md`](PHASE61_4_PRODUCT_CONTROL_AUDIT.md) ·
[`PHASE61_4_PRODUCT_CONTROL_FREEZE.md`](PHASE61_4_PRODUCT_CONTROL_FREEZE.md) ·
[`PHASE61_5_PRODUCTION_INTEGRATION_AUDIT.md`](PHASE61_5_PRODUCTION_INTEGRATION_AUDIT.md) ·
[`PHASE61_5_FREEZE.md`](PHASE61_5_FREEZE.md) ·
[`PHASE61_6_RUNTIME_OPERATIONS_AUDIT.md`](PHASE61_6_RUNTIME_OPERATIONS_AUDIT.md) ·
[`PHASE61_7_INTEGRATION_AUDIT.md`](PHASE61_7_INTEGRATION_AUDIT.md) ·
[`PHASE61_7_RUNTIME_INTEGRATION.md`](PHASE61_7_RUNTIME_INTEGRATION.md) ·
[`PHASE61_7_FREEZE.md`](PHASE61_7_FREEZE.md) — most recent freeze before this document

## Release Notes & Specifications

[`v0.2_release_notes.md`](v0.2_release_notes.md) ·
[`v0.3_RELEASE_NOTES.md`](v0.3_RELEASE_NOTES.md) ·
[`v0.3_final_audit.md`](v0.3_final_audit.md) ·
[`v0.3_stabilization_report.md`](v0.3_stabilization_report.md) ·
[`v0.3.5_SPECIFICATION.md`](v0.3.5_SPECIFICATION.md)

## Module READMEs (outside `docs/`)

Each major package carries its own `README.md`, unindexed here since
they live with their code, not under `docs/`: `data/README.md`,
`context/README.md`, `signals/README.md`, `decision/README.md`,
`risk/README.md`, `execution/README.md`, `database/README.md`,
`telegram/README.md`, `telegram/owner/README.md`, `ai/README.md`.

---

*This index reflects the real file listing under `docs/` as of Phase
62.0. When adding a new document, add it here in the same pass
(Constitution Article 6 applies to documentation completeness the
same way it applies to test completeness).*
