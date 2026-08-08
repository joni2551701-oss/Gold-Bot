# 21 — REAL-DATA-003 E2E

## Uchdan-uchgacha oqim (reconciliation'dan keyin)

```
TwelveData Provider (real fetch)
   -> MarketDataNormalizer.get_candles() (fetch + validate)
   -> MarketDataService._hydrate_memory() (Market Memory SSOT'ga yozish)
   -> MarketDataService.get_candles_from_memory() (SSOT'dan qayta o'qish)
   -> pipeline.py:303 candles (Core endi SSOT'dan iste'mol qiladi)
   -> Context -> Signal -> AI -> Decision -> Risk -> Telegram
```

HTF yordamchi yo'li (o'zgarmagan, memory'dan tashqarida):
```
pipeline.py:333 get_snapshot(Daily/H4/H1) -> compute_htf_bias (context-only)
```

## Lokal validatsiya

| Bosqich | Natija |
|---|---|
| `pyflakes` | Toza (nothing reported) |
| `compileall` | PASS |
| `pytest tests/data/test_market_data_service.py` | 18 passed (15→18, +3 fidelity) |
| `pytest tests/core tests/integration` | 158 passed |
| `python main.py` smoke | Pipeline barcha bosqichlarni ishlatadi, candle fetch shakli o'zgarmagan |
| `real_market_data_probe.py` (lokal) | exit 0, live bo'limlar BLOCKED (egress-blocked, kutilgan) |

## Trading Safety

- Signal/Strategy/Decision/Risk logikasiga TEGILMADI.
- Risk Manager chetlab o'tilmadi; pipeline oqimi bir xil.
- AI to'g'ridan-to'g'ri ijro yo'li qo'shilmadi.
- Primary traded candle'lar identifikatsiyasi isbotlangan (20-hujjat).
- HTF Daily/D1 degrade qilinmadi (memory'ga yo'naltirilmadi).
