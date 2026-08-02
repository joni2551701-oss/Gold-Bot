# Journal Repository
Status: CANONICAL
---
# Purpose
JournalRepository GoldBot Database Layer ichidagi Canonical AI Journal va Audit Persistence moduli hisoblanadi.
Uning asosiy vazifasi AI Analysis, Decision History, Audit Log, System Event va Explainability ma'lumotlarini Database'da saqlash, yangilash va o'qishdir.
JournalRepository Business Logic bajarmaydi.
JournalRepository AI Analysis bajarmaydi.
JournalRepository faqat Journal Domain ma'lumotlari bilan ishlaydi.
---
# Objective
JournalRepository quyidagi vazifalarni bajaradi.
• AI Journal Storage
• Decision History Storage
• Audit Log Storage
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
✓ Audit Log saqlaydi
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
• Audit Record
• System Event
• Query Request
---
# Output
JournalRepository yaratadi.
• Journal Result
• Decision History
• Audit History
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
# Golden Rules
1. Audit Log o'zgartirilmaydi.
2. Decision History immutable saqlanadi.
3. Har bir AI Analysis vaqt belgisi bilan yoziladi.
4. Journal yozuvlari izchil bo'lishi shart.
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
JournalRepository GoldBot Database Layer ichidagi AI Journal, Decision History, Audit Log va Explainability ma'lumotlarini boshqaruvchi Canonical Repository moduli hisoblanadi.
