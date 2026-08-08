# 08 — Risk → Service Audit (REAL-DATA-011, Item G)

REAL-DATA-009/08_ dalilini qayta ishlatib.

## Holat

Broadcast yo'lida alohida "Risk → Application Service" contract'i
YO'Q. Pipeline risk'dan o'tgan signalni to'g'ridan-to'g'ri qayta
ishlaydi:
- `SignalFormatter.format_signal()` — `core_layer/pipeline/pipeline.py:568`
- `Notifier.send_messages()` — `pipeline.py:599`

`platform_layer/telegram/*_service.py` xizmatlari faqat **bot command
oqimiga** xizmat qiladi (alohida flow — foydalanuvchi buyruqlari),
signal broadcast'ga emas.

## Xulosa

Risk → Service = **NOT WIRED** (topilma, kamchilik belgisi emas).
Yangi contract o'ylab topilmadi. Agar Director signal broadcast uchun
application service qatlamini istasa → **DRQ** (19_ — Risk → Service).
Aks holda joriy to'g'ridan-to'g'ri format+deliver yo'li = WORKING,
KEEP.
