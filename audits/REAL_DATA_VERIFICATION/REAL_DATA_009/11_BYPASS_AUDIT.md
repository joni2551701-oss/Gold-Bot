# 11 — Bypass Audit — REAL-DATA-009

## Maqsad

Har bir stage (Core/Context/Strategy/Signal/Decision/Risk/Service/
Telegram) TwelveData/Bitget/ProviderManager/MarketDataNormalizer'dan
QAYTA fetch qilmasligini tasdiqlash — faqat market_data stage
(MarketDataService, SSOT entry) provayderdan o'qiydi.

## Metodologiya

`grep -rn "ProviderManager|MarketDataNormalizer|TwelveData|Bitget"`
production (non-test) fayllar bo'yicha: core_layer, context_layer,
signal_layer, strategy_layer, decision_layer, risk_layer, ai_layer,
platform_layer/telegram.

## Natijalar

1. **market_data stage (SSOT entry):** `pipeline.py:325` va `:355`
   faqat `self.data_normalizer` (MarketDataService) orqali
   `get_candles`/`get_snapshot` chaqiradi. Bu yagona real provayder
   kirish nuqtasi.

2. **context_layer detektorlari:** `context_layer/*`da
   `from data_layer.providers.twelve_data_client import Candle` —
   bu FAQAT `Candle` **dataclass tipi**ning import'i (type import),
   provayderdan re-fetch EMAS. Hech qanday
   `TwelveDataClient()`/`.fetch_candles()`/`ProviderManager()`
   chaqiruvi bu qatlamlar ichida yo'q. (Masalan
   `market_regime/market_regime.py:38`, `wyckoff/wyckoff.py:47`,
   `fvg/fvg.py:5` — barchasi type import.)

3. **htf_bias.py:** MarketDataNormalizer'ga faqat docstring'da
   ishora qiladi (`htf_bias.py:10,62,97`) — real fetch pipeline'ning
   market_data stage'ida (`pipeline.py:355` `get_snapshot`) bajariladi,
   htf_bias ichida emas. `compute_htf_bias()` tayyor snapshot'ni
   qabul qiladi.

4. **ai_layer ProviderManager:** `ai_layer/*`dagi `ProviderManager`
   LLM/AI PROVIDER manageri (`ai_layer.ai_engine.providers.
   provider_manager`) — market data provayderi EMAS. Bu market data
   bypass emas.

5. **strategy/signal/decision/risk/telegram:** Hech biri
   provayder/normalizer chaqirmaydi — ular yuqoridagi stage'lar
   natijasini iste'mol qiladi.

## AI → Telegram/Execution bypass

- AIAnalyzer Telegram/execution/Risk chaqirmaydi — `ai/` faqat
  advisory (06_, `decision_engine.py:222` VETO-only).
- Notifier signal analiz qilmaydi/risk hisoblamaydi (`notifier.py:28-31`).
- Risk chetlab o'tilmaydi — har decision `risk_manager.evaluate()`dan
  o'tadi (`pipeline.py:494-497`).

## Xulosa

**0 bypass** — REAL-DATA-004 topilmasi qayta tasdiqlandi. Yagona real
provayder kirish nuqtasi market_data stage (MarketDataService, SSOT).
Boshqa barcha `TwelveData` uchrashuvlari `Candle` type import yoki
docstring; `ProviderManager` uchrashuvlari AI-provider (LLM), market
data emas.

## Status: PASS (0 bypass)
</content>
