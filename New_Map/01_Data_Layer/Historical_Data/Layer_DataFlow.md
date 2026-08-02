# Historical Data Layer Data Flow

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Data bo'limi ichidagi barcha Runtime Data Flow'ni tavsiflaydi.

Historical Data bo'limi tashqi Historical Provider'lardan tarixiy market ma'lumotlarini yuklaydi, saqlaydi, kerak bo'lganda tiklaydi va Data Validation orqali Market Memory'ga uzatadi.

Bu implementatsiya emas.

Bu Historical Data bo'limining Canonical Runtime Data Flow hujjati hisoblanadi.

---

# Layer Position

```text
Configuration Layer

        │
        ▼
Historical Data

        │
        ▼
Data Validation

        │
        ▼
Market Memory
```

---

# Complete Data Flow

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

# Pipeline Flow

```text
Configuration

↓

HistoricalDataService

↓

Bootstrap yoki Recovery talabi

↓

HistoricalProviders

↓

HistoricalDatabase

↓

Data Validation

↓

Market Memory
```

---

# Runtime Flow

```text
Initialize HistoricalDataService

↓

Bootstrap (birinchi ishga tushish) yoki Recovery (bo'shliq aniqlanganda)

↓

HistoricalProviders orqali ma'lumot olish

↓

HistoricalDatabase'ga yozish

↓

Data Validation

↓

Market Memory yangilanadi
```

---

# Module Interaction Flow

```text
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
```

```text
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
```

---

# Runtime Rules

1. Pipeline har doim HistoricalDataService orqali boshqariladi.
2. Bootstrap faqat tizim birinchi marta ishga tushganda ishlaydi.
3. Recovery faqat Data Gap aniqlanganda ishga tushadi.
4. Har bir ma'lumot HistoricalProviders orqali olinadi.
5. Har bir ma'lumot HistoricalDatabase'ga yozilishidan oldin ham, keyin ham Data Validation'dan o'tadi.
6. Market Memory faqat tekshirilgan ma'lumot bilan yangilanadi.
7. Bootstrap va Recovery bir vaqtning o'zida ishlamaydi.
8. Circular Data Flow qat'iyan taqiqlanadi.

---

# Layer Boundaries

Historical Data qabul qiladi:

• Configuration
• Historical Provider ma'lumotlari
• Recovery so'rovlari

Historical Data uzatadi:

• Tarixiy Candle
• Tarixiy OHLC
• Validated Historical Data

---

# Summary

Historical Data Layer Data Flow hujjati Historical Data bo'limi ichidagi barcha Runtime ma'lumot oqimini belgilaydi.

Canonical Layer Flow:

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

Ushbu Data Flow GoldBot Historical Data bo'limi uchun yagona Canonical Runtime Pipeline hisoblanadi.
