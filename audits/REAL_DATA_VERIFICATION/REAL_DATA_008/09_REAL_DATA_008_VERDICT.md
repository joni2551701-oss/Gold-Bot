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

---

## ⚡ YAKUNIY VERDIKT — PASS (run 31253603648, commit bfec9b7)

| Segment | Natija |
|---|---|
| Price Stream architecture | ✅ Current Price Stream (candle polling EMAS) |
| Current-price contract (`/price`) | ✅ REAL — empirik isbotlandi |
| Production provider | TwelveDataPriceSource (XAUUSD); Bitget inert (NOT VERIFIED) |
| Timeframe | N/A — current price (candle interval ishlatilmaydi) ✅ |
| Real API | ✅ TwelveData `/price`, real key, real tarmoq |
| Real updates | ✅ 3/3 (4342.1624, 4342.1624, 4342.35095) |
| Validation | ✅ PASS (3/3) |
| Market Memory | ✅ PASS (3/3, provider==validated==memory) |
| Event Bus (publish) | ✅ real kod (sink PRICE_UPDATED) |
| Event Bus → Core | ⚠️ NOT WIRED (bu task doirasidan tashqari, ataylab) |
| Reconnect | ✅ IMPLEMENTED (state machine) |
| Architecture | ✅ PASS (batch candle path tegilmagan) |
| Tests | ✅ 5503 |
| CI | ✅ validate + real_data_probe success |

**REAL-DATA-008 = PASS.** GoldBot endi haqiqiy real-time current-price
stream'ga ega, candle data'dan toza ajratilgan. Batch trading pipeline
(MarketDataService, M15 candles) o'zgarmagan (REAL-DATA-003/004 isbotlangan).

**Non-blocking carry-over items (bu task doirasidan tashqari):**
Event Bus → Core NOT WIRED (Director qaroriga havola — event-driven Core
kerak bo'lsa RFC/ADR); Bitget inert (NOT VERIFIED); Daily parse bug
(carried); HTF Daily/D1 (carried).
