# 02 — Risk → Execution Kontrakti (REAL-DATA-010)

## RiskManager chiqishi — `RiskResult`

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

Muhim fakt (`risk_manager.py:51-57` docstring): RiskManager
BUY/SELL/entry/TP/SL ni **hech qachon originate/o'zgartirmaydi** —
faqat ALLOW (`approved=True`) yoki REJECT (`approved=False`) qaytaradi.
`lot_size` — sizing tavsiyasi, order instruksiyasi emas. Entry/symbol/
direction `RiskResult` ichida YO'Q.

## Execution qabul qiladigan ikki kontrakt

| Mexanizm | file:line | Kirish | Chiqish | Holat |
|---|---|---|---|---|
| `ExecutionEngine.dispatch()` | `execution_engine.py:31-43` | `risk_result: RiskResult` | `ExecutionResult(dispatched=False, "Not implemented")` | INERT stub |
| `ExecutionSimulator.simulate()` | `simulator_engine.py:48-83` | `paper_trade: PaperTrade`, `risk_result: RiskResult`, `session`, `signal_time` | `ExecutionSimulationResult` | SAFE simulator |

## Field-by-field map (Risk chiqishi → Execution request)

`ExecutionSimulator.simulate()` (`simulator_engine.py:55-63`)
`SimulatedOrder` (`models.py:38-51`) quradi:

| Execution request field | Manba | file:line |
|---|---|---|
| `order_id` | `uuid.uuid4()` | `simulator_engine.py:56` |
| `trade_id` | `paper_trade.trade_id` | `simulator_engine.py:57` |
| `symbol` | `paper_trade.symbol` | `simulator_engine.py:58` |
| `direction` | `paper_trade.direction` | `simulator_engine.py:59` |
| `requested_price` | `paper_trade.entry` | `simulator_engine.py:60` |
| `lot_size` | **`risk_result.lot_size`** | `simulator_engine.py:61` |
| `requested_at` | `signal_time` yoki `now(utc)` | `simulator_engine.py:62` |

Xulosa: `RiskResult`dan Execution requestga **faqat `lot_size`** o'tadi;
entry/symbol/direction `PaperTrade` orqali keladi (u APPROVED
`SignalSchema`dan quriladi). Simulator RiskResult'ni yoki Decision'ni
qayta tekshirmaydi (`simulator_engine.py:8-13` docstring).

## Determinatsiya

Kontrakt **mavjud va well-formed** (RiskResult fields → Execution
request map to'liq). Ammo LIVE pipeline (`core_layer/pipeline/pipeline.py`)
bu kontraktni **chaqirmaydi** — na `ExecutionEngine.dispatch()`, na
`ExecutionSimulator.simulate()` pipeline'da mavjud (03-hujjatda trace).

### **RISK → EXECUTION = CONTRACT EXISTS — PRODUCTION NOT WIRED**

Adapter ixtiro qilinmadi. Bu — GoldBot v1'ning haqiqiy holati:
kontrakt tayyor, lekin production runtime'da ulanmagan (ataylab,
Trading Safety chegarasi).
