# Database Service
Status: CANONICAL
---
# Purpose
DatabaseService GoldBot Database Layer ichidagi Canonical Public Database Interface moduli hisoblanadi.
Uning asosiy vazifasi Database Layer uchun yagona Service Gateway bo'lish va barcha tashqi Layer'lar bilan standart Database API orqali ishlashdir.
DatabaseService Database Query yozmaydi.
DatabaseService Business Logic bajarmaydi.
DatabaseService faqat Database Layer Service Gateway hisoblanadi.
---
# Objective
DatabaseService quyidagi vazifalarni bajaradi.
• Database Request Management
• Database API Gateway
• Request Validation
• Response Standardization
• Database Session Management
• Database Layer Integration
---
# Layer Position
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
# Responsibilities
DatabaseService
✓ Database Request qabul qiladi
✓ Request formatini tekshiradi
✓ DatabaseManager'ga uzatadi
✓ Repository natijalarini qabul qiladi
✓ Standard Response yaratadi
✓ Platform Layer'ga uzatadi
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
• Database Request
• Repository Request
• Query Request
• Session Metadata
---
# Output
DatabaseService yaratadi.
• Database Response
• Query Result
• Standard Response
• Service Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
DatabaseManager
↓
Repositories
↓
Receive Repository Result
↓
Standardize Response
↓
Platform Layer
```
---
# Golden Rules
1. Database Layer'ga barcha kirishlar DatabaseService orqali amalga oshiriladi.
2. DatabaseService Business Logic bajarmaydi.
3. Har bir Request Validation'dan o'tadi.
4. Response yagona formatda qaytariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
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
DatabaseService GoldBot Database Layer uchun yagona Public Interface va Service Gateway hisoblanadi.
