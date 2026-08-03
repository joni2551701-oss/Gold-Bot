# AI Policy

The operational face of Constitution Articles 1, 3, and 5, scoped to
day-to-day AI-layer development.

## AI assists, never decides (Article 1)

No AI-layer module calls `decision_layer.decision_engine.decision_engine.DecisionEngine`,
`risk_layer.risk_engine.risk_manager.RiskManager`, triggers execution, or triggers a
Telegram send. `ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface` docstring is
the binding contract for any current or future provider. A new
`Capability` (Article 11's checklist item 5) never changes this — a
capability names *what a human can ask the AI to help with*, never a
trigger for the AI to act on the trading pipeline.

## Provider isolation (Article 5)

A new AI vendor integration is confined to `ai/providers/` (the
provider file, `provider_registry.py`, `provider_capabilities.py`)
plus a `ai/router/routing_rules.py` candidate-order entry. Nothing
above the provider boundary — no `Capability` handler, no Owner
command, no `telegram/` code — ever names a vendor.

## Adding a Capability

Adding a `Capability` enum member (`ai/capabilities/capability.py`)
always requires a matching `ai/router/routing_rules.py` entry (the
pre-existing `test_every_capability_has_a_routing_rule` invariant
enforces this mechanically). `ai/router/router.py` itself — the
selection *logic* — is never touched to add a capability; only the
declarative `ROUTING_RULES` data table is.

## Contract-first for anything not yet real

Phase 63.0 set the standing posture for any AI-adjacent capability
that does not yet have real generation/dispatch behind it: the
contract (`Persona`, `ExplanationOutput`, `ContentType`) ships first,
`AIService.ask()` dispatch ships in a later, separately-approved
phase. A capability without dispatch cleanly rejects — it never
fabricates a response.

## Related

- `docs/constitution/CONSTITUTION.md` Articles 1, 3, 5.
- `docs/ai/AI_ARCHITECTURE.md`.
- `docs/policies/BROADCAST_POLICY.md` — the same contract-first
  posture applied to broadcast/media/translation.
