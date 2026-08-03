# Market Memory Layer Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Market Memory Layer ichidagi barcha modullar va ularning o'zaro bog'lanishini tavsiflaydi.

---

# Layer Architecture

```text
Market Memory Layer
         │
         ▼
MarketMemoryService
         │
 ┌───────┼────────┐
 ▼       ▼        ▼
MemoryWriter
MemoryStorage
MemoryCache
MemoryLifecycle
MemoryReader
         │
         ▼
GoldBot Core
```

---

# Layer Modules

## MarketMemoryService

Layer Orchestrator.

---

## MemoryWriter

Memory yozadi.

---

## MemoryStorage

Persistent Storage.

---

## MemoryCache

Runtime Cache.

---

## MemoryLifecycle

Lifecycle Manager.

---

## MemoryReader

Read Interface.

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

# Ownership

Layer egalik qiladi.

✓ Runtime Memory

✓ Storage

✓ Cache

✓ Lifecycle

✓ Read/Write Interfaces

---

# Rules

1. MarketMemoryService yagona Orchestrator.

2. Storage yagona Data Source.

3. Cache faqat Runtime.

4. Reader yagona Read Interface.

5. Writer yagona Write Interface.

6. Circular Dependency taqiqlanadi.

---

# Summary

Market Memory Layer barcha Runtime Market Memory komponentlarini boshqaruvchi Canonical Layer hisoblanadi.
