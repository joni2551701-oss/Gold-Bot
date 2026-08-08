# 27 — Signal → Decision (TASK-05)

## Transition
Signal → Decision (DecisionConfidence → RuleEngine/ApprovalEngine →
DecisionEngine final owner → DecisionLogger → DecisionService; AI input
boundary; APPROVE/REJECT/HOLD/WAIT faqat canonical yo'l orqali).

## Input
`SignalCandidate`, `AIAnalysisResult` (advisory), `HTFBiasResult`.
Evidence: `core_layer/pipeline/pipeline.py:487`
`self.decision_engine.evaluate(candidate, ai_result, htf_bias)`.

## Processing (file:line)
- DecisionEngine.evaluate: `decision_layer/decision_engine/decision_engine.py:195-255`.
- Weighted confidence blend (signal 0.40 / htf 0.25 / risk 0.20 / ai 0.15):
  `decision_layer/decision_engine/decision_engine.py:60-63`, `:144-173`.
- Action tanlash (final owner): `decision_layer/decision_engine/decision_engine.py:222-242`.
- DecisionLogger: `decision_layer/decision_logger/decision_logger.py`.
- RuleEngine: `decision_layer/rule_engine/decision_rules.py`.

## Output
`TradeDecision` (action: APPROVE / REJECT / NO_TRADE).
Evidence: `decision_layer/decision_engine/decision_engine.py:244-255`,
`DecisionAction` enum `decision_layer/decision_engine/models.py`.

## Next Consumer
`risk` bosqichi — `core_layer/pipeline/pipeline.py:495`.

## Ownership-rule check — AI input boundary (kritik)
- AI faqat **advisory input**: `AIAnalysisResult` DecisionEngine'ga input
  sifatida kiradi va vaznli formulada 0.15 ulush oladi
  (`decision_engine.py:63`, `:139`). AI o'zi trade'ni approve/reject
  qilMAYDI — u faqat DecisionEngine hisoblaydigan skorga hissa qo'shadi.
- AI approval hard gate sifatida: `decision_engine.py:222`
  `if not ai_analysis.approved: action = REJECT` — AI faqat VETO
  (bloklash) yo'nalishida ta'sir qiladi, o'zi APPROVE bera olmaydi. Bu
  "AI never approves" chegarasini mustahkamlaydi (CLAUDE.md Trading
  Safety).
- APPROVE/REJECT/NO_TRADE faqat DecisionEngine `:222-242` orqali.
  **Eslatma:** task "APPROVE/REJECT/HOLD/WAIT" deydi; live engine
  `DecisionAction` = APPROVE/REJECT/NO_TRADE ishlatadi. HOLD/EXPIRE
  vocabulary'si `decision_layer/decision_service/decision_manager.py`
  (STEP-09 additive-parallel) da — live yo'lda emas
  (`decision_manager.py` docstringi: frozen engine "UNTOUCHED and lives
  on the live pipeline path", `:8-11`).
- Runtime dalil (main.py, real fetch, 23-hujjat): AI stub
  `approved=False` qaytaradi (`ai_layer/ai_engine/ai_analyzer.py:37`), shu
  sababli DecisionEngine `:222` bo'yicha REJECT beradi — AI o'zi hech
  narsa approve qilmagani real logda tasdiqlanadi.

**Ownership eslatma (STOP emas):** DecisionEngine yagona final owner
(live). DecisionConfidence/ApprovalEngine/DecisionService — skeleton yoki
additive-parallel; hujjatlashtirilgan Foundation Freeze holati.

## Status
**PASS** — Signal → Decision real kod bilan tasdiqlangan. AI chegarasi
(advisory-only, VETO-only, o'zi approve qilmaydi) buzilmagan.
</content>
