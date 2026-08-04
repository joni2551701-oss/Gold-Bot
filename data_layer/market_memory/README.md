# Market Memory

Status: CANONICAL

---

# Purpose

Market Memory — Senior Trading AI ekotizimining yagona bozor xotirasi (Single Source of Truth) hisoblanadi.

Uning asosiy vazifasi Historical Data va Live Data'dan kelgan barcha tasdiqlangan market ma'lumotlarini yagona markazda saqlash va GoldBot Core hamda boshqa Consumer modullariga ishonchli o'qish (Read-Only) interfeysini taqdim etishdir.

Market Memory hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Market Memory quyidagi vazifalarni bajaradi:

• Single Source of Truth

• Market State Storage

• Current Price Storage

• Candle Storage

• Timeframe Storage

• Read Interface

• Memory Synchronization

• Shared Market State

---

# GFL-001 FLOW-003 Holati (2026-08-04)

Status: Completed (Director Order GFL-003).

Joriy real implementatsiya blueprint'dagi `MarketMemoryService/`,
`MemoryWriter/`, `MemoryStorage/`, `MemoryCache/`, `MemoryLifecycle/`
papka nomlari ostida emas -- ular "Foundation Freeze v1.0" (MIR-001)
bo'sh skeletonlar, GFL-001 doirasidan tashqari alohida migratsiya
tashabbusi. Haqiqiy ishlaydigan kod hozircha shu paket ichidagi tekis
(flat) modullarda joylashgan: `market_memory.py`,
`market_memory_registry/`, `memory_reader/` (= `MemoryReader`),
`timeframe_memory/`, `candle_record/`, `data_cache/`, `persistence/*`.

Producer: Data Validation (`StreamValidator`) -> `CandleBuilder`
(yagona yozuvchi) -- `data_layer.live_data.price_stream_service`
orqali allaqachon production'da ishlaydi.

Consumer: `MemoryReader` / `data_layer.live_data.market.market_manager.MarketManager`
-- `PriceStreamService.memory_registry` public accessor orqali jonli
registry'ga ulanadi. To'liq zanjir (`Provider -> Validation -> Market
Memory -> Consumer`) E2E test bilan tasdiqlangan
(`tests/data/stream/test_flow_003_market_memory_e2e.py`).

Batafsil: `WORK_LOG.md`, `docs/GFL-001_FLOW_CATALOG.md` (FLOW-003).

---

# Layer Position

Live Data Layer

↓

Market Memory

↓

GoldBot Core

---

# Internal Structure

Market_Memory/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── MarketMemoryService/
├── MemoryWriter/
├── MemoryStorage/
├── MemoryCache/
├── MemoryLifecycle/
└── MemoryReader/

---

# Module Overview

## MarketMemoryService

Market Memory Layer'ning markaziy Orchestrator'i.

---

## MemoryWriter

Market Memory'ga yagona Write Interface.

---

## MemoryStorage

Market Memory'ning yagona Persistent Storage'i.

---

## MemoryCache

Market Memory'ning Runtime Cache'i.

---

## MemoryLifecycle

Market Memory'ning Runtime Lifecycle va Recovery boshqaruvchisi.

---

## MemoryReader

Market Memory'dan xavfsiz va Read-Only ma'lumot olish interfeysi.

Hech qachon yozmaydi.

---

# Responsibilities

Market Memory:

✓ Store Current Price

✓ Store Candles

✓ Store Historical Data

✓ Store Live Data

✓ Manage Timeframes

✓ Share Market State

✓ Provide Read Access

✓ Synchronize Market Data

---

# Not Responsible

Market Memory:

✗ Historical Download

✗ Live Streaming

✗ Tick Validation

✗ Candle Building

✗ Market Analysis

✗ Context Calculation

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

---

# Memory Flow

Live Data Layer

↓

Market Memory

↓

GoldBot Core

---

# Golden Rules

1. Market Memory — Single Source of Truth.

2. Historical Data va Live Data Market Memory'ga yozadi.

3. GoldBot Core hech qachon Market Memory'ga yozmaydi.

4. Consumer modullar faqat MemoryReader orqali o'qiydi.

5. Market Memory hech qachon marketni hisoblamaydi.

6. Market Memory hech qachon signal yaratmaydi.

7. Memory faqat tasdiqlangan (Validated) ma'lumotlarni saqlaydi.

8. Har bir instrument va timeframe uchun yagona Memory mavjud bo'ladi.

9. MemoryRegistry barcha Memory obyektlarini boshqaradi.

10. Market Memory butun GoldBot ekotizimi uchun yagona bozor holatini ta'minlaydi.

---

# Repository Structure

Market_Memory/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── MarketMemoryService/
├── MemoryWriter/
├── MemoryStorage/
├── MemoryCache/
├── MemoryLifecycle/
└── MemoryReader/

Har bir modul o'z README.md, Contracts.md, ModuleMap.md va SequenceDiagram.md hujjatlariga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Market Memory blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Market Memory — GoldBot Data Layer'ning markaziy xotira tizimi hisoblanadi.

Uning vazifasi:

• Historical va Live ma'lumotlarni yagona markazda saqlash;

• barcha timeframe va instrumentlar holatini boshqarish;

• GoldBot Core va boshqa Consumer modullariga ishonchli Read-Only ma'lumot taqdim etish.

Market Memory hech qachon bozorni tahlil qilmaydi va savdo qarorini hisoblamaydi. U faqat butun ekotizim uchun yagona, ishonchli va sinxron bozor holatini saqlaydi.
