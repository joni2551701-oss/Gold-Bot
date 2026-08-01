# Event System

Status: CANONICAL

---

# Purpose

Event System — Data Layer ichidagi modullar o'rtasida ma'lumot almashishni boshqaruvchi ichki kommunikatsiya qatlamidir.

Uning asosiy vazifasi modullarni bir-biridan mustaqil (Decoupled) holda ishlashini ta'minlash va barcha hodisalarni (Events) standart ko'rinishda tarqatishdir.

Event System hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Event System quyidagi vazifalarni bajaradi:

• Event Publishing

• Event Subscription

• Event Routing

• Module Communication

• Decoupled Architecture

• Event Distribution

• Event Lifecycle

• Internal Messaging

---

# Layer Position

Historical Data

+

Live Data

↓

Market Memory

↓

Event System

↓

GoldBot Core

↓

Application Services

---

# Internal Structure

Event_System/

├── README.md
│
├── EventBus.md
├── EventTypes.md
├── Publishers.md
├── Subscribers.md
├── EventFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

---

# Module Overview

## EventBus

Data Layer ichidagi barcha Event'larni qabul qiladi va tegishli Subscriber'larga uzatadi.

---

## EventTypes

Tizimdagi barcha Event turlarini belgilaydi.

Masalan:

• PRICE_UPDATED

• CANDLE_CLOSED

• MARKET_OPENED

• MARKET_CLOSED

• MEMORY_UPDATED

• PROVIDER_CONNECTED

• PROVIDER_DISCONNECTED

---

## Publishers

Event yaratadigan modullar.

Masalan:

• HistoricalDataService

• PriceStreamService

• CandleBuilder

• MarketMemory

---

## Subscribers

Event'larni qabul qiluvchi modullar.

Masalan:

• GoldBot Core

• Monitoring

• Analytics

• Notification

---

## EventFlow

Eventlarning tizim bo'ylab qanday harakatlanishini tavsiflaydi.

---

## SequenceDiagram

Event System ishlash ketma-ketligini ko'rsatadi.

---

## ModuleMap

Event System modullari orasidagi bog'lanishni ko'rsatadi.

---

# Responsibilities

Event System:

✓ Publish Events

✓ Subscribe Events

✓ Route Events

✓ Notify Modules

✓ Synchronize Modules

✓ Decouple Components

✓ Event Lifecycle

✓ Internal Communication

---

# Not Responsible

Event System:

✗ Historical Download

✗ Live Stream

✗ Market Memory Storage

✗ Market Analysis

✗ Strategy Calculation

✗ Decision Engine

✗ Risk Engine

✗ Signal Generation

✗ Trade Execution

---

# Event Flow

Publisher

↓

EventBus

↓

Subscribers

↓

Module Response

---

# Golden Rules

1. Modullar bir-birini to'g'ridan-to'g'ri chaqirmaydi.

2. Har qanday ichki hodisa EventBus orqali uzatiladi.

3. Publisher Subscriber'ni bilmaydi.

4. Subscriber Publisher'ni bilmaydi.

5. EventBus faqat hodisalarni tarqatadi.

6. Eventlar immutable bo'lishi kerak.

7. Event nomlari standartlashtirilgan bo'lishi kerak.

8. Event System biznes logikasini bajarmaydi.

9. Event System modul bog'liqligini kamaytiradi.

10. Event System Data Layer va GoldBot Core o'rtasidagi ichki kommunikatsiyani standartlashtiradi.

---

# Repository Structure

Event_System/

├── README.md
├── EventBus.md
├── EventTypes.md
├── Publishers.md
├── Subscribers.md
├── EventFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

Har bir modul o'z specification hujjatiga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Event System blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Event System — GoldBot Data Layer ichidagi ichki kommunikatsiya markazi hisoblanadi.

Uning vazifasi:

• hodisalarni yaratish va tarqatish;

• modullarni mustaqil ishlashini ta'minlash;

• komponentlar o'rtasidagi bog'liqlikni kamaytirish;

• yagona EventBus orqali tizim ichidagi barcha Event almashinuvini boshqarish.

Event System hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Uning vazifasi GoldBot ekotizimidagi modullarni bir-biriga bog'lamasdan, ishonchli va standart Event mexanizmi orqali ishlashini ta'minlashdir.
