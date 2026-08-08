# 08 — Risk → Service — REAL-DATA-009 (KEY: NOT WIRED vs WIRED)

## Savol

Risk'dan o'tgan signal broadcast yo'lida FLOW-019 Application Service
(`platform_layer/telegram/*_service.py`) orqali marshrutlanadimi, yoki
`telegram_format`/`Notifier` orqali to'g'ridan-to'g'ri format+deliver
qilinadimi?

## Aniqlangan kod yo'li (file:line)

Risk'dan keyingi broadcast yo'li `pipeline.py`da to'liq shunday:

1. `risk` → `risk_results` — `pipeline.py:494`
2. notification-eligibility filtri (`approved_indices`) — `pipeline.py:547-551`
3. best_index tanlash — `pipeline.py:558-562`
4. `telegram_format`: `self.signal_formatter.format_signal(...)` —
   `pipeline.py:568`
5. `telegram_delivery`: `self.notifier.send_messages(...)` —
   `pipeline.py:599`
6. `database`: `self.signal_repository.save_signal_record(...)` —
   `pipeline.py:625`

## Pipeline import'lari (dalil)

`grep import ... platform_layer` (`pipeline.py`):
- `pipeline.py:24` — `from platform_layer.telegram.signal_formatter import SignalFormatter`
- `pipeline.py:25` — `from platform_layer.telegram.notifier import Notifier`

Pipeline `platform_layer/telegram/`dan **faqat** `SignalFormatter` va
`Notifier`ni import qiladi. Hech qanday `*_service.py`
(UserService/SignalService/SubscriptionService/NotificationService)
broadcast yo'lida import QILINMAYDI yoki chaqirilMAYDI.

## Determination: **NOT WIRED**

Broadcast yo'lida alohida "Risk → Application Service" contract'i YO'Q.
Pipeline risk'dan o'tgan signalni to'g'ridan-to'g'ri `SignalFormatter`
(format) va `Notifier` (deliver) orqali qayta ishlaydi, oraliq
application-service qatlamisiz.

`platform_layer/telegram/*_service.py` xizmatlari
(UserService/SignalService/SubscriptionService/NotificationService va
b.) **ALOHIDA** oqimga — Telegram BOT COMMAND flow'iga (foydalanuvchi
registratsiyasi/subscription/signal-access) xizmat qiladi, bu esa
pipeline'ning signal BROADCAST oqimidan farq qiladi. Handler'lar
`handlers.py` → `*_service.py` → `*_repository.py` (FLOW-019) — bu bot
command yo'li, broadcast emas.

Yangi "Risk → Application Service" contract'i O'YLAB TOPILMAYDI (order
talabi). Broadcast yo'li to'g'ridan-to'g'ri format+deliver qiladi.

## Ownership

SignalFormatter — DTO/message qurish; Notifier — delivery. Ikkalasi
`platform_layer/telegram/`da, lekin ular application service emas,
formatter/notifier komponentlari.

## Status: **NOT WIRED** (pipeline to'g'ridan-to'g'ri format/deliver
qiladi — bu topilma, kamchilik-belgi emas; Director qaroriga havola —
15_ Final Gate).
</content>
