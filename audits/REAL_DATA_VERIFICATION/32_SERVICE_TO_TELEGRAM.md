# 32 — Service → Telegram (TASK-11)

## Transition
Service → Telegram (handler/formatter/Telegram API chaqiruvi; AI→Telegram
bypass yo'q).

## Input
Application service natijasi (matn) yoki pipeline'dagi formatlangan signal
matni.

## Processing (file:line)
- Pipeline delivery: `core_layer/pipeline/pipeline.py:599`
  `self.notifier.send_messages(telegram_messages)` — faqat
  `send_notifications=True` va `execution_decision.proceed` bo'lганда
  (`:593`).
- Notifier: `platform_layer/telegram/notifier.py` — `send()`/`send_message()`
  faqat matn yetkazadi, analiz/risk/approve QILMAYDI
  (`platform_layer/telegram/notifier.py:24-30` docstring: "It must never
  analyze signals, calculate risk, approve trades, or modify decisions").
- Telegram bot: `platform_layer/telegram/bot.py` (`TelegramBot`) — token
  yo'q bo'lsa graceful (`self._bot = None`), hech qachon raise qilmaydi
  (`notifier.py:39-41`).
- Bot buyruq yo'li: handler → service → matn → Telegram API.

## Output
Telegram API chaqiruvi (real send faqat token+chat mavjud bo'lganda).

## Next Consumer
Real foydalanuvchi (33-hujjat).

## Ownership-rule check — AI→Telegram bypass yo'qligi (kritik)
- AI layer (`ai_layer/`) Telegram'ni to'g'ridan-to'g'ri chaqirmaydi.
  Pipeline'da AI natijasi faqat DecisionEngine'ga input
  (`pipeline.py:487`), Telegram delivery esa alohida, faqat
  APPROVE+approved winner uchun (`:547-574`, `:599`).
- Notifier analiz qilmaydi (`notifier.py:24-30`) — signal mantiqidan
  ajratilgan.
- REJECT/NO_TRADE/risk-blocked nomzodlar hech qachon formatlanmaydi yoki
  yuborilmaydi (`pipeline.py:540-551`) — bu REJECT/BLOCKED signallar
  Telegram'ga yetib borgan insidentning tuzatmasi (CLAUDE.md AUDIT_REPORT).

## Status
**PASS** — Service/Pipeline → Telegram real kod bilan tasdiqlangan.
AI→Telegram bypass yo'q; Notifier faqat delivery. (Real send'ning o'zi
33-hujjatda NOT VERIFIED.)
</content>
