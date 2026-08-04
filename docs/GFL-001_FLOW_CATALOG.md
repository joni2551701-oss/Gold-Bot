# GFL-001 — Flow Catalog

## Maqsad

Ushbu hujjat GoldBot Data Flow'larini yagona katalog ko'rinishida boshqaradi.

Har bir Flow:

- mustaqil identifikatorga ega;
- aniq Input va Output'ga ega;
- End-to-End tekshiriladi;
- faqat Completed bo'lgandan keyin keyingi Flow boshlanadi.

**V3 qayta ko'rib chiqish (GFL-002, Director Order):** Flow tartibi
endi GoldBot V3 Architecture asosida quriladi:

Foundation Layer -> Data Layer -> GoldBot (GoldBot Core / Chart
Service / Personal AI Core / Backtesting Engine) -> Application
Services -> Platform Layer -> End User.

Eski (GFL-001 pilot davridagi) 21-Flow raqamlash **bekor qilindi**.
Old -> New mapping jadvali Director Review hisobotida keltirilgan
(shu buyruqqa javoban yozilgan chat xabarida).

---

# FLOW STATUS

Status:

🟦 Blueprint

🟨 In Progress

🟩 Completed

🟥 Blocked

---

# LAYER: Foundation Layer

# FLOW-001

## System Bootstrap / Configuration

Status

Blueprint (yangi -- V3 refactorda qo'shildi, ilgari GFL-001 21-Flow
katalogida alohida Flow sifatida mavjud emas edi)

Producer

System Start (`main.py`, `platform_layer/telegram/polling.py`)

Input

Environment variables, secrets (`core_layer.secrets`)

Processing

Settings build (`config.py` -- `build_settings()` / `get_settings()`)

Output

Runtime Config (`Settings`)

Consumer

Data Layer (FLOW-002)

Next Flow

FLOW-002

---

# LAYER: Data Layer

# FLOW-002

## Current Price

Status

**Completed** (GFL-001 pilot, 2026-08-04)

Producer

Provider Factory (mavjud, qayta ishlatildi -- ProviderRegistry/ProviderManager)

Input

Price Stream (PriceStreamService, `get_shared_price_stream_service()` orqali umumiy instance)

Processing

Data Validation (StreamValidator, default sifatida ulandi)

Output

