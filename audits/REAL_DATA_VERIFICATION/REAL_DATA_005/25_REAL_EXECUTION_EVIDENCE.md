# 25 — Real Execution Evidence (REAL-DATA-005)

## Halol bayonot (honest statement)

**Real broker execution evidence YO'Q va bo'lishi ham mumkin emas** —
Order bo'yicha bu qat'iy taqiqlangan (No real trade, No live order).
Real order OCHILMADI. Quyida keltirilgan yagona "real evidence" —
mavjud SAFE simulator mexanizmi orqali olingan, real broker orderi
bo'lmagan safe-runtime iz.

## Safe-Execution evidence (real app path, no real order)

Manba: mavjud test `tests/execution/simulator/test_simulator_engine.py`
(yangi harness qurilmadi — order bo'yicha faqat mavjud mexanizm
ishlatildi). Ishga tushirildi:

```
$ python -m pytest tests/execution/ tests/lifecycle/ -q
........................................................................
....
76 passed in 5.37s
```

Isbotlangan real handoff (mock'siz):
- `RiskResult(approved=True, lot_size=0.25)` → `ExecutionSimulator.simulate()`
  → `result.order.lot_size == 0.25`
  (`test_simulate_order_carries_lot_size_from_risk_result`, `:97-103`).
- BUY fill slippage bilan: entry 2350.0 + 0.15 → `fill_price ≈ 2350.15`
  (`test_simulate_fills_a_buy_order_with_slippage`, `:44-51`).
- Spread juda keng bo'lsa reject: `filled=False`, `rejection_reason`
  "too wide" (`test_simulate_rejects_when_spread_too_wide`, `:63-71`).
- PaperTrade hech qachon mutatsiya qilinmaydi (`:74-81`).

Bu — `ExecutionSimulationResult` (safe simulated result, NO real broker
order, `simulator/models.py:27-31`).

## Live runtime evidence

`python main.py` smoke run (bu audit, exit 0):

```
[XAUUSD|M15] Produced 0 risk result(s).
[XAUUSD|M15] stage=risk duration=0.000s
[XAUUSD|M15] stage=signal_history ...
[XAUUSD|M15] stage=telegram_format ...
[XAUUSD|M15] stage=telegram_delivery ...
[XAUUSD|M15] Persisted 0 signal record(s).
[XAUUSD|M15] stage=database duration=0.000s
[XAUUSD|M15] pipeline_finished
```

Log'da **hech qanday `execution` yoki `monitoring` stage yo'q** — bu
live-runtime Risk→Execution NOT WIRED faktining empirik isboti.

## Xulosa

| Evidence turi | Holat |
|---|---|
| Real broker execution | YO'Q (taqiqlangan, ochilmadi) |
| Safe-simulator execution (real app path, no order) | BOR — 76 passed |
| Live-runtime execution stage | YO'Q (wired emas, smoke log tasdiqladi) |
</content>
