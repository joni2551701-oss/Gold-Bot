# Layer Data Flow

Status: CANONICAL

---

# Purpose

Layer Data Flow hujjati Data Layer ichidagi barcha ma'lumot oqimini tavsiflaydi.

Bu hujjat market ma'lumotlari GoldBot tizimiga qanday kirishi, qaysi modullardan o'tishi va GoldBot Core'ga qanday yetib borishini ko'rsatadi.

Bu hujjat implementatsiya emas.

Bu Data Layer uchun rasmiy Data Flow Blueprint hisoblanadi.

---

# Data Layer Flow

```text
                 Historical Provider
                        │
                        ▼
            HistoricalDataService
                        │
             Bootstrap / Recovery
                        │
                        ▼
               Historical Database
                        │
                        ▼
               Data Validation
                        │
                        │
                        ▼
                  Market Memory
                        ▲
                        │
                        │
                 Candle Builder
                        ▲
                        │
              Current Price Provider
                        ▲
                        │
               Stream Validator
                        ▲
                        │
               Price Stream Service
                        ▲
                        │
                  Live Provider
```

---

# Complete Flow

Historical Data

↓

HistoricalDataService

↓

Bootstrap / Recovery

↓

Historical Database

↓

Data Validation

↓

Market Memory

↑

Current Price Provider

↑

Candle Builder

↑

Stream Validator

↑

Price Stream Service

↑

Live Provider

↓

GoldBot Core

---

# Historical Data Flow

```text
Historical Provider

↓

HistoricalDataService

↓

Bootstrap

↓

Recovery

↓

Historical Database

↓

Data Validation

↓

Market Memory
```

Historical Data faqat tarixiy Candle va OHLC ma'lumotlari bilan ishlaydi.

---

# Live Data Flow

```text
Live Provider

↓

Price Stream Service

↓

Stream Validator

↓

Current Price Provider

↓

Candle Builder

↓

Market Memory
```

Live Data faqat Real-Time ma'lumotlarni boshqaradi.

---

# Validation Flow

```text
Historical Data

        +

Live Data

↓

Data Validation

↓

Validation Passed

↓

Market Memory
```

Validation'dan o'tmagan ma'lumot Market Memory'ga yozilmaydi.

---

# Memory Flow

```text
Historical Data

        +

Live Data

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

Market Memory yagona ma'lumot manbai hisoblanadi.

---

# Provider Flow

```text
External Provider

↓

Provider Factory

↓

Provider Interface

↓

Historical Data

or

Live Data
```

Providerlar faqat Data Layer bilan ishlaydi.

---

# Event Flow

```text
Publisher

↓

Event Bus

↓

Subscribers
```

Event Bus modullarni bog'laydi.

Modullar bir-birini to'g'ridan-to'g'ri chaqirmaydi.

---

# Layer Output

Data Layer natijasi:

• Current Price

• Historical Candle

• Live Candle

• Timeframe Data

• Market State

• Market Memory

Ushbu ma'lumotlar GoldBot Core tomonidan o'qiladi.

---

# Layer Input

Data Layer quyidagi manbalardan ma'lumot oladi:

• Twelve Data

• Bitget

• Future Providers

---

# Consumer

Data Layer ma'lumotlarini quyidagi qatlam iste'mol qiladi:

```text
GoldBot Core
```

Data Layer boshqa qatlamlarga bog'liq emas.

---

# Golden Rules

1. Data Layer tashqi providerlardan ma'lumot qabul qiladi.

2. Har bir ma'lumot Validation'dan o'tadi.

3. Validation'dan o'tmagan ma'lumot saqlanmaydi.

4. Historical va Live Data bir xil Market Memory'dan foydalanadi.

5. Market Memory — Single Source of Truth.

6. GoldBot Core faqat MemoryReader orqali o'qiydi.

7. Data Layer hech qachon marketni tahlil qilmaydi.

8. Data Layer hech qachon signal yaratmaydi.

9. Data Layer faqat ma'lumotlarni boshqaradi.

10. Data Layer GoldBot Core uchun ishonchli market ma'lumotlarini tayyorlaydi.

---

# Summary

Data Layer Flow GoldBot ekotizimidagi barcha market ma'lumotlarining yagona rasmiy harakat yo'lini belgilaydi.

Har qanday Historical yoki Live market ma'lumoti quyidagi ketma-ketlikdan o'tadi:

External Provider

↓

Historical Data / Live Data

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

Bu oqim GoldBot Data Layer uchun o'zgarmas (Canonical) Data Flow hisoblanadi.
