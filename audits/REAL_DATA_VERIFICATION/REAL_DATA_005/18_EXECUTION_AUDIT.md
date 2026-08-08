# 18 — Execution Audit (REAL-DATA-005)

Director Order REAL-DATA-005 bo'yicha Risk → Execution → Trade
Monitoring zanjiri **audit-only** (verification) rejimida `file:line`
aniqligida tekshirildi. Hech qanday real trade, live order, yoki fake
execution/monitoring natijasi yaratilmadi. Yangi Execution/broker/
provider/monitoring arxitekturasi qo'shilmadi.

## Deliverable joylashuvi — Collision oldini olish (non-silent qaror)

Director so'ragan `18_..26_` fayl nomlari `audits/REAL_DATA_VERIFICATION/`
papkasida ALLAQACHON mavjud (ular REAL-DATA-003/004 ga tegishli:
`18_REAL_DATA_003_RUNTIME_TRACE.md` ... `26_STRATEGY_TO_SIGNAL.md`).
Ularni overwrite qilmaslik uchun REAL-DATA-005 deliverable'lari YANGI
kichik papkada yaratildi:
`audits/REAL_DATA_VERIFICATION/REAL_DATA_005/`. Bu qaror ataylab, ochiq
(non-silent) — 26-hujjatda ham takrorlangan.

## Execution Contract Audit — Risk output → Execution request

### RiskManager nima chiqaradi (`RiskResult`)

`risk_layer/risk_engine/risk_manager.py:41-49`:

```
@dataclass(frozen=True)
class RiskResult:
    approved: bool
    lot_size: float
    risk_amount: float
    risk_reward: float
    reason: str
    risk_percent: float = 0.0
    drawdown_percent: Optional[float] = None
```

Muhim fakt (`risk_manager.py:81-83`): `lot_size` — **manual execution
uchun sizing tavsiyasi, hech qachon order instruksiyasi emas**.
RiskManager broker spetsifikatsiyasini (contract size, tick value, lot
step, min/max lot, stop level) bilmaydi. Entry/SL/TP/symbol/direction
`RiskResult` ichida YO'Q — ular `TradeDecision`/`SignalCandidate`da
qoladi (RiskManager `risk_manager.py:56-57` bo'yicha BUY/SELL/entry/
TP/SL ni hech qachon o'zgartirmaydi/originate qilmaydi).

### Execution nima qabul qiladi

Ikki mexanizm mavjud:

| Mexanizm | Fayl | Kirish kontrakti | Holat |
|---|---|---|---|
| `ExecutionEngine.dispatch()` | `execution_layer/execution_engine/execution_engine.py:31-43` | `risk_result: RiskResult` → `ExecutionResult(dispatched=False, reason="Not implemented")` | INERT stub |
| `ExecutionSimulator.simulate()` | `execution_layer/execution_engine/simulator/simulator_engine.py:48-83` | `paper_trade: PaperTrade`, `risk_result: RiskResult`, `session`, `signal_time` → `ExecutionSimulationResult` | SAFE simulator |

### Field-by-field map (Risk output → Execution request → Engine)

`ExecutionSimulator.simulate()` (`simulator_engine.py:55-63`) yig'adi
`SimulatedOrder` (`simulator/models.py:38-51`):

| Execution request field | Manba | file:line |
|---|---|---|
| `order_id` | `uuid.uuid4()` | `simulator_engine.py:56` |
| `trade_id` | `paper_trade.trade_id` | `simulator_engine.py:57` |
| `symbol` | `paper_trade.symbol` | `simulator_engine.py:58` |
| `direction` | `paper_trade.direction` | `simulator_engine.py:59` |
| `requested_price` | `paper_trade.entry` | `simulator_engine.py:60` |
| `lot_size` | **`risk_result.lot_size`** | `simulator_engine.py:61` |
| `requested_at` | `signal_time` yoki `now(utc)` | `simulator_engine.py:62` |

Xulosa: `RiskResult`dan Execution requestga **faqat `lot_size`**
o'tadi; entry/symbol/direction esa `PaperTrade` orqali keladi (u o'z
navbatida APPROVED `SignalSchema`dan quriladi — `create_paper_trade`,
test `tests/execution/simulator/test_simulator_engine.py:34-37`).
Kontrakt to'liq va izchil (well-formed). Simulator RiskResult va
Decisionni **qayta tekshirmaydi** (`simulator_engine.py` docstring
10-13) — u faqat allaqachon OPEN bo'lgan (Decision APPROVE + Risk
approved) PaperTrade'ni qabul qiladi.

**Execution Contract = PASS** (verified, no real order).
</content>
