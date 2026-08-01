# 02_Repository_Structure.md

Senior Trading AI Repository Structure

Bu hujjat repository ichidagi barcha papka va fayllarning
rasmiy joylashuvi hamda vazifasini belgilaydi.

Hech bir modul ushbu strukturadan tashqarida yaratilmaydi.

══════════════════════════════════════════════════════════════════════
01. DATA LAYER
══════════════════════════════════════════════════════════════════════

data/
│
├── providers/
│   ├── provider_factory.py
│   │   Providerlarni yaratadi va boshqaradi.
│   │
│   ├── twelve_data_provider.py
│   │   Twelve Data bilan ishlaydi.
│   │
│   ├── bitget_provider.py
│   │   Bitget Live Stream bilan ishlaydi.
│   │
│   └── base_provider.py
│       Barcha providerlar uchun umumiy interfeys.
│
├── historical/
│   ├── historical_data_service.py
│   │   Tarixiy ma'lumotlarni boshqaradi.
│   │
│   ├── bootstrap.py
│   │   GoldBot ishga tushganda tarixni yuklaydi.
│   │
│   ├── recovery.py
│   │   Yetishmayotgan candlelarni tiklaydi.
│   │
│   ├── historical_database.py
│   │   Tarixiy ma'lumotlarni saqlaydi.
│   │
│   └── validator.py
│       Tarixiy ma'lumotlarni tekshiradi.
│
├── stream/
│   ├── price_stream_service.py
│   │   Live narx oqimini boshqaradi.
│   │
│   ├── current_price_provider.py
│   │   Joriy narxni taqdim etadi.
│   │
│   ├── candle_builder.py
│   │   Ticklardan candle yaratadi.
│   │
│   ├── stream_validator.py
│   │   Live Ticklarni tekshiradi.
│   │
│   ├── market_calendar.py
│   │   Forex va Exchange ish vaqtini boshqaradi.
│   │
│   ├── event_bus.py
│   │   Live Eventlarni uzatadi.
│   │
│   └── stream_event.py
│       Stream event modellari.
│
├── memory/
│   ├── market_memory.py
│   │   Single Source of Truth.
│   │
│   ├── memory_reader.py
│   │   Memorydan o‘qiydi.
│   │
│   ├── memory_registry.py
│   │   Memorylarni boshqaradi.
│   │
│   └── snapshot.py
│       Snapshot obyektlari.
│
├── validation/
│   ├── data_validation.py
│   │   Market ma'lumotlarini tekshiradi.
│   │
│   └── quality_checker.py
│       Data sifatini baholaydi.
│
└── cache/
    ├── smart_data_cache.py
    │   API chaqiruvlarini kamaytiradi.
    │
    ├── cache_state.py
    │   Cache holatini saqlaydi.
    │
    └── cache_manager.py
        Cache boshqaruvi.

══════════════════════════════════════════════════════════════════════
02. GOLDBOT CORE
══════════════════════════════════════════════════════════════════════

core/
│
├── market/
│   ├── market_engine.py
│   ├── market_state.py
│   └── market_phase.py
│
├── context/
│   ├── context_engine.py
│   ├── liquidity.py
│   ├── order_block.py
│   ├── fvg.py
│   ├── wyckoff.py
│   ├── amd.py
│   └── market_structure.py
│
├── analysis/
│   ├── analysis_engine.py
│   ├── probability.py
│   ├── scoring.py
│   └── confidence.py
│
├── strategy/
│   ├── strategy_engine.py
│   ├── liquidity_strategy.py
│   ├── fvg_strategy.py
│   ├── amd_strategy.py
│   └── strategy_manager.py
│
├── confluence/
│   ├── confluence_engine.py
│   └── confluence_score.py
│
├── decision/
│   ├── decision_engine.py
│   ├── trade_filter.py
│   └── approval.py
│
├── risk/
│   ├── risk_engine.py
│   ├── position_size.py
│   ├── drawdown.py
│   └── money_management.py
│
├── signal/
│   ├── signal_engine.py
│   ├── signal_builder.py
│   └── signal_formatter.py
│
└── monitoring/
    ├── monitoring.py
    ├── simulation.py
    └── trade_monitor.py

══════════════════════════════════════════════════════════════════════
03. APPLICATION SERVICES
══════════════════════════════════════════════════════════════════════

services/
│
├── signal/
├── chart/
├── replay/
├── analytics/
├── ai/
├── notification/
├── portfolio/
└── gateway/

══════════════════════════════════════════════════════════════════════
04. AI LAYER
══════════════════════════════════════════════════════════════════════

ai/
│
├── senior/
├── seniorita/
├── trading/
├── learning/
├── voice/
├── vision/
└── explanation/

══════════════════════════════════════════════════════════════════════
05. PLATFORM LAYER
══════════════════════════════════════════════════════════════════════

platform/
│
├── telegram/
├── mobile/
├── desktop/
├── web/
└── api/

══════════════════════════════════════════════════════════════════════
06. USER EXPERIENCE
══════════════════════════════════════════════════════════════════════

ux/
│
├── chart/
├── journal/
├── analytics/
├── replay/
├── notification/
└── portfolio/

══════════════════════════════════════════════════════════════════════
07. BUSINESS LAYER
══════════════════════════════════════════════════════════════════════

business/
│
├── identity/
├── subscription/
├── payment/
├── wallet/
├── referral/
└── billing/

══════════════════════════════════════════════════════════════════════
08. LEARNING LAYER
══════════════════════════════════════════════════════════════════════

learning/
│
├── academy/
├── simulator/
├── ai_coach/
├── challenge/
├── tournament/
├── certification/
└── career/

══════════════════════════════════════════════════════════════════════
09. MEDIA LAYER
══════════════════════════════════════════════════════════════════════

media/
│
├── youtube/
├── podcast/
├── broadcast/
├── ai_content/
└── live/

══════════════════════════════════════════════════════════════════════
10. FUTURE EXPANSION
══════════════════════════════════════════════════════════════════════

future/
│
├── marketplace/
├── sdk/
├── plugins/
├── enterprise/
├── cloud/
├── research/
└── roadmap/