# 35 — REAL-DATA-004 E2E (Core → User)

## Uchdan-uchgacha oqim (real kod yo'li)

```
Market Memory SSOT (REAL-DATA-003 isbotlagan: provider==validated==memory)
  -> pipeline.py:325 get_candles (Core SSOT'dan iste'mol qiladi)
  -> pipeline.py:369 build_context_snapshot -> ContextEngine.build (Core->Context)
  -> ContextEngine detektorlar (Context->Indicator, context_orchestrator.py:121-132)
  -> pipeline.py:405 SignalEngine.generate_signals -> StrategyManager (Indicator->Strategy)
  -> StrategyManager -> List[SignalCandidate] (Strategy->Signal)
  -> pipeline.py:487 DecisionEngine.evaluate (Signal->Decision, AI advisory-only)
  -> pipeline.py:495 RiskManager.evaluate (Decision->Risk, chetlab o'tilmagan)
  -> [Risk->Execution: INERT, dizayn bo'yicha]
  -> [Execution->Monitoring: real pozitsiya yo'q, dizayn bo'yicha]
  -> pipeline.py:568 SignalFormatter.format_signal (Core/API DTO)
  -> handlers.py:171-179 FLOW-019 *_service.py (Core/API->Service)
  -> pipeline.py:599 Notifier.send_messages (Service->Telegram, AI bypass yo'q)
  -> [Telegram->User: real send NOT VERIFIED, xavfsiz destination yo'q]
```

## Bypass audit natijasi (TASK-18)

Production yo'lida (test'lardan tashqari) TwelveData / Bitget /
ProviderFactory / ProviderManager / MarketDataNormalizer to'g'ridan-to'g'ri
import/chaqiruv:

| Hit | Fayl | Klassifikatsiya |
|---|---|---|
| `from data_layer.providers.twelve_data_client import Candle` | `context_layer/*` (market_structure, liquidity, order_block, fvg, amd, wyckoff, session, candle, context_orchestrator, market_regime) | **Bypass EMAS** — bu `Candle` DTO (data model) type import, provider fetch mantiqi emas |
| `ProviderManager` | `platform_layer/telegram/owner/ai_commands.py`, `runtime_commands.py` | **Bypass EMAS** — bu `ai_layer.ai_engine.providers.provider_manager` (AI provider health/status), owner diagnostika buyruqlari; market-data re-fetch emas |
| docstring/comment mentions | `htf_bias.py`, `pipeline.py:212` va b. | **Bypass EMAS** — hujjat/izoh |

**Xulosa:** production trading yo'lida haqiqiy provider bypass **YO'Q**.
market_data bosqichi yagona SSOT entry sifatida `MarketDataService`
ishlatadi (`pipeline.py:239-241,325`); hech bir downstream bosqich
provider'dan qayta fetch qilmaydi. Downstream faqat `Candle` type'ini
import qiladi.

## Arxitektura konflikt (STOP) topilmalari

Hech qanday architecture-vs-runtime CONFLICT topilmadi. Ownership
farqlari (`ContextService`/`IndicatorService`/`StrategyService`/
`RiskService`/`ExecutionService`/`MonitoringService` skeletonlari,
`SignalService`/`DecisionService` additive-parallel) — barchasi
hujjatlashtirilgan Foundation Freeze v1.0 / MIR-001 / ICR-001 migration
holati; live behavior engine'larda. Bu STOP talab qiladigan konflikt
emas.

## Production kod o'zgarishi

Trading yo'lida production kod o'zgarishi **YO'Q**. Yagona o'zgarish —
`.github/workflows/ci.yml`ning `real_data_probe` job'iga real runtime
trace qadami qo'shildi (probe'dan keyin, o'sha `workflow_dispatch` gate
ostida). `validate` job'iga tegilmadi. Trading logic'ga (decision/risk/
strategy/signal/execution) tegilmadi.

## Carried findings (o'zgartirilmadi)

- HTF Daily/D1 vocabulary (non-blocking) — o'zgartirilmadi.
- Bitget NOT_VERIFIED — o'zgartirilmadi (yangi Bitget/fallback arxitektura
  qo'shilmadi).
</content>
