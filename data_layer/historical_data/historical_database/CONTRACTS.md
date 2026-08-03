# Historical Database Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Database modulining rasmiy Architecture Contract hujjati hisoblanadi.

Historical Database moduliga qo'shiladigan har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

Historical Database — Historical Data modulining yagona tarixiy ma'lumotlarni saqlash (Storage) komponentidir.

---

# Module Responsibility

Historical Database quyidagi vazifalar uchun javobgar:

✓ Historical Data Storage

✓ Historical Data Retrieval

✓ Historical Query Processing

✓ Historical Index Management

✓ Duplicate Detection

✓ Historical Metadata Management

✓ Storage Integrity

Historical Database quyidagi vazifalarni bajarmaydi:

✗ Historical Download

✗ Provider Management

✗ Bootstrap Logic

✗ Recovery Logic

✗ Data Validation

✗ Market Memory Update

✗ Market Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

---

# Module Boundary

HistoricalDataService

↓

Historical Database

↓

Storage Engine

↓

Query Engine

↓

HistoricalDataService

↓

Boundary End

Historical Database faqat Storage qatlamidir.

---

# Input Contract

Historical Database quyidagilarni qabul qiladi:

• Historical Candle

• OHLC Data

• Volume

• Timestamp

• Symbol

• Timeframe

• Metadata

---

# Output Contract

Historical Database quyidagilarni qaytaradi:

• Historical Records

• Candle History

• Query Result

• Historical Dataset

• Storage Metadata

• Storage Status

---

# Read Contract

Historical Database quyidagilarni o'qishi mumkin:

✓ Storage Engine

✓ Index Engine

✓ Local Metadata

✓ Configuration

---

# Write Contract

Historical Database faqat quyidagilarga yozishi mumkin:

✓ Local Storage

✓ Storage Metadata

✓ Index Storage

Historical Database boshqa modullarga yozmaydi.

---

# Allowed Dependencies

Historical Database quyidagilar bilan ishlashi mumkin:

✓ HistoricalDataService

✓ Local Database Engine

✓ File System

✓ Configuration Layer

✓ Storage Engine

---

# Forbidden Dependencies

Historical Database quyidagilar bilan ishlashi mumkin emas:

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

# Ownership

Historical Database egalik qiladi:

✓ Historical Storage

✓ Historical Queries

✓ Storage Indexes

✓ Duplicate Detection

✓ Storage Metadata

✓ Storage Statistics

Historical Database egalik qilmaydi:

✗ Historical Download

✗ Bootstrap

✗ Recovery

✗ Validation

✗ Market Memory

✗ Current Price

✗ Live Data

✗ Trading Logic

---

# State Contract

Historical Database quyidagi holatlarda bo'lishi mumkin:

• Idle

• Reading

• Writing

• Querying

• Indexing

• Compacting

• Completed

• Failed

---

# Error Contract

Historical Database quyidagi xatolarni qaytarishi mumkin:

• StorageUnavailable

• DatabaseCorrupted

• RecordNotFound

• DuplicateRecord

• InvalidQuery

• ReadFailed

• WriteFailed

• IndexError

• StorageFull

• UnknownStorageError

Har qanday xato HistoricalDataService tomonidan boshqariladi.

---

# Runtime Contract

1. Historical Database faqat HistoricalDataService orqali ishlaydi.

2. Har bir yozish Duplicate Checker orqali tekshirilishi shart.

3. Timestamp ketma-ketligi saqlanishi shart.

4. Symbol va Timeframe indekslari doimo yangilanadi.

5. Historical Database ma'lumotni tahrir qilmaydi.

6. Historical Database Validation bajarmaydi.

7. Historical Database Market Memory bilan bevosita ishlamaydi.

8. Historical Database faqat tarixiy ma'lumotlarni boshqaradi.

9. Har qanday Query Read-Only hisoblanadi.

10. Storage Integrity har doim saqlanishi shart.

---

# Architecture Rules

Historical Database:

✓ Historical ma'lumotlarni saqlaydi.

✓ HistoricalDataService bilan ishlaydi.

✓ Query xizmatini taqdim etadi.

✓ Duplicate yozuvlarni oldini oladi.

✓ Storage Integrity'ni saqlaydi.

Historical Database:

✗ Historical Data yuklamaydi.

✗ Provider bilan ishlamaydi.

✗ Validation bajarmaydi.

✗ Market Memory'ni yangilamaydi.

✗ Trading qilmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi:

• Historical Database → Provider import

• Historical Database → Live Data import

• Historical Database → Validation import

• Historical Database → Market Memory Write

• Historical Database → Strategy import

• Historical Database → Decision import

• Historical Database → AI import

• Historical Database → Business Layer import

• Direct Database Access (HistoricalDataService'siz)

• Circular Dependency

---

# Acceptance Criteria

Historical Database to'g'ri ishlaydi agar:

✓ Historical Data muvaffaqiyatli saqlansa.

✓ Duplicate yozuvlar rad etilsa.

✓ Historical Query to'g'ri ishlasa.

✓ Timestamp tartibi saqlansa.

✓ Symbol va Timeframe indekslari yangilansa.

✓ Storage Integrity saqlansa.

✓ HistoricalDataService bilan to'g'ri integratsiya qilinsa.

---

# Summary

Historical Database Contract Historical Database modulining rasmiy arxitektura shartnomasi hisoblanadi.

Historical Database faqat tarixiy market ma'lumotlarini saqlash, o'qish va boshqarish uchun javobgardir.

Ushbu hujjatda belgilangan chegaralar, bog'lanishlar va qoidalardan chetga chiqadigan har qanday implementatsiya GoldBot Architecture Violation hisoblanadi.
