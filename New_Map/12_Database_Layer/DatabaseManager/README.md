# Database Manager
Status: CANONICAL
---
# Purpose
DatabaseManager GoldBot Database Layer ichidagi Canonical Database Management moduli hisoblanadi.
Uning asosiy vazifasi Database Connection, Connection Pool, Transaction, Migration va Database Lifecycle'ni boshqarishdir.
DatabaseManager Business Logic bajarmaydi.
DatabaseManager Repository vazifasini bajarmaydi.
DatabaseManager faqat Database Infrastructure bilan shug'ullanadi.
---
# Objective
DatabaseManager quyidagi vazifalarni bajaradi.
• Database Connection Management
• Connection Pool Management
• Transaction Management
• Migration Management
• Database Health Monitoring
• Database Configuration Management
---
# Layer Position
```text
DatabaseService
↓
DatabaseManager
↓
Repositories
```
---
# Responsibilities
DatabaseManager
✓ Database ulanishini boshqaradi
✓ Connection Pool yaratadi
✓ Transaction boshqaradi
✓ Migration ishga tushiradi
✓ Database Health tekshiradi
✓ Database Configuration boshqaradi
---
# Not Responsible
DatabaseManager
✗ Trade Storage
✗ User Storage
✗ Market Storage
✗ Journal Storage
✗ Cache Management
✗ Backup Management
---
# Input
DatabaseManager qabul qiladi.
• Database Configuration
• Connection Request
• Transaction Request
• Migration Request
---
# Output
DatabaseManager yaratadi.
• Database Connection
• Transaction Context
• Migration Status
• Database Health Report
• Database Metadata
---
# Database States
INITIALIZING
↓
CONNECTED
↓
READY
↓
TRANSACTION
↓
MAINTENANCE
↓
DISCONNECTED
---
# Workflow
```text
Receive Connection Request
↓
Load Configuration
↓
Initialize Connection Pool
↓
Open Database Connection
↓
Monitor Database Health
↓
Provide Connection
↓
Repositories
```
---
# Golden Rules
1. Database Connection yagona markaz orqali boshqariladi.
2. Connection Pool ishlatilishi shart.
3. Har bir Transaction atomik bo'lishi shart.
4. Migration nazorat ostida bajarilishi shart.
5. Database Health doim kuzatiladi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DatabaseManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DatabaseManager GoldBot Database Layer ichidagi Database Infrastructure va Connection Lifecycle'ni boshqaruvchi Canonical modul hisoblanadi.
