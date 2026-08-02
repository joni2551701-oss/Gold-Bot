# Database Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DatabaseService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DatabaseService quyidagilar uchun javobgar.
✓ Public Entry Point (Trade Monitoring Layer'dan Database Layer'ga kirish)
✓ Public Exit Point (Database Layer'dan Platform Layer'ga chiqish)
✓ Request Validation
✓ Response Serialization
✓ Session Management
✓ API Boundary Enforcement
DatabaseService bajarmaydi.
✗ Database Connection
✗ Repository Logic (CRUD)
✗ Cache Management
✗ Backup Management
✗ Business Logic
---
# Module Boundary
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
# Input Contract
Kirish tomonida (Trade Monitoring Layer'dan):
• Database Request
• Repository Request
• Query Request
• Session Metadata

Chiqish tomonida (BackupManager'dan):
• Database Records
---
# Output Contract
Kirish tomonida (DatabaseManager'ga):
• Validated Database Request

Chiqish tomonida (Platform Layer'ga):
• Database Response
• Query Result
• Standard Response
• Service Metadata
---
# Allowed Dependencies
✓ DatabaseManager
✓ BackupManager
---
# Forbidden Dependencies
✗ TradeRepository (to'g'ridan-to'g'ri)
✗ UserRepository (to'g'ridan-to'g'ri)
✗ MarketRepository (to'g'ridan-to'g'ri)
✗ JournalRepository (to'g'ridan-to'g'ri)
✗ CacheManager (to'g'ridan-to'g'ri)
✗ Platform Layer'dan boshqa tashqi Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Database Layer'ga barcha kirish va chiqishlar DatabaseService orqali amalga oshirilishi shart (Boundary Gateway).
2. Har bir kirish Request Validation'dan o'tishi shart.
3. DatabaseService Business Logic bajarmaydi — faqat Entry/Exit Boundary vazifasini bajaradi.
4. Response standart formatda qaytarilishi shart.
5. BackupManager Layer tashqarisiga chiqmaydi — faqat DatabaseService orqali chiqadi.
6. Session holati boshqarilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Trade Monitoring Layer'dan Request qabul qilinadi.
✓ Validation bajariladi.
✓ DatabaseManager'ga uzatiladi.
✓ BackupManager'dan Database Records qabul qilinadi.
✓ Response standartlashtiriladi.
✓ Platform Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DatabaseService Contract GoldBot Database Layer uchun ikki tomonlama (bidirectional) Boundary Gateway sifatida ishlashini — Trade Monitoring Layer'dan kirish va Platform Layer'ga chiqishni — belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
