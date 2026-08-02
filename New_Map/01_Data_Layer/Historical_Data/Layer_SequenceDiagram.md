# Historical Data Layer Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Data bo'limi ishga tushganda modullar qanday ketma-ketlikda ishlashini ko'rsatadi.

Bu Runtime Sequence bo'lib, implementatsiya emas.

---

# Bootstrap Sequence

```text
GoldBot Start
      │
      ▼
Configuration Layer
      │
      ▼
HistoricalDataService
      │
      ▼
Bootstrap
      │
      ▼
HistoricalProviders
      │
      ▼
HistoricalDatabase
      │
      ▼
Data Validation
      │
      ▼
Market Memory
      │
      ▼
Bootstrap Completed
```

---

# Recovery Sequence

```text
Data Gap aniqlandi
      │
      ▼
HistoricalDataService
      │
      ▼
Recovery
      │
      ▼
HistoricalProviders
      │
      ▼
HistoricalDatabase
      │
      ▼
Data Validation
      │
      ▼
Market Memory
      │
      ▼
Recovery Completed
```

---

# Module Interaction

```text
HistoricalDataService
        │
        ▼
Bootstrap / Recovery
        │
        ▼
HistoricalProviders
        │
        ▼
HistoricalDatabase
        │
        ▼
Data Validation
        │
        ▼
Market Memory
```

---

# Failure Sequence

```text
Bootstrap yoki Recovery Started

↓

HistoricalProviders Error

↓

Retry Download

↓

Retry Failed

↓

HistoricalDataService'ga Xato Xabari
```

---

# Runtime Rules

1. Bootstrap Configuration yuklangandan keyin boshlanadi.
2. HistoricalDataService barcha jarayonlarni boshqaradi.
3. HistoricalProviders orqali olingan ma'lumot avval HistoricalDatabase'ga yoziladi.
4. Har bir ma'lumot Data Validation'dan o'tishi shart.
5. Validation muvaffaqiyatli bo'lsa Market Memory yangilanadi.
6. Recovery faqat aniqlangan Data Gap uchun ishga tushadi.
7. Bootstrap tugamaguncha Live Data ishga tushmaydi.

---

# Summary

Historical Data Layer Sequence Diagram GoldBot ishga tushganda va Recovery kerak bo'lganda tarixiy ma'lumotlarning qanday yuklanishini va modullar orasidagi bajarilish ketma-ketligini belgilaydi.

Canonical Sequence:

HistoricalDataService

↓

Bootstrap / Recovery

↓

HistoricalProviders

↓

HistoricalDatabase

↓

Data Validation

↓

Market Memory
