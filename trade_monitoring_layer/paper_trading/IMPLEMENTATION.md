# lifecycle/

## Purpose
Phase 59 Preparation foundation (TASK 2: Paper Trading Contract,
TASK 4: Signal Lifecycle Audit). Simulyatsiya qilingan Trade
(`PaperTrade`, hech qachon real broker order emas) uchun va signal'ning
analysis pipeline bo'ylab o'z progressini (`SignalLifecycleState`)
ifodalash uchun standart, in-memory state machine'lar. Ikkisi ham bu
faza doirasida `core/pipeline.py`, `execution/` yoki database'ga
ulanmagan — ikkisi ham har bir Phase A/AC modulining o'z "foundation,
rewrite emas" pozitsiyasiga mos, alohida-mustaqil foundation'lardir.

## `strategies/lifecycle/` bilan bir xil emas
`strategies/lifecycle/` (Phase A11) — bu har bir *strategy* uchun
metadata registry (`StrategyDefinition`/`StrategyRegistry` — SMC
metodologiyasi bo'yicha status/version). `lifecycle/` (mana shu
package) — bu har bir *trade*/*signal* uchun runtime state machine.
Bir-biriga aloqasi bo'lmagan, faqat "lifecycle" so'zini baham
ko'radigan tushunchalar — ikki package bir-birini import qilmaydi.

## `execution/` bilan bir xil emas
`execution_layer/execution_engine/execution_engine.py` va
`execution_layer/execution_monitor/signal_lifecycle.py` — Trading-Safety
bilan himoyalangan `execution/` package'ida oldindan mavjud bo'lgan,
ataylab inert qilingan stub'lardir (`ExecutionEngine.dispatch()` va
`SignalLifecycle.transition()` ikkisi ham doim "Not implemented"
qaytaradi). `execution_layer/execution_monitor/signal_lifecycle.py`'ning o'z
`SignalState` enum'i (`CREATED`/`SENT`/`ACKNOWLEDGED`/`CLOSED`) Telegram
xabar yetkazilishini tasvirlaydi, signal'ning analysis-pipeline
progressini yoki trade'ning o'z hayotini emas. `lifecycle/` hech qachon
`execution/`dan import qilmaydi yoki uni chaqirmaydi va
`execution/`ning o'z stub'larini kamroq inert qilmaydi — bu package
hech qanday broker call, real order, MT5 integratsiya qo'shmaydi.
Aniq nomlash farqlanishi (`PaperTrade`/`TradeState` vs oldindan mavjud
hech narsa; `SignalLifecycleState` vs
`execution_layer.execution_monitor.signal_lifecycle.SignalState`) uchun
`trade_monitoring_layer/paper_trading/paper_trade.py` va
`trade_monitoring_layer/paper_trading/signal_state.py`'ning o'z docstring'lariga
qarang.

## Modules

### `trade_state.py`
`TradeState` — `CREATED`/`OPEN`/`CLOSED`/`CANCELLED`. `PaperTrade` uchun
status lug'ati.

### `paper_trade.py`
`PaperTrade` (`trade_id`, `signal_id`, `symbol`, `direction`, `entry`,
`stop_loss`, `take_profit`, `status`, `result`, `opened_at`,
`closed_at`, `created_at`) plus:
- `create_paper_trade(signal)` — allaqachon `APPROVED` bo'lgan
  `SignalSchema`'dan `CREATED` `PaperTrade` yaratadi. Agar signal
  `APPROVED` bo'lmasa yoki narx maydoni yetishmasa `ValueError`
  ko'taradi — bu haqiqiy chaqiruvchi xatosi, ma'lumotga bog'liq holat
  emas.
- `open_paper_trade(trade)` / `close_paper_trade(trade, result)` /
  `cancel_paper_trade(trade)` — har biri
  `PaperTradeTransitionResult(trade, success, reason)` qaytaruvchi
  sof transition function'lar. Hech qachon ko'tarmaydi: noto'g'ri
  transition (masalan, hech qachon ochilmagan trade'ni yopish)
  `success=False`ni asl, o'zgarmagan trade bilan qaytaradi.
- `ALLOWED_PAPER_TRADE_RESULTS = ("TP", "SL", "BE", "EXPIRED")` —
  `docs/PHASE59_VALIDATION.md`'ning o'z Result lug'ati, ataylab
  `database_layer/trade_repository/signal_repository.py`'da oldindan mavjud
  bo'lgan `{"WIN","LOSS","BE","CANCELLED"}`dan farqli (bu to'plam
  real, persisted `signals` jadvaliga tegishli, bu faza tomonidan
  tegilmagan, va allaqachon `CANCELLED`ni `PaperTrade` uni status
  sifatida ishlatgan joyda result sifatida ishlatadi).

### `signal_state.py`
`SignalLifecycleState` — `CREATED`/`QUALITY_CHECKED`/`EXPLAINED`/
`APPROVED`/`REJECTED`/`PAPER_OPEN`/`CLOSED`, plus:
- `ALLOWED_TRANSITIONS` / `transition_signal_state(current, next)` —
  sof transition validator, `SignalStateTransitionResult(success,
  reason)`, hech qachon ko'tarmaydi.
- `derive_signal_lifecycle_state(signal, paper_trade=None)` —
  allaqachon hisoblangan `SignalSchema`/`PaperTrade` maydonlaridan
  observational klassifikatsiya (xuddi
  `context_layer/trend/market_phase.py`'ning `compute_market_phase()`
  o'rnatgan priority-ordered, read-only pattern). Hujjatlashtirilgan
  cheklov: `EXPLAINED` ishonchli tarzda chiqarib bo'lmaydi, chunki
  `SignalSchema.explanation_id` bu kodbazada hech qayerda hech qachon
  to'ldirilmagan (function'ning o'z docstring'iga qarang).

## Dependencies
`paper_trade.py` `trade_monitoring_layer.paper_trading.trade_state`ni (bir xil
package) import qiladi, plus, faqat `TYPE_CHECKING`,
`signal_layer.signal_builder.schema.SignalSchema`. `signal_state.py`
`trade_monitoring_layer.paper_trading.trade_state`ni import qiladi, plus, faqat
`TYPE_CHECKING`, `trade_monitoring_layer.paper_trading.paper_trade.PaperTrade` va
`signal_layer.signal_builder.schema.SignalSchema`. Ikkisi ham `context/`,
`strategies/`, `ai/`, `decision/`, `risk/`, `execution/`, `database/`
yoki `telegram/`ni import qilmaydi.

### `paper_trade_monitor.py` (Phase 59.4, TASK 2)
`check_paper_trade_against_candles(trade, candles)` — quyida
implementatsiya qilinmagan deb nomlangan monitor loop, endi
qurilgan: chaqiruvchi tomonidan berilgan candle ro'yxati bo'ylab
entry'ni, keyin TP/SL'ni qidirib o'tadi, trade'ni `close_paper_trade()`
orqali (qayta ishlatilgan, takrorlanmagan) `"TP"`/`"SL"` bilan yopadi,
yoki agar entry butun window davomida hech qachon tegilmasa
`"EXPIRED"` bilan yopadi. Har bir chaqiruv uchun stateless — chaqiruvchi
`trade.opened_at`dan boshlab to'liq candle tarixini berishi kerak, har
bir sikldagi faqat yangi candle'larni emas (nima uchun ekanligi uchun
modulning o'z docstring'iga qarang). Noaniqlik qoidasi: agar bitta
candle'ning diapazoni ham TP'ni, ham SL'ni qamrab olsa, SL g'alaba
qiladi (konservativ backtesting konvensiyasi).

## Future Roadmap
Persistence (`paper_trades` jadvali, `PaperTradeRepository` — e'tibor
bering, `database_layer/market_repository/raw_candle_repository.py`/
`market_snapshot_repository.py`, Phase 59.3, allaqachon real monitor
loop `paper_trade_monitor.py`ga uzatadigan raw candle tarixini
ta'minlaydi) va `core/pipeline.py` ulanishi (har bir `APPROVE` qilingan
decision uchun avtomatik ravishda `PaperTrade` yaratish va har bir
siklda yangi monitor'ni chaqirish) ikkisi ham implementatsiya
qilinmagan holda qolmoqda — har biri alohida, aniq tasdiqlanishi
mumkin bo'lgan kelajakdagi qadam, `docs/PHASE59_VALIDATION.md`'ning o'z
scope eslatmalariga muvofiq.
