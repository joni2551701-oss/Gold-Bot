# Telegram Layer

## Responsibility
User communication — commands, settings, subscriptions, admin panel,
feedback, and outbound signal notification. **Telegram never makes a
trading decision.** It formats and delivers what the pipeline already
decided; it never approves, rejects, sizes, or alters a signal. See
`docs/ARCHITECTURE_RULES.md`'s Telegram Layer section.

## Input
`signal_layer.signal_builder.models.SignalCandidate`, `ai_layer.ai_engine.ai_analyzer.AIAnalysisResult`,
`decision_layer.decision_engine.models.TradeDecision`, `risk_layer.risk_engine.risk_manager.RiskResult`
(`platform_layer.telegram.signal_formatter.SignalFormatter.format_signal(signal, ai_analysis, decision, risk_result)`)
— the four already-computed pipeline outputs, read defensively
(`getattr` with a safe `"N/A"` default, never raising on a missing/
malformed field). `platform_layer.telegram.notifier.Notifier.send_message()`/
`send_messages()` take the already-formatted message string(s).

## Output
`str` — a complete, human-readable message (`format_signal()`); the
brief's "Message" is this plain string, not a formal `Message`
dataclass. `platform_layer.telegram.notifier.NotifierResult`/a `bool` list from
`send_messages()` reports delivery success per message.

## Allowed Dependencies
✅ `signals/` — reads `SignalCandidate`'s fields to format a message.
Note this is a *read-only, formatting* dependency, not the same
relationship as Decision/Risk consuming a signal — Telegram never
evaluates or scores the candidate itself.

## Forbidden Dependencies
❌ Trading decisions — `telegram/` never imports `strategies/`,
`decision/`, or `risk/` to *make* a call; it only receives their
already-computed `TradeDecision`/`RiskResult` objects as formatting
input, exactly the same way `signal_formatter.py`'s four parameters
work today. It never calls `DecisionEngine.evaluate()` or
`RiskManager.evaluate()` itself.
❌ Direct database access from handlers —
`platform_layer/telegram/handlers.py` never imports `database/*` directly; only
`telegram/*_service.py` does (stated in `platform_layer/telegram/handlers.py`'s own
module docstring, enforced today). See `CLAUDE.md`'s Architecture
Rules for the same boundary.
❌ `ai/`, `execution/`, `context/` — Telegram never re-analyzes a
signal or re-derives context; it renders what other layers already
produced.

## Error Contract
`format_signal()` never raises — every field access is defensive
(`_safe()`/`getattr` with a default), so a missing or malformed
attribute renders as `"N/A"` rather than throwing, guaranteeing a
message is always producible from a well-formed pipeline result.
Telegram API failures (network error, rate limit, blocked bot) are
caught by `Notifier` and reported as a failed delivery result, never
raised past it — a delivery failure must not crash a pipeline cycle.
Per `contracts/error_contract.md`, a Telegram API failure should map
to `ExternalAPIError`; a malformed inbound command should map to
`ValidationError` — not yet formally implemented as typed exceptions.

## Future Extension
`docs/EXPLAINABILITY.md`'s "How AI will use this in the future"
section names Telegram message enrichment with `SignalExplanation`'s
reasons as a not-yet-implemented step. `SignalSchema`/
`ContextSnapshotSchema` (Phase A15/A16) are not read by
`signal_formatter.py` in this phase.
