# 19 — DRQ — Risk → Service (REAL-DATA-011)

**DRQ turi:** Director Review Question / architecture decision.
**Holat:** NOT WIRED. Bu passda O'ZGARTIRILMADI.

## Bir jumlalik so'rov

Director signal broadcast oqimi uchun alohida "Application Service"
qatlamini istaydimi (hozir pipeline risk'dan o'tgan signalni
to'g'ridan-to'g'ri `SignalFormatter` + `Notifier` bilan qayta
ishlaydi)?

## Kontekst

- `pipeline.py:568` `SignalFormatter.format_signal()`, `pipeline.py:599`
  `Notifier.send_messages()` — to'g'ridan-to'g'ri, WORKING.
- `platform_layer/telegram/*_service.py` xizmatlari faqat **bot
  command** oqimiga xizmat qiladi (alohida flow), signal broadcast'ga
  emas.
- Bu topilma (NOT WIRED), kamchilik EMAS — joriy yo'l ishlaydi.

## Nega DRQ

Signal broadcast uchun yangi service qatlami = arxitektura qarori
(yangi contract). Worker yangi arxitekturani implement qilmaydi.

## Tavsiya

Joriy to'g'ridan-to'g'ri format+deliver yo'li = WORKING, KEEP. Agar
Director broadcast uchun rasmiy service qatlamini istasa — RFC + ADR
orqali. Aks holda bu DRQ yopiladi (o'zgarish shart emas).
