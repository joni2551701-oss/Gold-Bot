# Audit Log
Status: CANONICAL
---
# Purpose
AuditLog GoldBot Database Layer ichidagi Canonical Audit Trail repository moduli hisoblanadi.
Uning asosiy vazifasi "kim, nima qildi, qachon" savoliga har doim javob bera olishdir — Login, Configuration o'zgarishi, Permission o'zgarishi, API Access va Critical Event'larni yozib borish.
AuditLog Trade Journal EMAS — u savdo tarixini emas, tizim va foydalanuvchi harakatlarini yozadi.
AuditLog yozilgan yozuvni hech qachon o'zgartirmaydi va o'chirmaydi.
---
# Objective
AuditLog quyidagi vazifalarni bajaradi.
• Login Event Recording
• Configuration Change Recording
• Permission Change Recording
• API Access Recording
• Critical Event Recording
• Audit Query
---
# Layer Position
```text
DatabaseManager
↓
AuditLog
↓
Database Storage
```
---
# Responsibilities
AuditLog
✓ Har bir Owner/Admin harakatini yozib boradi
✓ Actor, Action, Timestamp va Detail maydonlarini saqlaydi
✓ Audit tarixini so'rov bo'yicha qaytaradi
✓ Yozuvlarni faqat qo'shadi (append-only)
---
# Not Responsible
AuditLog
✗ Trade Journal (JournalRepository vazifasi)
✗ Business Logic
✗ Authentication (13_Platform_Layer/Authentication vazifasi)
✗ Authorization
✗ Cache Management
✗ Backup Management
---
# Input
AuditLog qabul qiladi.
• Audit Entry (Actor, Action, Timestamp, Detail)
• Audit Query Request
---
# Output
AuditLog yaratadi.
• Audit Record
• Audit History
• Query Result
• Repository Metadata
---
# Workflow
```text
DatabaseManager
↓
AuditLog
↓
Database Storage
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
AuditLog
├── AuditEntryModel
├── AuditWriter
├── AuditReader
└── AuditQuery
```
---
# Golden Rules
1. AuditLog append-only hisoblanadi — yozuv hech qachon o'zgartirilmaydi va o'chirilmaydi.
2. Har bir yozuvda Actor, Action va Timestamp majburiy.
3. AuditLog Trade Journal bilan aralashtirilmaydi — ular alohida modullar.
4. AuditLog maxfiy qiymatlarni (API Key, Token, Password) hech qachon yozmaydi.
5. AuditLog Business Logic bajarmaydi — faqat yozadi va o'qiydi.
6. AuditLog foydalanuvchini autentifikatsiya yoki avtorizatsiya qilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
AuditLog/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
AuditLog GoldBot'dagi barcha Owner/Admin harakatlari va Critical Event'lar uchun Canonical append-only Audit Trail repository moduli hisoblanadi.
