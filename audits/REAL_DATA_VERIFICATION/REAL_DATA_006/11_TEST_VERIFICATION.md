# REAL-DATA-006 — 11. Test Verification (mavjud stream testlari klassifikatsiyasi)

## Klassifikatsiya

| Test fayli | def test | Mock/Fake | Turi |
|---|---|---|---|
| `tests/data/stream/test_price_stream_service.py` | 19 | Ha | **Unit** (fake provider/sink) |
| `tests/data/stream/test_price_stream.py` | — | Ha | **Unit** (fake provider, state machine) |
| `tests/data/stream/test_stream_manager.py` | — | Ha | **Unit** |
| `tests/data/stream/test_canonical_stream_validator.py` | 13 | Yo'q | **Unit** (sof validator mantiqi) |
| `tests/data/stream/test_stream_integration.py` | 1 | Ha | **Integration** (mock provider bilan) |
| `tests/data/stream/test_stream_event.py` | — | — | **Unit** |
| `tests/stream/test_stream_*.py` (legacy) | — | Ha | **Unit** (legacy stream layer) |

## Muhim xulosa

**Barcha mavjud stream testlari Unit yoki mock-asosli Integration.**
Hech biri real TwelveData oqimini ishlatmaydi — mock testlar
**real-stream isboti EMAS** (order shuni ta'kidlaydi). `test_stream_integration.py`
ham mock provider ishlatadi, real HTTP emas.

## Real-Probe / E2E bo'shlig'i

Bu auditgacha real continuous Price Stream oqimini tekshiruvchi
Real-Probe YO'Q edi. Ushbu audit uni qo'shadi:
`scripts/verification/real_price_stream_probe.py` (gated CI step).
Bu yagona **Real-Probe** darajali dalil manbai (mock emas).

## Regression holati

`python -m pytest tests/` — barcha mavjud testlar o'zgarishsiz. Probe
+ CI step production testlariga tegmaydi (yangi `.py` faqat
`scripts/verification/` ostida). Test soni report qismida qayd
etiladi.

## Status: **Mavjud testlar = Unit/mock-Integration; Real-Probe endi qo'shildi (mock ≠ real-stream isboti)**
