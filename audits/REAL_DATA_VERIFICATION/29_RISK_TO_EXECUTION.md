# 29 — Risk → Execution (TASK-07)

## Transition
Risk → Execution (ExecutionEngine orchestration / BrokerGateway /
ExecutionMonitor — dizayn bo'yicha inert).

## Input
`RiskResult` (sizing tavsiyasi).
Evidence: `core_layer/pipeline/pipeline.py:494-499`.

## Processing (file:line)
- Live pipeline'da Risk natijasidan **real broker order** ijro etuvchi
  hech qanday chaqiruv YO'Q. `execution_layer` `core_layer/pipeline/
  pipeline.py`ga import qilinmagan (pipeline import bloki `:1-29` —
  execution_layer yo'q).
- Pipeline docstringi buni aniq belgilaydi:
  `core_layer/pipeline/pipeline.py:176-179` — "Execution and TP/SL
  Monitoring are intentionally not part of this pipeline (Phase 27.2+).
  Risk Layer output is a sizing suggestion only -- no MT5/broker
  connection, no order execution."
- `ExecutionEngine`: `execution_layer/execution_engine/execution_engine.py`
  — mavjud, lekin real MT5/broker order chaqiruvi yo'q (inert).
- `pipeline_guard.before_execution()` (`pipeline.py:586`) — "execution"
  bu yerda Telegram delivery gate'iga xaritalanadi, `execution_layer`ga
  emas (pipeline docstringi `:578-585` buni aniq izohlaydi).

## Output
Real order YO'Q. Risk natijasi faqat sizing tavsiyasi sifatida result
dict'da qoladi (`pipeline.py:648` `risk_results`).

## Next Consumer
Yo'q (real execution consumer mavjud emas).

## Ownership-rule check
- CLAUDE.md Trading Safety: "execution/ is intentionally inert (no MT5
  order calls exist yet)". Runtime shu holatga to'liq mos.
- Execution'ni ulash = Director approval talab qiladigan o'zgarish
  (CLAUDE.md). Ushbu auditda ULANMADI.

## Status
**NOT VERIFIED (dizayn bo'yicha)** — real broker order → real filled
trade real dalil bera olmaydi, chunki `execution_layer` ataylab inert
(CLAUDE.md Trading Safety). Bu yashiriladigan nosozlik EMAS, balki
hujjatlashtirilgan dizayn holati.

## Unblock qilish uchun
Execution'ni yoqish (real broker order) — **Director approval** talab
qiladi (CLAUDE.md). Worker buni avtonom ulamaydi.
</content>
