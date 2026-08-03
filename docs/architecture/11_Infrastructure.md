# GoldBot Ecosystem Architecture — Infrastructure

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Infrastructure
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

**Status: partially real.** Security/Authentication/Authorization exist
inside `core_layer/gateway/` (internal-only, Section 6) and `core/secrets.py`.
Monitoring is real and substantial (`monitoring/` — system, market,
error, resource, provider-health, risk, signal, performance monitors).
Logging exists throughout (`core_layer/logger/logger.py`, used everywhere). Storage
is `database/` (SQLite, Constitution Article 4) plus `data/persistence/`
(foundation only). Scheduler is the GitHub Actions workflow
(`trading_bot.yml`) that runs the pipeline every 5 minutes — not an
in-process scheduler. Queue System, dedicated Cache (beyond
`SmartDataCache`, foundation-only), Backup, Disaster Recovery, Metrics/
Observability as a distinct product, and Audit Logs as a first-class
system (beyond `database/audit_log`, which does exist) are largely not
built as named, standalone infrastructure.

