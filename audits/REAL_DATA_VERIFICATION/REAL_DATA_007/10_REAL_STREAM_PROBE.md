# REAL-DATA-007 — 10. Real Stream Probe

## Yangi probe: YO'Q (asoslangan holda)
REAL-DATA-007 audit-only. Yangi probe ishga tushirilmadi va CI dispatch
qilinmadi (topshiriq talabi).

## Nega yangi probe qo'llanilmaydi
1. **Current-price probe imkonsiz**: current-price/quote kontrakti repoda
   mavjud emas (`03_TWELVEDATA_STREAM_VERIFICATION.md`) — sinaydigan narsa
   yo'q.
2. **M5 probe = taqiqlangan workaround**: default interval'ni M1→M5
   o'zgartirish production wiring o'zgarishi (Direktor Review) va u
   candle-polling'ni stream deb yashiradi — REAL-DATA-007 buni taqiqlaydi.

## Mavjud real dalil (qayta ishlatilgan)
REAL-DATA-006 real probe — CI run **31251456946**:
- 3 tick, 0 update, M1 `ValueError`.
Bu M1 muvaffaqiyatsizligini allaqachon empirik ko'rsatgan real dalil.
Qayta ishga tushirish shart emas va topshiriq bo'yicha taqiqlangan.

## Xulosa
Yangi probe yo'q; kontrakt bo'shlig'i har qanday to'g'ri probe'ni
qo'llab bo'lmaydigan qiladi. 006'ning real CI dalili yetarli.
