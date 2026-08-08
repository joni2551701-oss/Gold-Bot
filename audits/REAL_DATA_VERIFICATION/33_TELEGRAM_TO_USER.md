# 33 — Telegram → User (TASK-12/13)

## Transition
Telegram → real USER delivery.

## Input
Formatlangan signal matni (`telegram_messages`), real bot token va real
chat destination.

## Processing (file:line)
- Delivery chaqiruvi: `core_layer/pipeline/pipeline.py:599`
  `self.notifier.send_messages(telegram_messages)`.
- `Notifier` → `TelegramBot` (`platform_layer/telegram/bot.py`) → Telegram
  Bot API.
- Real yetkazish uchun kerak: real `TELEGRAM_*` token + real chat ID +
  yuboriladigan signal.

## Output
Real foydalanuvchi qurilmasidagi xabar (bu auditda tasdiqlanmagan).

## Ownership-rule check / Xavfsizlik
- Real xabar yuborish — tashqariga (destination'ga) qaratilgan harakat.
  Ushbu audit muhitida xavfsiz test kanali ekanligi tasdiqlanmagan
  destination'ga real xabar yuborilMADI (order buni aniq taqiqlaydi).
- main.py graceful: token yo'q bo'lganda `TelegramBot` `None` bo'ladi va
  hech narsa yuborilmaydi (`notifier.py:39-41`) — 23-hujjat runtime logi
  buni tasdiqlaydi ("Sent 0/0 telegram notification(s)").

## Status
**NOT VERIFIED** — real foydalanuvchi qabul qilishi ushbu auditda
xavfsiz tarzda bajarib bo'lmaydi (noma'lum destination'ga real xabar
yuborish taqiqlangan). Bu yashiriladigan nosozlik EMAS.

## Unblock qilish uchun
- VPS'da nazorat ostidagi test chat bilan tekshirilishi, YOKI Director
  xavfsiz test chat ID'ni tasdiqlashi kerak. Shundan keyingina Telegram →
  User real dalil bilan tasdiqlanadi.
</content>