Validated Current Price (PriceTick, PriceCache'da)

Consumer

Market Memory (FLOW-003)

Next Flow

FLOW-003

---

# FLOW-003

## Market Memory (SSOT)

Status

Completed (2026-08-04, Director Order GFL-003)

Producer

Data Validation (`StreamValidator`) -> `CandleBuilder` (yagona yozuvchi, FLOW-002 orqali allaqachon ulangan)

Input

Validated PriceTick / Candle (FLOW-002 chiqishi)

Processing

Store / Update / Sync (`data_layer.market_memory` -- `MarketMemoryRegistry`,
`MarketMemory`, `TimeframeMemory`, `CandleBuilder` single-writer)

Output

Current Price / Current Candle / Market Snapshot / Historical Data --
`MemoryReader` (kanonik o'qish fasadi) va `MarketManager` (Facade Layer,
`data_layer/live_data/market/`) orqali

Consumer (bugungi kunda haqiqiy va sinovdan o'tgan)

`MemoryReader` / `MarketManager` -- kelajakda GoldBot Core (FLOW-004),
Chart Service (FLOW-016), Personal AI Core (FLOW-017), Backtesting Engine
(FLOW-018) shular orqali o'qiydi (bu Flow'lar hali boshlanmagan, shuning
uchun hozircha real chaqiruvchi yo'q -- lekin o'qish yo'li E2E test bilan
isbotlangan).

Audit natijasi

Yozish tomoni (Producer) FLOW-001/002 ishi natijasida allaqachon
production'da ishlagan. Consumer (`MemoryReader`/`MarketManager`) to'liq
qurilgan va unit test qilingan edi, lekin production kodida hech qachon
chaqirilmagan edi -- `PriceStreamService` yozayotgan jonli
`MarketMemoryRegistry`ga yetib borishning ochiq (public) yo'li yo'q edi.
Tuzatildi: `PriceStreamService.memory_registry` public accessor qo'shildi
(qarang: `data_layer/live_data/price_stream_service/WORK_LOG.md`,
`data_layer/market_memory/WORK_LOG.md`).

Next Flow

FLOW-004

---

# LAYER: GoldBot > GoldBot Core

Real modullar: `core_layer/`, `context_layer/`, `strategy_layer/`,
`signal_layer/`, `decision_layer/`, `risk_layer/`, `execution_layer/`,
`trade_monitoring_layer/`, `indicator_layer/`.

# FLOW-004

## Market Engine

Status

Completed (2026-08-04, Director Order GFL-004)

Producer

Market Memory (FLOW-003) -- `data_layer.market_memory.MemoryReader`
orqali

Input

Market State -- Market Memory'dagi yopilgan (closed) candle seriyasi

Processing

Market Processing -- `MarketDataService.get_candles_from_memory()`:
Market Memory'dan `MemoryReader.get_series()` orqali o'qiydi va
`context.context_orchestrator.ContextEngine.build()`ning mavjud,
o'zgarmagan `candles` kontraktiga (`List[Candle]`) mos shaklda
qaytaradi. Hech qanday yangi tahlil/hisoblash yo'q -- faqat o'qish va
shakl moslashtirish.

Output

Market Context -- `List[Candle]`, `get_candles()`'ning o'zi bilan bir
xil shaklda, Context Engine (FLOW-005) uchun tayyor.

Consumer

Context Engine (FLOW-005) -- hali real chaqiruvchi yo'q (Sequential
Flow Rule bo'yicha FLOW-005 hali boshlanmagan), lekin chiqish shakli
E2E test bilan Context Engine'ning mavjud kontraktiga mosligi
isbotlangan (`core_layer/pipeline/pipeline.py`ga tegilmadi).

Audit natijasi

Real "Market Engine" moduli GoldBot Core'da mavjud emas edi
(`core_layer/core_engine/` faqat "Foundation Freeze v1.0" bo'sh
skeleton). `data_layer/live_data/market/` (`MarketManager`) dastlab
nomi bo'yicha nomzod ko'rindi, lekin o'z hujjatida aniq: "market/ is
NOT a Data Layer member and NOT GoldBot Core" -- FLOW-004 esa GoldBot
Core doirasida. Haqiqiy Reuse: `MarketDataService`
(`data_layer/live_data/market_data_service/`) Market Memory'ga
allaqachon yozar edi (TASK-DATA-004), lekin o'qib qaytarish yo'q edi.
Tuzatildi: `get_candles_from_memory()` + `get_shared_market_data_service()`
qo'shildi -- yangi modul yaratilmadi (qarang:
`data_layer/live_data/market_data_service/WORK_LOG.md`).

Next Flow

FLOW-005

---

# FLOW-005

## Context Engine

Status

Completed (2026-08-04, GFL-004 Lightweight Loop -- Qisqa Audit)

Producer

Market Engine (FLOW-004)

Input

Market Context

Processing

SMC, Wyckoff, Liquidity, Structure -- `context_layer.context_engine
.context_orchestrator.ContextEngine` (mavjud, real kod) orqali.

Output

Market Context Result -- `ContextSnapshot` (candles, structure,
bos_events, choch_events, liquidity_zones, liquidity_sweeps,
order_blocks, fair_value_gaps, amd_events, wyckoff_events,
session_events, market_regime).

Consumer

Analysis Engine (FLOW-006) -- amalda hozircha `core_layer/pipeline.py`
o'zi (`build_context_snapshot`) to'g'ridan-to'g'ri ishlatadi.

Qisqa Audit

`ContextEngine` allaqachon to'liq amalga oshirilgan va allaqachon real
`TradingPipeline`ga ulangan (`core_layer/pipeline.py`). Kod yozish
kerak emas.

Next Flow

FLOW-006

---

# FLOW-006

## Analysis Engine

Producer

Context Engine (FLOW-005)

Input

Market Context Result

Processing

Analysis, Scoring

Output

Analysis Result

Consumer

Indicator Engine (FLOW-007)

Next Flow

FLOW-007

---

# FLOW-007

## Indicator Engine

Producer

Analysis Engine (FLOW-006)

Input

Analysis Result

Processing

Indicator calculation

Output

Indicators

Consumer

Strategy Engine (FLOW-008)

Next Flow

FLOW-008

---

# FLOW-008

## Strategy Engine

Producer

Indicator Engine (FLOW-007)

Input

Indicators

Processing

Strategy rules

Output

Strategy Result

Consumer

