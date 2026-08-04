# execution/

## Purpose
Kelajakdagi MT5 order-execution layer uchun scaffolding
(`execution_engine.py`/`signal_lifecycle.py`, ikkisi ham hali inert),
plus — Phase 60.3 — faqat `backtesting/` va analytics tomonidan
ishlatiladigan, hech qachon live execution tomonidan emas, simulated-fill
subpackage (`simulator/`).

## Flow
```
Risk Manager (approved signal)
      |
      v
execution/   -- execution_engine.py/signal_lifecycle.py: NOT WIRED, "not implemented" today
      |
      v
(future) MT5 order

Separately, for backtesting only:

lifecycle.paper_trade.PaperTrade (OPEN) + RiskResult
      |
      v
execution/simulator/   -- Phase 60.3, real logic, never calls execution_engine.py
      |
      v
ExecutionSimulationResult (simulated fill or reject) -- see docs/EXECUTION_SIMULATOR.md
```

## Responsibilities
`execution_engine.py`/`signal_lifecycle.py` shartsiz ravishda "not
implemented" qaytaradi — MT5 client yo'q, order call yo'q, I/O yo'q.
GoldBot v0.2/v0.3 avtomatik ravishda trade joylashtirmaydi; execution
trader tomonidan qo'lda amalga oshiriladi. Phase 60.3 ikkala faylni ham
o'zgartirmaydi.

`simulator/` (Phase 60.3: Execution Simulator Foundation) —
`models.py`/`slippage.py`/`spread.py`/`latency.py`/`simulator_engine.py`.
Fill qanday ko'rinishga ega bo'lishini (spread + slippage + latency)
hisoblaydi, faqat `backtesting/`/analytics tomonidan iste'mol qilinishi
uchun — hech qachon broker, MT5 yoki
`execution_engine.py`/`signal_lifecycle.py`ni chaqirmaydi. To'liq
kontrakt uchun `docs/EXECUTION_SIMULATOR.md`ga qarang.

## Input
`execution_engine.py`/`signal_lifecycle.py`: yo'q — hech qanday runtime
yo'lidan chaqirilmaydi. `simulator/`: allaqachon-OPEN `PaperTrade` +
`RiskResult`, kelajakdagi `backtesting/` chaqiruvchisidan (Phase
60.3 holatiga ko'ra ulanmagan).

## Output
`execution_engine.py`/`signal_lifecycle.py`: yo'q.
`simulator/`: `ExecutionSimulationResult`.

## Dependencies
`execution_engine.py`/`signal_lifecycle.py`: stdlib'dan tashqari yo'q.
`core/pipeline.py` yoki `main.py` tomonidan import qilinmaydi (Phase 48
audit tomonidan tasdiqlangan). `simulator/`
`trade_monitoring_layer.paper_trading.paper_trade.PaperTrade` va
`risk_layer.risk_engine.risk_manager.RiskResult`ni (faqat
`TYPE_CHECKING`) import qiladi — yangi, bir tomonlama `execution/` →
`lifecycle/`/`risk/` dependency, faqat read, hech qachon teskari
yo'nalishda emas; `lifecycle/`/`risk/` `execution/`ni import qilmaydi.

## Future Roadmap
Real MT5 integratsiya bu directory'ning yakuniy maqsadi hisoblanadi,
lekin hech bir faza bu ishni hali scope qilmagan. Uning taqdirini
(implement qilish vs olib tashlash) v0.4'dan oldin, uni cheksiz inert
holatda qoldirmasdan hal qilish kerak — `docs/AUDIT_REPORT.md`da ochiq
band sifatida qayd etilgan.
