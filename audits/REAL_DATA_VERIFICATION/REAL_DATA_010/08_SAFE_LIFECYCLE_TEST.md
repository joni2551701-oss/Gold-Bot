# 08 — Safe Lifecycle Test (REAL-DATA-010)

## Maqsad

Faqat mavjud xavfsiz mexanizmlar/testlar bilan
Risk → ExecutionSimulator → Simulated Order → Simulated Fill →
Monitoring → Close zanjirini ko'rsatishga urinish. Yangi link
QURILMADI.

## Bosqichma-bosqich holat

| Bosqich | Mexanizm | Holat |
|---|---|---|
| Risk → Simulator | `ExecutionSimulator.simulate(paper_trade, risk_result)` (`simulator_engine.py:48-63`) | **ISHLAYDI** — `lot_size` `risk_result`dan (`:61`) |
| Simulator → Simulated Order | `SimulatedOrder` (`models.py:38-51`) | **ISHLAYDI** |
| Simulated Order → Simulated Fill | spread/slippage/latency → `SimulatedFill` (`simulator_engine.py:72-83`) | **ISHLAYDI** |
| Fill → Monitoring | — | **ULANMAGAN** — monitor `SimulatedFill` qabul qilmaydi (`paper_trade_monitor.py:42-45`) |
| Monitoring → Close | `close_paper_trade(trade, "TP"/"SL"/"EXPIRED")` (`paper_trade_monitor.py:101-106`) | ISHLAYDI, lekin `PaperTrade` ustida, fill'dan mustaqil |

## Dalil

`pytest tests/execution/ tests/lifecycle/ → 76 passed`. Testlar
Risk→Simulator→Order→Fill qismini qamraydi; monitor testlari
(`paper_trade_monitor`) `PaperTrade`+candle bilan alohida ishlaydi.
Ikkalasini ulaydigan test yo'q, chunki kodda handoff yo'q.

## Verdikt

### **SAFE LIFECYCLE = PARTIAL**

- Risk → Simulator → Order → Fill = **ishlaydi (PASS)**.
- Simulator → Monitor = **ULANMAGAN (NOT WIRED)** — REAL-DATA-005
  topilmasi qayta tasdiqlandi.
- Monitor → Close = mustaqil ishlaydi, lekin simulator fill'idan
  haydalmaydi.

Yetishmayotgan link (Simulator→Monitor) **qurilmadi** — bu Trading
Safety o'zgarishi, Director Approval talab qiladi.
