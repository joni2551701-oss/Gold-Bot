# MemoryReader Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryReader modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

MemoryReader Market Memory Layer ichidagi yagona Canonical Read komponenti hisoblanadi.

Bu implementatsiya emas.

Bu MemoryReader modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
          Market Memory Layer

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
               MemoryReader
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Request Manager Read Manager State Manager
      │              │              │
      └──────────────┼──────────────┘
                     ▼
            Snapshot Loader
                     │
                     ▼
            Version Checker
                     │
                     ▼
            Response Builder
                     │
                     ▼
            Event Publisher
```

---

# Internal Components

## Request Manager

Read Request'larni qabul qiladi.

Mas'ul:

- Read Request

- Snapshot Request

- Version Request

---

## Read Manager

Memory o'qishni boshqaradi.

Mas'ul:

- Load Memory

- Load Candle

- Load Price

---

## State Manager

MemoryReader holatini boshqaradi.

Holatlar:

- Idle

- Reading

- Loading

- Returning

- Failed

---

## Snapshot Loader

Snapshot'larni yuklaydi.

Mas'ul:

- Current Snapshot

- Recovery Snapshot

- Runtime Snapshot

---

## Version Checker

Memory Version tekshiradi.

Mas'ul:

- Version Match

- Version Validation

---

## Response Builder

Natijani tayyorlaydi.

Mas'ul:

- Read Response

- Snapshot Response

---

## Event Publisher

Read hodisalarini yaratadi.

Masalan:

- Read Completed

- Read Failed

- Snapshot Loaded

---

# Dependency Map

```text
GoldBot Core

↓

MemoryReader

↓

MemoryStorage
```

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

# Input

MemoryReader qabul qiladi.

• Read Request

• Snapshot Request

• Runtime Request

• Version Request

---

# Output

MemoryReader yaratadi.

• Runtime Snapshot

• Current Candle

• Current Price

• Memory Version

• Read Response

---

# Ownership

MemoryReader egalik qiladi.

✓ Read Requests

✓ Read Responses

✓ Snapshot Responses

✓ Read State

MemoryReader egalik qilmaydi.

✗ Memory Storage

✗ Memory Updates

✗ Runtime Data

✗ Candle Generation

✗ Trading Logic

---

# Module Rules

1. MemoryReader yagona Read Interface hisoblanadi.

2. MemoryStorage yagona Data Source hisoblanadi.

3. Read Operation ma'lumotni o'zgartirmaydi.

4. Har bir Read Request Version tekshiruvini bajaradi.

5. GoldBot Core faqat MemoryReader bilan ishlaydi.

6. Write Operation qat'iyan taqiqlanadi.

7. Circular Dependency taqiqlanadi.

---

# Summary

MemoryReader Module Map Market Memory Layer ichidagi Read komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

GoldBot Core

↓

MemoryReader

↓

MemoryStorage

MemoryReader Market Memory Layer ichidagi yagona Canonical Read moduli hisoblanadi.
