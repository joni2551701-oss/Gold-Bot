# 06 — Signal → Decision — REAL-DATA-009

## Transition

Signal → Decision (DecisionEngine — yakuniy egasi; AI advisory/VETO-only).

- **INPUT:** `candidate` (SignalCandidate), `ai_result`
  (AIAnalysisResult), `htf_bias` (HTFBiasResult) — `pipeline.py:487-488`.
- **PROCESSING:** `self.decision_engine.evaluate(candidate, ai_result,
  htf_bias)` — `pipeline.py:487`
  (`decision_layer/decision_engine/decision_engine.py:198+`). Signal
  confidence, HTF bias, (inverted) AI risk score va AI confidence
  DecisionWeights bo'yicha blend qilinadi; AI'ning approve flag'i
  **hard gate** sifatida tekshiriladi.
- **OUTPUT:** `decisions: List[TradeDecision]` — `pipeline.py:486`,
  `action` = APPROVE/REJECT/NO_TRADE.
- **NEXT CONSUMER:** RiskManager (`pipeline.py:495`).

## AI advisory / VETO-only — file:line

`decision_layer/decision_engine/decision_engine.py:222`:
```
if not ai_analysis.approved:
    ... reason = f"AI Analyzer did not approve this signal: ..."
```
AI faqat VETO qila oladi (approve=False → signal o'tmaydi), lekin AI
o'zi trade'ni APPROVE/REJECT/NO_TRADE qilolmaydi — yakuniy qaror faqat
DecisionEngine'niki (canonical path). AIAnalyzer Telegram/execution/Risk
chaqirmaydi (11_BYPASS_AUDIT).

## Ownership

DecisionEngine — qarorning yagona egasi. AI (`ai_layer/`) — faqat
advisory input.

## Real runtime dalil

Run `31240675527`: `ai approved=False` (heuristic stub) → `decision
Produced 1 trade decision(s)`. AI rad etdi, lekin DecisionEngine har
candidate uchun evaluate qildi.

## Status: PASS
</content>
