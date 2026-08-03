# Position Monitor
Status: CANONICAL
---
# Purpose
PositionMonitor GoldBot Trade Monitoring Layer ichidagi Canonical Open Position Monitoring moduli hisoblanadi.
Uning asosiy vazifasi Broker yoki Exchange'dagi barcha ochiq Position'larni real vaqt rejimida kuzatish, ularning holatini yangilash va Monitoring Pipeline'ga uzatishdir.
PositionMonitor yangi Trade ochmaydi.
PositionMonitor Trading Decision qabul qilmaydi.
PositionMonitor faqat Open Position Monitoring bilan shug'ullanadi.
---
# Objective
PositionMonitor quyidagi vazifalarni bajaradi.
• Open Position Monitoring
• Position Status Tracking
• Position Synchronization
• Position State Detection
• Position Event Generation
• Position Report Generation
---
# Layer Position
```text
MonitoringService
↓
PositionMonitor
↓
TradeLifecycleManager
```
---
# Responsibilities
PositionMonitor
✓ Open Position'larni kuzatadi
✓ Position Status yangilaydi
✓ Broker Position bilan sinxronlaydi
✓ Position Event yaratadi
✓ Position Report yaratadi
✓ Monitoring Context yaratadi
---
# Not Responsible
PositionMonitor
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Stop Loss Management
✗ Trailing Stop
✗ Partial Close
---
# Input
PositionMonitor qabul qiladi.
• Execution Result
• Broker Position
• Position Metadata
• Monitoring Context
---
# Output
PositionMonitor yaratadi.
• Position Status
• Position Context
• Position Events
• Position Report
• Monitoring Metadata
---
# Position States
OPEN
↓
ACTIVE
↓
BREAKEVEN
↓
TRAILING
↓
PARTIAL
↓
CLOSING
↓
CLOSED
---
# Workflow
```text
Receive Position
↓
Synchronize Position
↓
Track Position State
↓
Detect Position Events
↓
Generate Position Report
↓
TradeLifecycleManager
```
---
# Golden Rules
1. Faqat OPEN Position monitoring qilinadi.
2. Broker holati asosiy manba hisoblanadi.
3. Har bir Position Event qayd etiladi.
4. Monitoring uzluksiz ishlashi kerak.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
PositionMonitor/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
PositionMonitor GoldBot Trade Monitoring Layer ichidagi barcha ochiq Position'larni real vaqt rejimida kuzatuvchi Canonical Monitoring moduli hisoblanadi.
