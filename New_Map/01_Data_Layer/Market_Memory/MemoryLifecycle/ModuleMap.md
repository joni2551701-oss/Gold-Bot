# MemoryLifecycle Module Map

Status: CANONICAL

---

# Purpose

MemoryLifecycle modulining ichki arxitekturasi va komponentlarini tavsiflaydi.

---

# Module Position

```text
MemoryStorage

↓

MemoryCache

↓

MemoryLifecycle

↓

MemoryReader
```

---

# Module Architecture

```text
MemoryLifecycle
        │
        ├── Lifecycle Manager
        ├── Startup Manager
        ├── Runtime Manager
        ├── Recovery Manager
        ├── Restart Manager
        ├── Shutdown Manager
        ├── State Manager
        └── Event Publisher
```

---

# Internal Components

## Lifecycle Manager

Lifecycle jarayonlarini boshqaradi.

---

## Startup Manager

Boshlang'ich ishga tushirishni boshqaradi.

---

## Runtime Manager

Runtime holatini kuzatadi.

---

## Recovery Manager

Nosozlikdan tiklanishni boshqaradi.

---

## Restart Manager

Restart jarayonini boshqaradi.

---

## Shutdown Manager

Shutdown jarayonini boshqaradi.

---

## State Manager

Lifecycle holatini saqlaydi.

---

## Event Publisher

Lifecycle hodisalarini yaratadi.

---

# Dependency Map

```text
MemoryStorage

↓

MemoryCache

↓

MemoryLifecycle

↓

MemoryReader
```

---

# Allowed Dependencies

✓ MemoryStorage

✓ MemoryCache

✓ MemoryReader

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

✗ Live Data Layer

✗ Context Layer

✗ Strategy Layer

✗ Decision Layer

✗ AI Layer

---

# Ownership

MemoryLifecycle egalik qiladi.

✓ Lifecycle State

✓ Runtime State

✓ Recovery State

✓ Restart State

✓ Shutdown State

---

# Module Rules

1. Lifecycle markazlashgan holda boshqariladi.

2. Startup → Runtime → Shutdown ketma-ketligi saqlanadi.

3. Recovery mustaqil ishlaydi.

4. Circular Dependency taqiqlanadi.

---

# Summary

MemoryLifecycle Market Memory Layer ichidagi Runtime Lifecycle boshqaruvining yagona Canonical moduli hisoblanadi.
