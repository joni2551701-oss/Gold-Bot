# GoldBot — System Layers

Governed by `docs/constitution/CONSTITUTION.md` Article 2 (Dependency
Law). `docs/architecture/ARCHITECTURE_MASTER.md` groups the system by
*pipeline order* (Trading Engine track vs. AI Layer track, meeting
only at the Telegram delivery boundary). This document groups the
same real modules by *responsibility cluster* instead — a second,
complementary view of the same system, not a competing one. Where the
two disagree on a detail, `ARCHITECTURE_MASTER.md` and
`MODULE_DEPENDENCIES.md` are authoritative (they are checked
mechanically; this document is a reading aid).

## The seven layers

```
Layer 0   Foundation           core/, core/secrets.py, config.py
Layer 1   Market Intelligence  data/, context/
Layer 2   Decision Intelligence strategies/, signals/, decision/, risk/
Layer 3   Execution            execution/, lifecycle/
Layer 4   AI Intelligence      ai/ (19 subpackages)
Layer 5   Product Layer        telegram/, platform_layer/telegram/owner/
Layer 6   Media Intelligence   ai/content/, broadcast/, media/, translation/, ai/persona/
```

## Layer detail

**Layer 0 — Foundation.** `core/` (pipeline orchestration, emergency
state, system state), `core/secrets.py` (secret access), `config.py`
(configuration/feature flags). Every layer above depends on Layer 0;
Layer 0 depends on nothing else (Constitution Article 2).

**Layer 1 — Market Intelligence.** `data/` (providers, normalization,
historical collection) and `context/` (context orchestration,
fundamental/economic context). Feeds Layer 2.

**Layer 2 — Decision Intelligence.** `strategies/` → `signals/` →
`decision/` → `risk/`, in that exact order (Constitution Article 2's
Dependency Law). This is the layer the Constitution calls the
"Trading Engine" — deterministic, rule-based, fully auditable. It
accepts one advisory value from Layer 4 (`AIAnalysisResult`, type-only,
Constitution Article 1/3) and calls into nothing in Layer 4, 5, or 6.

**Layer 3 — Execution.** `execution/` (intentionally inert — no live
MT5 order calls exist yet) and `lifecycle/` (paper trade monitoring,
signal lifecycle state). Depends on Layer 2's output only.

**Layer 4 — AI Intelligence.** All 19 subpackages under `ai/` — see
`docs/ai/AI_ARCHITECTURE.md` and `docs/architecture/AI_FLOW.md` for
the internal flow. Never calls Layer 2 or Layer 3 (Constitution
Article 1/3, mechanically verified by the `ai/` import sweep in
`docs/architecture/IMPORT_RULES.md`).

**Layer 5 — Product Layer.** `telegram/` and `platform_layer/telegram/owner/` — the
delivery boundary where Layer 2's trading output and Layer 4's AI
explanation meet a human reader, per Handler → Service → Repository
(Constitution Article 4). See `docs/architecture/TELEGRAM_FLOW.md`.

**Layer 6 — Media Intelligence.** `ai/content/` (content type/contract
foundation, inside `ai/` per the Phase 63.0 Reuse Audit — see
`docs/PHASE63_0_FOUNDATION_AUDIT.md`), plus the three genuinely new
top-level packages `broadcast/`, `media/`, `translation/`, and
`ai/persona/`. Foundation/contract-only as of Phase 63.0 — no real
generation, delivery, or translation call anywhere (`docs/AI_BROADCAST_FOUNDATION.md`,
`docs/policies/BROADCAST_POLICY.md`). Depends on Layer 4 for its
contracts (`ContentType`, `ExplanationOutput`), never triggers a
Layer 2 or Layer 3 action.

## Why Layer 6 is separate from Layer 4

`broadcast/`, `media/`, and `translation/` are top-level packages, not
`ai/broadcast/` etc. — the same reasoning that keeps `execution/`
(Layer 3) separate from `decision/` (Layer 2): channel/delivery
management and media-type management are genuinely different
responsibilities from AI content *generation*, even though Layer 6
consumes Layer 4's contracts. See
`docs/PHASE63_0_FOUNDATION_AUDIT.md` for the original Reuse Audit that
established this split.

## Related

- `docs/architecture/LAYER_CONTRACT.md` — the one-page per-layer
  Input / Output / Allowed / Forbidden contract.
- `docs/architecture/ARCHITECTURE_MASTER.md` — the pipeline-order view
  of the same system.
- `docs/architecture/MODULE_DEPENDENCIES.md` — the mechanically
  checked per-module dependency map.
- `docs/architecture/DATA_FLOW.md`, `docs/architecture/AI_FLOW.md` —
  the request-by-request flow through Layers 1–4.
