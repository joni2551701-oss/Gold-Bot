# Bootstrap

Status: CANONICAL

---

# Purpose

Bootstrap — Historical Data bo'limining boshlang'ich yuklash (Initial Data Loading) moduli hisoblanadi.

Uning asosiy vazifasi GoldBot ishga tushganda Market Memory'ni ishlash uchun zarur bo'lgan tarixiy market ma'lumotlari bilan to'ldirishdir.

Bootstrap faqat tizim ishga tushish jarayonida ishlaydi.

---

# Objective

Bootstrap quyidagi vazifalarni bajaradi:

• Initial Historical Data Loading

• Required Timeframe Loading

• Required Symbol Loading

• Initial Market Memory Population

• Bootstrap Validation

• Bootstrap Completion Check

---

# Layer Position

Configuration Layer

↓

HistoricalDataService

↓

Bootstrap

↓

Historical Providers

↓

Historical Database

↓

Data Validation

↓

Market Memory

---

# Responsibilities

Bootstrap:

✓ Historical Data yuklash

✓ Kerakli timeframe'larni yuklash

✓ Kerakli instrumentlarni yuklash

✓ Market Memory'ni boshlang'ich ma'lumot bilan to'ldirish

✓ Validation'dan o'tkazish

✓ Bootstrap holatini tekshirish

---

# Not Responsible

Bootstrap:

✗ Live Streaming

✗ Recovery

✗ Current Price

✗ Candle Building

✗ Strategy

✗ Analysis

✗ Decision

✗ Risk

✗ Signal Generation

---

# Input

Bootstrap quyidagilarni qabul qiladi:

• Configuration

• Symbols

• Timeframes

• Historical Provider

---

# Output

Bootstrap quyidagilarni yaratadi:

• Historical Candles

• Historical OHLC

• Validated Data

• Initialized Market Memory

---

# Bootstrap Flow

Configuration

↓

HistoricalDataService

↓

Bootstrap

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Bootstrap Completed

---

# Golden Rules

1. Bootstrap faqat tizim ishga tushganda bajariladi.

2. Bootstrap tugamaguncha Live Stream boshlanmaydi.

3. Har bir ma'lumot Validation'dan o'tishi shart.

4. Market Memory faqat tekshirilgan ma'lumot bilan to'ldiriladi.

5. Bootstrap marketni tahlil qilmaydi.

6. Bootstrap signal yaratmaydi.

7. Bootstrap Recovery o'rnini bosmaydi.

8. Bootstrap muvaffaqiyatli yakunlangandan keyingina tizim keyingi bosqichga o'tadi.

---

# Related Documents

Bootstrap/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md

---

# Summary

Bootstrap — Historical Data modulining boshlang'ich yuklash komponentidir.

U GoldBot ishga tushganda kerakli tarixiy market ma'lumotlarini yuklaydi, ularni tekshiradi va Market Memory'ni ishga tayyor holatga keltiradi.
