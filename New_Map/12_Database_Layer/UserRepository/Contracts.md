# User Repository Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat UserRepository modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
UserRepository quyidagilar uchun javobgar.
✓ User Storage
✓ Profile Storage
✓ User Settings Storage
✓ Subscription Storage
✓ Preference Storage
✓ User Query Processing
UserRepository bajarmaydi.
✗ Authentication
✗ Authorization
✗ Trading Decision
✗ Trade Storage
✗ Market Storage
✗ Cache Management
---
# Module Boundary
```text
DatabaseManager
↓
UserRepository
↓
Database Storage
```
---
# Input Contract
• User Record
• Profile Record
• Settings Record
• Subscription Record
• Query Request
---
# Output Contract
• User Result
• User Profile
• Query Result
• Repository Metadata
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ TradeRepository
✗ MarketRepository
✗ JournalRepository
✗ AuditLog
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Har bir User Unique ID bilan saqlanishi shart.
2. User Settings atomik Transaction ichida yangilanishi shart.
3. Subscription holati doimo aktual bo'lishi shart.
4. Sensitive ma'lumotlar himoyalangan holda saqlanishi shart.
5. Query natijalari standart formatda qaytarilishi shart.
6. UserRepository Business Logic bajarmaydi.
7. UserRepository `user`, `subscription`, `feedback` va `admin` storage'larini o'z ichki mas'uliyati sifatida boshqaradi (RAR-001) — ular alohida modul emas.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ User saqlanadi.
✓ Profile saqlanadi.
✓ Settings yangilanadi.
✓ Subscription saqlanadi.
✓ User Query bajariladi.
✓ Repository Metadata yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
UserRepository Contract GoldBot Database Layer ichidagi User, Profile, Settings va Subscription ma'lumotlarini ishonchli saqlash, yangilash va o'qishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
