# GoldBot Ecosystem Architecture — Business Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Business Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

**Status: mostly not built.** Subscription tiers exist
(`database_layer/user_repository/subscription_repository.py`, `telegram/subscription_service.py`)
as access-tier gating, not billing. Identity exists, but as
`assistant/identity*.py` — the AI assistant's own identity model, not
a user-authentication/business-identity system. Payment, Wallet,
Billing, and Referral were not found anywhere in the codebase. Future
monetization (per the diagram) is therefore entirely a roadmap item
(Section 19), not a present capability.

