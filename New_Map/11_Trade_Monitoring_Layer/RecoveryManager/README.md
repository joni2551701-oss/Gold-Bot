# Recovery Manager
Status: CANONICAL
---
# Purpose
RecoveryManager GoldBot Trade Monitoring Layer ichidagi Canonical Trade Recovery Management moduli hisoblanadi.
Uning asosiy vazifasi GoldBot qayta ishga tushganda (Restart), Broker yoki Exchange'dagi barcha ochiq Position'larni qayta tiklash, Monitoring Session'ni davom ettirish va Trade Lifecycle'ni uzluksiz saqlashdir.
RecoveryManager yangi Trade ochmaydi.
RecoveryManager Trading Decision qabul qilmaydi.
RecoveryManager faqat Recovery va State Restoration bilan shug'ullanadi.
---
# Objective
RecoveryManager quyidagi vazifalarni bajaradi.
• Restart Recovery
• Open Position Recovery
• Session Recovery
• Trade State Restoration
• Recovery Validation
• Recovery Report Generation
---
# Layer Position
```text
PartialClose
↓
RecoveryManager
↓
MonitoringService
```
---
# Responsibilities
RecoveryManager
✓ Open Position tiklaydi
✓ Trade State tiklaydi
✓ Monitoring Session tiklaydi
✓ Recovery Validation bajaradi
✓ Recovery Event yaratadi
✓ Recovery Report yaratadi
---
# Not Responsible
RecoveryManager
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Stop Loss Management
✗ Trailing Stop
✗ Partial Close
---
# Input
RecoveryManager qabul qiladi.
• Trade Context
• Broker Open Positions
• Monitoring Metadata
• Recovery Configuration
---
# Output
RecoveryManager yaratadi.
• Recovered Position
• Recovery Status
• Recovery Report
• Recovery Metadata
• Recovery Events
---
# Recovery States
NOT_REQUIRED
↓
RECOVERING
↓
VALIDATING
↓
RECOVERED
↓
FAILED
---
# Workflow
```text
Detect Restart
↓
Load Recovery Configuration
↓
Load Open Positions
↓
Restore Trade State
↓
Validate Recovery
↓
Generate Recovery Report
↓
MonitoringService
```
---
# Golden Rules
1. Broker Open Positions asosiy manba hisoblanadi.
2. Har bir Position qayta tiklanishi shart.
3. Recovery tugamaguncha Monitoring boshlanmaydi.
4. Recovery natijasi log qilinishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RecoveryManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RecoveryManager GoldBot Trade Monitoring Layer ichidagi Restart Recovery va Trade State Restoration uchun Canonical modul hisoblanadi.
