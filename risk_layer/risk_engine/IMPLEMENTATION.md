# risk/

## Maqsad
Decision'ning trade geometriyasini tekshiradi va sizing bo'yicha
tavsiya hisoblab chiqaradi. Signal Telegram'ga yetib borishidan oldingi
oxirgi to'siq (gate).

## Oqim
```
Decision Engine
      |
      v
Risk Manager   -- geometriya + stop-loss validatsiyasi
      |
      v
Telegram Notification Filter (core/pipeline.py)
```

## Vazifalar
- SL/TP geometriya validatsiyasi (BUY: `stop_loss < entry < take_profit`;
  SELL: teskarisi).
- Stop-loss masofasi validatsiyasi.
- Risk/reward va position-size hisoblash (faqat sizing bo'yicha
  tavsiya — broker/MT5 ulanishi yo'q, hech qachon order instruksiyasi
  emas).

## Kirish (Input)
`TradeDecision` (`decision/`dan), ixtiyoriy `account_balance`.

## Chiqish (Output)
`RiskResult` (`approved`, `lot_size`, `risk_amount`, `risk_reward`,
`reason`).

## Bog'liqliklar (Dependencies)
`decision/` va `signals/` (ularning model turlari uchun). `database/`,
`telegram/` yoki `ai/`ga bog'liqlik yo'q.

## Kelajakdagi Roadmap
Hech narsa rejalashtirilmagan. Bu shu Layer'ning `CLAUDE.md`sidagi
Trading Safety qoidalari aynan nomlaydigan narsa: hech qachon chetlab
o'tilmaydi, ruxsatsiz o'zgartirilmaydi.
