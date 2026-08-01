# MemoryStorage Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryStorage modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

MemoryStorage Market Memory Layer ichidagi yagona Canonical Persistent Storage komponenti hisoblanadi.

Bu implementatsiya emas.

Bu MemoryStorage modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                Live Data Layer
                       │
                       ▼
                 MemoryWriter
                       │
                       ▼
                 MemoryStorage
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 MemoryReader    MemoryCache    Recovery Engine
                       │
                       ▼
                 GoldBot Core
```

---

# Module Architecture

```text
                  MemoryStorage
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 Storage Manager   Version Manager   State Manager
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
                Integrity Validator
                         │
                         ▼
                  Snapshot Manager
                         │
                         ▼
                 Persistence Manager
                         │
                         ▼
                 Cache Synchronizer
                         │
                         ▼
                   Event Publisher
```

---

# Internal Components

## Storage Manager

Memory yozish va saqlashni boshqaradi.

Mas'ul:

- Write Memory

- Read Memory

- Update Memory

- Delete Memory

---

## Version Manager

Memory versiyalarini boshqaradi.

Mas'ul:

- Version Increment

- Version Tracking

- Snapshot Version

---

## State Manager

MemoryStorage holatini boshqaradi.

Holatlar:

- Idle

- Initializing

- Ready

- Writing

- Reading

- Recovering

- Failed

---

## Integrity Validator

Saqlanayotgan ma'lumotlarni tekshiradi.

Tekshiradi:

- Data Integrity

- Timestamp

- Version

- Structure

---

## Snapshot Manager

Runtime Snapshot yaratadi.

Mas'ul:

- Create Snapshot

- Load Snapshot

- Restore Snapshot

---

## Persistence Manager

Doimiy saqlashni boshqaradi.

Mas'ul:

- Persist Memory

- Flush Memory

- Commit Changes

---

## Cache Synchronizer

Storage va Cache sinxronligini saqlaydi.

Mas'ul:

- Cache Update

- Cache Refresh

- Cache Consistency

---

## Event Publisher

Memory hodisalarini yaratadi.

Masalan:

- Memory Updated

- Snapshot Created

- Recovery Completed

- Storage Failed

---

# Dependency Map

```text
Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryCache

↓

MemoryReader

↓

GoldBot Core
```

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

✗ StreamValidator

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

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Input

MemoryStorage qabul qiladi:

• Validated Candle

• Current Price

• Runtime Snapshot

• Memory Update Request

• Recovery Request

---

# Output

MemoryStorage yaratadi:

• Stored Memory

• Memory Snapshot

• Runtime State

• Storage Events

• Recovery Snapshot

---

# Ownership

MemoryStorage egalik qiladi.

✓ Stored Market Data

✓ Runtime Memory

✓ Memory Versions

✓ Storage State

✓ Snapshots

✓ Persistence State

✓ Storage Metadata

MemoryStorage egalik qilmaydi.

✗ Live Tick

✗ Current Price Calculation

✗ Tick Validation

✗ Candle Generation

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. MemoryStorage yagona Canonical Storage komponentidir.

2. Har bir yozuv Integrity Validator orqali o'tishi shart.

3. Snapshot faqat muvaffaqiyatli yozuvdan keyin yaratiladi.

4. Storage va Cache doimo sinxron bo'lishi kerak.

5. MemoryReader yagona o'qish interfeysi hisoblanadi.

6. MemoryWriter yagona yozish interfeysi hisoblanadi.

7. GoldBot Core Storage bilan bevosita ishlamaydi.

8. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

MemoryStorage Module Map Market Memory Layer ichidagi Persistent Storage komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

Integrity Validator

↓

Persistence Manager

↓

Cache Synchronizer

↓

Snapshot Manager

↓

MemoryReader

↓

GoldBot Core

MemoryStorage Market Memory Layer ichidagi yagona Canonical Persistent Storage moduli hisoblanadi.
