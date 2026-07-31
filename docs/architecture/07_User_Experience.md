# GoldBot Ecosystem Architecture — User Experience Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the User Experience Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

**Status: not built as standalone products.** Chart, Replay, Journal,
Analytics, Notifications, Portfolio, and Learning as *user-facing
experiences* (as opposed to the internal packages with similar names
audited in Sections 6/7/11) do not exist as their own UX layer — there
is no separate presentation/UX code beyond what Telegram's message
formatting already does. This layer depends entirely on Section 8's
Platform Layer existing first (a Web/Mobile client to render it), which
it does not yet.

