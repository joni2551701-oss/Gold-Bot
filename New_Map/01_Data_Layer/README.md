# Data Layer

Status: CANONICAL

---

# Purpose

Data Layer — GoldBot ekotizimining eng quyi va eng muhim qatlamidir.

Uning yagona vazifasi market ma'lumotlarini yig'ish, tekshirish, saqlash va GoldBot Core'ga uzatishdir.

Data Layer hech qachon marketni tahlil qilmaydi va savdo qarorini qabul qilmaydi.

---

# Objective

Data Layer quyidagi vazifalarni bajaradi:

• Historical Data yuklash

• Live Data qabul qilish

• Data Validation

• Market Memory boshqarish

• Event tarqatish

• Providerlarni boshqarish

• GoldBot Core uchun ishonchli ma'lumot tayyorlash

---

# Layer Position

GoldBot Start

↓

Configuration

↓

Provider Factory

↓

DATA LAYER

↓

GoldBot Core

↓

Application Services

↓

Platform Layer

---

# Internal Structure

Data_Layer/

├── README.md
│
├── Historical_Data/
│
├── Live_Data/
│
├── Market_Memory/
│
├── Event_System/
│
├── Data_Validation/
│
└── Providers/

---

# Module Overview

## Historical_Data

Historical market ma'lumotlarini yuklash va Recovery jarayonlarini boshqaradi.

---

## Live_Data

Live Tick oqimini qabul qiladi va real vaqt ma'lumotlarini boshqaradi.

---

## Market_Memory

Single Source of Truth.

Data Layer ichidagi barcha ma'lumotlarning yagona saqlash joyi.

---

## Event_System

Data Layer modullari orasidagi event almashinuvini boshqaradi.

---

## Data_Validation

Har bir Tick va Candle tekshiriladi.

Validation'dan o'tmagan ma'lumot tizimga kiritilmaydi.

---

## Providers

TwelveData, Bitget va kelajakdagi barcha providerlarni boshqaradi.

---

# Responsibilities

Data Layer:

✓ Historical Data

✓ Live Data

✓ Bootstrap

✓ Recovery

✓ Market Memory

✓ Current Price

✓ Candle Builder

✓ Event System

✓ Data Validation

✓ Provider Management

---

# Not Responsible

Data Layer:

✗ Market Analysis

✗ Context

✗ Strategy

✗ Confluence

✗ Decision

✗ Risk

✗ Signal

✗ AI

✗ Telegram

✗ Mobile

✗ Desktop

✗ Web

✗ Execution

---

# Data Flow

Provider

↓

HistoricalDataService

↓

PriceStreamService

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

---

# Golden Rules

1. Data Layer faqat market ma'lumotlari bilan ishlaydi.

2. Market Memory — yagona ma'lumot manbai.

3. Historical Data faqat HistoricalDataService orqali kiradi.

4. Live Data faqat PriceStreamService orqali kiradi.

5. Har bir ma'lumot Validation'dan o'tadi.

6. Core hech qachon provider bilan to'g'ridan-to'g'ri ishlamaydi.

7. Providerlar faqat Data Layer ichida mavjud bo'ladi.

8. Data Layer yuqori qatlamlarga bog'liq bo'lmaydi.

9. Har bir modul Single Responsibility prinsipiga amal qiladi.

10. Reuse First — dublikat logika yaratilmaydi.

11. Event_System GoldBot'ning Canonical Event Bus hisoblanadi. Barcha Layerlar (Data Layer'ning o'zidan tashqari — Context, Strategy, Signal, AI, Decision, Risk, Execution, Trade Monitoring, Database, Platform, Media, Chart va boshqalar) bir-biriga asinxron xabar yuborish uchun Event_System orqali ishlaydi. Bu yagona rasmiy Event Bus — boshqa hech qanday Layer o'zining alohida Event Bus'ini yaratmaydi.

---

# Repository Structure

Data_Layer/

├── README.md
│
├── Historical_Data/
├── Live_Data/
├── Market_Memory/
├── Event_System/
├── Data_Validation/
└── Providers/

Har bir papka o'z README.md fayliga ega bo'lishi kerak.

Har bir .py fayl uchun mos specification (.md) mavjud bo'lishi kerak.

---

# Refactoring Rule

Repository Data Layer blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Data Layer — GoldBot'ning market ma'lumotlari uchun yagona kirish nuqtasi hisoblanadi.

Uning vazifasi:

• ma'lumotni yig'ish;

• tekshirish;

• saqlash;

• Core'ga uzatish.

Data Layer hech qachon marketni tahlil qilmaydi, signal yaratmaydi yoki savdo qarori qabul qilmaydi.
