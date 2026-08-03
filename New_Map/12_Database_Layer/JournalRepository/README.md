# Journal Repository
Status: CANONICAL
---
# Purpose
JournalRepository GoldBot Database Layer ichidagi Canonical AI Journal Persistence moduli hisoblanadi.
Uning asosiy vazifasi AI Analysis, Decision History, System Event va Explainability ma'lumotlarini Database'da saqlash, yangilash va o'qishdir.
JournalRepository Business Logic bajarmaydi.
JournalRepository AI Analysis bajarmaydi.
JournalRepository faqat Journal Domain ma'lumotlari bilan ishlaydi.
---
# Objective
JournalRepository quyidagi vazifalarni bajaradi.
• AI Journal Storage
• Decision History Storage
• Explainability Storage
• System Event Storage
• Journal Query Processing
---
# Layer Position
```text
DatabaseManager
↓
JournalRepository
↓
Database Storage
```
---
# Responsibilities
JournalRepository
✓ AI Journal saqlaydi
✓ Decision History saqlaydi
✓ Explainability ma'lumotlarini saqlaydi
✓ System Event saqlaydi
✓ Journal Query bajaradi
---
# Not Responsible
JournalRepository
✗ AI Analysis
✗ Trading Decision
✗ Trade Storage
✗ User Storage
✗ Cache Management
✗ Backup Management
---
# Input
JournalRepository qabul qiladi.
• AI Journal Record
• Decision Record
• System Event
• Query Request
---
# Output
JournalRepository yaratadi.
• Journal Result
• Decision History
• Query Result
• Repository Metadata
---
# Workflow
```text
Receive Repository Request
↓
Validate Journal Data
↓
Save / Update / Query
↓
Return Repository Result
```
---
# Internal Storage (Real Implementations)
Domen: AI Journal va tizim holati domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
JournalRepository
├── learning
├── config_snapshot
└── runtime_feature
```
| Storage | Mas'uliyat |
|---|---|
| `learning` | Learning Loop yozuvlari (append-only) |
| `config_snapshot` | Konfiguratsiya snapshot'lari (append-only) |
| `runtime_feature` | Runtime Feature Toggle holati (upsert, feature/enabled/updated_by) |
---
# Golden Rules
1. Decision History immutable saqlanadi.
2. Har bir AI Analysis vaqt belgisi bilan yoziladi.
3. Journal yozuvlari izchil bo'lishi shart.
4. JournalRepository Audit Trail saqlamaydi — Login/Configuration/Permission/API Access/Critical Event yozuvlari AuditLog modulining vazifasi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
JournalRepository/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
JournalRepository GoldBot Database Layer ichidagi AI Journal, Decision History va Explainability ma'lumotlarini boshqaruvchi Canonical Repository moduli hisoblanadi.
