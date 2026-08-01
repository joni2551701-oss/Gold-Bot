# Historical Data Flow

Status: CANONICAL

---

# Purpose

Historical Data Flow — Historical Data moduli ichidagi ma'lumot oqimini (Data Flow) tavsiflovchi hujjatdir.

Uning asosiy vazifasi tarixiy market ma'lumotlari Provider'dan boshlab Market Memory'gacha qanday harakatlanishini standartlashtirishdir.

Bu implementatsiya emas.

Bu Historical Data modulining Canonical Data Flow Blueprint hisoblanadi.

---

# Objective

Historical Data Flow quyidagi jarayonlarni tavsiflaydi:

• Historical Data Loading

• Bootstrap Flow

• Recovery Flow

• Provider Flow

• Database Flow

• Validation Flow

• Market Memory Update

---

# Flow Position

```text
Historical Provider

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

↓

GoldBot Core
```

---

# Complete Historical Data Flow

```text
External Provider

↓

Provider Factory

↓

Historical Provider

↓

HistoricalDataService

↓

Bootstrap
        │
        └─────┐
              ▼
          Recovery
              │
              ▼
Historical Database

↓

Data Validation

↓

Market Memory

↓

MemoryReader

↓

GoldBot Core
```

---

# Bootstrap Flow

```text
GoldBot Start

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
```

Bootstrap tizim ishga tushganda faqat bir marta bajariladi.

---

# Recovery Flow

```text
Recovery Request

↓

HistoricalDataService

↓

Recovery

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Recovery Completed
```

Recovery faqat yetishmayotgan ma'lumotlarni tiklaydi.

---

# Historical Download Flow

```text
HistoricalDataService

↓

Provider Factory

↓

Historical Provider

↓

Download Historical Data

↓

Normalize Response

↓

Historical Database
```

---

# Database Flow

```text
Historical Database

↓

Duplicate Check

↓

Store Historical Data

↓

Read Historical Data

↓

Return Result
```

---

# Validation Flow

```text
Historical Database

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
Market Memory

↓

MemoryReader

↓

GoldBot Core
```

Historical Data hech qachon GoldBot Core bilan bevosita ishlamaydi.

---

# Input

Historical Data quyidagi ma'lumotlarni qabul qiladi:

• Symbol

• Timeframe

• Start Time

• End Time

• Candle Limit

• Provider Configuration

---

# Output

Historical Data quyidagilarni yaratadi:

• Historical Candle

• Historical OHLC

• Historical Dataset

• Validated Historical Data

• Updated Market Memory

---

# Flow Rules

1. Historical Data faqat Historical Provider orqali ma'lumot oladi.

2. HistoricalDataService barcha oqimni boshqaradi.

3. Bootstrap va Recovery bir xil Database'dan foydalanadi.

4. Har bir ma'lumot Validation'dan o'tishi shart.

5. Validation'dan o'tmagan ma'lumot Market Memory'ga yozilmaydi.

6. Market Memory faqat yakuniy tasdiqlangan ma'lumotni saqlaydi.

7. GoldBot Core faqat MemoryReader orqali o'qiydi.

8. Historical Data oqimi Live Data oqimidan mustaqil ishlaydi.

---

# Golden Rules

• Provider faqat ma'lumot beradi.

• HistoricalDataService oqimni boshqaradi.

• Bootstrap boshlang'ich yuklashni bajaradi.

• Recovery yetishmayotgan ma'lumotlarni tiklaydi.

• Historical Database ma'lumotlarni saqlaydi.

• Data Validation ma'lumotlarni tekshiradi.

• Market Memory yagona saqlash markazi hisoblanadi.

• GoldBot Core faqat tayyor ma'lumotni o'qiydi.

---

# Related Documents

```text
Historical_Data/

├── README.md
├── HistoricalDataService/
├── Bootstrap/
├── Recovery/
├── HistoricalProviders/
├── HistoricalDatabase/
└── HistoricalDataFlow/
```

---

# Summary

Historical Data Flow Historical Data modulidagi barcha ma'lumot oqimining yagona rasmiy tavsifidir.

Canonical Data Flow:

External Provider

↓

Historical Provider

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

↓

MemoryReader

↓

GoldBot Core

Historical Data oqimidagi har qanday yangi modul ushbu Data Flow qoidalariga mos bo'lishi shart.
