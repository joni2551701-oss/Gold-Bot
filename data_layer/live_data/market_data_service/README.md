# data_layer/live_data/market_data_service

**Canonical module** (market_data_service) — GEL-001 package form.

## Purpose

See `IMPLEMENTATION.md` and the module docstring in `market_data_service.py`.

## Public API

- `annotations`
- `Any`
- `List`
- `Optional`
- `setup_logger`
- `MarketDataNormalizer`
- `MarketSnapshot`
- `Candle`
- `logger`
- `MarketDataService`
- `build_default_market_data_service`
- `get_shared_market_data_service`
- `reset_shared_market_data_service`

## Import

    from data_layer.live_data.market_data_service import <name>

## GFL-001 FLOW-004 Holati (2026-08-04)

Status: Completed (Director Order GFL-004).

`MarketDataService` allaqachon Market Memory'ga yozar edi
(`get_candles()`/`get_snapshot()` -> `_hydrate_memory()`, TASK-DATA-004),
lekin o'qib qaytarish (Market Engine, FLOW-004) yo'q edi. Qo'shildi:
`MarketDataService.get_candles_from_memory()` -- `data_layer.market_memory
.MemoryReader` orqali Market Memory'dan yopilgan (closed) candle
seriyasini `get_candles()` bilan bir xil shaklda (`List[Candle]`)
qaytaradi, `context.context_orchestrator.ContextEngine.build()`ning
mavjud, o'zgarmagan `candles` kontraktiga tayyor holda.

`get_shared_market_data_service()` -- `data_layer.live_data
.price_stream_service.get_shared_price_stream_service()` bilan bir xil
`MarketMemoryRegistry`ni ulashadigan process darajasidagi yagona
instance (`build_default_price_stream_service()`ning o'z hujjatida
oldindan ko'zda tutilgan juftlik, TASK-DATA-004).

To'liq zanjir (`Provider -> Validation -> Market Memory -> Market
Engine`) E2E test bilan tasdiqlangan:
`tests/data/stream/test_flow_004_market_engine_e2e.py`.

Batafsil: `WORK_LOG.md`, `docs/GFL-001_FLOW_CATALOG.md` (FLOW-004).

---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `market_data_service.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
