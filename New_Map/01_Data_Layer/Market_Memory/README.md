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

# Layer Position

Historical Data

+

Live Data

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

↓

Application Services

---

# Internal Structure

Market_Memory/

├── README.md
│
├── MarketMemory.md
├── MemoryReader.md
├── MemoryRegistry.md
├── TimeframeMemory.md
├── CachePolicy.md
├── MemoryDataFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

---

# Module Overview

## MarketMemory

Data Layer ichidagi barcha market ma'lumotlarini saqlovchi asosiy xotira.

Single Source of Truth.

---

## MemoryReader

Market Memory'dan xavfsiz va Read-Only ma'lumot olish interfeysi.

Hech qachon yozmaydi.

---

## MemoryRegistry

Barcha instrument va timeframe Memory obyektlarini boshqaradi.

Memory Lifecycle'ni nazorat qiladi.

---

## TimeframeMemory

Har bir timeframe uchun OHLC Candle tarixini saqlaydi.

Masalan:

• M1

• M5

• M15

• H1

• H4

• D1

---

## CachePolicy

Memory hajmini va eski ma'lumotlarni boshqaradi.

Retention Policy.

Cleanup Strategy.

Performance Optimization.

---

## MemoryDataFlow

Market Memory ichidagi ma'lumot oqimini tavsiflaydi.

---

## SequenceDiagram

Market Memory ishlash ketma-ketligini ko'rsatadi.

---

## ModuleMap

Market Memory modullari orasidagi bog'lanishni ko'rsatadi.

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

Historical Data

↓

Live Data

↓

Data Validation

↓

Market Memory

↓

MemoryReader

↓

GoldBot Core

↓

Application Services

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
├── MarketMemory.md
├── MemoryReader.md
├── MemoryRegistry.md
├── TimeframeMemory.md
├── CachePolicy.md
├── MemoryDataFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

Har bir modul o'z specification hujjatiga ega bo'lishi kerak.

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
