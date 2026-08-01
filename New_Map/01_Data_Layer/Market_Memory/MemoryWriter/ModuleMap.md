# MemoryWriter Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryWriter modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

MemoryWriter Market Memory Layer ichidagi yagona Canonical Write komponenti hisoblanadi.

Bu implementatsiya emas.

Bu MemoryWriter modulining Canonical Architecture Blueprint hisoblanadi.

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
                   ▼
             MemoryReader

                   │
                   ▼
              GoldBot Core
```

---

# Module Architecture

```text
                MemoryWriter
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Request Manager Write Manager State Manager
      │               │               │
      └───────────────┼───────────────┘
                      ▼
             Request Validator
                      │
                      ▼
             Version Manager
                      │
                      ▼
             Storage Dispatcher
                      │
                      ▼
              Event Publisher
```

---

# Internal Components

## Request Manager

Write Request'larni qabul qiladi.

Mas'ul:

- Candle Request

- Price Request

- Snapshot Request

---

## Write Manager

Yozish jarayonini boshqaradi.

Mas'ul:

- Write Memory

- Update Memory

- Commit Request

---

## State Manager

MemoryWriter holatini boshqaradi.

Holatlar:

- Idle

- Validating

- Writing

- Waiting

- Failed

---

## Request Validator

Write Request'ni tekshiradi.

Tekshiradi:

- Structure

- Timestamp

- Version

- Required Fields

---

## Version Manager

Version yangilanishini boshqaradi.

Mas'ul:

- Increment Version

- Verify Version

---

## Storage Dispatcher

MemoryStorage'ga yozuv yuboradi.

Mas'ul:

- Dispatch Write

- Dispatch Snapshot

- Dispatch Update

---

## Event Publisher

Write hodisalarini yaratadi.

Masalan:

- Write Completed

- Write Failed

- Version Updated

---

# Dependency Map

```text
Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryReader

↓

GoldBot Core
```

---

# Allowed Dependencies

MemoryWriter quyidagilar bilan ishlashi mumkin.

✓ Live Data Layer

✓ MemoryStorage

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

MemoryWriter quyidagilar bilan ishlashi mumkin emas.

✗ MemoryReader

✗ Context Layer

✗ Strategy Layer

✗ Decision Layer

✗ Risk Layer

✗ AI Layer

✗ Platform Layer

✗ Business Layer

---

# Input

MemoryWriter qabul qiladi.

• Validated Candle

• Current Price

• Runtime Update

• Snapshot Request

---

# Output

MemoryWriter yaratadi.

• Storage Write Request

• Storage Update

• Version Update

• Write Events

---

# Ownership

MemoryWriter egalik qiladi.

✓ Write Requests

✓ Write Queue

✓ Write State

✓ Version Requests

MemoryWriter egalik qilmaydi.

✗ Stored Memory

✗ Read Requests

✗ Market Analysis

✗ Trading Logic

---

# Module Rules

1. MemoryWriter yagona Canonical Write Interface hisoblanadi.

2. MemoryWriter faqat Live Data Layer'dan yozuv qabul qiladi.

3. MemoryStorage yagona Storage hisoblanadi.

4. Har bir Write Request tekshiriladi.

5. MemoryReader faqat yozuv tugagandan keyin o'qiydi.

6. GoldBot Core MemoryWriter bilan ishlamaydi.

7. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

MemoryWriter Module Map Market Memory Layer ichidagi Write komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryReader

↓

GoldBot Core

MemoryWriter Market Memory Layer ichidagi yagona Canonical Write moduli hisoblanadi.
