# MarketMemoryService Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat MarketMemoryService modulining ichki arxitekturasi va komponentlarini tavsiflaydi.

---

# Module Position

```text
Live Data Layer

↓

MarketMemoryService

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryCache

↓

MemoryLifecycle

↓

MemoryReader

↓

GoldBot Core
```

---

# Module Architecture

```text
MarketMemoryService
        │
        ├── Request Manager
        ├── Module Coordinator
        ├── Runtime Manager
        ├── Recovery Manager
        ├── Lifecycle Manager
        ├── Health Monitor
        ├── State Manager
        └── Event Publisher
```

---

# Internal Components

## Request Manager

Runtime so'rovlarini qabul qiladi.

---

## Module Coordinator

Memory modullarini boshqaradi.

---

## Runtime Manager

Runtime jarayonlarini nazorat qiladi.

---

## Recovery Manager

Recovery jarayonlarini boshqaradi.

---

## Lifecycle Manager

Startup va Shutdown boshqaradi.

---

## Health Monitor

Memory Layer sog'ligini kuzatadi.

---

## State Manager

Runtime holatini boshqaradi.

---

## Event Publisher

Runtime hodisalarini yaratadi.

---

# Dependency Map

```text
Live Data Layer

↓

MarketMemoryService

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryCache

↓

MemoryLifecycle

↓

MemoryReader

↓

GoldBot Core
```

---

# Allowed Dependencies

✓ MemoryWriter

✓ MemoryStorage

✓ MemoryCache

✓ MemoryLifecycle

✓ MemoryReader

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

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

MarketMemoryService egalik qiladi.

✓ Runtime Lifecycle

✓ Memory Coordination

✓ Runtime State

✓ Recovery State

✓ Health State

---

# Module Rules

1. MarketMemoryService yagona Canonical Orchestrator hisoblanadi.

2. Memory modullari mustaqil emas.

3. Runtime markazlashgan boshqariladi.

4. Circular Dependency taqiqlanadi.

---

# Summary

MarketMemoryService Market Memory Layer ichidagi barcha Memory modullarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
