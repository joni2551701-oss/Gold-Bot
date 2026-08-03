# Audit Log Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AuditLog modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AuditLog quyidagilar uchun javobgar.
✓ Har bir Owner/Admin harakatini yozib boradi
✓ Actor, Action, Timestamp va Detail maydonlarini saqlaydi
✓ Audit tarixini so'rov bo'yicha qaytaradi
✓ Yozuvlarni faqat qo'shadi (append-only)
AuditLog bajarmaydi.
✗ Trade Journal (JournalRepository vazifasi)
✗ Business Logic
✗ Authentication (13_Platform_Layer/Authentication vazifasi)
✗ Authorization
✗ Cache Management
✗ Backup Management
---
# Module Boundary
```text
DatabaseManager
↓
AuditLog
↓
Database Storage
```
---
# Input Contract
• Audit Entry (Actor, Action, Timestamp, Detail)
• Audit Query Request
---
# Output Contract
• Audit Record
• Audit History
• Query Result
• Repository Metadata
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ TradeRepository
✗ UserRepository
✗ MarketRepository
✗ JournalRepository
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. AuditLog append-only hisoblanadi — yozuv hech qachon o'zgartirilmaydi va o'chirilmaydi.
2. Har bir yozuvda Actor, Action va Timestamp majburiy.
3. AuditLog Trade Journal bilan aralashtirilmaydi — ular alohida modullar.
4. AuditLog maxfiy qiymatlarni (API Key, Token, Password) hech qachon yozmaydi.
5. AuditLog Business Logic bajarmaydi — faqat yozadi va o'qiydi.
6. AuditLog foydalanuvchini autentifikatsiya yoki avtorizatsiya qilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Audit Entry qabul qilinadi.
✓ Yozuv append-only tarzda saqlanadi.
✓ Audit History so'rov bo'yicha qaytariladi.
✓ Maxfiy qiymat yozilmaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AuditLog Contract AuditLog GoldBot'dagi barcha Owner/Admin harakatlari va Critical Event'lar uchun Canonical append-only Audit Trail repository moduli hisoblanadi.
