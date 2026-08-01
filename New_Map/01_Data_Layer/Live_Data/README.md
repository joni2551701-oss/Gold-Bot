# Live Data

Status: CANONICAL

---

# Purpose

Live Data — Data Layer ichidagi real vaqt (Real-Time) market ma'lumotlarini boshqaruvchi bo'limdir.

Uning asosiy vazifasi providerlardan kelayotgan Tick, Quote va Price Stream ma'lumotlarini qabul qilish, tekshirish, Candle yaratish va Market Memory'ni doimo yangilab borishdir.

Live Data tarixiy ma'lumotlar bilan ishlamaydi.

---

# Objective

Live Data quyidagi vazifalarni bajaradi:

• Live Price Streaming

• Current Price Management

• Tick Processing

• Candle Building

• Tick Validation

• Market Calendar

• Live Provider Management

• Market Memory Update

---

# Layer Position

Live Providers

↓

Price Stream

↓

Live Data

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

---

# Internal Structure

Live_Data/

├── README.md
│
├── PriceStreamService.md
├── CurrentPriceProvider.md
├── CandleBuilder.md
├── StreamValidator.md
├── MarketCalendar.md
├── LiveProviders.md
├── LiveDataFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

---

# Module Overview

## PriceStreamService

Live providerlardan kelayotgan Tick va Quote ma'lumotlarini qabul qiladi.

Live Data oqimining markaziy boshqaruvchisi hisoblanadi.

---

## CurrentPriceProvider

Har bir instrument uchun eng so'nggi (Current Price) narxni taqdim etadi.

---

## CandleBuilder

Tick ma'lumotlaridan OHLC Candle hosil qiladi.

Timeframe bo'yicha Candle'larni yaratadi.

---

## StreamValidator

Har bir kelayotgan Tick va Stream paketini tekshiradi.

Noto'g'ri ma'lumotlarni rad etadi.

---

## MarketCalendar

Market ochiq yoki yopiq holatini nazorat qiladi.

Trading Session va Holiday qoidalarini boshqaradi.

---

## LiveProviders

Bitget va boshqa Live Providerlar bilan ishlaydi.

Realtime ulanishlarni boshqaradi.

---

## LiveDataFlow

Live Data ichidagi ma'lumot oqimini tavsiflaydi.

---

## SequenceDiagram

Live Data ishlash ketma-ketligini ko'rsatadi.

---

## ModuleMap

Live Data modullari orasidagi bog'lanishni ko'rsatadi.

---

# Responsibilities

Live Data:

✓ Receive Live Tick

✓ Receive Live Quote

✓ Validate Tick

✓ Build Candle

✓ Update Current Price

✓ Update Market Memory

✓ Monitor Market Session

✓ Manage Live Providers

---

# Not Responsible

Live Data:

✗ Historical Download

✗ Bootstrap

✗ Recovery

✗ Market Analysis

✗ Context Engine

✗ Strategy Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

---

# Live Flow

Live Provider

↓

PriceStreamService

↓

StreamValidator

↓

CurrentPriceProvider

↓

CandleBuilder

↓

Market Memory

↓

GoldBot Core

---

# Golden Rules

1. Live Data faqat real vaqt ma'lumotlari bilan ishlaydi.

2. Historical Data bilan aralashmaydi.

3. Har bir Tick Validation'dan o'tishi shart.

4. Current Price har doim eng so'nggi tasdiqlangan Tick asosida yangilanadi.

5. Candle faqat CandleBuilder tomonidan yaratiladi.

6. Market Memory'ga faqat tekshirilgan ma'lumot yoziladi.

7. Live Providerlar faqat Live Data orqali ishlaydi.

8. Market Calendar trading vaqtlarini nazorat qiladi.

9. Live Data hech qachon marketni tahlil qilmaydi.

10. Live Data GoldBot Core uchun ishonchli Real-Time ma'lumot manbai hisoblanadi.

---

# Repository Structure

Live_Data/

├── README.md
├── PriceStreamService.md
├── CurrentPriceProvider.md
├── CandleBuilder.md
├── StreamValidator.md
├── MarketCalendar.md
├── LiveProviders.md
├── LiveDataFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

Har bir modul o'z specification hujjatiga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Live Data blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Live Data — Data Layer ichidagi real vaqt market ma'lumotlarini boshqaruvchi bo'limdir.

Uning vazifasi:

• live providerlardan narxlarni qabul qilish;

• Tick va Quote ma'lumotlarini tekshirish;

• Current Price'ni yangilash;

• OHLC Candle yaratish;

• Market Memory'ni doimiy ravishda yangilash.

Live Data marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Uning yagona vazifasi GoldBot Core uchun ishonchli va uzluksiz Real-Time ma'lumot oqimini ta'minlashdir.
