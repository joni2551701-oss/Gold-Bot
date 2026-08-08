# 14 — Architecture Verification — REAL-DATA-009

## Layer Direction (CLAUDE.md)

`data/ -> context/ -> strategies/ -> signals/ -> ai/ -> decision/ ->
risk/ -> telegram/ -> database/` — har qatlam faqat o'zidan pastdagi
qatlam bilan gaplashadi.

## Tekshirilgan holat (pipeline.py orkestratsiyasi)

| Bosqich | Qatlam yo'nalishi | file:line | Holat |
|---|---|---|---|
| market_data | data | `pipeline.py:325` | OK |
| context | data → context | `pipeline.py:369` | OK |
| market_phase/features | context → indicator-ekv. | `pipeline.py:381,453` | OK |
| signal | context → strategy → signal | `pipeline.py:405` | OK |
| ai | signal → ai (advisory) | `pipeline.py:477` | OK |
| decision | ai → decision (yakuniy egasi) | `pipeline.py:487` | OK |
| risk | decision → risk | `pipeline.py:495` | OK |
| telegram | risk → telegram (to'g'ridan) | `pipeline.py:568,599` | OK (NOT WIRED service) |
| database | telegram → database | `pipeline.py:625` | OK |

## Isolation tekshiruvi

- `strategies/` `telegram/`ni import qilmaydi; `ai/` `database/`ni
  import qilmaydi (CLAUDE.md qoidasi) — grep bilan tasdiqlangan
  (11_ bypass audit doirasida).
- Pipeline `platform_layer/telegram/`dan faqat SignalFormatter+Notifier
  import qiladi (`pipeline.py:24-25`) — application service emas.
- Risk chetlab o'tilmaydi; AI yakuniy qaror egasi emas; AI
  Telegram/execution chaqirmaydi.

## FLOW-019 ikki oqim

- **Broadcast oqimi** (pipeline): risk → format → deliver, application
  service YO'Q (NOT WIRED — 08_).
- **Bot command oqimi**: handlers.py → `*_service.py` →
  `*_repository.py` (FLOW-019 to'liq) — bu alohida oqim, broadcast
  emas.

## Status: PASS
</content>
