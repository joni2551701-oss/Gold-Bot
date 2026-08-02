# Trade Monitoring Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Trade Monitoring Layer ichidagi ma'lumotlar oqimini (Data Flow) tavsiflaydi.
Trade Monitoring Layer Execution Layer tomonidan muvaffaqiyatli ochilgan Position'larni kuzatadi, ularni boshqaradi va Position yopilguniga qadar barcha Monitoring jarayonlarini amalga oshiradi.
---
# Layer Data Flow
```text
Execution Layer
        │
        ▼
MonitoringService
        │
        ▼
PositionMonitor
        │
        ▼
TradeLifecycleManager
        │
        ▼
SLTPMonitor
        │
        ▼
BreakevenManager
        │
        ▼
TrailingStop
        │
        ▼
PartialClose
        │
        ▼
RecoveryManager
        │
        ▼
Database Layer
```
---
# Input Sources
• Execution Result
• Position Information
• Broker Position
• Market Price
• Monitoring Rules
• Recovery Configuration
---
# Output
• Position Status
• Trade Status
• Monitoring Report
• Recovery Report
• Monitoring Events
• Monitoring Metadata
---
# Data Flow Rules
1. Monitoring faqat OPEN Position uchun boshlanadi.
2. Broker Position asosiy ma'lumot manbai hisoblanadi.
3. Har bir Monitoring Event ketma-ket qayta ishlanadi.
4. Recovery faqat Restart holatida ishga tushadi.
5. Monitoring natijalari Database Layer'ga uzatiladi.
---
# Summary
Trade Monitoring Layer GoldBot arxitekturasidagi Canonical Position Lifecycle Monitoring Pipeline hisoblanadi.
