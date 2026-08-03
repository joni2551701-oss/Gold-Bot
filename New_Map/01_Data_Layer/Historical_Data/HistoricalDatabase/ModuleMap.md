# Historical Database Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Database modulining ichki arxitekturasini, komponentlari orasidagi bog'lanishni va boshqa modullar bilan o'zaro ishlashini tavsiflaydi.

Bu Historical Database modulining Canonical Architecture Blueprint hisoblanadi.

Bu implementatsiya emas.

---

# Module Position

```text
Historical Provider

        │
        ▼
HistoricalDataService

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

# Module Architecture

```text
                Historical Database
                         │
     ┌───────────────────┼────────────────────┐
     ▼                   ▼                    ▼
 Storage Manager    Query Manager      Index Manager
     │                   │                    │
     └──────────────┬────┴────────────────────┘
                    ▼
             Duplicate Checker
                    │
                    ▼
             Historical Storage
                    │
                    ▼
             Metadata Manager
                    │
                    ▼
            HistoricalDataService
```

---

# Internal Components

## Storage Manager

Historical Candle ma'lumotlarini yozish va saqlashni boshqaradi.

Mas'ul:

- Save
- Update
- Delete (agar ruxsat etilgan bo'lsa)

---

## Query Manager

Historical ma'lumotlarni qidirish va o'qish.

Masalan:

- Symbol

- Timeframe

- Date Range

- Latest Candle

---

## Index Manager

Ma'lumotlarni tez topish uchun indekslarni boshqaradi.

Masalan:

- Symbol Index

- Timeframe Index

- Timestamp Index

---

## Duplicate Checker

Yozishdan oldin Candle mavjudligini tekshiradi.

Duplicate yozuvlarga yo'l qo'ymaydi.

---

## Historical Storage

Tarixiy Candle ma'lumotlarini saqlaydi.

Masalan:

- OHLC

- Volume

- Timestamp

- Symbol

- Timeframe

---

## Metadata Manager

Quyidagilarni boshqaradi:

- Database Version

- Record Count

- Last Update Time

- Storage Statistics

---

## HistoricalDataService

Historical Database bilan ishlovchi yagona servis.

---

# Dependency Map

```text
HistoricalDataService

↓

Historical Database

↓

Storage Manager

↓

Duplicate Checker

↓

Historical Storage

↓

Query Manager

↓

Index Manager

↓

Metadata Manager
```

---

# Allowed Dependencies

Historical Database quyidagilar bilan ishlashi mumkin.

✓ HistoricalDataService

✓ Local Database Engine

✓ File System

✓ Configuration Layer

✓ Storage Engine

---

# Forbidden Dependencies

Historical Database quyidagilar bilan ishlashi mumkin emas.

✗ Historical Provider

✗ Live Data

✗ Data Validation

✗ Market Memory

✗ MemoryReader

✗ Event System

✗ Context Engine

✗ Analysis Engine

✗ Strategy Engine

✗ Confluence Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

✗ AI Layer

✗ Platform Layer

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Input

Historical Database qabul qiladi:

• Historical Candles

• OHLC Records

• Symbol

• Timeframe

• Timestamp

• Volume

---

# Output

Historical Database qaytaradi:

• Historical Records

• Query Results

• Historical Dataset

• Database Metadata

• Storage Status

---

# Ownership

Historical Database egalik qiladi:

✓ Historical Storage

✓ Query Processing

✓ Index Management

✓ Duplicate Detection

✓ Metadata

Historical Database egalik qilmaydi:

✗ Historical Download

✗ Bootstrap

✗ Recovery

✗ Validation

✗ Market Memory

✗ Trading Logic

---

# Module Rules

1. Historical Database faqat HistoricalDataService orqali ishlaydi.

2. Historical Database tashqi Provider bilan ishlamaydi.

3. Har bir yozuv Duplicate Checker orqali tekshiriladi.

4. Query Manager faqat o'qish operatsiyalarini bajaradi.

5. Historical Storage ma'lumotni o'zgartirmaydi.

6. Metadata Manager faqat texnik statistikalarni boshqaradi.

7. Historical Database Validation bajarmaydi.

8. Historical Database Market Memory bilan bevosita ishlamaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

Historical Database Module Map Historical Database modulining ichki arxitekturasini va komponentlari orasidagi bog'lanishni belgilaydi.

Canonical Architecture:

HistoricalDataService

↓

Historical Database

↓

Storage Manager

↓

Duplicate Checker

↓

Historical Storage

↓

Query Manager

↓

Index Manager

↓

Metadata Manager

Historical Database Data Layer ichidagi tarixiy market ma'lumotlarini saqlovchi yagona Storage moduli hisoblanadi.
