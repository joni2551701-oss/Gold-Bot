# Recovery Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat RecoveryManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
PartialClose
↓
RecoveryManager
↓
Detect Restart
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
# Runtime Rules
1. Restart aniqlanishi shart.
2. Broker Open Positions olinishi shart.
3. Trade State tiklanishi shart.
4. Recovery Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Restart Detected
↓
Recovering
↓
Validating
↓
Reporting
↓
Completed
```
---
# Summary
PartialClose
↓
RecoveryManager
↓
MonitoringService
