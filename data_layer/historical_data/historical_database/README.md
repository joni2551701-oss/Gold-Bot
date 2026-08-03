# Historical Database

Status: CANONICAL

---

# Purpose

Historical Database — Historical Data modulining tarixiy market ma'lumotlarini saqlash va boshqarish komponentidir.

Uning asosiy vazifasi Historical Providers orqali yuklangan va Data Validation'dan o'tgan tarixiy ma'lumotlarni xavfsiz saqlash hamda Bootstrap va Recovery modullariga tezkor o'qish imkoniyatini taqdim etishdir.

Historical Database faqat tarixiy ma'lumotlarni saqlaydi.

U hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Historical Database quyidagi vazifalarni bajaradi:

• Historical Data Storage

• Historical Data Retrieval

• Timeframe Storage

• Symbol Storage

• Historical Indexing

• Historical Cache Support

• Historical Query Support

• Historical Synchronization

---

# Layer Position

```text
Historical Provider

↓

HistoricalDataService

↓

Historical Database

↓

Data Validation

↓

Market Memory
```

---

# Responsibilities

Historical Database:

✓ Historical Candle saqlash

✓ OHLC ma'lumotlarini saqlash

✓ Symbol bo'yicha ma'lumotlarni boshqarish

✓ Timeframe bo'yicha ma'lumotlarni boshqarish

✓ Tarixiy ma'lumotlarni o'qish

✓ Historical Query bajarish

✓ Bootstrap va Recovery'ni qo'llab-quvvatlash

---

# Not Responsible

Historical Database:

✗ Historical Download

✗ Provider Management

✗ Data Validation

✗ Market Memory

✗ Live Data

✗ Current Price

✗ Strategy

✗ Context

✗ Decision

✗ Risk

✗ Signal Generation

---

# Input

Historical Database quyidagilarni qabul qiladi:

• Historical Candles

• OHLC Data

• Symbol

• Timeframe

• Timestamp

• Volume

---

# Output

Historical Database quyidagilarni qaytaradi:

• Historical Records

• Historical Candle List

• Timeframe History

• Symbol History

• Historical Query Result

---

# Database Contents

Historical Database quyidagilarni saqlaydi:

• Candle History

• OHLC

• Volume

• Timestamp

• Symbol

• Timeframe

• Metadata

---

# Data Flow

```text
Historical Provider

↓

HistoricalDataService

↓

Historical Database

↓

Data Validation

↓

Market Memory
```

---

# Storage Rules

Historical Database:

• Duplicate Candle saqlamaydi.

• Timestamp bo'yicha tartibni saqlaydi.

• Symbol bo'yicha ajratadi.

• Timeframe bo'yicha ajratadi.

• Historical ma'lumotlarni o'zgartirmaydi.

---

# Golden Rules

1. Historical Database faqat tarixiy ma'lumotlarni saqlaydi.

2. Har bir yozuv yagona Timestamp asosida saqlanadi.

3. Duplicate Candle yozilishi taqiqlanadi.

4. Historical Database Validation o'rnini bosmaydi.

5. Historical Database Market Memory bilan to'g'ridan-to'g'ri ishlamaydi.

6. Bootstrap va Recovery Historical Database'dan foydalanishi mumkin.

7. Historical Database Live Data bilan ishlamaydi.

8. Historical Database Trading Logic'dan mustaqil bo'lishi kerak.

---

# Related Documents

```text
HistoricalDatabase/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

Historical Database — Historical Data modulining tarixiy market ma'lumotlarini saqlovchi markaziy komponentidir.

Uning vazifasi:

• tarixiy Candle va OHLC ma'lumotlarini saqlash;

• Bootstrap va Recovery modullariga ishonchli ma'lumot taqdim etish;

• tarixiy market ma'lumotlarini tartibli va xavfsiz boshqarish.

Historical Database faqat saqlash (Storage) vazifasini bajaradi va hech qachon bozorni tahlil qilmaydi yoki savdo qarorini hisoblamaydi.
