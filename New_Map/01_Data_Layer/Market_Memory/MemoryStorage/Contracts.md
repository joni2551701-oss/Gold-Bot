# MemoryStorage Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryStorage modulining rasmiy Architecture Contract hujjati hisoblanadi.

MemoryStorage Market Memory Layer ichidagi yagona Canonical Persistent Storage komponentidir.

Validated Market Data, Runtime State va Snapshot ma'lumotlarini saqlash aynan ushbu modul orqali amalga oshiriladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

MemoryStorage quyidagi vazifalar uchun javobgar.

✓ Persistent Memory Storage

✓ Runtime Memory Storage

✓ Snapshot Storage

✓ Memory Version Management

✓ Data Integrity

✓ Cache Synchronization

✓ Storage Recovery

✓ Storage Event Publishing

MemoryStorage quyidagi vazifalarni bajarmaydi.

✗ Live Tick Receiving

✗ Current Price Calculation

✗ Tick Validation

✗ Candle Generation

✗ Market Analysis

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Module Boundary

Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryReader

↓

Boundary End

---

# Input Contract

MemoryStorage quyidagilarni qabul qiladi.

• Validated Candle

• Current Price

• Runtime Snapshot

• Memory Update Request

• Storage Request

• Recovery Request

---

# Output Contract

MemoryStorage quyidagilarni yaratadi.

• Stored Memory

• Runtime Snapshot

• Storage State

• Memory Version

• Recovery Snapshot

• Storage Events

---

# Read Contract

MemoryStorage quyidagilarni o'qishi mumkin.

✓ Runtime Memory

✓ Stored Memory

✓ Snapshot

✓ Configuration Layer

✓ Storage Metadata

---

# Write Contract

MemoryStorage quyidagilarga yozishi mumkin.

✓ Persistent Storage

✓ Memory Cache

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

MemoryStorage quyidagilar bilan ishlashi mumkin.

✓ MemoryWriter

✓ MemoryReader

✓ MemoryCache

✓ Recovery Engine

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

MemoryStorage quyidagilar bilan ishlashi mumkin emas.

✗ LiveProviders

✗ PriceStreamService

✗ CurrentPriceProvider

✗ StreamValidator

✗ CandleBuilder

✗ Context Layer

✗ Analysis Layer

✗ Strategy Layer

✗ Decision Layer

✗ Risk Layer

✗ Signal Layer

✗ AI Layer

✗ Platform Layer

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Ownership

MemoryStorage egalik qiladi.

✓ Persistent Memory

✓ Runtime Memory

✓ Memory Versions

✓ Memory Snapshots

✓ Storage Metadata

✓ Storage State

✓ Cache Synchronization State

✓ Storage Events

MemoryStorage egalik qilmaydi.

✗ Live Tick

✗ Current Price Logic

✗ Tick Validation

✗ Candle Generation

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

MemoryStorage quyidagi holatlarda bo'lishi mumkin.

• Initializing

• Ready

• Reading

• Writing

• Persisting

• Synchronizing

• Recovering

• Stopping

• Failed

---

# Error Contract

MemoryStorage quyidagi xatolarni qaytarishi mumkin.

• StorageWriteFailed

• StorageReadFailed

• IntegrityCheckFailed

• SnapshotCreationFailed

• SnapshotRestoreFailed

• CacheSynchronizationFailed

• InvalidMemoryState

• VersionMismatch

• StorageUnavailable

• UnknownStorageError

Har qanday xato Event Bus orqali e'lon qilinadi va Recovery Engine tomonidan boshqariladi.

---

# Runtime Contract

1. MemoryStorage Market Memory Layer uchun yagona Canonical Persistent Storage hisoblanadi.

2. MemoryStorage faqat MemoryWriter orqali yozuv qabul qiladi.

3. Har bir yozuv Data Integrity tekshiruvidan o'tishi shart.

4. Memory Version har bir muvaffaqiyatli yozuvdan keyin yangilanadi.

5. Snapshot faqat muvaffaqiyatli saqlashdan keyin yaratiladi.

6. Cache har doim Storage bilan sinxron bo'lishi shart.

7. MemoryReader yagona o'qish interfeysi hisoblanadi.

8. GoldBot Core MemoryStorage bilan bevosita ishlamaydi.

9. Recovery Snapshot orqali amalga oshiriladi.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Architecture Rules

MemoryStorage:

✓ Market Memory saqlaydi.

✓ Runtime State saqlaydi.

✓ Snapshot yaratadi.

✓ Version boshqaradi.

✓ Cache bilan sinxronlashadi.

✓ Recovery uchun ma'lumot tayyorlaydi.

✓ Storage Event yaratadi.

MemoryStorage:

✗ Tick yaratmaydi.

✗ Current Price yaratmaydi.

✗ Tick Validation bajarmaydi.

✗ Candle yaratmaydi.

✗ Market Analysis bajarmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• MemoryStorage → LiveProviders import

• MemoryStorage → PriceStreamService import

• MemoryStorage → StreamValidator import

• MemoryStorage → CandleBuilder import

• MemoryStorage → Context Layer import

• MemoryStorage → Strategy Layer import

• MemoryStorage → Decision Layer import

• MemoryStorage → AI Layer import

• MemoryStorage → Business Layer import

• Tick Validation bajarish

• Candle yaratish

• Current Price hisoblash

• MemoryWriter'dan tashqari yozuv qabul qilish

• Circular Dependency

---

# Acceptance Criteria

MemoryStorage to'g'ri ishlaydi agar:

✓ Validated Market Data muvaffaqiyatli saqlansa.

✓ Runtime Memory doimo mavjud bo'lsa.

✓ Memory Version izchil boshqarilsa.

✓ Snapshot yaratish ishlasa.

✓ Recovery Snapshot orqali tiklansa.

✓ Cache va Storage sinxron bo'lsa.

✓ MemoryReader orqali o'qish ishlasa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

MemoryStorage Contract Market Memory Layer ichidagi Persistent Storage komponentining rasmiy arxitektura shartnomasi hisoblanadi.

MemoryStorage Validated Market Data, Runtime Memory va Snapshot ma'lumotlarini saqlovchi yagona Canonical Storage modulidir.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
