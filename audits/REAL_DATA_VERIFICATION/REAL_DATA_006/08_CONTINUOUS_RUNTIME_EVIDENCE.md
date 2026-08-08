# REAL-DATA-006 — 08. Continuous Runtime Evidence (3-update probe)

## Probe: `scripts/verification/real_price_stream_probe.py`

Probe REAL production stream'ni
`build_default_price_stream_service(memory_registry=MarketMemoryRegistry())`
orqali quradi, `PRICE_UPDATED`ga probe-tomonidagi counter subscribe
qiladi (faqat VERIFICATION INSTRUMENTATION — production consumer EMAS),
so'ng `tick(datetime.now(timezone.utc))`ni **3 marta** ~3s oralab
chaqiradi. Har tick uchun: provider price+timestamp (cache read),
validation outcome, memory read-back (`MemoryReader.get_last_candle`),
va `PRICE_UPDATED` chiqqan-chiqmaganini (counter) qayd etadi.

Xavfsizlik kontrakti `real_market_data_probe.py` bilan bir xil: faqat
presence flag / price / timestamp / exception CLASS. API key hech qachon
chop etilmaydi.

## Local run (egress-blocked sandbox — BLOCKED, kutilganidek)

Local ishga tushirish tarmoqsiz, shuning uchun BLOCKED. Muhim: probe
crash bo'lmadi, non-network mantiq to'g'ri ishladi:

```
TWELVE_DATA_API_KEY: MISSING
---
UPDATE #1: price=None, timestamp=None, validated=NOT, memory=NOT, event_published=NO
UPDATE #2: price=None, timestamp=None, validated=NOT, memory=NOT, event_published=NO
UPDATE #3: price=None, timestamp=None, validated=NOT, memory=NOT, event_published=NO
---
Stream: BLOCKED
Stream Reason: TWELVE_DATA_API_KEY not configured
```

Qo'shimcha (local log): PriceStream XAUUSD uchun
`ValueError: Unsupported timeframe 'M1'`ni izolyatsiya qildi — bu
03-fayldagi M1 mismatch topilmasini empirik tasdiqlaydi.

## OGOHLANTIRISH — real CI run kutilishi (M1 mismatch)

03-fayldagi M1 interval mismatch tufayli, **real TWELVE_DATA_API_KEY
bilan CI dispatch'da ham XAUUSD source `read()` `ValueError` beradi va
0 real update tushadi**. Ya'ni continuous-update dalili
BLOCKED bo'lishi kutiladi — bu M1/M5 wiring tuzatilmaguncha davom
etadi. Order shuni belgilaydi: real probe 3 real update olmasa,
stream portion BLOCKED (aniq sabab: production XAUUSD wiring
`interval="M1"`, client faqat M5/M15/H1/H4/Daily).

## <<< PLACEHOLDER — REAL CI 3-UPDATE LOG (orchestrator to'ldiradi) >>>

Quyidagi blok CI `workflow_dispatch` run'ining haqiqiy 3-update
log'i bilan orchestrator tomonidan to'ldiriladi. Worker o'zi
dispatch QILMAYDI.

```
UPDATE #1: price=<>, timestamp=<>, validated=<>, memory=<>, event_published=<>
UPDATE #2: price=<>, timestamp=<>, validated=<>, memory=<>, event_published=<>
UPDATE #3: price=<>, timestamp=<>, validated=<>, memory=<>, event_published=<>
Stream: <PASS/BLOCKED>
```

Agar CI'da ham `M1` mismatch tufayli 0 real update bo'lsa — stream
portion rasman **BLOCKED**, sabab: XAUUSD `interval="M1"` production
wiring vs client M5/M15/H1/H4/Daily.
