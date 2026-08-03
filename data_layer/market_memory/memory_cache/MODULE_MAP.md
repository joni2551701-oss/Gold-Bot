# MemoryCache Module Map

Status: CANONICAL

---

# Purpose

MemoryCache modulining ichki arxitekturasi va komponentlarini tavsiflaydi.

---

# Module Position

```text
MemoryStorage

↓

MemoryCache

↓

MemoryReader
```

---

# Module Architecture

```text
MemoryCache
      │
      ├── Cache Manager
      ├── State Manager
      ├── Cache Loader
      ├── Cache Synchronizer
      ├── Cache Validator
      ├── Cache Cleaner
      └── Event Publisher
```

---

# Internal Components

## Cache Manager

Cache'ni boshqaradi.

---

## State Manager

Cache holatini boshqaradi.

Holatlar:

- Idle

- Loading

- Ready

- Updating

- Failed

---

## Cache Loader

Storage'dan Cache'ni yuklaydi.

---

## Cache Synchronizer

Storage bilan sinxronlashadi.

---

## Cache Validator

Cache Integrity'ni tekshiradi.

---

## Cache Cleaner

Eskirgan Cache'ni tozalaydi.

---

## Event Publisher

Cache hodisalarini yaratadi.

---

# Dependency Map

```text
MemoryStorage

↓

MemoryCache

↓

MemoryReader
```

---

# Allowed Dependencies

✓ MemoryStorage

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

✗ Platform Layer

---

# Ownership

MemoryCache egalik qiladi.

✓ Runtime Cache

✓ Cache Metadata

✓ Cache Version

✓ Cache State

---

# Module Rules

1. Cache Runtime komponentidir.

2. Persistent Storage emas.

3. MemoryStorage yagona Source hisoblanadi.

4. Cache avtomatik sinxronlashadi.

5. Circular Dependency taqiqlanadi.

---

# Summary

MemoryCache Market Memory Layer ichidagi yagona Canonical Runtime Cache moduli hisoblanadi.
