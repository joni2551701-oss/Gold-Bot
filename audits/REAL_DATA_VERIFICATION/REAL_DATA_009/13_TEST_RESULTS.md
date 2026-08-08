# 13 — Test Results — REAL-DATA-009

## Test count

`python -m pytest tests/` → **5503 passed in 96.88s**. Kutilgan 5503
bilan mos.

## Test klassifikatsiyasi

| Turi | Ta'rif | Bu audit uchun ahamiyati |
|---|---|---|
| **Unit** | Yakka funksiya/class, mock input | Kod to'g'riligi; real runtime EMAS |
| **Integration** | Bir necha modul birga, ko'pincha mock provayder | Layer contract'lar; real API EMAS |
| **Real-Runtime-Probe** | `real_data_probe` CI job (main.py, real TWELVE_DATA_API_KEY) | Haqiqiy runtime dalil (12_) |
| **E2E** | To'liq pipeline data→risk→persist | Zanjir yaxlitligi |

## Muhim ogohlantirish

**Mock PASS ≠ real runtime PASS.** 5503 test'ning aksariyati mock/
fixture input bilan ishlaydi — ular kod contract'ini tasdiqlaydi, real
market data bilan runtime'ni EMAS. Haqiqiy runtime dalil faqat
REAL-DATA-004 CI run `31240675527` (real XAU/USD 200 candle) orqali
keladi (12_). Shu sabab data→risk zanjiri real runtime bilan PASS,
Telegram→User esa NOT VERIFIED (mock test uni "qamrasa" ham, real
delivery bajarilmadi).

## Validation (bu audit uchun)

- pyflakes: toza
- compileall: PASS
- pytest: 5503 passed
- main.py: graceful (sandbox, 0 candle — kalit yo'q, kutilgan)

## Status: PASS (5503) — mock coverage; real runtime alohida (12_)
</content>
