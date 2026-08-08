# 14 — Runtime Evidence (REAL-DATA-010)

## A. Real Production Runtime dalili

`python main.py` (exit 0, graceful) smoke run log'i — oxirgi stage'lar
ketma-ketligi:

```
[XAUUSD|M15] stage=risk duration=0.000s
[XAUUSD|M15] Produced 0 risk result(s).
[XAUUSD|M15] stage=signal_history duration=0.000s
[XAUUSD|M15] stage=telegram_format duration=0.000s
[XAUUSD|M15] Produced 0 telegram message(s).
[XAUUSD|M15] Sent 0/0 telegram notification(s).
[XAUUSD|M15] stage=telegram_delivery duration=0.000s
[XAUUSD|M15] Persisted 0 signal record(s).
[XAUUSD|M15] stage=database duration=0.000s
[XAUUSD|M15] pipeline_finished duration=0.003s
```

**`stage=execution` yoki `stage=monitoring` umuman chiqmaydi.** Risk
oxirgi trading stage; keyingi barcha stage'lar signal_history/telegram/
database — execution/monitoring EMAS.

**→ Real Runtime: Risk → Execution = NOT WIRED.**

## B. Safe Runtime dalili

```
python -m pytest tests/execution/ tests/lifecycle/ -q  → 76 passed
```

`ExecutionSimulator.simulate(paper_trade, risk_result)` real obyektlar
bilan `ExecutionSimulationResult` ishlab chiqaradi; `risk_result.lot_size`
→ `order.lot_size` handoff isbotlangan. Real broker order YUBORILMADI.

**→ Safe Runtime: Risk → ExecutionSimulator → Result = PASS.**

## Kafolatlar

- Real trade/broker order OCHILMADI.
- Fake broker/consumer yaratilMADI.
- Production execution yoqilMADI; live-trading flag force qilinMADI.
- Yangi execution/monitoring arxitekturasi qo'shilMADI.
- Price Stream (008) va 009 flowlariga tegilMADI.
- Kod o'zgarMADI (audit-only).
