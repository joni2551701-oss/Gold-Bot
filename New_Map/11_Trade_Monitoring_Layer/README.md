# Trade Monitoring Layer
Status: CANONICAL
---
# Purpose
Trade Monitoring Layer GoldBot arxitekturasidagi Canonical Trade Lifecycle Management qatlami hisoblanadi.
Uning asosiy vazifasi Execution Layer tomonidan ochilgan pozitsiyalarni real vaqt rejimida kuzatish, boshqarish va yakuniy yopilguniga qadar butun Trade Lifecycle'ni nazorat qilishdir.
Trade Monitoring Layer yangi Trade ochmaydi.
Trade Monitoring Layer Trading Decision qabul qilmaydi.
Trade Monitoring Layer faqat ochiq pozitsiyalarni boshqaradi.
---
# Objective
Trade Monitoring Layer quyidagi vazifalarni bajaradi.
• Position Monitoring
• Trade Lifecycle Management
• Stop Loss Monitoring
• Take Profit Monitoring
• Breakeven Management
• Trailing Stop Management
• Partial Close Management
• Recovery Management
---
# Layer Position
```text
Execution Layer
↓
Trade Monitoring Layer
↓
Database Layer
```
---
# Internal Modules
```text
Trade Monitoring Layer
├── PositionMonitor
├── TradeLifecycleManager
├── SLTPMonitor
├── BreakevenManager
├── TrailingStop
├── PartialClose
├── RecoveryManager
└── MonitoringService
```
---
# Responsibilities
Trade Monitoring Layer
✓ Open Position kuzatadi
✓ Trade holatini boshqaradi
✓ Stop Loss triggerlarini kuzatadi
✓ Take Profit triggerlarini kuzatadi
✓ Breakeven qo'llaydi
✓ Trailing Stop yangilaydi
✓ Partial Close bajaradi
✓ Restart Recovery bajaradi
---
# Not Responsible
Trade Monitoring Layer
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Order Execution
✗ Portfolio Management
---
# Input
Trade Monitoring Layer qabul qiladi.
• Execution Result
• Order Status
• Position Information
• Trade Metadata
• Broker Events
---
# Output
Trade Monitoring Layer yaratadi.
• Position Status
• Trade Status
• Monitoring Report
• Position Metadata
• Trade Events
---
# Trade States
```text
OPEN
↓
MONITORING
↓
BREAKEVEN
↓
TRAILING
↓
PARTIAL_CLOSE
↓
CLOSED
```
---
# Workflow
```text
Receive Execution Result
↓
MonitoringService (Entry)
↓
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
↓
PartialClose
↓
RecoveryManager
↓
MonitoringService (Exit)
↓
Database Layer
```
---
# Golden Rules
1. Faqat ochilgan Trade monitoring qilinadi.
2. Har bir Position real vaqt rejimida kuzatiladi.
3. Breakeven faqat Strategy qoidalariga mos bo'lsa qo'llaniladi.
4. Trailing Stop mavjud Stop Loss'ni dinamik boshqaradi.
5. Partial Close faqat belgilangan qoidalarga muvofiq bajariladi.
6. RecoveryManager restartdan keyin barcha ochiq Position'larni tiklaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
11_Trade_Monitoring_Layer/
├── README.md
├── PositionMonitor/
├── TradeLifecycleManager/
├── SLTPMonitor/
├── BreakevenManager/
├── TrailingStop/
├── PartialClose/
├── RecoveryManager/
├── MonitoringService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Trade Monitoring Layer GoldBot arxitekturasidagi Canonical Trade Lifecycle Management Layer hisoblanadi.
Execution Layer Trade'ni ochadi.
Trade Monitoring Layer esa ushbu Trade'ni ochilganidan boshlab yopilguniga qadar kuzatadi, boshqaradi va barcha monitoring jarayonlarini amalga oshiradi.
