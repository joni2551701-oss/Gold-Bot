# Market Memory Layer Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Market Memory Layer Runtime Sequence'ni tavsiflaydi.

---

# Complete Runtime Sequence

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

# Startup Sequence

```text
System Start

↓

MarketMemoryService

↓

Initialize Storage

↓

Initialize Cache

↓

Initialize Reader

↓

Ready
```

---

# Runtime Sequence

```text
Validated Candle

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

# Recovery Sequence

```text
Failure

↓

MemoryLifecycle

↓

Restore Snapshot

↓

Restore Cache

↓

Ready
```

---

# Shutdown Sequence

```text
Shutdown

↓

Flush Memory

↓

Release Resources

↓

Stopped
```

---

# Runtime Rules

1. Runtime MarketMemoryService tomonidan boshqariladi.

2. Har bir Write Cache bilan sinxronlashadi.

3. Reader faqat Cache yoki Storage'dan o'qiydi.

4. Recovery Snapshot asosida bajariladi.

5. Circular Runtime taqiqlanadi.

---

# Summary

Canonical Runtime Sequence:

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
