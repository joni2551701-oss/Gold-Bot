# 09 — Telegram → User (REAL-DATA-011, Item H)

## Holat: NOT VERIFIED — SAFE DESTINATION REQUIRED

Kod yo'li mavjud va PASS:
`SignalFormatter.format_signal()` (`pipeline.py:568`) →
`Notifier.send_messages()` (`pipeline.py:599`). Ammo real chat'ga
xabar yuborish uchun **xavfsiz, tasdiqlangan test destination YO'Q**.

**Bu passda HECH QANDAY real Telegram xabar yuborilmadi** (guardrail).

## Nazoratli test nima talab qiladi (hujjatlashtirilgan)

Xavfsiz Telegram→User tekshiruvi uchun kerak:
1. **Director tomonidan tasdiqlangan test chat id** — CI/environment
   secret sifatida saqlanadi (masalan `TELEGRAM_TEST_CHAT_ID`),
   loglarda **MASKED** ko'rinadi, hech qachon ochiq bosilmaydi.
2. Faqat **approved** (APPROVE + risk_result.approved) signal
   ishlatiladi — REJECT/BLOCKED signal Telegram'ga chiqmasligi kerak
   (pipeline notification-eligibility filtri, `AUDIT_REPORT.md`).
3. Bitta izolatsiya qilingan real send, natija masklangan tarzda
   qayd etiladi, keyin o'chiriladi.

Bularsiz Telegram→User = **NOT VERIFIED**. Worker buni bir tomonlama
qila olmaydi (real chat send — Director Approval talab qiladi).
