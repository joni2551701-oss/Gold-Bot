# Decision Logger Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionLogger ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DecisionEngine
↓
DecisionLogger
↓
DecisionService
```
---
# Module Architecture
```text
DecisionLogger
        │
        ├── Decision Recorder
        ├── Audit Builder
        ├── History Manager
        ├── Metadata Generator
        ├── Log Formatter
        └── Log Dispatcher
```
---
# Internal Components
## Decision Recorder
Decision ma'lumotlarini yig'adi.
---
## Audit Builder
Audit Record yaratadi.
---
## History Manager
Decision History obyektini yaratadi.
---
## Metadata Generator
Timestamp va Metadata yaratadi.
---
## Log Formatter
Log'ni standart formatga o'tkazadi.
---
## Log Dispatcher
Log'ni Database Layer'ga yuboradi.
---
# Logged Information
• Decision ID
• Signal ID
• AI Package ID
• Approval Status
• Decision Confidence
• Rule Results
• Reject Reason
• Timestamp
• Version
---
# Allowed Dependencies
✓ DecisionEngine
✓ DecisionService
---
# Forbidden Dependencies
✗ RuleEngine
✗ Risk Layer
✗ Execution Layer
✗ Database Layer (to'g'ridan-to'g'ri)
---
# Summary
DecisionLogger GoldBot ichidagi barcha Decision Audit va History yozuvlarini boshqaruvchi Canonical modul hisoblanadi.
