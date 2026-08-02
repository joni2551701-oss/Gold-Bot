# Database Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DatabaseService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DatabaseService quyidagilar uchun javobgar.
✓ Database Request Management
✓ Request Validation
✓ Database Layer Gateway
✓ Session Management
✓ Response Formatting
✓ Service Monitoring
DatabaseService bajarmaydi.
✗ Database Connection
✗ Repository Logic
✗ Cache Management
✗ Backup Management
✗ Business Logic
---
# Module Boundary
```text
Trade Monitoring Layer
↓
DatabaseService
↓
DatabaseManager
↓
Repositories
```
---
# Input Contract
• Database Request
• Repository Request
• Query Request
• Session Metadata
---
# Output Contract
• Database Response
• Query Result
• Standard Response
• Service Metadata
---
# Allowed Dependencies
✓ DatabaseManager
✓ TradeRepository
✓ UserRepository
✓ MarketRepository
✓ JournalRepository
✓ CacheManager
✓ BackupManager
---
# Forbidden Dependencies
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Database Layer'ga barcha kirishlar DatabaseService orqali amalga oshirilishi shart.
2. Har bir Request Validation'dan o'tishi shart.
3. DatabaseService Business Logic bajarmaydi.
4. Response standart formatda qaytarilishi shart.
5. Repository natijalari o'zgartirilmasdan qaytarilishi shart.
6. Session holati boshqarilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Validation bajariladi.
✓ DatabaseManager ishga tushiriladi.
✓ Repository natijasi olinadi.
✓ Response standartlashtiriladi.
✓ Platform Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DatabaseService Contract GoldBot Database Layer uchun yagona Public Interface va Service Gateway sifatida ishlashni, barcha Database so'rovlarini boshqarishni, Repository natijalarini standart formatga o'tkazishni va Platform Layer'ga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
