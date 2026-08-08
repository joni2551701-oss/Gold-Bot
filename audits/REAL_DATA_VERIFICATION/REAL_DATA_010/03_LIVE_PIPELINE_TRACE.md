# 03 — Live Pipeline Trace (REAL-DATA-010)

## Import ro'yxati — Execution/Monitoring YO'Q

`core_layer/pipeline/pipeline.py:1-29` — import ro'yxati Data → Context
→ Features → Signal → AI → Decision → Risk → Telegram → Database
bilan tugaydi. **`execution_layer` ham, `trade_monitoring_layer` ham
import qilinmaydi.** Empirik grep tasdiqi:

```
grep -rn 'execution_layer|trade_monitoring_layer' core_layer/pipeline/  → NONE
```

## Decision → Risk'dan keyingi haqiqiy call chain

| Stage | file:line | Nima chaqiriladi |
|---|---|---|
| Decision | `pipeline.py` (`decision` stage) | `DecisionEngine.evaluate(...)` |
| Risk (oxirgi trading stage) | `pipeline.py:494-499` mintaqasi | `self.risk_manager.evaluate(decision)` |
| Signal history | keyingi stage | `SignalRepository`/history |
| Telegram format | `pipeline.py:564-575` mintaqasi | `SignalFormatter` |
| Telegram delivery | `pipeline.py:586-606` | `Notifier` (guard bilan) |
| Database persist | `pipeline.py:617-630` mintaqasi | `SignalRepository.persist(...)` |

## "execution" so'zi haqida muhim tushuntirish

Pipeline'da "execution" so'zi uchraydi (`pipeline.py:578-606`), ammo bu
`execution_layer`ni ANGLATMAYDI:

- `pipeline.py:586` — `self.pipeline_guard.before_execution()` — bu
  Phase 60.8 Safe Integration guard'i bo'lib, "execution" bu yerda
  **Telegram delivery**ni bildiradi (`pipeline.py:583-585` docstring:
  "why 'execution' maps to Telegram delivery here, not to
  `execution_layer/execution_engine/execution_engine.py` (untouched,
  still inert)").
- Ya'ni pipeline'dagi yagona "execution" gate — Telegram yuborishni
  bloklovchi/ruxsat beruvchi guard, `ExecutionEngine`ga bironta ham
  chaqiruv emas.

## Talab qilingan handoff elementlari

| Element | Holat | Dalil |
|---|---|---|
| Execution import/chaqiruv | **YO'Q** | `pipeline.py:1-29`, grep NONE |
| Order yaratish | **YO'Q** | `SimulatedOrder` faqat simulator ichida, pipeline'da emas |
| Result/trade-ID ishlab chiqarish (execution) | **YO'Q** | `run()` dict'da execution/monitoring kaliti yo'q |
| Monitoring'ga uzatish | **YO'Q** | monitoring stage yo'q |

## Empirik tasdiq (`python main.py`, exit 0)

Smoke run log'ida oxirgi stage'lar ketma-ketligi:
`stage=risk` → `stage=signal_history` → `stage=telegram_format` →
`stage=telegram_delivery` → `stage=database` → `pipeline_finished`.
**`execution` yoki `monitoring` stage log'i umuman chiqmaydi.**

`pipeline.py:176-179` docstring buni ochiq aytadi: "Execution and TP/SL
Monitoring are intentionally not part of this pipeline (Phase 27.2+).
Risk Layer output is a sizing suggestion only -- no MT5/broker
connection, no order execution."

## Verdikt

**LIVE PIPELINE'DA RISK OXIRGI TRADING STAGE.** Execution import
qilinmaydi, order yaratilmaydi, trade-ID ishlab chiqilmaydi, monitoring'ga
uzatilmaydi. Kutilgan natija (Risk oxirgi) — TASDIQLANDI.
