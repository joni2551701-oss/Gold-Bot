# Database Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DatabaseManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DatabaseService
↓
DatabaseManager
↓
Load Configuration
↓
Initialize Connection Pool
↓
Open Connection
↓
Health Check
↓
Provide Connection
↓
Repositories
```
---
# Runtime Rules
1. Database Configuration mavjud bo'lishi shart.
2. Connection Pool yaratilishi shart.
3. Database Connection muvaffaqiyatli ochilishi shart.
4. Health Check bajarilishi shart.
---
# State Flow
```text
Idle
↓
Initializing
↓
Connecting
↓
Ready
↓
Serving
↓
Completed
```
---
# Summary
DatabaseService
↓
DatabaseManager
↓
Repositories
