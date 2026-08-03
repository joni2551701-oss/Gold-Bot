# MemoryCache Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryCache modulining Runtime Sequence'ni tavsiflaydi.

---

# Complete Runtime Sequence

```text
MemoryStorage

↓

MemoryCache

↓

Update Cache

↓

Verify Cache

↓

MemoryReader

↓

GoldBot Core
```

---

# Cache Update Sequence

```text
Memory Updated

↓

MemoryStorage

↓

MemoryCache

↓

Refresh Cache

↓

Cache Ready
```

---

# Cache Read Sequence

```text
Read Request

↓

MemoryReader

↓

MemoryCache

↓

Cache Hit

↓

Return Data
```

---

# Cache Miss Sequence

```text
Read Request

↓

MemoryReader

↓

MemoryCache

↓

Cache Miss

↓

MemoryStorage

↓

Load Memory

↓

Update Cache

↓

Return Data
```

---

# Recovery Sequence

```text
Restart

↓

MemoryStorage

↓

Load Snapshot

↓

MemoryCache

↓

Restore Cache

↓

Ready
```

---

# Runtime Rules

1. MemoryReader har doim avval Cache'ni tekshiradi.

2. Cache Miss bo'lsa Storage ishlatiladi.

3. Cache avtomatik yangilanadi.

4. Cache Runtime davomida saqlanadi.

5. Cache Restart'dan keyin qayta tiklanadi.

---

# State Flow

```text
Idle

↓

Loading

↓

Ready

↓

Updating

↓

Serving

↓

Refreshing

↓

Ready

or

Failed
```

---

# Summary

MemoryCache Runtime ketma-ketligi:

MemoryStorage

↓

MemoryCache

↓

MemoryReader

↓

GoldBot Core
