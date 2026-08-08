# 17 — DRQ — Production Execution (REAL-DATA-011)

**DRQ turi:** Director Review Question / Trading-Safety wiring.
**Holat:** CONTRACT EXISTS — PRODUCTION NOT WIRED. Bu passda
YOQILMADI, real order OCHILMADI.

## Bir jumlalik so'rov

Director ruxsat beradimi — `RiskResult`ni production
`ExecutionEngine`/`BrokerGateway`'ga wire qilib, real broker order
oqimini yoqishga (hozir live pipeline Risk'da to'xtaydi, execution
inert)?

## Kontekst

- `RiskManager.evaluate()` real `RiskResult` beradi (`pipeline.py:495`).
- `ExecutionSimulator` yo'li = **SAFE, PASS** (76 test), real order
  yo'q — production'dan alohida.
- `BrokerGateway` = bo'sh skeleton, real order call YO'Q.
- Live pipeline approved signalni faqat SignalFormatter+Notifier'ga
  beradi, ExecutionEngine'ga EMAS.

## Nega DRQ

`CLAUDE.md` Trading Safety: "execution/ is intentionally inert …
wiring it up is itself a change requiring explicit approval". Real
order = REAL TRADE — Worker HECH QACHON qilmaydi.

## Tavsiya

RFC + ADR orqali "Production Execution Flow" sifatida
rasmiylashtirish; Live Trading enable/disable esa hatto Phase 2'da ham
har doim Director Approval talab qiladi (Director Order No. 021).
**SAFE SIMULATION = PASS va PRODUCTION EXECUTION = NOT VERIFIED
aralashtirilmaydi.**