Confluence Engine (FLOW-009)

Next Flow

FLOW-009

---

# FLOW-009

## Confluence Engine

Producer

Strategy Engine (FLOW-008)

Input

Strategy Result

Processing

Confluence scoring

Output

Confluence

Consumer

Decision Engine (FLOW-010)

Next Flow

FLOW-010

---

# FLOW-010

## Decision Engine

Producer

Confluence Engine (FLOW-009)

Input

Confluence

Processing

Confidence blending, APPROVE/REJECT/NO_TRADE

Output

Decision

Consumer

Risk Engine (FLOW-011)

Next Flow

FLOW-011

---

# FLOW-011

## Risk Engine

Producer

Decision Engine (FLOW-010)

Input

Decision

Processing

Geometry/stop-loss validation, sizing

Output

Safe Decision

Consumer

Signal Engine (FLOW-012)

Next Flow

FLOW-012

---

# FLOW-012

## Signal Engine

Producer

Risk Engine (FLOW-011)

Input

Safe Decision

Processing

Signal assembly/validation

Output

Signal

Consumer

Execution Engine (FLOW-013)

Next Flow

FLOW-013

---

# FLOW-013

## Execution Engine

Producer

Signal Engine (FLOW-012)

Input

Signal

Processing

Order placement (hozircha inert -- haqiqiy MT5 order yo'q)

Output

Execution Result

Consumer

Trade Monitoring (FLOW-014)

Next Flow

FLOW-014

---

# FLOW-014

## Trade Monitoring

Producer

Execution Engine (FLOW-013)

Input

Execution Result

Processing

Lifecycle tracking

Output

Trade State

Consumer

GoldBot Core API (FLOW-015)

Next Flow

FLOW-015

---

# FLOW-015

## GoldBot Core API

Producer

Trade Monitoring (FLOW-014)

Input

Trade State

Processing

API response assembly

Output

API Response

Consumer

Application Services (FLOW-019)

Next Flow

FLOW-019

---

# LAYER: GoldBot > Chart Service

# FLOW-016

## Chart Service

Status

Blueprint (yangi -- V3 refactorda subsystem sifatida ajratildi, ichi
hali GFL Flow sifatida rasmiylashtirilmagan)

Sub-Status Lifecycle (GFL-003)

Blueprint -> Design -> Development -> Testing -> Stable

Hozirgi bosqich: **Blueprint** (Design hali boshlanmagan)

Producer

Market Memory (FLOW-003)

Input

Market State (aniq kontrakt hali belgilanmagan)

Processing

`chart_layer/` (mavjud kod, GFL Flow sifatida hali audit qilinmagan)

Output

Aniqlanmagan

Consumer

Application Services (FLOW-019)

Next Flow

FLOW-019 (kelajakda)

---

# LAYER: GoldBot > Personal AI Core

# FLOW-017

## Personal AI Core

Status

Blueprint (yangi -- V3 refactorda subsystem sifatida ajratildi, ichi
hali GFL Flow sifatida rasmiylashtirilmagan)

Sub-Status Lifecycle (GFL-003)

Blueprint -> Design -> Development -> Testing -> Stable

Hozirgi bosqich: **Blueprint** (Design hali boshlanmagan)

Producer

Market Memory (FLOW-003) / GoldBot Core (FLOW-004..FLOW-015, advisory input)

Input

Aniqlanmagan (Constitution Article 1/3: faqat advisory, hech qachon
boshqaruvchi emas)

Processing

`ai_layer/` (mavjud kod, GFL Flow sifatida hali audit qilinmagan)

Output

Aniqlanmagan

Consumer

Application Services (FLOW-019)

Next Flow

FLOW-019 (kelajakda)

---

# LAYER: GoldBot > Backtesting Engine

# FLOW-018

## Backtesting Engine

Status

Blueprint (yangi -- V3 refactorda subsystem sifatida ajratildi, ichi
hali GFL Flow sifatida rasmiylashtirilmagan)

Sub-Status Lifecycle (GFL-003)

Blueprint -> Design -> Development -> Testing -> Stable

Hozirgi bosqich: **Blueprint** (Design hali boshlanmagan)

Producer

Data Layer (tarixiy ma'lumot) / GoldBot Core (strategiya qoidalari)

Input

Aniqlanmagan

Processing

`backtesting_layer/` (mavjud kod, GFL Flow sifatida hali audit qilinmagan)

Output

Aniqlanmagan

Consumer

Application Services (FLOW-019)

Next Flow

FLOW-019 (kelajakda)

---

# LAYER: Application Services

# FLOW-019

## Application Services

Producer

GoldBot Core API (FLOW-015) / Chart Service (FLOW-016) / Personal AI Core (FLOW-017) / Backtesting Engine (FLOW-018)

Input

API Response (va boshqa subsystemlar output'i)

Processing

Service composition

Output

Service Data

Consumer

Telegram (FLOW-020), Mini App (FLOW-021), Android (FLOW-022), iOS (FLOW-023), Desktop (FLOW-024), Web (FLOW-025)

Next Flow

FLOW-020...025 (Fan-Out Rule qo'llanadi -- barcha Consumer PASS bo'lishi shart)

---

# LAYER: Platform Layer

# FLOW-020

## Telegram

Producer

Application Services (FLOW-019)

Input

Service Data

Processing

Handler -> Service -> Repository

Output

User Message

Consumer

End User

Next Flow

-- (Platform Layer terminal flow)

---

# FLOW-021

## Mini App

Producer

Application Services (FLOW-019)

Input

Service Data

Processing

UI render

Output

UI View

Consumer

End User

Next Flow

-- (Platform Layer terminal flow)

---

# FLOW-022

## Android

Producer

Application Services (FLOW-019)

Input

Service Data

Processing

UI render

Output

UI View

Consumer

End User

Next Flow

-- (Platform Layer terminal flow)

---

# FLOW-023

## iOS

Producer

Application Services (FLOW-019)

Input

Service Data

Processing

UI render

Output

UI View

Consumer

End User

Next Flow

-- (Platform Layer terminal flow)

---

# FLOW-024

## Desktop

Producer

Application Services (FLOW-019)

Input

Service Data

Processing

UI render

Output

UI View

Consumer

End User

Next Flow

-- (Platform Layer terminal flow)

---

# FLOW-025

## Web

Producer

Application Services (FLOW-019)

Input

Service Data

Processing

UI render

Output

UI View

Consumer

End User

Next Flow

-- (Platform Layer terminal flow)

---

# Development Rule

Worker faqat bitta Flow ustida ishlaydi.

**GFL-003 (Sequential Flow Rule):** navbatdagi ishlanadigan Flow --
eng kichik raqamli bajarilmagan Flow ID (`GFL-001_FLOW_PROGRESS.md`da
yuqoridan pastga birinchi 🟩 Completed bo'lmagan qator). Har bir Flow
faqat o'zidan oldingi Flow Approved + Completed + CI Passed
bo'lgandan keyingina boshlanadi -- tartibdan tashqariga chiqib orqaga
qaytish (masalan FLOW-010'dan FLOW-005'ga) taqiqlanadi.

Har bir Flow:

Audit

↓

Implementation

↓

Testing

↓

Validation

↓

Documentation

↓

WORK_LOG

↓

Completed

↓

Next Flow

---

# Completion Checklist

□ Producer ishlaydi

□ Input ishlaydi

□ Processing ishlaydi

□ Output ishlaydi

□ Consumer ishlaydi

□ Barcha Consumer'lar PASS (Fan-Out Rule)

□ End-to-End Test PASS

□ Producer→Consumer latency o'lchandi va yozildi (Latency Rule)

□ Documentation yangilandi

□ WORK_LOG yozildi

□ Director Review talab qilinmaydi

---

# Forbidden

Worker:

- Flow o'tkazib yubormaydi.
- Ikki Flow ustida parallel ishlamaydi.
- Completed bo'lmagan Flow'dan keyingisiga o'tmaydi.
- Batch Development qilmaydi.
- V3 Architecture'dan tashqari yangi Layer/Subsystem qo'shmaydi (Director tasdig'isiz).
- GFL-003 Sequential Flow Rule'ni buzib, tartibdan tashqariga chiqib Flow boshlamaydi.

---

# Final Principle

GoldBot har doim bitta Flow bo'yicha, V3 Architecture (Foundation ->
Data -> GoldBot[Core/Chart/AI/Backtesting] -> Application Services ->
Platform -> End User) doirasida rivojlanadi.

Flow tugaydi.

↓

Validation.

↓

Documentation.

↓

WORK_LOG.

↓

Keyingi Flow.

Hech qachon bundan chetga chiqilmaydi.
