# Provider Router Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderRouter ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
RAG
↓
ProviderRouter
↓
ValidationEngine
```
---
# Module Architecture
```text
ProviderRouter
        │
        ├── Provider Selector
        ├── Routing Engine
        ├── Failover Manager
        ├── Health Monitor
        ├── Response Normalizer
        └── Provider Registry
```
---
# Internal Components
## Provider Selector
Eng mos AI Provider'ni tanlaydi.
---
## Routing Engine
So'rovni Provider'ga yuboradi.
---
## Failover Manager
Xatolik bo'lsa boshqa Provider'ga o'tadi.
---
## Health Monitor
Provider holatini kuzatadi.
---
## Response Normalizer
Barcha javoblarni yagona formatga o'tkazadi.
---
## Provider Registry
Mavjud AI Provider'lar ro'yxatini boshqaradi.
---
# Allowed Dependencies
✓ RAG
✓ ValidationEngine
---
# Forbidden Dependencies
✗ MemoryManager
✗ LearningEngine
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
ProviderRouter GoldBot AI ichidagi barcha AI Provider'larni boshqaruvchi Canonical Gateway modulidir.
