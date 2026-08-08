# 04 — SSOT / Memory Re-verification (REAL-DATA-011, Item C)

REAL-DATA-003 topilmasi regressiya qilmaganini qayta tasdiqlash.

## Tekshiruvlar

| Tekshiruv | Natija | Dalil (file:line) |
|---|---|---|
| Raw-provider bypass yo'q | PASS | Pipeline provider'ni to'g'ridan-to'g'ri chaqirmaydi; `data_normalizer.get_candles()` orqali `core_layer/pipeline/pipeline.py:325` |
| Core provider'ni qayta so'ramaydi | PASS | `MarketMemoryRegistry` SSOT; `pipeline.py:220-225,240` — "Market Memory as SSOT for the traded primary asset" izohi |
| Duplicate writer yo'q | PASS | Stream tomonida bitta yozuvchi: `price_stream_service.py:33,123` (register_source per-asset MarketMemory quradi) |
| Stale protection | PASS | Stale/duplicate handling (006/09_ da tasdiqlangan) o'zgarmadi |

## SSOT contract

- Pipeline `MarketMemoryRegistry()` ni bitta marta quradi
  (`pipeline.py:240`) va o'sha registry orqali barcha candle
  o'qishlarini o'z-ichida izchil qiladi (Option B, REAL-DATA-003).
- Current-price stream (008) MarketMemory'ni yangilaydi, ammo bu Pipeline
  o'qiydigan batch-candle SSOT'dan alohida contract — regressiya yo'q.

## Xulosa

**REAL-DATA-003 REGRESSIYA QILMADI.** SSOT/Memory = **WORKING → KEEP.**
Hech qanday bypass, qayta-so'rov, dublikat yozuvchi topilmadi.
