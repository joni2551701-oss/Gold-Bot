# 07 — Decision → Risk — REAL-DATA-009

## Transition

Decision → Risk (RiskManager.evaluate() — chetlab o'tilmagan).

- **INPUT:** `decision` (TradeDecision) — `pipeline.py:495`.
- **PROCESSING:** `self.risk_manager.evaluate(decision)` —
  `pipeline.py:495` (`risk_layer/risk_engine/risk_manager.py`).
  Geometry/stop-loss validatsiyasi va sizing.
- **OUTPUT:** `risk_results: List[RiskResult]` — `pipeline.py:494`,
  `.approved` maydoni bilan.
- **NEXT CONSUMER:** notification-eligibility filtri (`pipeline.py:547-551`)
  — faqat `decision.action == APPROVE AND risk_result.approved` bo'lgan
  candidate Telegram uchun eligible.

## Risk chetlab o'tilmaydi

Har bir `decision` majburan `risk_manager.evaluate()` orqali o'tadi
(`pipeline.py:494-497` list comprehension — har decision uchun). Telegram
yo'liga (`pipeline.py:547-551`) faqat risk_result.approved=True bo'lgan
candidate kiradi. Risk'ni chetlab o'tuvchi hech qanday yo'l yo'q
(CLAUDE.md Trading Safety: "Never bypass Risk Manager").

## Ownership

RiskManager — risk geometry/sizing egasi. Public API
`RiskManager.evaluate()` o'zgarmagan.

## Real runtime dalil

Run `31240675527`: `risk Produced 1 risk result(s)` —
`RiskManager.evaluate() ran` real decision bilan.

## Status: PASS
</content>
