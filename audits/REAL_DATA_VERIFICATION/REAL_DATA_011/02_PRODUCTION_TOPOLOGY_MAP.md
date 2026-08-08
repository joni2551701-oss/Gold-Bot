# 02 — Production Topology Map (REAL-DATA-011, Item A)

Haqiqiy runtime yo'lining bitta konsolidatsiyalangan xaritasi. Har bir
o'tish uchun: Producer / Input / Processing / Output / Consumer +
Status + file:line. Dalil REAL-DATA-002→010'dan qayta ishlatilgan.

## Ikki alohida data contract

GoldBot'da **ikkita alohida, toza ajratilgan** data yo'li bor:

1. **Current-price stream (008)** — real-time tick oqimi.
   `TwelveDataPriceSource` → `PriceStreamService` → validation →
   `MarketMemory` + EventBus `PRICE_UPDATED`. `/price`, dashboard,
   chart uchun.
2. **Batch candle path** — `data_normalizer.get_candles()` orqali
   M5/M15/H1/H4/Daily svechalar. **TradingPipeline shu yo'lni
   o'qiydi** (`core_layer/pipeline/pipeline.py:325`).

Bu ikki contract bir-biriga aralashmaydi (Item B, 03_ da tasdiqlangan).

## Runtime o'tishlar jadvali

| # | O'tish | Producer → Consumer | Processing | Status | file:line |
|---|---|---|---|---|---|
| 1 | Data → PriceStream | `TwelveDataPriceSource` → `PriceStreamService` | tick fetch/adapt | PASS | `data_layer/live_data/price_stream_service/price_stream_service.py:245` |
| 2 | PriceStream → Validation | stream → validation | tick sanity | PASS | `price_stream_service.py:88-95` |
| 3 | Validation → Memory | → `MarketMemory` | SSOT write | PASS | `price_stream_service.py:33,123` |
| 4 | Memory → EventBus | → `PRICE_UPDATED` publish | event emit | PASS (publish) | `price_stream_service.py:95-96` |
| 5 | EventBus → Core | `PRICE_UPDATED` → (hech kim) | — | **NOT WIRED** | consumer yo'q — faqat probe `scripts/verification/real_price_stream_probe.py:145` |
| 6 | Data → Core (batch) | `data_normalizer.get_candles()` → Pipeline | candle fetch | PASS | `core_layer/pipeline/pipeline.py:325` |
| 7 | Core → Memory SSOT | Pipeline → `MarketMemoryRegistry` | SSOT | PASS | `pipeline.py:240,220-225` |
| 8 | Core → Context | Pipeline → context build | HTF/context | PASS (Daily bias non-binding) | `pipeline.py:369` (009/02_) |
| 9 | Context → Indicator | → indicators | compute | PASS | `pipeline.py:381,453` |
| 10 | Indicator → Strategy | → strategy | signal gen | PASS | `pipeline.py:405` |
| 11 | Strategy → Signal | → SignalEngine | candidate | PASS | `pipeline.py:405,519` |
| 12 | Signal → Decision | → DecisionEngine | AI+veto blend | PASS | `pipeline.py:487`; veto `decision_layer/.../decision_engine.py:222` |
| 13 | Decision → Risk | → `RiskManager.evaluate()` | geometry/size | PASS | `pipeline.py:495` |
| 14 | Risk → Notification | approved → `SignalFormatter` | format | PASS (kod yo'li) | `pipeline.py:246,568` |
| 15 | Notification → Telegram | → `Notifier.send_messages()` | deliver | PASS (kod yo'li) | `pipeline.py:247,599` |
| 16 | Telegram → User | → real chat | send | **NOT VERIFIED** | xavfsiz destination yo'q (09_) |
| 17 | Risk → Service | Pipeline → (app service yo'q) | — | **NOT WIRED** | broadcast to'g'ridan-to'g'ri format+deliver (009/08_) |
| 18 | Risk → Execution | `RiskResult` → ExecutionEngine | — | **CONTRACT EXISTS, NOT WIRED** | `execution_layer/` inert (010) |
| 19 | Execution → Monitoring | fill → monitor | — | **NOT WIRED** | fill→monitor handoff yo'q (010/07_) |
| 20 | Execution Simulator | `RiskResult`→`ExecutionSimulator` | safe sim | PASS (76 test) | (010/04_,08_) |

## Diagramma vs haqiqiy kod — nomuvofiqliklar (flag)

- **Diagramma:** `Data→...→EventBus→Core→Context→...`. **Haqiqat:**
  Core EventBus'ga **subscribe qilmaydi** — Core batch `get_candles()`
  o'qiydi va MarketMemory SSOT'ni ishlatadi. `PRICE_UPDATED` faqat
  publish qilinadi, production consumer yo'q. → **NOT WIRED**, DRQ (16_).
- **Diagramma:** `Risk→Notification→Telegram→User` uzluksiz. **Haqiqat:**
  Risk→Notification→Telegram kod yo'li bor, ammo `Telegram→User` real
  send xavfsiz destination yo'qligi sababli **NOT VERIFIED**.
- **Diagramma:** `Risk→Execution→Monitoring`. **Haqiqat:** ataylab
  inert; contract skeletoni bor, production wiring yo'q.
- **CLAUDE.md ichidagi path'lar** (`core/pipeline.py`,
  `risk/`, `signals/`) — tarixiy/aspirational; haqiqiy fayllar
  `core_layer/pipeline/pipeline.py`, `risk_layer/risk_engine/…`.
  Bu nomuvofiqlik N (14_) da qayd etilgan.

## Xulosa

**data → risk = to'liq PASS (real runtime).** Risk'dan keyingi barcha
o'tishlar (5, 16, 17, 18, 19) NOT WIRED yoki NOT VERIFIED — **dizayn
bo'yicha**, nuqson emas. Wiring — Director DRQ'lari.
