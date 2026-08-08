# 03 — Haqiqiy narx oqimi dalili (CI 3-update log)

**Holat: PLACEHOLDER — orkestrator to'ldiradi.**

Haqiqiy dalil sandboxdan emas, CI `workflow_dispatch` (`real_data_probe`
job) dan keladi. Bu yerga `scripts/verification/real_price_stream_probe.py`
ning CI chiqishi (3 ta yangilanish) joylashtiriladi.

Har bir yangilanish uchun kutiladigan maydonlar:
`provider_price`, `validated_price`, `memory_price`, `timestamp`,
`validated`, `memory`, `equality_chain`, `event_published`.

## PASS sharti (qat'iy)

- 3/3 yangilanishda real `provider_price` keldi, VA
- 3/3 da tenglik zanjiri `provider_price == validated_price ==
  memory_price` (`equality_chain=PASS`).

Aks holda → **BLOCKED + Director Review** (workaround YO'Q). Agar CI da
`/price` endpoint ishlamasa (plan cheklovi, kutilmagan shakl, xato),
to'g'ri natija — BLOCKED, real sabab bilan (`tick_error` klass nomi).

```
(CI PROBE OUTPUT — TO BE INSERTED BY ORCHESTRATOR)
```

---

## ⚡ REAL CI EVIDENCE — 3/3 real current-price updates (run 31253603648, commit bfec9b7)

Real GitHub Actions muhitida (TWELVE_DATA_API_KEY = CONFIGURED, real
tarmoq), `real_price_stream_probe.py` yangi `TwelveDataPriceSource`
(TwelveData `/price` current-price endpoint) orqali 3 ta haqiqiy update
oldi. Har biri uchun `provider_price == validated_price == memory_price`:

| # | provider_price | validated_price | memory_price | timestamp | equality |
|---|---|---|---|---|---|
| 1 | 4342.1624 | 4342.1624 | 4342.1624 | 2026-08-08T10:49:44.258Z | ✅ PASS |
| 2 | 4342.1624 | 4342.1624 | 4342.1624 | 2026-08-08T10:49:47.763Z | ✅ PASS (unchanged spot — valid) |
| 3 | 4342.35095 | 4342.35095 | 4342.35095 | 2026-08-08T10:50:13.546Z | ✅ PASS (narx harakatlandi) |

Stream: **PASS** (real_updates=3, equality_updates=3).

**Muhim:** UPDATE #3 narxi UPDATE #1/#2 dan FARQ qiladi (4342.1624 →
4342.35095). Bu — bu candle.close emas (candle bir interval davomida
o'zgarmaydi), balki haqiqiy real-time current price ekanligining isboti.
`/price` endpoint real-time spot narx qaytaradi. Mock/hardcoded
ishlatilmadi; API key oqmadi (GitHub masking, probe faqat narx/status).

**Contract javob:** GoldBot Price Stream endi candle polling EMAS — u
haqiqiy Current Price Stream (Symbol/Price/Timestamp/Source), candle
data'dan (M5/M15/H1/H4/Daily) toza ajratilgan.
