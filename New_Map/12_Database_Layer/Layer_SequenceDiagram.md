# Database Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Database Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Trade Monitoring Layer
↓
DatabaseService (Entry)
↓
DatabaseManager
        │
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
TradeRepository  UserRepository  MarketRepository  JournalRepository
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
                       ▼
                 CacheManager
↓
BackupManager
↓
DatabaseService (Exit)
↓
Platform Layer
```
---
# Runtime Rules
1. Database Request mavjud bo'lishi shart.
2. DatabaseService Database Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
3. Request Validation bajarilishi shart.
4. Database Connection mavjud bo'lishi shart.
5. TradeRepository, UserRepository, MarketRepository, JournalRepository bir-birining natijasiga bog'liq emas va parallel ishga tushiriladi.
6. Cache sinxronlashtirilishi shart.
7. Backup kerak bo'lsa yaratilishi shart, lekin Layer tashqarisiga chiqmaydi.
8. Standard Response DatabaseService orqali qaytarilishi shart.
---
# State Flow
```text
Idle
↓
Receiving Request
↓
Connecting
↓
Processing
↓
Caching
↓
Backup
↓
Completed
```
---
# Summary
Trade Monitoring Layer
↓
Database Layer
↓
Platform Layer
