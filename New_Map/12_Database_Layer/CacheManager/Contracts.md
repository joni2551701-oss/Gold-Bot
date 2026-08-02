# Cache Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat CacheManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
CacheManager quyidagilar uchun javobgar.
✓ Cache Storage
✓ Cache Retrieval
✓ Cache Update
✓ Cache Invalidation
✓ Cache Synchronization
✓ Cache Statistics Generation
CacheManager bajarmaydi.
✗ Persistent Storage
✗ Trade Storage
✗ User Storage
✗ Market Storage
✗ Journal Storage
✗ Business Logic
---
# Module Boundary
```text
Repositories
↓
CacheManager
↓
BackupManager
```
---
# Input Contract
• Cache Request
• Cache Key
• Cache Value
• Cache Policy
---
# Output Contract
• Cache Response
• Cache Status
• Cache Statistics
• Cache Metadata
---
# Allowed Dependencies
✓ TradeRepository
✓ UserRepository
✓ MarketRepository
✓ JournalRepository
✓ BackupManager
---
# Forbidden Dependencies
✗ DatabaseManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Cache Key yagona bo'lishi shart.
2. Cache va Database sinxron bo'lishi shart.
3. Expired Cache avtomatik o'chirilishi shart.
4. Cache Miss holati standart formatda qaytarilishi shart.
5. Cache Statistics muntazam yangilanishi shart.
6. CacheManager Persistent Storage o'rnini bosmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Cache yoziladi.
✓ Cache o'qiladi.
✓ Cache yangilanadi.
✓ Cache tozalanadi.
✓ Cache Statistics yaratiladi.
✓ Cache sinxronlashtiriladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
CacheManager Contract GoldBot Database Layer ichidagi Cache Infrastructure'ni boshqarish, tezkor ma'lumotlarni saqlash, yangilash va Database bilan sinxronlashtirishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
