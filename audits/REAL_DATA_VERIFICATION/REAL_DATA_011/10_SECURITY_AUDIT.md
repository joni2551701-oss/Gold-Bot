# 10 — Security Audit (REAL-DATA-011, Item I)

Kod / log / exception / repr / CI / audit dalili bo'ylab secret
leakage tekshiruvi.

## Masking mexanizmi

- **`MaskedSecret` sinfi** (`config.py:138-161`) — `__repr__` va `str`
  har doim `***` (yoki `unset`) qaytaradi:
  `return "MaskedSecret(***)" if self._value else "MaskedSecret(unset)"`
  (`config.py:161`). Izoh (`config.py:33,138`): "so a secret value can
  never appear in a log line".
- **Barcha secretlar `_masked()` orqali o'raladi** (`config.py:166`):
  - `TWELVE_DATA_API_KEY` (`config.py:400`)
  - `BITGET_API_KEY` (`config.py:401`)
  - `BINANCE_API_KEY` (`config.py:402`)
  - `KEYNORQ_API_KEY` (`config.py:403`)
  - `TELEGRAM_BOT_TOKEN` (`config.py:423`)
  - `GEMINI_API_KEY` (`config.py:433`)

## Probe / verification dalili

- `real_price_stream_probe.py:94` — faqat `CONFIGURED`/`MISSING`
  presence flag bosadi, hech qachon qiymat.
- `real_price_stream_probe.py:306` — chiqishda `apikey`/`api_key`
  bo'lgan satrlarni qo'shimcha filtrlaydi.
- `real_market_data_probe.py` — xuddi shu CONFIGURED/MISSING pattern.

## Xulosa

Kod, log, exception, repr, CI va audit dalillari bo'ylab faqat
**CONFIGURED / *** / MASKED** shakllari uchraydi. Ochiq secret
qiymat leakage **topilmadi**. Security = **PASS → KEEP.**
