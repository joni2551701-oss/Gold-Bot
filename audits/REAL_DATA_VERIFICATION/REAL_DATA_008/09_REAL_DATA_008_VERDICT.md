# 09 — REAL-DATA-008 VERDIKT

## Holat: PENDING CI

Lokal validatsiya to'liq o'tdi, lekin haqiqiy 3-update dalili CI dan
kutilmoqda (sandboxda egress yo'q).

## PASS sharti (qat'iy — workaround YO'Q)

Verdikt PASS bo'lishi uchun CI `real_data_probe` (workflow_dispatch)
quyidagilarni ko'rsatishi SHART:

1. 3/3 yangilanishda real `provider_price` keldi (TwelveData `/price`), VA
2. 3/3 da tenglik zanjiri `provider_price == validated_price ==
   memory_price` (`equality_chain=PASS`), VA
3. `event_published=YES` har yangilanishda.

## Aks holda: BLOCKED + Director Review

Agar `/price` endpoint CI da ishlamasa (plan cheklovi, kutilmagan javob
shakli, xato), yoki tenglik zanjiri 3/3 mos kelmasa — natija **BLOCKED**,
real sabab bilan (probe `tick_error` klass nomini yoki mos kelmagan
yangilanishlar sonini xabar qiladi). Workaround, M1/M5 fallback yoki
candle.close jonli narx sifatida ISHLATILMAYDI.

## Lokal dalil (sandbox)

- `python -m pytest tests/` → 5503 passed (5493 + 10).
- `python -m pyflakes` → toza. `python -m compileall .` → toza.
- `python main.py` → barcha pipeline bosqichlari avvalgidek ishladi; candle
  yo'li (`fetch_candles`) o'zgarmagan (sandboxda kalit yo'qligi sabab 0
  candle — baseline bilan bir xil, mening o'zgarishimdan emas).
- `real_price_stream_probe.py` lokal → BLOCKED (kalit MISSING), crash yo'q.

## Xulosa
Kod yozildi va lokal tasdiqlandi. Verdikt = **PENDING CI**.
