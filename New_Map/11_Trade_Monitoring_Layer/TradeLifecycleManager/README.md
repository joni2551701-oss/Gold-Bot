# Trade Lifecycle Manager
Status: CANONICAL
---
# Purpose
TradeLifecycleManager GoldBot Trade Monitoring Layer ichidagi Canonical Trade Lifecycle Control moduli hisoblanadi.
Uning asosiy vazifasi Trade'ning OPEN holatidan CLOSED holatigacha bo'lgan barcha Lifecycle bosqichlarini boshqarish va Trade State Machine'ni yuritishdir.
TradeLifecycleManager yangi Trade ochmaydi.
TradeLifecycleManager Order Execution bajarmaydi.
TradeLifecycleManager faqat Trade Lifecycle boshqaruvi bilan shug'ullanadi.
---
# Objective
TradeLifecycleManager quyidagi vazifalarni bajaradi.
• Trade State Management
• Lifecycle Management
• Trade Event Processing
• State Transition Validation
• Lifecycle Report Generation
• Trade Context Generation
---
# Layer Position
```text
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
```
---
# Responsibilities
TradeLifecycleManager
✓ Trade State boshqaradi
✓ Lifecycle Transition tekshiradi
✓ Trade Event qayta ishlaydi
✓ Trade Context yaratadi
✓ Lifecycle Report yaratadi
✓ Trade History yangilaydi
---
# Not Responsible
TradeLifecycleManager
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Stop Loss Calculation
✗ Trailing Stop
✗ Partial Close
---
# Input
TradeLifecycleManager qabul qiladi.
• Position Report
• Position Status
• Position Events
• Monitoring Context
---
# Output
TradeLifecycleManager yaratadi.
• Trade State
• Trade Context
• Lifecycle Report
• Lifecycle Metadata
• Trade Events
---
# Trade States
```text
OPEN
↓
ACTIVE
↓
BREAKEVEN
↓
TRAILING
↓
PARTIAL_CLOSE
↓
CLOSING
↓
CLOSED
```
---
# Workflow
```text
Receive Position Report
↓
Validate State
↓
Process Transition
↓
Update Lifecycle
↓
Generate Lifecycle Report
↓
SLTPMonitor
```
---
# Golden Rules
1. Trade faqat ruxsat etilgan State Transition orqali o'tishi kerak.
2. CLOSED holatidan keyin Lifecycle tugaydi.
3. Har bir State Transition log qilinishi shart.
4. Trade State faqat TradeLifecycleManager tomonidan boshqariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
TradeLifecycleManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
TradeLifecycleManager GoldBot Trade Monitoring Layer ichidagi barcha Trade State va Lifecycle jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
