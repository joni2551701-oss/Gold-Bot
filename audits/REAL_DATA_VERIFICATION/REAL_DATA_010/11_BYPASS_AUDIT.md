# 11 — Bypass Audit + Ikki Xil Dalil (REAL-DATA-010)

## Ikki xil dalilni ARALASHTIRMASLIK (Order section 11)

### A. Real Production Runtime dalili

**Risk → Execution = NOT WIRED.** Live pipeline
(`core_layer/pipeline/pipeline.py:1-29`) `execution_layer`ni import
qilmaydi; Risk oxirgi trading stage (`pipeline.py:494-499`); `run()`
dict'da execution/monitoring kaliti yo'q. Empirik: `python main.py`
(exit 0) log'ida oxirgi stage `stage=database`, execution/monitoring
stage umuman yo'q.

**→ Real Production Execution = NOT VERIFIED (wired emas).**

### B. Safe Runtime dalili

**Risk → ExecutionSimulator → Result = PASS.** Mavjud mock-free
testlar orqali: `pytest tests/execution/ tests/lifecycle/ → 76 passed`.
`risk_result.lot_size` → `SimulatedOrder.lot_size` handoff isbotlangan
(`test_simulate_order_carries_lot_size_from_risk_result`). Real order
yo'q.

**→ Safe Simulation = PASS.**

Bu ikki dalil ALOHIDA: A (production) = NOT VERIFIED, B (safe sim) =
PASS. B hech qachon A'ni isbotlamaydi.

## Bypass tekshiruvlari (takroran, konsolidatsiya)

| Bypass yo'li | Holat | Dalil |
|---|---|---|
| Signal → Execution | YO'Q (PASS) | grep NONE, pipeline Risk'da to'xtaydi |
| AI → Execution | YO'Q (PASS) | faqat docstring/FAQ havolalari |
| Telegram → Execution | YO'Q (PASS) | grep NONE; owner cmd registered emas |
| Rejected risk → Execution | YO'Q (PASS) | execution wired emas |
| RiskManager bypass | YO'Q (PASS) | `pipeline.py:494-499` majburiy |

## Verdikt

Bypass topilmadi. Ikki dalil turi to'g'ri ajratilgan: Production =
NOT WIRED / NOT VERIFIED, Safe Simulation = PASS.
