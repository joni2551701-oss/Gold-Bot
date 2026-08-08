# 10 — Telegram → User — REAL-DATA-009

## Transition

Telegram → User (real foydalanuvchiga yetkazish).

- **INPUT:** `telegram_messages` + resolved `chat_id`.
- **PROCESSING:** `Notifier.send_messages()` → `_send_all()` →
  `TelegramBot.send_message(message, chat_id)` — `notifier.py:77`.
  chat_id `Secrets().TELEGRAM_CHAT_ID`dan resolve qilinadi
  (`notifier.py:57-64`).
- **OUTPUT:** Telegram API'ga real HTTP send.

## Nega NOT VERIFIED

Real user delivery uchun ikki shart kerak:
1. **Approved signal** — REAL-DATA-004 run'da AI signalni rad etdi
   (approved=False), shuning uchun 0 xabar quriDI — yuboriladigan
   xabar bo'lmadi.
2. **Confirmed-safe destination** — sandbox'da real
   `TELEGRAM_CHAT_ID`/token yo'q; tasodifiy real chat'ga yuborish
   Trading Safety va order taqiqiga zid ("send to a random user/chat"
   — do NOT).

Shu sabab bu transition xavfsiz tarzda bajarib bo'lmaydi. Kod yo'li
mavjud va PASS (09_), lekin real user delivery **bajarilMADI**.

## Status: **NOT VERIFIED** (real chat'ga hech narsa yuborilmadi;
xavfsiz destination + approved signal kerak — Director qaroriga havola)
</content>
