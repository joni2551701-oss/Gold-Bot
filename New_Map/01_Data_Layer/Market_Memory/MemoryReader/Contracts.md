# MemoryReader Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryReader modulining rasmiy Architecture Contract hujjati hisoblanadi.

MemoryReader Market Memory Layer ichidagi yagona Canonical Read komponentidir.

Market Memory'dan barcha o'qish amallari aynan ushbu modul orqali bajariladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

MemoryReader quyidagi vazifalar uchun javobgar.

✓ Runtime Memory Reading

✓ Current Price Reading

✓ Candle Reading

✓ Snapshot Reading

✓ Memory Version Reading

✓ Read Consistency

✓ Read Response Generation

✓ Read Event Publishing

MemoryReader quyidagi vazifalarni bajarmaydi.

✗ Memory Writing

✗ Tick Validation

✗ Candle Generation

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Module Boundary

GoldBot Core

↓

MemoryReader

↓

MemoryStorage

↓

Boundary End

---

# Input Contract

MemoryReader qabul qiladi.

• Read Request

• Snapshot Request

• Runtime Request

• Version Request

---

# Output Contract

MemoryReader yaratadi.

• Runtime Snapshot

• Current Candle

• Current Price

• Memory Version

• Read Response

---

# Read Contract

MemoryReader quyidagilarni o'qishi mumkin.

✓ MemoryStorage

✓ Configuration Layer

✓ Storage Metadata

---

# Write Contract

MemoryReader quyidagilarga yozishi mumkin.

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

MemoryReader quyidagilar bilan ishlashi mumkin.

✓ MemoryStorage

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

MemoryReader quyidagilar bilan ishlashi mumkin emas.

✗ MemoryWriter

✗ Live Data Layer

✗ Context Layer

✗ Strategy Layer

✗ Decision Layer

✗ Risk Layer

✗ AI Layer

✗ Platform Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Ownership

MemoryReader egalik qiladi.

✓ Read Requests

✓ Read Responses

✓ Snapshot Responses

✓ Read State

MemoryReader egalik qilmaydi.

✗ Stored Memory

✗ Memory Updates

✗ Runtime Memory

✗ Trading Logic

---

# State Contract

MemoryReader quyidagi holatlarda bo'lishi mumkin.

• Idle

• Waiting Request

• Reading

• Returning

• Failed

---

# Error Contract

MemoryReader quyidagi xatolarni qaytarishi mumkin.

• ReadFailed

• SnapshotNotFound

• VersionMismatch

• StorageUnavailable

• InvalidRequest

• UnknownReadError

Har qanday xato Event Bus orqali e'lon qilinadi.

---

# Runtime Contract

1. MemoryReader yagona Canonical Read Interface hisoblanadi.

2. Har bir Read Request MemoryStorage orqali bajariladi.

3. MemoryReader Memory'ni o'zgartirmaydi.

4. Har bir Read Response izchil bo'lishi shart.

5. GoldBot Core MemoryStorage bilan bevosita ishlamaydi.

6. Write Operation bajarilishi taqiqlanadi.

7. Circular Dependency qat'iyan taqiqlanadi.

---

# Architecture Rules

MemoryReader:

✓ Memory o'qiydi.

✓ Snapshot qaytaradi.

✓ Version tekshiradi.

✓ Read Response yaratadi.

MemoryReader:

✗ Memory yozmaydi.

✗ Candle yaratmaydi.

✗ Tick Validation bajarmaydi.

✗ Trading Logic bajarmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• MemoryReader → MemoryWriter import

• MemoryReader → Live Data Layer import

• MemoryReader → Strategy Layer import

• MemoryReader → Decision Layer import

• MemoryReader → AI Layer import

• MemoryReader orqali Memory yozish

• MemoryStorage'ni chetlab o'tish

• Circular Dependency

---

# Acceptance Criteria

MemoryReader to'g'ri ishlaydi agar:

✓ Read Request muvaffaqiyatli bajarilsa.

✓ Snapshot to'g'ri qaytarilsa.

✓ Current Candle o'qilsa.

✓ Current Price o'qilsa.

✓ Memory Version tekshirilsa.

✓ Read Consistency saqlansa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

MemoryReader Contract Market Memory Layer ichidagi Canonical Read komponentining rasmiy arxitektura shartnomasi hisoblanadi.

MemoryReader Market Memory'dan ma'lumot o'qish uchun yagona ruxsat etilgan modul hisoblanadi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
