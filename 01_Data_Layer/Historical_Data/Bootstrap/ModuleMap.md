# Bootstrap Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Bootstrap modulining ichki arxitekturasini va boshqa modullar bilan bog'lanishini tavsiflaydi.

Bu modul xaritasi (Module Architecture Blueprint) hisoblanadi.

Bu hujjat implementatsiya emas.

---

# Module Position

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

# Bootstrap Architecture

```text
                 Bootstrap

                     │

     ┌───────────────┼───────────────┐

     ▼               ▼               ▼

Configuration   Provider Factory   State Manager

     │               │               │

     ▼               ▼               ▼

Historical Provider  Retry Logic   Progress Tracker

            │

            ▼

Historical Database

            │

            ▼

Data Validation

            │

            ▼

Market Memory
```

---

# Internal Modules

## Configuration

Bootstrap konfiguratsiyasini yuklaydi.

Masalan:

• Symbols

• Timeframes

• Candle Limit

• Bootstrap Mode

---

## Provider Factory

Kerakli Historical Provider yaratadi.

Masalan:

• Twelve Data

• CSV

• Backup Source

---

## Historical Provider

Tarixiy market ma'lumotlarini yuklaydi.

---

## Retry Logic

Provider xatolik bersa qayta urinadi.

---

## State Manager

Bootstrap holatini boshqaradi.

States:

• Idle

• Running

• Completed

• Failed

---

## Progress Tracker

Bootstrap jarayonining bajarilish foizini kuzatadi.

---

## Historical Database

Yuklangan ma'lumotlarni vaqtinchalik yoki doimiy saqlaydi.

---

## Data Validation

Ma'lumotlarni tekshiradi.

---

## Market Memory

Tasdiqlangan ma'lumotlarni saqlaydi.

---

# Dependency Map

Bootstrap

↓

Configuration

↓

Provider Factory

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

---

# Allowed Dependencies

Bootstrap quyidagilar bilan ishlashi mumkin:

✓ Configuration

✓ HistoricalDataService

✓ Provider Factory

✓ Historical Provider

✓ Historical Database

✓ Data Validation

✓ Market Memory

---

# Forbidden Dependencies

Bootstrap quyidagilar bilan ishlashi mumkin emas:

✗ Live Data

✗ CurrentPriceProvider

✗ CandleBuilder

✗ Context Engine

✗ Analysis Engine

✗ Strategy Engine

✗ Confluence Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

✗ AI Layer

✗ Platform Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

---

# Input

Bootstrap qabul qiladi:

• Configuration

• Symbols

• Timeframes

• Historical Provider

---

# Output

Bootstrap yaratadi:

• Historical Candles

• Historical OHLC

• Bootstrap Status

• Validated Historical Data

• Initialized Market Memory

---

# Ownership

Bootstrap egalik qiladi:

✓ Startup Historical Loading

✓ Initial Synchronization

✓ Bootstrap State

Bootstrap egalik qilmaydi:

✗ Live Stream

✗ Current Price

✗ Market Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal

---

# Module Rules

1. Bootstrap faqat Historical Data bilan ishlaydi.

2. Bootstrap Provider Factory orqali provider yaratadi.

3. Bootstrap Live Data'ni ishga tushirmaydi.

4. Bootstrap Validation'ni chetlab o'tmaydi.

5. Bootstrap Market Memory'ga faqat Validation'dan o'tgan ma'lumot yozadi.

6. Bootstrap tugagach HistoricalDataService boshqaruvni qaytarib oladi.

---

# Summary

Bootstrap Module Map Bootstrap modulining ichki arxitekturasini va boshqa modullar bilan bog'lanishini belgilaydi.

Bootstrap faqat tizimning boshlang'ich tarixiy ma'lumotlarini yuklash uchun javobgar bo'lib, barcha ma'lumotlar Provider → Database → Validation → Market Memory yo'nalishi bo'yicha harakat qiladi.
