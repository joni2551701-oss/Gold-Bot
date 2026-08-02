# Cache Manager
Status: CANONICAL
---
# Purpose
CacheManager GoldBot Database Layer ichidagi Canonical Cache Management moduli hisoblanadi.
Uning asosiy vazifasi tez-tez foydalaniladigan ma'lumotlarni vaqtinchalik xotirada (Cache) saqlash, yangilash va boshqarish orqali tizim ishlash tezligini oshirishdir.
CacheManager Business Logic bajarmaydi.
CacheManager Persistent Storage vazifasini bajarmaydi.
CacheManager faqat Cache Infrastructure bilan shug'ullanadi.
---
# Objective
CacheManager quyidagi vazifalarni bajaradi.
• Cache Storage
• Cache Retrieval
• Cache Invalidation
• Cache Synchronization
• Cache Health Monitoring
• Cache Statistics Generation
---
# Layer Position
```text
Repositories
↓
CacheManager
↓
BackupManager
```
---
# Responsibilities
CacheManager
✓ Cache yozadi
✓ Cache o'qiydi
✓ Cache yangilaydi
✓ Cache tozalaydi
✓ Cache sinxronlashtiradi
✓ Cache statistikalarini yaratadi
---
# Not Responsible
CacheManager
✗ Trade Storage
✗ User Storage
✗ Market Storage
✗ Journal Storage
✗ Backup Management
✗ Business Logic
---
# Input
CacheManager qabul qiladi.
• Cache Request
• Cache Key
• Cache Value
• Cache Policy
---
# Output
CacheManager yaratadi.
• Cache Response
• Cache Status
• Cache Statistics
• Cache Metadata
---
# Cache States
EMPTY
↓
LOADED
↓
ACTIVE
↓
EXPIRED
↓
INVALIDATED
↓
CLEARED
---
# Workflow
```text
Receive Cache Request
↓
Check Cache
↓
Read / Write Cache
↓
Synchronize
↓
Generate Statistics
↓
BackupManager
```
---
# Golden Rules
1. Cache Persistent Storage o'rnini bosa olmaydi.
2. Cache va Database sinxron bo'lishi shart.
3. Expired Cache avtomatik tozalanadi.
4. Cache Key yagona bo'lishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
CacheManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
CacheManager GoldBot Database Layer ichidagi tezkor ma'lumotlarni boshqaruvchi Canonical Cache Infrastructure moduli hisoblanadi.
