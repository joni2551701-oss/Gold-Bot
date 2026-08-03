# Database Service
Status: CANONICAL
---
# Purpose
DatabaseService GoldBot Database Layer uchun Canonical Boundary Gateway hisoblanadi.
Uning asosiy vazifasi Database Layer'ning yagona Public Entry Point va Public Exit Point bo'lishidir — Trade Monitoring Layer'dan kelgan so'rovlarni DatabaseManager'ga kiritish va BackupManager'dan qaytgan yakuniy natijani Platform Layer'ga chiqarish.
DatabaseService Database Query yozmaydi.
DatabaseService Repository Logic bajarmaydi.
DatabaseService faqat Entry/Exit Boundary, Validation va Serialization vazifalarini bajaradi.
---
# Objective
DatabaseService quyidagi vazifalarni bajaradi.
• Public Entry Point
• Public Exit Point
• Request Validation
• Response Serialization
• Session Management
• API Boundary Enforcement
---
# Layer Position
```text
Trade Monitoring Layer
↓
DatabaseService (Entry)
↓
DatabaseManager
↓
TradeRepository / UserRepository / MarketRepository / JournalRepository
↓
CacheManager
↓
BackupManager
↓
DatabaseService (Exit)
↓
Platform Layer
```
---
# Responsibilities
DatabaseService
✓ Trade Monitoring Layer'dan Database Request qabul qiladi (Entry)
✓ Request formatini tekshiradi
✓ DatabaseManager'ga uzatadi
✓ BackupManager'dan yakuniy natijani qabul qiladi
✓ Standard Response yaratadi
✓ Platform Layer'ga uzatadi (Exit)
---
# Not Responsible
DatabaseService
✗ Trading Decision
✗ Database Connection
✗ Repository Logic
✗ Cache Management
✗ Backup Management
✗ Business Logic
---
# Input
DatabaseService qabul qiladi.
• Database Request (Trade Monitoring Layer'dan)
• Database Records (BackupManager'dan)
• Session Metadata
---
# Output
DatabaseService yaratadi.
• Validated Database Request (DatabaseManager'ga)
• Database Response (Platform Layer'ga)
• Query Result
• Service Metadata
---
# Workflow
```text
Receive Request (Trade Monitoring Layer)
↓
Validate Request
↓
Forward To DatabaseManager
↓
Receive Database Records (BackupManager)
↓
Standardize Response
↓
Return Response (Platform Layer)
```
---
# Golden Rules
1. DatabaseService Database Layer'ning yagona Entry Point va yagona Exit Point hisoblanadi.
2. Business Logic DatabaseService ichida bajarilmaydi.
3. Response yagona formatga o'tkaziladi.
4. Database Layer tashqarisiga faqat DatabaseService orqali kiriladi va chiqiladi.
5. BackupManager Layer tashqarisiga chiqmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DatabaseService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DatabaseService GoldBot Database Layer uchun ikki tomonlama (bidirectional) Boundary Gateway hisoblanadi — Trade Monitoring Layer'dan Database Layer'ga kirish va Database Layer'dan Platform Layer'ga chiqish uchun yagona nuqta.
