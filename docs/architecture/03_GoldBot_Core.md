# GoldBot Ecosystem Architecture — GoldBot Core

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the GoldBot Core
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

Full per-engine Responsibility/Input/Output/Dependencies/Forbidden
detail is `docs/architecture/ARCHITECTURE_MASTER.md`'s "Per-Layer
Responsibility" section and `docs/architecture/LAYER_CONTRACT.md` — the
authoritative, Constitution-governed version. Not restated here.
Ecosystem-level summary and the one genuine finding this audit adds
(the three named engines that do not exist as separate modules):

| Ecosystem diagram box | Real module | Note |
|---|---|---|
| Market Engine | *(no separate module)* | Absorbed into `data/` (fetch) + `context/` (structure) |
| Context Engine | `context_layer/context_engine/context_orchestrator.py` | Real, matches `ARCHITECTURE_MASTER.md` |
| Analysis Engine | *(no separate module)* | Absorbed into `context/`'s detectors (Wyckoff/Regime/Session) + `signals/signal_quality.py` |
| Strategy Engine | `strategies/strategy_manager.py` | Real |
| Confluence Engine | *(no separate module)* | Confluence logic lives inside each strategy in `strategies/*.py`, reinforced by `signals/signal_quality.py` |
| Decision Engine | `decision/decision_engine.py` | Real |
| Risk Engine | `risk/risk_manager.py` | Real |
| Signal Engine | `signals/signal_engine.py` | Real |
| Monitoring | `monitoring/` | Real, matches by name |
| Simulation | `backtesting/` + `execution/simulator/` | Real, different name |

This "Market/Analysis/Confluence Engine absorbed, not separate" finding
is logged again in Section 18 (Gap Analysis) and is a genuine
diagram-vs-code discrepancy — listed, not resolved here, per the
Owner's instruction (Section 21).

