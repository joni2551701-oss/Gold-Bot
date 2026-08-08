# 20 — Risk → Execution (REAL-DATA-005)

## (a) Live pipeline = NOT WIRED (tasdiqlandi)

`core_layer/pipeline/pipeline.py` — LIVE pipeline `execution_layer`ni
ham, `trade_monitoring_layer`ni ham **import qilmaydi**. Import ro'yxati
(`pipeline.py:1-29`) risk stage'da to'xtaydi:

| Stage | file:line |
|---|---|
| Risk (oxirgi trading stage) | `pipeline.py:494-499` — `self.risk_manager.evaluate(decision)` |
| Signal history | `pipeline.py:515-533` |
| Telegram format | `pipeline.py:564-575` |
| Telegram delivery | `pipeline.py:591-606` |
| Database persist | `pipeline.py:617-630` |

`run()` qaytaradigan dict (`pipeline.py:635-652`) da `execution_result`
yoki `monitoring` kaliti YO'Q. Pipeline docstring buni ochiq aytadi
(`pipeline.py:176-179`): "Execution and TP/SL Monitoring are
intentionally not part of this pipeline (Phase 27.2+). Risk Layer
output is a sizing suggestion only -- no MT5/broker connection, no
order execution."

Empirik tasdiq: `python main.py` smoke run log'ida oxirgi stage =
`stage=database`; `execution` yoki `monitoring` stage log'i umuman
chiqmaydi (smoke run exit 0, graceful).

**LIVE-runtime Risk→Execution = NOT WIRED / NOT VERIFIED.**

## (b) Contract + SAFE simulator path

Risk-derived execution requestni ExecutionSimulator orqali xavfsiz
natijaga o'tkazish MUMKIN va mavjud test bilan isbotlangan — real order
OCHILMADI, yangi harness QURILMADI, faqat mavjud test ishga tushirildi.

Evidence — `tests/execution/simulator/test_simulator_engine.py` (real
`RiskResult` + real `PaperTrade`, mock YO'Q; docstring `:2-3`):

- `_risk_result()` (`:40-41`) haqiqiy `RiskResult(approved=True,
  lot_size=0.1, ...)` quradi.
- `_open_trade()` (`:34-37`) APPROVED `SignalSchema`dan real OPEN
  `PaperTrade` quradi (`create_paper_trade` → `open_paper_trade`).
- `test_simulate_order_carries_lot_size_from_risk_result` (`:97-103`) —
  `risk_result.lot_size=0.25` → `result.order.lot_size == 0.25`.
  Bu aynan Risk output → Execution request handoff'ining safe-runtime
  isboti.

Ishga tushirildi (bu audit): `pytest tests/execution/ tests/lifecycle/`
→ **76 passed** (real objects, no broker). Owner `/execution` command
(`platform_layer/telegram/owner/execution_commands.py:32-47`) ham
`ExecutionSimulator`ni chaqiradi, lekin faqat status/config reporting
uchun; u `command_router`/`handlers`ga registered EMAS (`:5-7`).

**Risk→Execution CONTRACT + SAFE simulator path = PASS** (verified via
existing simulator tests, no real order).

## Yakuniy holat

| Jihat | Verdikt |
|---|---|
| Live-runtime Risk→Execution | NOT VERIFIED / NOT WIRED |
| Contract (Risk output → Execution request map) | PASS |
| SAFE simulator path | PASS (76 passed, no real order) |
</content>
