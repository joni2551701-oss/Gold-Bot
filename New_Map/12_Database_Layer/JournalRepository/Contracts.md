# Journal Repository Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat JournalRepository modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
JournalRepository quyidagilar uchun javobgar.
✓ AI Journal Storage
✓ Decision History Storage
✓ Explainability Storage
✓ System Event Storage
✓ Journal Query Processing
JournalRepository bajarmaydi.
✗ AI Analysis
✗ Trading Decision
✗ Trade Storage
✗ User Storage
✗ Cache Management
✗ Backup Management
---
# Module Boundary
```text
DatabaseManager
↓
JournalRepository
↓
Database Storage
```
---
# Input Contract
• AI Journal Record
• Decision Record
• System Event
• Query Request
---
# Output Contract
• Journal Result
• Decision History
• Query Result
• Repository Metadata
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ AuditLog
✗ TradeRepository
✗ UserRepository
✗ MarketRepository
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Har bir Journal Record vaqt belgisi bilan saqlanishi shart.
2. Decision History immutable bo'lishi shart.
3. Explainability ma'lumotlari Decision bilan bog'lanishi shart.
4. Query natijalari standart formatda qaytarilishi shart.
5. JournalRepository Business Logic bajarmaydi.
6. JournalRepository Audit Trail saqlamaydi — bu AuditLog modulining vazifasi (Trade Journal va Audit Log aralashtirilmaydi).
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ AI Journal saqlanadi.
✓ Decision History saqlanadi.
✓ System Event saqlanadi.
✓ Journal Query bajariladi.
✓ Repository Metadata yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
JournalRepository Contract GoldBot Database Layer ichidagi AI Journal, Decision History, Explainability va System Event ma'lumotlarini ishonchli saqlash, qidirish va boshqarishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
