# GoldBot Ecosystem Architecture — Platform Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Platform Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

**Status: one platform is real.** Telegram (`telegram/`) is fully
built — Command Router → Permission Check → Handler → Service →
Repository, plus an Owner-only subsystem (`platform_layer/telegram/owner/`). None of
Web, Desktop, Android, iOS, or a Mini App exist in the repository —
no `web/`, no frontend server, no mobile app code, no Mini App/webview
integration was found. A Public API does not exist (`core_layer/gateway/` is
internal-only, Section 6). Constitution Article 13 (Future First
Principle) already requires that architecture account for all
platforms from the start without requiring their code today — this
section is that accounting, made explicit and honest rather than
implied.

