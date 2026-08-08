# 28 — Decision → Risk (TASK-06)

## Transition
Decision → Risk (RiskEngine/PositionSizing/MoneyManagement/DrawdownManager/
ExposureManager/PortfolioManager/RiskValidator; Decision Risk'ni chetlab
o'tmasligi kerak — `RiskManager.evaluate()` yo'lda ekanligini tekshir).

## Input
`TradeDecision`.
Evidence: `core_layer/pipeline/pipeline.py:495`
`self.risk_manager.evaluate(decision)`.

## Processing (file:line)
- RiskManager.evaluate: `risk_layer/risk_engine/risk_manager.py:100-248`.
- Non-APPROVE reject (birinchi tekshiruv): `risk_layer/risk_engine/risk_manager.py:131-136`.
- Emergency bloklash: `:138-145`.
- Geometry validatsiya: `:149-156` (`validate_geometry`, `:348`).
- Stop-loss masofa validatsiya: `:160-164`.
- Risk % chegara: `:166-172`.
- Risk/Reward: `:174-182`.
- Duplicate (RiskValidator): `:196-204` (`duplicate_checker`).
- Drawdown (DrawdownManager/account_state_tracker): `:206-217`.
- Daily loss: `:219-228`.
- Position sizing: `:239-240` (`calculate_position_size`).

## Output
`RiskResult` (approved: bool, lot_size, risk_amount, risk_reward).
Evidence: `risk_layer/risk_engine/risk_manager.py:42-50`, `:242-246`.

## Next Consumer
`signal_history` (`:519`) va approve-filtri (`:547-551`) — faqat
`decision.action == APPROVE AND risk_result.approved` bo'lgan nomzod
Telegram'ga eligible.

## Ownership-rule check — Risk chetlab o'tilmaganligi (kritik)
- Har bir `decision` uchun `RiskManager.evaluate()` chaqiriladi
  (`pipeline.py:494-497`, list comprehension — har bir decision uchun).
  Chetlab o'tish yo'li yo'q.
- Telegram eligibility'ning har ikkala sharti majburiy: DecisionEngine
  APPROVE **VA** RiskManager approved (`pipeline.py:547-551`). Risk
  reject qilsa, hatto APPROVE decision ham Telegram'ga bormaydi.
- RiskManager birinchi navbatda non-APPROVE decision'ni rad etadi
  (`:131`), ya'ni Decision → Risk yo'nalishi bir tomonlama va Risk
  hokim.
- PositionSizing/MoneyManagement/ExposureManager/PortfolioManager —
  `risk_layer/` ichida; live pipeline `evaluate()` bilan yagona entry
  ishlatadi (public API `RiskManager.evaluate()` barqaror, CLAUDE.md).
- Trading Safety: Risk mantiqiga TEGILMADI (read-only audit).

## Status
**PASS** — Decision → Risk tasdiqlangan. `RiskManager.evaluate()` yo'lda
va chetlab o'tilmagan; Telegram eligibility Risk approval'ga bog'liq.
</content>
