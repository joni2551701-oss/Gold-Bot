# SLTP Monitor
Status: CANONICAL
---
# Purpose
SLTPMonitor GoldBot Trade Monitoring Layer ichidagi Canonical Stop Loss va Take Profit Monitoring moduli hisoblanadi.
Uning asosiy vazifasi ochiq Position uchun Stop Loss (SL) va Take Profit (TP) triggerlarini real vaqt rejimida kuzatish, trigger yuz berganda tegishli Monitoring Event yaratish va keyingi modullarga uzatishdir.
SLTPMonitor Trade ochmaydi.
SLTPMonitor Order Execution bajarmaydi.
SLTPMonitor faqat SL/TP Monitoring bilan shug'ullanadi.
---
# Objective
SLTPMonitor quyidagi vazifalarni bajaradi.
• Stop Loss Monitoring
• Take Profit Monitoring
• Trigger Detection
• Price Validation
• SLTP Event Generation
• Monitoring Report Generation
---
# Layer Position
```text
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
```
---
# Responsibilities
SLTPMonitor
✓ Stop Loss kuzatadi
✓ Take Profit kuzatadi
✓ Trigger aniqlaydi
✓ Broker Position bilan taqqoslaydi
✓ SLTP Event yaratadi
✓ Monitoring Report yaratadi
---
# Not Responsible
SLTPMonitor
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Trailing Stop
✗ Partial Close
✗ Recovery Management
---
# Input
SLTPMonitor qabul qiladi.
• Trade State
• Position Information
• Current Market Price
• Broker Position
• Monitoring Context
---
# Output
SLTPMonitor yaratadi.
• SLTP Status
• Trigger Events
• Monitoring Report
• Monitoring Metadata
• Trade Context
---
# Trigger States
NO_TRIGGER
↓
SL_TRIGGERED
↓
TP_TRIGGERED
↓
COMPLETED
---
# Workflow
```text
Receive Trade Context
↓
Monitor Market Price
↓
Validate SL/TP
↓
Detect Trigger
↓
Generate Monitoring Report
↓
BreakevenManager
```
---
# Golden Rules
1. Broker narxi asosiy manba hisoblanadi.
2. Stop Loss va Take Profit mustaqil tekshiriladi.
3. Har bir Trigger Event log qilinishi shart.
4. Trigger bir martadan ortiq qayta ishlanmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SLTPMonitor/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SLTPMonitor GoldBot Trade Monitoring Layer ichidagi Stop Loss va Take Profit triggerlarini real vaqt rejimida kuzatuvchi Canonical Monitoring moduli hisoblanadi.
