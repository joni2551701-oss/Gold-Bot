# Trade Monitoring Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
11_Trade_Monitoring_Layer
│
├── MonitoringService
│
├── PositionMonitor
│
├── TradeLifecycleManager
│
├── SLTPMonitor
│
├── BreakevenManager
│
├── TrailingStop
│
├── PartialClose
│
└── RecoveryManager
```
---
# Processing Pipeline
```text
Execution Layer
        │
        ▼
MonitoringService (Entry)
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
MonitoringService (Exit)
        │
        ▼
Database Layer
```
---
# Module Responsibilities
## MonitoringService
Trade Monitoring Layer'ning ikki tomonlama (bidirectional) Boundary Gateway'i — Entry va Exit.
---
## PositionMonitor
Open Position'larni kuzatadi.
---
## TradeLifecycleManager
Trade State va Lifecycle'ni boshqaradi.
---
## SLTPMonitor
Stop Loss va Take Profit triggerlarini kuzatadi.
---
## BreakevenManager
Break Even qoidalarini qo'llaydi.
---
## TrailingStop
Dynamic Stop Loss boshqaradi.
---
## PartialClose
Position'ni qisman yopadi.
---
## RecoveryManager
Restart Recovery va State Restoration bajaradi. Layer tashqarisiga chiqmaydi — natijani MonitoringService orqali uzatadi.
---
# Summary
Trade Monitoring Layer GoldBot arxitekturasidagi Canonical Trade Lifecycle Management Layer hisoblanadi.
