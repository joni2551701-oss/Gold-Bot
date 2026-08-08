# 20 — Core Consumption Proof (REAL-DATA-003)

## Data fidelity testi (mavjud kod, yashil)

`tests/data/test_market_data_service.py`ga qo'shildi:

- `test_get_candles_via_memory_ssot_is_identical_to_validated_candles`
  — mocklangan provider ma'lum candle to'plamini qaytarganda, Core
  memory-SSOT yo'li orqali oladigan candle'lar YOZILGAN validated
  candle'lar bilan AYNAN bir xil: bir xil son (5), bir xil OHLC, bir xil
  timestamp, bir xil tartib (oldest→newest). Truncation (capacity),
  qayta tartiblash (reordering), va `CandleRecord↔Candle` type-conversion
  drift'iga qarshi himoya.
- `test_get_candles_via_memory_ssot_actually_reads_from_memory` — qaytgan
  seriya haqiqatan memory-SSOT read-back ekanini isbotlaydi
  (`get_candles_from_memory()` bilan bir xil).
- `test_get_candles_falls_back_to_validated_when_memory_empty` —
  fail-safe: bo'sh/noma'lum memory timeframe (masalan Daily/D1 gap)
  `[]` qaytarsa, `get_candles()` original validated candle'larni
  o'zgarmagan holda qaytaradi — hech qachon bo'sh ro'yxat, hech qachon
  degrade qilingan savdo yo'li.

**Natija:** 3 ta yangi test qo'shildi, hammasi PASS
(`tests/data/test_market_data_service.py`: 15 → 18 passed).

## Fidelity xulosasi

Reconciliation traded data'ni O'ZGARTIRMAYDI. Provider→validated→
memory-stored→memory-read (Core-consumed) zanjiri bo'ylab candle
identifikatsiyasi (count/OHLC/timestamp/order) saqlanadi. Hech qanday
divergensiya topilmadi; BLOCKED shart bajarilmadi.

## Real-data equality natijasi (placeholder — GitHub Actions)

Jonli tenglik zanjiri (`provider price == validated price ==
memory-stored == memory-read`) `scripts/verification/real_market_data_probe.py`
ning "Core consumption" bo'limida real registry-backed
`MarketDataService` bilan sinaladi. Bu sandbox egress-blocked bo'lgani
uchun lokal run `core_consumption = BLOCKED` beradi (kutilgan). Haqiqiy
natija GitHub Actions (`real_data_verification.yml`, workflow_dispatch)
run'idan keyin shu yerga yoziladi:

```
Core Consumption: <PASS/BLOCKED>
Core Symbol: XAU/USD
Core provider_price: <...>
Core validated_price: <...>
Core memory_read_price: <...>
Core Timestamp: <...>
```

Lokal tekshiruv: probe crash qilmasdan ishlaydi, exit 0, non-network
mantiq sog'lom.
