# REAL-DATA-006 — 13. Verdikt (Honest Overall Verdict)

## Umumiy verdikt: **PARTIAL (stream portion BLOCKED)**

Live Price Stream runtime zanjiri kod darajasida REAL va production-wired
(tick → Validation → Memory fold → Event Bus publish), ammo ikkita
segment to'liq PASS bermaydi:

1. **Event Bus → Core = FOUNDATION / NOT WIRED** (kutilgan PARTIAL
   sabab) — `PRICE_UPDATED` iste'molchisi yo'q; Core Market Memory'ni
   jadval bo'yicha o'qiydi (REAL-DATA-003).
2. **XAUUSD continuous-update = BLOCKED** (yangi topilma) — production
   wiring `TwelveDataProvider(asset="XAUUSD")` default `interval="M1"`,
   client esa M5/M15/H1/H4/Daily'ni qo'llaydi → `read()` `ValueError`
   → real tick tushmaydi.

## Segment-by-segment

| Transition | Status | Izoh |
|---|---|---|
| tick() production driver | **PASS** | `polling.py:308`, real long-lived jarayon |
| Provider stream (XAUUSD → TwelveData real HTTP) | **BLOCKED** | client real, lekin M1 mismatch (03) → runtime BLOCKED |
| Stream → Validation | **PASS** | canonical StreamValidator, drop-on-invalid (04) |
| Validation → Memory (single-writer fold) | **PASS (kod)** | CandleBuilder single writer (05); upstream BLOCKED |
| Memory → Event Bus (PRICE_UPDATED publish) | **PASS (kod)** | payload=PriceTick, symbol/price/timestamp (06); upstream BLOCKED |
| Event Bus → Core | **FOUNDATION / NOT WIRED** | subscriber yo'q (07) |
| Continuous updates (3-tick real) | **BLOCKED** | M1 mismatch → 0 real update kutiladi (08) |

## Stale/duplicate + reconnect

- Duplicate/stale/invalid: **PASS** — uch qatlamli mavjud himoya
  (provider dedupe, stream ordering, validator) (09).
- Reconnect/recovery: **IMPLEMENTED** — PriceStream state-machine
  (backoff, max attempts, RECONNECTING/WAITING) (10).

## Production-path javobi

Price Stream `main.py`da EMAS (u one-shot pipeline), balki
`platform_layer/telegram/polling.py`da (uzoq yashovchi jarayon)
`tick()` orqali haydaladi (`polling.py:308`, `:339`). Bu real
production driver — Foundation emas.

## Architecture

**PASS** — Layer boundary'lar buzilmagan, Memory SSOT chetlab
o'tilmagan, Foundation Freeze saqlangan (12). Ochiq: M1 wiring nuqsoni
(kod, Director Review), stale docstring (hujjat).

## Kod o'zgarishi

Faqat: (1) `scripts/verification/real_price_stream_probe.py` (yangi
probe), (2) `.github/workflows/ci.yml` gated CI step (mavjud
`real_data_probe` job ichida yangi step). Hech qanday production `.py`
o'zgartirilmadi. M1 mismatch va stale docstring TUZATILMADI (audit-only;
M1 tuzatish Director Review talab qiladi).

## Ochiq topilmalar (Director Review uchun)

1. **M1 interval mismatch (Major).** `price_stream_service.py:238`
   XAUUSD source `interval="M1"` bilan quriladi, client M1'ni rad
   etadi. Production live Price Stream XAUUSD uchun hech qachon real
   tick tushira olmaydi. Tavsiya: default interval'ni M5 yoki M15'ga
   o'tkazish (provider/stream wiring o'zgarishi — Director Review).
2. **Stale docstring (Minor).** `price_stream_service.py:47`
   "nothing drives tick() in production" — eskirgan.

## <<< PLACEHOLDER — REAL CI 3-UPDATE DALIL (orchestrator to'ldiradi) >>>

CI `workflow_dispatch` run'ining haqiqiy 3-update log'i shu yerga
qo'yiladi. Agar CI'da ham M1 mismatch tufayli 0 real update bo'lsa,
yuqoridagi "Continuous updates = BLOCKED" verdikti rasman tasdiqlanadi
(aniq sabab: XAUUSD `interval="M1"` vs client M5/M15/H1/H4/Daily).
Worker o'zi dispatch QILMAYDI.

---

## ⚡ YAKUNIY VERDIKT — real CI evidence bilan (run 31251456946, e31b48d)

| Segment | Natija | Evidence |
|---|---|---|
| tick() production driver | ✅ PASS | polling.py:308 |
| Provider stream XAUUSD (real) | ❌ BLOCKED | real CI: `ValueError: Unsupported timeframe 'M1'` (3/3 tick, 0 update) |
| Stream → Validation | ⚠️ real kod, lekin ishga tushmadi (tick land bo'lmadi) |
| Validation → Memory | ⚠️ real kod, ishga tushmadi |
| Memory → Event Bus | ⚠️ real kod, ishga tushmadi (0 PRICE_UPDATED) |
| Event Bus → Core | ⚠️ FOUNDATION / NOT WIRED (subscriber yo'q) |
| Continuous 3-tick | ❌ BLOCKED (real CI: 0/3 update) |
| Reconnect/Recovery | ✅ IMPLEMENTED (PriceStream state machine) |
| Architecture | ✅ PASS |
| Tests | ✅ 5493 |
| CI | ✅ validate + real_data_probe success |

**REAL-DATA-006 = PARTIAL / BLOCKED (stream portion).** Stream
infrastructure (tick driver, StreamValidator, single-writer Memory
fold, Event Bus publish, reconnect state machine) REAL va production-
wired, LEKIN XAUUSD continuous stream real CI'da BLOCKED — M1 interval
defect empirik isbotlandi. Event Bus → Core NOT WIRED.

**Muhim:** bu trading pipeline'ga ta'sir qilmaydi — pipeline BATCH
`MarketDataService` (M15) yo'lidan foydalanadi (REAL-DATA-003/004'da
isbotlangan, ishlaydi), stream yo'lidan emas. Bu faqat continuous
Price Stream subsystem'iga tegishli.

**Director-decision items (bu task'da tuzatilmaydi — provider/stream
wiring o'zgarishi Director Review talab qiladi):**
1. **M1 defect** — `price_stream_service.py:238` `TwelveDataProvider(asset="XAUUSD")`
   default `interval="M1"` -> M5/M15 ga o'zgartirish (bir qatorli fix),
   YOKI `TwelveDataClient`ga M1 qo'shish. Shu tuzatilmaguncha live Price
   Stream XAUUSD uchun ishlamaydi.
2. **Event Bus → Core** — hech qanday `PRICE_UPDATED` consumer yo'q;
   Core schedule-driven, event-driven emas. Agar event-driven Core
   kerak bo'lsa, bu yangi wiring (RFC/ADR).
3. **Stale docstring** — `price_stream_service.py:47` "nothing drives
   tick() in production" — endi noto'g'ri (polling.py:308 driver mavjud).
