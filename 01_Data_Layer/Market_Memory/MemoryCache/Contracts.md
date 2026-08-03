# MemoryCache Contracts

Status: CANONICAL

---

# Purpose

MemoryCache modulining rasmiy Architecture Contract hujjati.

---

# Module Responsibility

MemoryCache quyidagilar uchun javobgar.

✓ Runtime Cache

✓ Fast Read Access

✓ Cache Synchronization

✓ Cache Recovery

✓ Cache Consistency

MemoryCache bajarmaydi.

✗ Persistent Storage

✗ Memory Writing

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Module Boundary

MemoryStorage

↓

MemoryCache

↓

MemoryReader

---

# Input Contract

• Storage Update

• Runtime Snapshot

• Cache Refresh

• Recovery Request

---

# Output Contract

• Cached Snapshot

• Cached Candle

• Cached Current Price

• Cache Status

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

# State Contract

• Initializing

• Loading

• Ready

• Updating

• Refreshing

• Failed

---

# Runtime Contract

1. MemoryCache Persistent Storage emas.

2. MemoryReader avval Cache'dan o'qiydi.

3. Cache Miss bo'lsa Storage ishlatiladi.

4. Cache doimo Storage bilan sinxron bo'ladi.

5. Runtime Recovery Cache'ni qayta tiklaydi.

6. Cache ma'lumotni o'zgartirmaydi.

7. Circular Dependency taqiqlanadi.

---

# Architecture Rules

MemoryCache:

✓ Runtime Cache yaratadi.

✓ Fast Read ta'minlaydi.

✓ Storage bilan sinxronlashadi.

MemoryCache:

✗ Memory yozmaydi.

✗ Tick Validation bajarmaydi.

✗ Candle yaratmaydi.

✗ Trading Logic bajarmaydi.

✗ AI ishlatmaydi.

---

# Acceptance Criteria

✓ Cache avtomatik yangilanadi.

✓ Cache Hit tezkor javob beradi.

✓ Cache Miss Storage orqali tiklanadi.

✓ Cache Recovery ishlaydi.

✓ Cache Consistency saqlanadi.

---

# Summary

MemoryCache Contract Market Memory Layer ichidagi Canonical Runtime Cache komponentining rasmiy arxitektura shartnomasi hisoblanadi.

MemoryCache GoldBot Runtime davomida yuqori tezlikdagi Memory Access ta'minlovchi yagona Cache moduli hisoblanadi.
