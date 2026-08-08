# REAL-DATA-007 — 05. Real Price Stream Evidence

## Haqiqiy dalil manbai: REAL-DATA-006 CI run
CI run **31251456946** (REAL-DATA-006 real probe) — empirik natija:
- **3 tick** urinildi (real TwelveData HTTP probe).
- **0 update** — birorta ham real narx yangilanishi bo'lmadi.
- **M1 `ValueError`** — `TwelveDataProvider(asset="XAUUSD")` default
  `interval="M1"`, client esa M5/M15/H1/H4/Daily'ni qo'llaydi →
  `fetch_candles()` `ValueError` (`twelve_data_client.py:66-70`).

Bu — GoldBot Price Stream'ining production'da 0 real update chiqarishini
ko'rsatadigan CHINAKAM (mock emas) dalil.

## Bu REAL-DATA-007 kontrakt bo'shlig'ini qanday tasdiqlaydi
1. M1 xatosi alomat, sabab emas: chinakam sabab — candle-only API'ga
   tick-darajali interval berilishi. To'g'ri yechim M1→M5 EMAS (u shunchaki
   candle polling'ni "stream" deb qayta nomlaydi), balki chinakam
   current-price/quote kontrakti kerak — u YO'Q.
2. Stream ishga tushsa ham (M5'da), u faqat candle close'larni emit qiladi,
   tik emas — ya'ni baribir current-price oqimi bo'lmaydi.

## Nega YANGI probe ishga tushirilmadi (audit-only)
- Current-price probe **qo'llanilmaydi**: current-price kontrakti yo'q
  (`03`), shuning uchun uni sinaydigan probe yozib bo'lmaydi.
- M5 probe **taqiqlangan workaround**: M1→M5 o'zgarishi (production wiring
  o'zgarishi) Direktor Review talab qiladi va u candle polling'ni stream
  deb yashiradi — REAL-DATA-007 aynan shuni qilmaslikni buyuradi.
- REAL-DATA-006'ning real probe'i (run 31251456946) M1 muvaffaqiyatsizligini
  allaqachon empirik ko'rsatdi — qayta ishga tushirish shart emas.

## Xulosa
Real dalil: 0 real update, M1 `ValueError`, real CI (006, run 31251456946).
Yangi probe yo'q — kontrakt bo'shlig'i uni qo'llab bo'lmaydigan qiladi.
