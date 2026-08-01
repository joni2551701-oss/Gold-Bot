# MarketMemoryService Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat MarketMemoryService modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

Bu implementatsiya emas.

Bu MarketMemoryService modulining Canonical Runtime Blueprint hisoblanadi.

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

Initialize Modules

↓

Verify Memory State

↓

Ready
```

---

# Runtime Sequence

```text
Memory Update Request

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

MarketMemoryService

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
Shutdown Request

↓

MarketMemoryService

↓

Stop Modules

↓

Flush Runtime

↓

Shutdown Complete
```

---

# Error Sequence

```text
Module Failure

↓

MarketMemoryService

↓

Create Error Event

↓

Recovery

↓

Recovered

or

Failed
```

---

# Runtime Rules

1. MarketMemoryService barcha Memory modullarini boshqaradi.

2. Runtime Lifecycle markazlashgan holda boshqariladi.

3. Recovery avtomatik ishlashi mumkin.

4. Shutdown tartibli amalga oshiriladi.

5. Circular Runtime Sequence taqiqlanadi.

---

# State Flow

```text
Idle

↓

Initializing

↓

Ready

↓

Running

↓

Recovering

↓

Stopping

↓

Stopped

or

Failed
```

---

# Summary

MarketMemoryService Runtime Lifecycle boshqaruvining Canonical Sequence'ni belgilaydi.
